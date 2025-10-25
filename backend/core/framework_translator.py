"""
Framework Translator / 框架翻译器

Handles framework-specific code translation with template generation.
处理框架特定的代码翻译并生成模板。

Features / 功能:
- Framework-specific code patterns / 框架特定代码模式
- Project structure generation / 项目结构生成
- Configuration file migration / 配置文件迁移
- Dependency mapping / 依赖映射
"""

from typing import Dict, List, Any, Optional
from pathlib import Path
from loguru import logger
import yaml
import json


class FrameworkTranslator:
    """
    Framework Translator / 框架翻译器
    
    Translates framework-specific code and generates target project structure.
    翻译框架特定代码并生成目标项目结构。
    """
    
    # Framework-specific project templates / 框架特定项目模板
    PROJECT_TEMPLATES = {
        "fastapi": {
            "structure": [
                "app/",
                "app/api/",
                "app/api/v1/",
                "app/core/",
                "app/models/",
                "app/schemas/",
                "app/services/",
                "app/db/",
                "tests/",
                "alembic/versions/"
            ],
            "files": {
                "main.py": """from fastapi import FastAPI
from app.api.v1 import router as api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to {project_name}"}
""",
                "app/__init__.py": "",
                "app/core/config.py": """from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "{project_name}"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    class Config:
        env_file = ".env"

settings = Settings()
""",
                "requirements.txt": """fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
sqlalchemy==2.0.23
alembic==1.13.0
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0
""",
                ".env.example": """PROJECT_NAME={project_name}
VERSION=1.0.0
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your-secret-key-here
""",
                "Dockerfile": """FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
            }
        },
        
        "django": {
            "structure": [
                "{project_name}/",
                "{project_name}/settings/",
                "apps/",
                "static/",
                "media/",
                "templates/",
                "tests/"
            ],
            "files": {
                "manage.py": """#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{project_name}.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    execute_from_command_line(sys.argv)
""",
                "requirements.txt": """Django==4.2.7
djangorestframework==3.14.0
django-cors-headers==4.3.1
psycopg2-binary==2.9.9
python-dotenv==1.0.0
gunicorn==21.2.0
""",
                "{project_name}/settings.py": """from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-changeme')

DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = '{project_name}.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', '{project_name}'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
"""
            }
        },
        
        "spring-boot": {
            "structure": [
                "src/main/java/com/example/{project_name}/",
                "src/main/java/com/example/{project_name}/controller/",
                "src/main/java/com/example/{project_name}/service/",
                "src/main/java/com/example/{project_name}/repository/",
                "src/main/java/com/example/{project_name}/model/",
                "src/main/java/com/example/{project_name}/config/",
                "src/main/resources/",
                "src/test/java/"
            ],
            "files": {
                "pom.xml": """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>
    
    <groupId>com.example</groupId>
    <artifactId>{project_name}</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>
    
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.2.0</version>
    </parent>
    
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>
        <dependency>
            <groupId>org.postgresql</groupId>
            <artifactId>postgresql</artifactId>
        </dependency>
    </dependencies>
</project>
""",
                "src/main/resources/application.properties": """spring.application.name={project_name}
server.port=8080

spring.datasource.url=jdbc:postgresql://localhost:5432/{project_name}
spring.datasource.username=postgres
spring.datasource.password=postgres

spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
""",
                "Dockerfile": """FROM eclipse-temurin:17-jdk-alpine
WORKDIR /app
COPY target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java","-jar","app.jar"]
"""
            }
        },
        
        "express": {
            "structure": [
                "src/",
                "src/routes/",
                "src/controllers/",
                "src/models/",
                "src/middlewares/",
                "src/config/",
                "tests/"
            ],
            "files": {
                "package.json": """{
  "name": "{project_name}",
  "version": "1.0.0",
  "description": "Express.js application",
  "main": "src/index.js",
  "scripts": {
    "start": "node src/index.js",
    "dev": "nodemon src/index.js",
    "test": "jest"
  },
  "dependencies": {
    "express": "^4.18.2",
    "cors": "^2.8.5",
    "dotenv": "^16.3.1",
    "helmet": "^7.1.0",
    "morgan": "^1.10.0"
  },
  "devDependencies": {
    "nodemon": "^3.0.2",
    "jest": "^29.7.0"
  }
}
""",
                "src/index.js": """const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
require('dotenv').config();

const app = express();

// Middleware
app.use(helmet());
app.use(cors());
app.use(morgan('dev'));
app.use(express.json());

// Routes
app.get('/', (req, res) => {
  res.json({ message: 'Welcome to {project_name}' });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
""",
                ".env.example": """PORT=3000
NODE_ENV=development
DATABASE_URL=postgresql://user:password@localhost:5432/{project_name}
"""
            }
        },
        
        "gin": {
            "structure": [
                "cmd/server/",
                "internal/",
                "internal/handler/",
                "internal/service/",
                "internal/repository/",
                "internal/model/",
                "pkg/",
                "config/"
            ],
            "files": {
                "go.mod": """module github.com/example/{project_name}

go 1.21

require (
    github.com/gin-gonic/gin v1.9.1
    github.com/joho/godotenv v1.5.1
)
""",
                "cmd/server/main.go": """package main

import (
    "github.com/gin-gonic/gin"
    "github.com/joho/godotenv"
    "log"
    "os"
)

func main() {
    godotenv.Load()
    
    r := gin.Default()
    
    r.GET("/", func(c *gin.Context) {
        c.JSON(200, gin.H{
            "message": "Welcome to {project_name}",
        })
    })
    
    port := os.Getenv("PORT")
    if port == "" {
        port = "8080"
    }
    
    log.Printf("Server starting on port %s", port)
    r.Run(":" + port)
}
""",
                ".env.example": """PORT=8080
GIN_MODE=debug
DATABASE_URL=postgresql://user:password@localhost:5432/{project_name}
""",
                "Dockerfile": """FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY . .
RUN go build -o server cmd/server/main.go

FROM alpine:latest
WORKDIR /app
COPY --from=builder /app/server .
EXPOSE 8080
CMD ["./server"]
"""
            }
        }
    }
    
    # Dependency mappings between frameworks / 框架间的依赖映射
    DEPENDENCY_MAPPINGS = {
        ("spring-boot", "fastapi"): {
            "spring-boot-starter-web": "fastapi",
            "spring-boot-starter-data-jpa": "sqlalchemy",
            "spring-boot-starter-security": "python-jose[cryptography], passlib[bcrypt]",
            "spring-boot-starter-validation": "pydantic",
            "postgresql": "psycopg2-binary",
            "lombok": "pydantic (auto-generates methods)",
            "jackson": "pydantic (built-in JSON)"
        },
        ("express", "fastapi"): {
            "express": "fastapi",
            "cors": "fastapi-cors (built-in)",
            "helmet": "fastapi security headers",
            "morgan": "python logging",
            "passport": "python-jose",
            "sequelize": "sqlalchemy",
            "mongoose": "mongoengine / motor"
        },
        ("django", "spring-boot"): {
            "django": "spring-boot-starter-web",
            "djangorestframework": "spring-boot-starter-web",
            "django.contrib.auth": "spring-security",
            "psycopg2": "postgresql driver (auto-included)"
        }
    }
    
    def __init__(self, project_name: str = "myproject"):
        """
        Initialize framework translator / 初始化框架翻译器
        
        Args:
            project_name: Target project name / 目标项目名称
        """
        self.project_name = project_name.replace("-", "_").replace(" ", "_").lower()
    
    def generate_project_structure(
        self,
        target_framework: str,
        output_path: Path
    ) -> Dict[str, Any]:
        """
        Generate target framework project structure / 生成目标框架项目结构
        
        Args:
            target_framework: Target framework name / 目标框架名称
            output_path: Output directory path / 输出目录路径
            
        Returns:
            Dictionary with created files and directories / 创建的文件和目录字典
        """
        if target_framework not in self.PROJECT_TEMPLATES:
            logger.warning(f"⚠️ 没有找到 {target_framework} 的项目模板")
            return {"success": False, "message": "Template not found"}
        
        template = self.PROJECT_TEMPLATES[target_framework]
        created_files = []
        created_dirs = []
        
        try:
            # Create directories / 创建目录
            for dir_path in template["structure"]:
                dir_full_path = output_path / dir_path.format(project_name=self.project_name)
                dir_full_path.mkdir(parents=True, exist_ok=True)
                created_dirs.append(str(dir_full_path))
                logger.debug(f"📁 创建目录: {dir_full_path}")
            
            # Create files / 创建文件
            for file_path, content in template["files"].items():
                file_full_path = output_path / file_path.format(project_name=self.project_name)
                file_full_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Replace placeholders in content / 替换内容中的占位符
                processed_content = content.format(project_name=self.project_name)
                
                file_full_path.write_text(processed_content, encoding='utf-8')
                created_files.append(str(file_full_path))
                logger.debug(f"📄 创建文件: {file_full_path}")
            
            logger.info(f"✅ 成功生成 {target_framework} 项目结构")
            logger.info(f"   - 创建了 {len(created_dirs)} 个目录")
            logger.info(f"   - 创建了 {len(created_files)} 个文件")
            
            return {
                "success": True,
                "framework": target_framework,
                "created_directories": created_dirs,
                "created_files": created_files,
                "project_name": self.project_name
            }
            
        except Exception as e:
            logger.error(f"❌ 生成项目结构失败: {e}")
            return {
                "success": False,
                "message": str(e)
            }
    
    def map_dependencies(
        self,
        source_framework: str,
        target_framework: str,
        source_dependencies: List[str]
    ) -> Dict[str, str]:
        """
        Map dependencies from source to target framework
        将依赖从源框架映射到目标框架
        
        Args:
            source_framework: Source framework / 源框架
            target_framework: Target framework / 目标框架
            source_dependencies: List of source dependencies / 源依赖列表
            
        Returns:
            Dictionary of mapped dependencies / 映射的依赖字典
        """
        mapping_key = (source_framework, target_framework)
        
        if mapping_key not in self.DEPENDENCY_MAPPINGS:
            logger.warning(f"⚠️ 没有找到 {source_framework} → {target_framework} 的依赖映射")
            return {}
        
        mapping = self.DEPENDENCY_MAPPINGS[mapping_key]
        result = {}
        
        for dep in source_dependencies:
            # Try exact match / 尝试精确匹配
            if dep in mapping:
                result[dep] = mapping[dep]
            else:
                # Try partial match / 尝试部分匹配
                for source_key, target_val in mapping.items():
                    if source_key in dep:
                        result[dep] = target_val
                        break
        
        logger.info(f"📦 映射了 {len(result)} 个依赖")
        return result
    
    def get_migration_guide(
        self,
        source_framework: str,
        target_framework: str
    ) -> str:
        """
        Get migration guide for framework conversion
        获取框架转换的迁移指南
        
        Args:
            source_framework: Source framework / 源框架
            target_framework: Target framework / 目标框架
            
        Returns:
            Migration guide text / 迁移指南文本
        """
        guide = f"""
# 框架迁移指南 / Framework Migration Guide
## {source_framework} → {target_framework}

### 1. 项目结构变化 / Project Structure Changes
查看生成的项目结构以了解新的文件组织方式。

### 2. 依赖映射 / Dependency Mapping
主要依赖已自动映射。请检查 requirements.txt/pom.xml/package.json。

### 3. 配置迁移 / Configuration Migration
- 环境变量: 查看 .env.example
- 应用配置: 根据目标框架调整

### 4. 代码模式变化 / Code Pattern Changes
AI 已自动转换大部分代码模式。请注意:
- 路由定义方式
- 依赖注入模式
- 错误处理机制
- 异步/同步模式

### 5. 测试 / Testing
记得更新测试代码以适应新框架。

### 6. 部署 / Deployment
Dockerfile 已生成，可直接用于容器化部署。
"""
        return guide

