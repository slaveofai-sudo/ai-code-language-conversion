# 🚀 Installation Guide / 安装指南

完整的安装和配置指南，包含新增的缓存、WebSocket和成本估算功能。

Complete installation and configuration guide including new cache, WebSocket, and cost estimation features.

---

## 📋 Prerequisites / 先决条件

### Required / 必需
- Python 3.9+ 
- Node.js 18+
- Redis 6.0+ (用于缓存)
- Git

### Optional / 可选
- Docker & Docker Compose (用于容器化部署)
- PostgreSQL 13+ (用于生产环境)

---

## 🔧 Installation / 安装

### Method 1: Quick Setup (Recommended) / 方法1：快速安装（推荐）

#### Linux/macOS:
```bash
chmod +x setup.sh
./setup.sh
```

#### Windows:
```powershell
.\setup.ps1
```

### Method 2: Manual Setup / 方法2：手动安装

#### Step 1: Clone Repository / 克隆仓库
```bash
git clone https://github.com/slaveofai-sudo/ai-code-language-conversion.git
cd ai-code-language-conversion
```

#### Step 2: Install Redis / 安装Redis

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server

# 验证Redis是否运行
redis-cli ping
# 应该返回: PONG
```

**macOS:**
```bash
brew install redis
brew services start redis

# 验证Redis是否运行
redis-cli ping
```

**Windows:**
```powershell
# 下载Redis for Windows
# https://github.com/microsoftarchive/redis/releases

# 或使用WSL2
wsl --install
# 然后在WSL中安装Redis
```

**Docker方式:**
```bash
docker run -d -p 6379:6379 --name redis redis:7-alpine
```

#### Step 3: Backend Setup / 后端设置

```bash
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# 安装依赖
pip install -r ../requirements.txt

# 配置环境变量
cp .env.example .env
```

**编辑 `.env` 文件:**
```bash
# AI API Keys
OPENAI_API_KEY=sk-your-openai-key
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key
GOOGLE_API_KEY=your-google-key
DEEPSEEK_API_KEY=your-deepseek-key
QWEN_API_KEY=your-qwen-key

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# Server Configuration
HOST=0.0.0.0
PORT=8000
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# Directories
UPLOAD_DIR=./data/uploads
OUTPUT_DIR=./data/outputs
CACHE_DIR=./data/cache
```

#### Step 4: Frontend Setup / 前端设置

```bash
cd ../frontend

# 安装依赖
npm install

# 配置环境变量
cp .env.example .env.local
```

**编辑 `.env.local` 文件:**
```bash
VITE_API_BASE_URL=http://localhost:8000
VITE_WS_BASE_URL=ws://localhost:8000
```

---

## 🚀 Running the Application / 运行应用

### Development Mode / 开发模式

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # 或 .\venv\Scripts\activate (Windows)
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Terminal 3 - Redis (如果没有作为服务运行):**
```bash
redis-server
```

### Production Mode with Docker / Docker生产模式

```bash
# 构建和启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

---

## ✅ Verification / 验证

### 1. Check Redis / 检查Redis
```bash
redis-cli ping
# 应该返回: PONG
```

### 2. Check Backend / 检查后端
```bash
curl http://localhost:8000/
# 应该返回: {"service":"AI Code Migration Platform","status":"running","version":"1.4.0"}
```

### 3. Check Cache / 检查缓存
```bash
curl http://localhost:8000/api/v1/cache/stats
# 应该返回缓存统计信息
```

### 4. Check WebSocket / 检查WebSocket
```bash
# 使用wscat工具测试
npm install -g wscat
wscat -c ws://localhost:8000/ws/task/test-id
```

### 5. Check Frontend / 检查前端
打开浏览器访问: http://localhost:3000

### 6. Check Dashboard / 检查仪表板
访问: http://localhost:3000/dashboard

---

## 🎯 Testing New Features / 测试新功能

### 1. Test Cost Estimation / 测试成本估算

```bash
curl -X POST http://localhost:8000/api/v1/estimate \
  -H "Content-Type: application/json" \
  -d '{
    "lines_of_code": 10000,
    "source_language": "java",
    "target_language": "python",
    "ai_model": "gpt-4o"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "estimate": {
    "cost_usd": 1.25,
    "time_minutes": 8.5,
    "total_tokens": 250000,
    "alternative_options": [...]
  }
}
```

### 2. Test Caching / 测试缓存

```bash
# 第一次请求（会调用API）
time curl -X POST http://localhost:8000/api/v1/convert ...

# 第二次相同请求（从缓存读取）
time curl -X POST http://localhost:8000/api/v1/convert ...
# 应该快得多！
```

### 3. Test WebSocket Progress / 测试WebSocket进度

**前端示例:**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/task/YOUR_TASK_ID');

ws.onopen = () => console.log('Connected');
ws.onmessage = (event) => {
  const progress = JSON.parse(event.data);
  console.log(`Progress: ${progress.progress}%`);
  console.log(`Status: ${progress.message}`);
};
```

---

## 🔧 Configuration / 配置

### Redis Configuration / Redis配置

**基础配置** (`redis.conf`):
```conf
# 最大内存限制
maxmemory 256mb

# 内存淘汰策略
maxmemory-policy allkeys-lru

# 持久化（可选）
save 900 1
save 300 10
save 60 10000
```

**应用配置**:
```python
# backend/core/cache_manager.py
cache_manager = CacheManager(
    redis_url="redis://localhost:6379/0",
    default_ttl=3600  # 1小时
)
```

### Cache Strategy / 缓存策略

```yaml
# config.yaml
cache:
  enabled: true
  backend: redis  # redis or memory
  ttl:
    development: 600      # 10分钟（开发）
    production: 86400     # 24小时（生产）
  max_size: 1000         # 最大缓存项数
  clear_on_startup: false
```

---

## 📊 Monitoring / 监控

### 1. Redis Monitoring / Redis监控

```bash
# 实时监控Redis命令
redis-cli monitor

# 查看Redis状态
redis-cli info

# 查看缓存键数量
redis-cli DBSIZE

# 查看特定模式的键
redis-cli KEYS "translation:*"
```

### 2. Application Monitoring / 应用监控

访问Dashboard查看实时统计:
- 成本统计
- 缓存命中率
- 转换历史
- 性能指标

### 3. Logs / 日志

```bash
# Backend logs
tail -f backend/logs/app.log

# Redis logs
tail -f /var/log/redis/redis-server.log

# Docker logs
docker-compose logs -f backend
```

---

## 🐛 Troubleshooting / 故障排查

### Issue 1: Redis Connection Failed / Redis连接失败

**症状:**
```
ConnectionError: Error connecting to Redis
```

**解决方案:**
```bash
# 检查Redis是否运行
redis-cli ping

# 如果没运行，启动Redis
sudo systemctl start redis-server  # Linux
brew services start redis          # macOS
docker start redis                 # Docker

# 检查端口是否被占用
netstat -an | grep 6379
```

### Issue 2: WebSocket Connection Error / WebSocket连接错误

**症状:**
```
WebSocket connection failed
```

**解决方案:**
```bash
# 1. 检查后端是否运行
curl http://localhost:8000/

# 2. 检查防火墙设置
sudo ufw allow 8000

# 3. 检查CORS配置
# 确保 .env 中 ALLOWED_ORIGINS 包含前端地址
```

### Issue 3: Cache Not Working / 缓存不工作

**症状:**
```
Cache hit rate: 0%
```

**解决方案:**
```bash
# 1. 检查Redis连接
redis-cli ping

# 2. 检查缓存配置
curl http://localhost:8000/api/v1/cache/stats

# 3. 清空缓存重试
curl -X POST http://localhost:8000/api/v1/cache/clear

# 4. 检查日志
tail -f backend/logs/app.log | grep cache
```

### Issue 4: High Memory Usage / 内存占用过高

**解决方案:**
```bash
# 1. 检查Redis内存使用
redis-cli info memory

# 2. 设置内存限制
redis-cli CONFIG SET maxmemory 256mb
redis-cli CONFIG SET maxmemory-policy allkeys-lru

# 3. 清空缓存
redis-cli FLUSHDB
```

---

## 🔒 Security Checklist / 安全检查清单

### Before Production / 生产环境前

- [ ] 更改所有默认密码
- [ ] 配置Redis密码认证
- [ ] 启用HTTPS
- [ ] 配置CORS白名单
- [ ] 设置API速率限制
- [ ] 启用日志记录
- [ ] 配置防火墙规则
- [ ] 定期备份Redis数据
- [ ] 监控异常活动
- [ ] 更新所有依赖到最新版本

### Redis Security / Redis安全

```bash
# 编辑 redis.conf
requirepass your-strong-password
bind 127.0.0.1
protected-mode yes
```

**更新应用配置:**
```bash
REDIS_URL=redis://:your-strong-password@localhost:6379/0
```

---

## 📈 Performance Tuning / 性能调优

### Redis Optimization / Redis优化

```conf
# redis.conf
maxclients 10000
tcp-backlog 511
timeout 0
tcp-keepalive 300

# 使用更快的持久化策略
appendonly no
save ""
```

### Application Optimization / 应用优化

```python
# 增加连接池大小
cache_manager = CacheManager(
    redis_url="redis://localhost:6379/0",
    connection_pool_size=50
)

# 批量操作
await cache_manager.set_many([
    ("key1", "value1"),
    ("key2", "value2")
])
```

---

## 📚 Additional Resources / 其他资源

- [Redis Documentation](https://redis.io/docs/)
- [FastAPI WebSockets](https://fastapi.tiangolo.com/advanced/websockets/)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [Project README](README.md)
- [API Documentation](http://localhost:8000/docs)

---

## 🆘 Getting Help / 获取帮助

如果遇到问题:

1. **查看日志文件** - 通常包含详细错误信息
2. **检查GitHub Issues** - 可能有人遇到过相同问题
3. **提交Issue** - 详细描述问题和复现步骤
4. **联系支持** - your-email@example.com

---

**🎉 安装完成！享受强大的代码迁移平台吧！**

访问 http://localhost:3000/dashboard 查看漂亮的可视化界面！

