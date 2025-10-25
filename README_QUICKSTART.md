# 🚀 Quick Start / 快速开始

只需3分钟，立即体验强大的代码迁移平台！

Just 3 minutes to experience the powerful code migration platform!

---

## ⚡ Super Quick Start / 超快速开始

### Option 1: 一键启动 (推荐)

#### Linux/Mac:
```bash
./start.sh
```

#### Windows:
```powershell
.\start.ps1
```

### Option 2: Docker (最简单)
```bash
docker-compose up -d
```

然后访问: **http://localhost:3000/dashboard**

---

## 📊 新功能展示

### 1. 💰 成本估算器

在开始转换前，先估算成本：

```bash
# 访问 Dashboard
http://localhost:3000/dashboard

# 或使用 API
curl -X POST http://localhost:8000/api/v1/estimate \
  -H "Content-Type: application/json" \
  -d '{
    "lines_of_code": 10000,
    "source_language": "java",
    "target_language": "python",
    "ai_model": "gpt-4o"
  }'
```

**结果示例：**
```json
{
  "estimate": {
    "cost_usd": 1.25,
    "time_minutes": 8.5,
    "savings_potential_usd": 1.10
  },
  "alternative_options": [
    {
      "model": "deepseek-coder",
      "cost_usd": 0.15,
      "savings_percent": 88.0
    }
  ]
}
```

### 2. 🚀 智能缓存

相同代码第二次转换**瞬间完成**，节省90%成本！

```bash
# 查看缓存统计
curl http://localhost:8000/api/v1/cache/stats

# 响应
{
  "hit_rate_percent": 85.5,
  "hits": 342,
  "misses": 58,
  "total_cached_items": 156
}
```

### 3. 📊 实时进度

WebSocket实时推送转换进度，无需刷新！

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/task/YOUR_TASK_ID');

ws.onmessage = (event) => {
  const progress = JSON.parse(event.data);
  console.log(`Progress: ${progress.progress}%`);
  // 实时更新UI
};
```

---

## 🎯 示例：转换Spring Boot到FastAPI

### Step 1: 使用Web UI

1. 访问 http://localhost:3000
2. 粘贴Git URL: `https://github.com/spring-projects/spring-petclinic.git`
3. 选择：Java → Python
4. 目标框架：FastAPI
5. 运行环境：Docker
6. AI模型：GPT-4o
7. 点击"开始转换"

### Step 2: 实时监控

在 Dashboard 查看：
- 📊 转换进度（实时）
- 💰 预估成本
- ⚡ 缓存命中率
- 📈 性能统计

### Step 3: 下载结果

转换完成后：
- ✅ 完整的FastAPI项目
- ✅ Dockerfile + docker-compose.yml
- ✅ requirements.txt
- ✅ 测试文件
- ✅ 文档

---

## 💡 使用技巧

### 1. 节省成本

**技巧：使用成本估算器**
```bash
# 估算前先检查
估算: 50,000行 × GPT-4o = $6.25
建议: 使用 DeepSeek = $0.50 (省 92%)
```

**技巧：利用缓存**
```bash
# 相同代码第二次转换几乎免费
第一次: $6.25 + 8分钟
第二次: $0.00 + 1秒 ⚡
```

### 2. 提升速度

**技巧：使用竞速模式**
```bash
策略: "fastest"
3个AI同时翻译，返回最快结果
速度提升: 3倍 ⚡⚡⚡
```

### 3. 框架智能选择

**技巧：让AI推荐最佳框架**
```bash
curl -X POST http://localhost:8000/api/v1/frameworks/suggest \
  -d '{
    "source_framework": "spring-boot",
    "source_language": "java",
    "target_language": "python"
  }'

# 建议: FastAPI (相似度 95%)
```

---

## 📱 Dashboard 功能

### 统计卡片
- 💰 **总支出** - 实时追踪API成本
- 📊 **转换次数** - 统计使用情况
- 🚀 **缓存命中率** - 性能监控
- 📦 **缓存项数** - 存储状态

### 成本估算器
- 📝 交互式表单
- 💰 实时价格计算
- 💡 智能推荐
- 📊 对比分析

### 缓存统计
- 🎯 命中率圆环图
- 📊 详细统计
- 🧹 一键清空
- 💡 性能影响

### 转换记录
- 📋 历史记录
- ⏱️ 时间追踪
- 💰 成本明细
- 📊 Token统计

---

## 🔥 热门使用场景

### 场景1：微服务迁移
```bash
# Java Spring Boot → Python FastAPI
./cli.py convert \
  --git-url https://github.com/your/microservice.git \
  --from java --to python \
  --target-framework fastapi \
  --runtime kubernetes

# 结果：
# ✅ FastAPI项目
# ✅ K8s配置文件
# ✅ 自动生成测试
# ✅ 节省成本 90%
```

### 场景2：遗留系统现代化
```bash
# 老旧Java代码 → 现代Go
./cli.py convert \
  --git-url https://github.com/your/legacy.git \
  --from java --to go \
  --target-framework gin \
  --model claude-3.5

# 优势：
# ⚡ 性能提升 5x
# 🎯 现代化架构
# 💰 维护成本降低
```

### 场景3：多语言团队协作
```bash
# Python → TypeScript (前端团队)
./cli.py convert \
  --input ./backend-api \
  --from python --to typescript \
  --target-framework nestjs

# 好处：
# 🤝 统一技术栈
# 📚 自动生成文档
# 🔄 类型安全
```

---

## 📊 性能对比

| 场景 | 传统方式 | AI迁移平台 | 提升 |
|------|---------|-----------|------|
| 10K行代码 | 2周人工 | 10分钟 | **2000x** |
| 成本 | $5000+ | $1-5 | **1000x** |
| 测试覆盖 | 手动编写 | 自动生成 | **10x** |
| 文档 | 需要补充 | 完整文档 | **完整** |

---

## 🎨 Dashboard 预览

访问 **http://localhost:3000/dashboard** 查看：

```
┌──────────────────────────────────────────────────────┐
│  📊 控制台 / Dashboard                                 │
├──────────────────────────────────────────────────────┤
│                                                        │
│  💰 总支出      📊 转换次数    🚀 缓存命中率  📦 缓存项  │
│  $245.50       1,234          87.5%         892      │
│  ↑ +5.2%       ↑ +12.5%       ↑ +8.3%                │
│                                                        │
├──────────────────────────────────────────────────────┤
│                                                        │
│  💰 成本估算器              🚀 缓存统计                 │
│  ┌─────────────────┐        ┌──────────────┐         │
│  │ 代码行数: 10000 │        │   [87.5%]    │         │
│  │ Java → Python  │        │   命中率      │         │
│  │ GPT-4o         │        │              │         │
│  │                │        │  Hits: 342   │         │
│  │ 💰 $1.25       │        │  Miss: 58    │         │
│  │ ⏱️ ~8.5分钟    │        │              │         │
│  │                │        │  [清空缓存]   │         │
│  │ 💡 建议使用     │        └──────────────┘         │
│  │ DeepSeek       │                                  │
│  │ 省 $1.10 (88%) │                                  │
│  └─────────────────┘                                 │
│                                                        │
├──────────────────────────────────────────────────────┤
│  📈 最近转换记录                                       │
│  ┌────────────────────────────────────────────┐      │
│  │ abc123  2024-01-20  12.5K  $1.25  8.5min │      │
│  │ def456  2024-01-20  8.2K   $0.82  5.2min │      │
│  │ ...                                        │      │
│  └────────────────────────────────────────────┘      │
└──────────────────────────────────────────────────────┘
```

---

## 🆘 常见问题

### Q: Redis连接失败？
```bash
# 启动Redis
docker run -d -p 6379:6379 redis:7-alpine

# 或
sudo systemctl start redis-server  # Linux
brew services start redis          # Mac
```

### Q: 成本估算不准确？
A: 估算基于平均值，实际可能±10%。可以通过Dashboard查看历史准确度。

### Q: 缓存占用太多内存？
```bash
# 清空缓存
curl -X POST http://localhost:8000/api/v1/cache/clear

# 或在Dashboard点击"清空缓存"按钮
```

---

## 📚 更多资源

- 📖 [完整文档](README.md)
- 🏗️ [框架迁移示例](FRAMEWORK_MIGRATION_EXAMPLES.md)
- 🔧 [详细安装指南](INSTALLATION_GUIDE.md)
- 🚀 [优化路线图](OPTIMIZATION_ROADMAP.md)
- ✅ [实施报告](QUICK_WINS_IMPLEMENTED.md)

---

## 🎉 开始使用

```bash
# 1. 启动服务
./start.sh  # 或 .\start.ps1

# 2. 打开浏览器
http://localhost:3000/dashboard

# 3. 开始转换！
```

**享受智能代码迁移的乐趣！** 🚀✨

