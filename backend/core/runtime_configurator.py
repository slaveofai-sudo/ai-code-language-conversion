"""
Runtime Configurator / 运行环境配置器

Generates runtime-specific configurations for different deployment environments.
为不同的部署环境生成运行时特定的配置。

Supports / 支持:
- Docker configurations / Docker配置
- Cloud platforms (AWS, Azure, GCP) / 云平台
- Kubernetes / Kubernetes
- Traditional servers / 传统服务器
"""

from typing import Dict, List, Any, Optional
from pathlib import Path
from loguru import logger


class RuntimeConfigurator:
    """
    Runtime Environment Configurator / 运行环境配置器
    
    Generates configuration files for different runtime environments.
    为不同的运行环境生成配置文件。
    """
    
    # Runtime environment templates / 运行环境模板
    RUNTIME_CONFIGS = {
        "docker": {
            "description": "Docker容器化部署 / Docker containerized deployment",
            "files": {
                "Dockerfile": {
                    "python-fastapi": """FROM python:3.11-slim

WORKDIR /app

# Install dependencies / 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code / 复制应用代码
COPY . .

# Expose port / 暴露端口
EXPOSE 8000

# Health check / 健康检查
HEALTHCHECK --interval=30s --timeout=3s \\
  CMD curl -f http://localhost:8000/health || exit 1

# Run application / 运行应用
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
""",
                    "python-django": """FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Collect static files / 收集静态文件
RUN python manage.py collectstatic --no-input

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "project.wsgi:application"]
""",
                    "java-spring-boot": """FROM eclipse-temurin:17-jdk-alpine AS build

WORKDIR /workspace/app

COPY mvnw .
COPY .mvn .mvn
COPY pom.xml .
COPY src src

RUN ./mvnw package -DskipTests

FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

COPY --from=build /workspace/app/target/*.jar app.jar

EXPOSE 8080

HEALTHCHECK CMD wget --no-verbose --tries=1 --spider http://localhost:8080/actuator/health || exit 1

ENTRYPOINT ["java","-jar","app.jar"]
""",
                    "nodejs-express": """FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 3000

USER node

CMD ["node", "src/index.js"]
"""
                },
                "docker-compose.yml": """version: '3.8'

services:
  app:
    build: .
    ports:
      - "${PORT:-8000}:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    depends_on:
      - db
      - redis
    networks:
      - app-network

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=${DB_NAME}
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - app-network

  redis:
    image: redis:7-alpine
    networks:
      - app-network

volumes:
  postgres-data:

networks:
  app-network:
    driver: bridge
"""
            }
        },
        
        "kubernetes": {
            "description": "Kubernetes集群部署 / Kubernetes cluster deployment",
            "files": {
                "k8s/deployment.yaml": """apiVersion: apps/v1
kind: Deployment
metadata:
  name: {app_name}
  labels:
    app: {app_name}
spec:
  replicas: 3
  selector:
    matchLabels:
      app: {app_name}
  template:
    metadata:
      labels:
        app: {app_name}
    spec:
      containers:
      - name: {app_name}
        image: {image_name}:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: {app_name}-secret
              key: database-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: {app_name}-service
spec:
  selector:
    app: {app_name}
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
---
apiVersion: v1
kind: Secret
metadata:
  name: {app_name}-secret
type: Opaque
stringData:
  database-url: "postgresql://user:password@postgres:5432/dbname"
""",
                "k8s/ingress.yaml": """apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {app_name}-ingress
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
  - hosts:
    - {app_domain}
    secretName: {app_name}-tls
  rules:
  - host: {app_domain}
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: {app_name}-service
            port:
              number: 80
"""
            }
        },
        
        "aws": {
            "description": "AWS云平台部署 / AWS cloud platform deployment",
            "files": {
                "aws/eb-config.yml": """# AWS Elastic Beanstalk configuration
option_settings:
  aws:elasticbeanstalk:environment:proxy:
    ProxyServer: nginx
  aws:elasticbeanstalk:application:environment:
    PORT: 8000
    PYTHON_VERSION: 3.11
  aws:autoscaling:asg:
    MinSize: 2
    MaxSize: 6
  aws:autoscaling:trigger:
    MeasureName: CPUUtilization
    Statistic: Average
    Unit: Percent
    UpperThreshold: 80
    LowerThreshold: 20
""",
                "aws/lambda-function.py": """import json
import awsgi
from main import app

def lambda_handler(event, context):
    return awsgi.response(app, event, context)
""",
                "aws/sam-template.yaml": """AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Resources:
  ApiFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: .
      Handler: aws/lambda-function.lambda_handler
      Runtime: python3.11
      Timeout: 30
      Events:
        ApiEvent:
          Type: Api
          Properties:
            Path: /{proxy+}
            Method: ANY
"""
            }
        },
        
        "heroku": {
            "description": "Heroku平台部署 / Heroku platform deployment",
            "files": {
                "Procfile": {
                    "python-fastapi": "web: uvicorn main:app --host 0.0.0.0 --port $PORT",
                    "python-django": "web: gunicorn project.wsgi --log-file -",
                    "nodejs-express": "web: node src/index.js",
                    "java-spring-boot": "web: java -Dserver.port=$PORT -jar target/*.jar"
                },
                "runtime.txt": {
                    "python": "python-3.11.0",
                    "nodejs": "node-18.x"
                }
            }
        },
        
        "systemd": {
            "description": "Linux系统服务 / Linux system service",
            "files": {
                "/etc/systemd/system/{app_name}.service": {
                    "python": """[Unit]
Description={app_name} Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/{app_name}
Environment="PATH=/opt/{app_name}/venv/bin"
ExecStart=/opt/{app_name}/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
""",
                    "nodejs": """[Unit]
Description={app_name} Service
After=network.target

[Service]
Type=simple
User=nodejs
WorkingDirectory=/opt/{app_name}
ExecStart=/usr/bin/node src/index.js
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""
                }
            }
        }
    }
    
    def __init__(self, app_name: str = "myapp", app_domain: str = "example.com"):
        """
        Initialize runtime configurator / 初始化运行环境配置器
        
        Args:
            app_name: Application name / 应用名称
            app_domain: Application domain / 应用域名
        """
        self.app_name = app_name.replace("-", "_").replace(" ", "_").lower()
        self.app_domain = app_domain
        self.image_name = f"{self.app_name}"
    
    def generate_runtime_config(
        self,
        runtime_type: str,
        framework: str,
        output_path: Path
    ) -> Dict[str, Any]:
        """
        Generate runtime-specific configuration files
        生成运行时特定的配置文件
        
        Args:
            runtime_type: Runtime environment type / 运行环境类型
                         (docker, kubernetes, aws, heroku, systemd)
            framework: Target framework / 目标框架
            output_path: Output directory path / 输出目录路径
            
        Returns:
            Dictionary with generated files / 生成的文件字典
        """
        if runtime_type not in self.RUNTIME_CONFIGS:
            logger.warning(f"⚠️ 不支持的运行环境类型: {runtime_type}")
            return {"success": False, "message": "Unsupported runtime type"}
        
        config = self.RUNTIME_CONFIGS[runtime_type]
        generated_files = []
        
        try:
            for file_path_template, content in config["files"].items():
                # Handle framework-specific content / 处理框架特定的内容
                if isinstance(content, dict):
                    # Select framework-specific template / 选择框架特定的模板
                    framework_key = self._get_framework_key(framework)
                    if framework_key in content:
                        file_content = content[framework_key]
                    else:
                        # Try to find a matching key / 尝试找到匹配的键
                        file_content = next(
                            (v for k, v in content.items() if framework in k),
                            list(content.values())[0]  # Use first available
                        )
                else:
                    file_content = content
                
                # Replace placeholders / 替换占位符
                file_path = file_path_template.format(
                    app_name=self.app_name,
                    app_domain=self.app_domain
                )
                file_content = file_content.format(
                    app_name=self.app_name,
                    app_domain=self.app_domain,
                    image_name=self.image_name
                )
                
                # Write file / 写入文件
                full_path = output_path / file_path
                full_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.write_text(file_content, encoding='utf-8')
                
                generated_files.append(str(full_path))
                logger.debug(f"📄 生成配置文件: {full_path}")
            
            logger.info(f"✅ 成功生成 {runtime_type} 运行环境配置")
            logger.info(f"   - 创建了 {len(generated_files)} 个配置文件")
            
            return {
                "success": True,
                "runtime_type": runtime_type,
                "description": config["description"],
                "generated_files": generated_files
            }
            
        except Exception as e:
            logger.error(f"❌ 生成运行环境配置失败: {e}")
            return {
                "success": False,
                "message": str(e)
            }
    
    def _get_framework_key(self, framework: str) -> str:
        """
        Get framework key for template selection / 获取模板选择的框架键
        
        Args:
            framework: Framework name / 框架名称
            
        Returns:
            Framework key / 框架键
        """
        # Map framework names to template keys / 将框架名称映射到模板键
        framework_map = {
            "fastapi": "python-fastapi",
            "django": "python-django",
            "flask": "python-flask",
            "spring-boot": "java-spring-boot",
            "express": "nodejs-express",
            "nestjs": "nodejs-express",  # Similar setup
            "gin": "go-gin"
        }
        
        return framework_map.get(framework, "python-fastapi")
    
    def get_deployment_instructions(self, runtime_type: str) -> str:
        """
        Get deployment instructions for the runtime environment
        获取运行环境的部署说明
        
        Args:
            runtime_type: Runtime environment type / 运行环境类型
            
        Returns:
            Deployment instructions / 部署说明
        """
        instructions = {
            "docker": """
# Docker部署说明 / Docker Deployment Instructions

## 构建镜像 / Build Image
```bash
docker build -t {app_name}:latest .
```

## 运行容器 / Run Container
```bash
docker run -d -p 8000:8000 --name {app_name} {app_name}:latest
```

## 使用 Docker Compose
```bash
docker-compose up -d
```

## 查看日志 / View Logs
```bash
docker logs -f {app_name}
```
""",
            "kubernetes": """
# Kubernetes部署说明 / Kubernetes Deployment Instructions

## 应用配置 / Apply Configuration
```bash
kubectl apply -f k8s/
```

## 查看状态 / Check Status
```bash
kubectl get pods
kubectl get services
kubectl get ingress
```

## 查看日志 / View Logs
```bash
kubectl logs -f deployment/{app_name}
```

## 扩容 / Scale
```bash
kubectl scale deployment/{app_name} --replicas=5
```
""",
            "heroku": """
# Heroku部署说明 / Heroku Deployment Instructions

## 创建应用 / Create App
```bash
heroku create {app_name}
```

## 部署代码 / Deploy Code
```bash
git push heroku main
```

## 查看日志 / View Logs
```bash
heroku logs --tail
```

## 扩容 / Scale
```bash
heroku ps:scale web=2
```
"""
        }
        
        return instructions.get(runtime_type, "").format(app_name=self.app_name)

