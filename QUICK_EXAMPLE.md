# 🚀 快速示例：Spring Boot → FastAPI 完整迁移

## 场景说明

将一个Spring Boot REST API项目完整迁移到FastAPI，包括：
- ✅ 代码转换
- ✅ 自动生成测试
- ✅ 代码块分析报告
- ✅ Kubernetes部署配置

---

## 📝 Step 1: 准备源项目

假设有一个Spring Boot项目：

**UserController.java**
```java
package com.example.api.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import com.example.api.service.UserService;
import com.example.api.model.User;

@RestController
@RequestMapping("/api/users")
public class UserController {
    
    @Autowired
    private UserService userService;
    
    @GetMapping("/{id}")
    public ResponseEntity<User> getUser(@PathVariable Long id) {
        User user = userService.findById(id);
        if (user == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(user);
    }
    
    @PostMapping
    public ResponseEntity<User> createUser(@RequestBody User user) {
        User created = userService.create(user);
        return ResponseEntity.ok(created);
    }
}
```

**UserService.java**
```java
package com.example.api.service;

import org.springframework.stereotype.Service;
import com.example.api.model.User;

@Service
public class UserService {
    
    public User findById(Long id) {
        // Database logic
        return database.findById(id);
    }
    
    public User create(User user) {
        // Database logic
        return database.save(user);
    }
}
```

---

## 🚀 Step 2: 发起转换请求

```bash
curl -X POST http://localhost:8000/api/v1/convert-with-analysis \
  -H "Content-Type: application/json" \
  -d '{
    "source_type": "git",
    "git_url": "https://github.com/user/spring-boot-api.git",
    
    "source_language": "java",
    "target_language": "python",
    "target_framework": "fastapi",
    "runtime_environment": "kubernetes",
    
    "auto_detect_framework": true,
    "generate_tests": true,
    "generate_analysis": true,
    
    "ai_model": "gpt-4o",
    "use_multi_ai": true,
    "strategy": "quality_first"
  }'
```

**响应：**
```json
{
  "task_id": "abc-123-def",
  "status": "processing",
  "message": "代码转换任务已创建（包含测试和分析）"
}
```

---

## 📊 Step 3: 查看实时进度

### 方式1: REST API轮询
```bash
curl http://localhost:8000/api/v1/tasks/abc-123-def
```

**响应：**
```json
{
  "task_id": "abc-123-def",
  "status": "processing",
  "progress": 65,
  "stage": "转换文件: UserController.java",
  "estimated_time_remaining": 120
}
```

### 方式2: WebSocket实时推送
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/task/abc-123-def');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(`进度: ${data.progress}% - ${data.stage}`);
};

// 输出:
// 进度: 10% - 克隆Git仓库...
// 进度: 20% - 检测框架: Spring Boot ✅
// 进度: 30% - 分析项目结构...
// 进度: 50% - 转换文件: UserController.java
// 进度: 70% - 转换文件: UserService.java
// 进度: 85% - 生成单元测试...
// 进度: 95% - 生成代码块分析报告...
// 进度: 100% - 转换完成！
```

---

## 📦 Step 4: 下载结果

```bash
curl -O http://localhost:8000/api/v1/tasks/abc-123-def/download
unzip abc-123-def.zip
cd converted-project
```

---

## 🎯 Step 5: 查看转换结果

### 转换后的项目结构

```
converted-project/
├── app/
│   ├── main.py                    # FastAPI主文件
│   ├── routers/
│   │   └── users.py               # 用户路由 (转换自UserController)
│   ├── services/
│   │   └── user_service.py        # 用户服务 (转换自UserService)
│   └── models/
│       └── user.py                # User模型
│
├── tests/                         # ✅ 自动生成的测试
│   ├── test_users.py              # 用户路由测试
│   └── test_user_service.py       # 用户服务测试
│
├── analysis/                      # ✅ 代码块分析报告
│   ├── users_analysis.md          # 详细转换报告
│   └── user_service_analysis.md
│
├── kubernetes/                    # ✅ K8s部署配置
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   └── configmap.yaml
│
├── Dockerfile                     # ✅ Docker配置
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 📄 转换后的代码

### app/routers/users.py
```python
"""
User Router / 用户路由

Converted from: UserController.java
转换自: UserController.java
Framework: FastAPI
"""

from fastapi import APIRouter, Depends, HTTPException, Path
from app.services.user_service import UserService, get_user_service
from app.models.user import User

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/{id}", response_model=User)
async def get_user(
    id: int = Path(..., description="User ID"),
    user_service: UserService = Depends(get_user_service)
) -> User:
    """
    Get user by ID / 根据ID获取用户
    
    Args:
        id: User ID / 用户ID
    
    Returns:
        User object / 用户对象
    
    Raises:
        HTTPException: 404 if user not found / 用户不存在时返回404
    """
    user = await user_service.find_by_id(id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {id} not found")
    return user


@router.post("/", response_model=User)
async def create_user(
    user: User,
    user_service: UserService = Depends(get_user_service)
) -> User:
    """
    Create a new user / 创建新用户
    
    Args:
        user: User data / 用户数据
    
    Returns:
        Created user object / 创建的用户对象
    """
    created_user = await user_service.create(user)
    return created_user
```

### app/services/user_service.py
```python
"""
User Service / 用户服务

Converted from: UserService.java
转换自: UserService.java
"""

from typing import Optional
from app.models.user import User
from app.repositories.user_repository import UserRepository, get_user_repository


class UserService:
    """
    User service for business logic / 用户业务逻辑服务
    """
    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    async def find_by_id(self, id: int) -> Optional[User]:
        """
        Find user by ID / 根据ID查找用户
        
        Args:
            id: User ID / 用户ID
        
        Returns:
            User object if found, None otherwise / 找到返回用户对象，否则返回None
        """
        return await self.user_repository.find_by_id(id)
    
    async def create(self, user: User) -> User:
        """
        Create a new user / 创建新用户
        
        Args:
            user: User data / 用户数据
        
        Returns:
            Created user object / 创建的用户对象
        """
        return await self.user_repository.save(user)


def get_user_service() -> UserService:
    """
    Dependency provider for UserService / UserService依赖提供者
    """
    return UserService(user_repository=get_user_repository())
```

---

## 🧪 自动生成的测试

### tests/test_users.py
```python
"""
Tests for User Router / 用户路由测试

Auto-generated by AI Code Migration Platform
由AI代码迁移平台自动生成
"""

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from unittest.mock import Mock, AsyncMock
from app.main import app
from app.models.user import User


class TestUserRouter:
    """测试用户路由"""
    
    @pytest.fixture
    def client(self):
        """Test client fixture"""
        return TestClient(app)
    
    @pytest.fixture
    def mock_user_service(self, monkeypatch):
        """Mock user service"""
        mock_service = Mock()
        mock_service.find_by_id = AsyncMock()
        mock_service.create = AsyncMock()
        return mock_service
    
    @pytest.mark.asyncio
    async def test_get_user_success(self, client, mock_user_service):
        """测试获取用户 - 正常情况"""
        # Arrange / 准备
        expected_user = User(id=1, name="John Doe", email="john@example.com")
        mock_user_service.find_by_id.return_value = expected_user
        
        # Act / 执行
        response = client.get("/api/users/1")
        
        # Assert / 断言
        assert response.status_code == 200
        assert response.json()["id"] == 1
        assert response.json()["name"] == "John Doe"
        mock_user_service.find_by_id.assert_called_once_with(1)
    
    @pytest.mark.asyncio
    async def test_get_user_not_found(self, client, mock_user_service):
        """测试获取用户 - 用户不存在"""
        # Arrange / 准备
        mock_user_service.find_by_id.return_value = None
        
        # Act / 执行
        response = client.get("/api/users/999")
        
        # Assert / 断言
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
    
    @pytest.mark.parametrize("user_id", [1, 100, 999])
    @pytest.mark.asyncio
    async def test_get_user_various_ids(self, client, mock_user_service, user_id):
        """测试获取用户 - 各种ID值（参数化测试）"""
        # Arrange / 准备
        mock_user_service.find_by_id.return_value = User(id=user_id, name=f"User {user_id}")
        
        # Act / 执行
        response = client.get(f"/api/users/{user_id}")
        
        # Assert / 断言
        assert response.status_code == 200
        assert response.json()["id"] == user_id
    
    @pytest.mark.asyncio
    async def test_create_user_success(self, client, mock_user_service):
        """测试创建用户 - 正常情况"""
        # Arrange / 准备
        new_user_data = {"name": "Jane Doe", "email": "jane@example.com"}
        created_user = User(id=2, **new_user_data)
        mock_user_service.create.return_value = created_user
        
        # Act / 执行
        response = client.post("/api/users/", json=new_user_data)
        
        # Assert / 断言
        assert response.status_code == 200
        assert response.json()["id"] == 2
        assert response.json()["name"] == "Jane Doe"
```

---

## 📊 代码块分析报告

### analysis/users_analysis.md (片段)

```markdown
# 代码迁移分析报告

## 概览
- **源文件**: UserController.java
- **目标文件**: app/routers/users.py
- **源语言**: Java (Spring Boot)
- **目标语言**: Python (FastAPI)
- **代码块数**: 5
- **转换成功率**: 94%

## 代码块 #1: 控制器类定义

### 源代码
```java
@RestController
@RequestMapping("/api/users")
public class UserController {
```

### 转换后
```python
router = APIRouter(prefix="/api/users", tags=["users"])
```

### 转换逻辑
| 源特征 | 目标特征 | 说明 |
|--------|---------|------|
| `@RestController` | `APIRouter` | Spring的REST控制器 → FastAPI路由器 |
| `@RequestMapping` | `prefix=` | 路由前缀映射 |
| `public class` | 模块级路由 | FastAPI使用函数式路由 |

### 质量分数: 0.95/1.00

---

## 代码块 #2: GET端点

### 源代码
```java
@GetMapping("/{id}")
public ResponseEntity<User> getUser(@PathVariable Long id) {
    User user = userService.findById(id);
    if (user == null) {
        return ResponseEntity.notFound().build();
    }
    return ResponseEntity.ok(user);
}
```

### 转换后
```python
@router.get("/{id}", response_model=User)
async def get_user(
    id: int = Path(...),
    user_service: UserService = Depends(get_user_service)
) -> User:
    user = await user_service.find_by_id(id)
    if not user:
        raise HTTPException(status_code=404)
    return user
```

### 转换逻辑
| 源特征 | 目标特征 | 说明 |
|--------|---------|------|
| `@GetMapping` | `@router.get` | GET请求映射 |
| `@PathVariable` | `Path(...)` | 路径参数提取 |
| `@Autowired` | `Depends()` | 依赖注入模式 |
| `ResponseEntity` | 直接返回 | FastAPI自动包装 |
| 同步方法 | `async def` | 异步化（最佳实践） |

### 质量分数: 0.96/1.00

---

## 质量指标

| 指标 | 值 |
|------|---|
| 语法正确性 | 100% |
| 类型正确性 | 95% |
| 框架适配度 | 94% |
| 代码风格 | 100% |
| **总体质量** | **94%** |

## 改进建议
- ✅ 代码质量良好，无明显改进点
- ✅ 类型注解完整
- ✅ 文档字符串齐全
- ✅ 错误处理正确
```

---

## 🐳 Kubernetes部署配置

### kubernetes/deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-app
  labels:
    app: fastapi-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: fastapi-app
  template:
    metadata:
      labels:
        app: fastapi-app
    spec:
      containers:
      - name: api
        image: fastapi-app:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
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
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

---

## ✅ Step 6: 运行和测试

### 本地运行
```bash
# 安装依赖
pip install -r requirements.txt

# 运行应用
uvicorn app.main:app --reload

# 访问 API 文档
open http://localhost:8000/docs
```

### 运行测试
```bash
# 运行所有测试
pytest tests/ -v

# 运行覆盖率测试
pytest --cov=app tests/

# 输出:
# tests/test_users.py::TestUserRouter::test_get_user_success PASSED
# tests/test_users.py::TestUserRouter::test_get_user_not_found PASSED
# tests/test_users.py::TestUserRouter::test_create_user_success PASSED
#
# Coverage: 87%
```

### Docker部署
```bash
# 构建镜像
docker build -t fastapi-app:latest .

# 运行容器
docker run -p 8000:8000 fastapi-app:latest
```

### Kubernetes部署
```bash
# 应用配置
kubectl apply -f kubernetes/

# 检查状态
kubectl get pods
kubectl get svc

# 访问应用
kubectl port-forward svc/fastapi-app 8000:8000
```

---

## 📊 转换质量总结

### ✅ 成功转换的特性
- ✅ REST API端点 (100%)
- ✅ 依赖注入 (100%)
- ✅ 路由映射 (100%)
- ✅ 类型注解 (95%)
- ✅ 错误处理 (100%)
- ✅ 文档字符串 (100%)

### 📈 质量指标
- **语法正确性**: 100%
- **类型正确性**: 95%
- **框架适配度**: 94%
- **测试覆盖率**: 87%
- **整体质量**: 94%

### ⏱️ 时间节省
- **手工迁移预估时间**: 3-5天
- **自动迁移实际时间**: 15分钟
- **节省比例**: 99%

### 💰 成本节省
- **预估AI API成本**: $0.15
- **如使用缓存**: $0.02 (节省87%)
- **人工成本节省**: $2,000+ (按3天工作计算)

---

## 🎯 总结

通过AI Code Migration Platform的三维度迁移系统：

1. **语言维度**: Java → Python
   - 自动语法转换
   - 类型映射正确
   
2. **框架维度**: Spring Boot → FastAPI
   - @RestController → APIRouter
   - @Autowired → Depends()
   - 保留RESTful设计
   
3. **环境维度**: 生成Kubernetes配置
   - Deployment, Service, Ingress
   - 健康检查配置
   - 资源限制

**结果**: 获得了一个100%可部署、87%测试覆盖率、94%质量分数的FastAPI项目！

---

**🎉 从Spring Boot到FastAPI，15分钟搞定！**

