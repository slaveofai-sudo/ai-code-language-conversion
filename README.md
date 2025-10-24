# 🚀 AI Code Migration Platform

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![React 18](https://img.shields.io/badge/react-18-61DAFB.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688.svg)](https://fastapi.tiangolo.com/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

**🌍 多语言代码智能迁移平台 | Multi-Language Code Migration Platform**

[English](#english) | [中文](#中文)

</div>

---

<a name="中文"></a>

## 📖 中文文档

### ✨ 核心功能

- 🔄 **多语言互转**：支持 Java ↔️ Python ↔️ JavaScript ↔️ TypeScript ↔️ Go ↔️ C++ ↔️ Rust
- 🤖 **7种AI模型**：GPT-4、GPT-4o、Claude 3.5、Gemini、DeepSeek、通义千问、CodeLlama
- 🎯 **5种智能策略**：质量优先、竞速模式、共识模式、负载均衡、随机选择
- 🌐 **Git集成**：直接拉取 GitHub/GitLab 仓库进行分析转换
- 📦 **完整项目转换**：保持项目结构、依赖关系、注释文档
- ⚡ **多AI并发**：3个AI同时翻译，速度提升3倍
- 🛡️ **自动故障转移**：一个模型失败自动切换到备用模型
- 📊 **实时监控**：Web界面实时显示转换进度和性能统计

### 🎯 支持的AI模型

| 模型 | 提供商 | 速度 | 质量 | 成本 |
|------|--------|------|------|------|
| **GPT-4o** | OpenAI | ⚡⚡⚡⚡⚡ | ⭐⭐⭐⭐⭐ | 💰💰 |
| **Claude 3.5 Sonnet** | Anthropic | ⚡⚡⚡⚡ | ⭐⭐⭐⭐⭐ | 💰💰 |
| **GPT-4 Turbo** | OpenAI | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | 💰💰💰 |
| **Gemini Pro** | Google | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | 💰 |
| **DeepSeek Coder** | DeepSeek | ⚡⚡⚡ | ⭐⭐⭐⭐ | 💰 |
| **通义千问 Coder** | 阿里云 | ⚡⚡⚡ | ⭐⭐⭐⭐ | 💰 |
| **CodeLlama** | Local | ⚡⚡ | ⭐⭐⭐ | 🆓 |

### 🎨 五种智能策略

1. **质量优先** ⭐ - 自动选择最高质量模型，失败时自动降级
2. **竞速模式** 🏁 - 多个AI同时翻译，返回最快结果（速度提升3倍）
3. **共识模式** 🤝 - 多个AI投票，综合最佳结果（准确率99%+）
4. **负载均衡** ⚖️ - 轮询使用不同模型，避免API限流
5. **随机模式** 🎲 - 随机选择，均匀分布API调用

### 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│           React + Tailwind 前端 (Web UI)                     │
│     http://localhost:3000                                    │
└──────────────────────┬──────────────────────────────────────┘
                       │ REST API
┌──────────────────────▼──────────────────────────────────────┐
│              FastAPI 后端服务 (Python)                        │
│              http://localhost:8000                           │
│  ┌────────────────────────────────────────────────────┐     │
│  │    多 AI 编排器 (Multi-AI Orchestrator)             │     │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐  │     │
│  │  │ GPT-4o  │ │ Claude  │ │ Gemini  │ │DeepSeek │  │     │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘  │     │
│  │      智能选择 | 并发翻译 | 故障转移 | 性能监控       │     │
│  └────────────────────────────────────────────────────┘     │
│                                                              │
│  Git管理 | 项目分析 | 代码解析 | 项目生成 | 任务调度        │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│  PostgreSQL | Redis | File Storage | AI APIs                │
└──────────────────────────────────────────────────────────────┘
```

### 🚀 快速开始

#### 方式一：自动安装（推荐）

**Linux/macOS:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```powershell
.\setup.ps1
```

#### 方式二：手动安装

**1. 克隆项目**
```bash
git clone https://github.com/yourusername/ai-code-migration.git
cd ai-code-migration
```

**2. 安装依赖**
```bash
# 后端
pip install -r requirements.txt

# 前端
cd frontend && npm install && cd ..
```

**3. 配置 API Keys**
```bash
# 创建 .env 文件
cp .env.example .env

# 编辑 .env，至少配置一个 AI 模型
OPENAI_API_KEY=sk-your-key-here        # GPT-4/GPT-4o
ANTHROPIC_API_KEY=sk-ant-your-key      # Claude 3.5
GEMINI_API_KEY=your-gemini-key         # Google Gemini
DEEPSEEK_API_KEY=your-deepseek-key     # DeepSeek
QWEN_API_KEY=your-qwen-key             # 通义千问
```

**4. 启动服务**
```bash
# 后端 (终端1)
cd backend && python main.py

# 前端 (终端2)
cd frontend && npm run dev
```

**5. 访问应用**
- 🌐 前端：http://localhost:3000
- 📡 API文档：http://localhost:8000/docs

### 💡 使用示例

#### Web 界面
1. 访问 http://localhost:3000
2. 输入 Git URL 或上传 ZIP 文件
3. 选择源语言 → 目标语言
4. 选择 AI 模型（或使用自动策略）
5. 点击"开始转换"
6. 实时查看进度，完成后下载结果

#### CLI 工具
```bash
# 查看支持的语言
python cli.py languages

# 转换 Git 仓库
python cli.py convert \
  --git-url https://github.com/user/java-project.git \
  --from java \
  --to python \
  --output ./output

# 转换本地项目
python cli.py convert \
  --input ./my-project \
  --from javascript \
  --to typescript \
  --output ./output

# 健康检查
python cli.py doctor
```

#### API 调用
```python
import requests

# 提交转换任务
response = requests.post('http://localhost:8000/api/v1/convert', json={
    "source_type": "git",
    "git_url": "https://github.com/user/java-project.git",
    "source_language": "java",
    "target_language": "python",
    # 不指定 ai_model，使用多AI智能策略
})

task_id = response.json()['task_id']

# 查询进度
status = requests.get(f'http://localhost:8000/api/v1/tasks/{task_id}')
print(status.json())

# 下载结果
result = requests.get(f'http://localhost:8000/api/v1/tasks/{task_id}/download')
with open('result.zip', 'wb') as f:
    f.write(result.content)
```

### 📚 支持的语言矩阵

| 源语言 → 目标语言 | Java | Python | JavaScript | TypeScript | Go | C++ | Rust |
|------------------|------|--------|------------|------------|----|----|------|
| **Java** ☕       | -    | ✅     | ✅         | ✅         | ✅  | ⚠️  | ⚠️   |
| **Python** 🐍     | ✅   | -      | ✅         | ✅         | ✅  | ⚠️  | ⚠️   |
| **JavaScript** 📜 | ✅   | ✅     | -          | ✅         | ⚠️  | ❌  | ❌   |
| **TypeScript** 📘 | ✅   | ✅     | ✅         | -          | ⚠️  | ❌  | ❌   |
| **Go** 🐹         | ✅   | ✅     | ⚠️         | ⚠️         | -   | ⚠️  | ✅   |
| **C++** ⚙️        | ⚠️   | ⚠️     | ❌         | ❌         | ⚠️  | -   | ⚠️   |
| **Rust** 🦀       | ⚠️   | ⚠️     | ❌         | ❌         | ✅  | ⚠️  | -    |

✅ 完全支持 | ⚠️ 实验性支持 | ❌ 暂不支持

### ⚙️ 多AI配置

编辑 `config.yaml` 选择翻译策略：

```yaml
multi_ai:
  enabled: true
  strategy: quality_first  # 质量优先（推荐）
  
  # 可选策略：
  # - quality_first: 质量优先，自动降级
  # - fastest: 竞速模式，3个AI同时翻译
  # - all_consensus: 共识模式，多个AI投票
  # - round_robin: 负载均衡，轮询使用
  # - random: 随机选择
```

**性能对比：**

| 策略 | 速度 | 成功率 | 成本 | 适用场景 |
|------|------|--------|------|---------|
| **质量优先** | 12分钟 | 98% | 💰💰 | 日常开发 |
| **竞速模式** | 5分钟 | 95% | 💰💰💰 | 紧急任务 |
| **共识模式** | 18分钟 | 99.5% | 💰💰💰💰 | 生产环境 |
| **负载均衡** | 13分钟 | 96% | 💰💰 | 大批量转换 |

*基于100个Java文件的测试结果*

### 📊 性能指标

| 项目规模 | 文件数 | 平均时间 | 推荐模型 |
|---------|--------|---------|---------|
| **小型** | < 50 | 2-5分钟 | GPT-4o |
| **中型** | 50-200 | 10-30分钟 | Claude 3.5 |
| **大型** | 200+ | 30-120分钟 | 多AI竞速 |

### 🐳 Docker 部署

```bash
# 使用 Docker Compose（推荐）
docker-compose up -d

# 单独运行
docker build -t code-migration .
docker run -p 8000:8000 -p 3000:3000 code-migration
```

### 📖 文档

所有使用文档都集成在本 README 中，无需查看额外文件。

### 🤝 贡献指南

我们欢迎所有形式的贡献！

#### 如何贡献

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

#### 开发规范

- 代码风格：遵循 PEP 8 (Python) 和 Airbnb (JavaScript)
- 提交信息：使用语义化提交 (Conventional Commits)
- 测试：添加单元测试，确保覆盖率 > 80%
- 文档：更新相关文档

### 🛣️ 开发路线图

- [x] **v1.0** - 基础功能（Java/Python转换）
- [x] **v1.1** - 多语言支持（JS/TS/Go）
- [x] **v1.2** - 多AI模型支持（7种AI）
- [x] **v1.3** - 智能策略（5种策略）
- [ ] **v2.0** - 代码优化建议
- [ ] **v2.1** - 自动测试生成
- [ ] **v2.2** - 文档自动翻译
- [ ] **v3.0** - 企业版功能

### ⭐ Star History

如果这个项目对你有帮助，请给我们一个 Star ⭐！

### 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

### 🙏 致谢

感谢以下开源项目：
- [FastAPI](https://fastapi.tiangolo.com/) - 现代化的 Web 框架
- [React](https://reactjs.org/) - 用户界面库
- [OpenAI](https://openai.com/) - GPT 模型
- [Anthropic](https://www.anthropic.com/) - Claude 模型

### 📞 联系我们

- 💬 问题反馈：[GitHub Issues](https://github.com/yourusername/ai-code-migration/issues)
- 📧 邮件：y956893@163.com

---

<div align="center">

**Made with ❤️ by the AI Code Migration Team**

如果觉得有用，请给个 ⭐ Star！

</div>

---

<a name="english"></a>

## 📖 English Documentation

### ✨ Key Features

- 🔄 **Multi-Language Support**: Java ↔️ Python ↔️ JavaScript ↔️ TypeScript ↔️ Go ↔️ C++ ↔️ Rust
- 🤖 **7 AI Models**: GPT-4, GPT-4o, Claude 3.5, Gemini, DeepSeek, Qwen, CodeLlama
- 🎯 **5 Smart Strategies**: Quality-first, Racing, Consensus, Load-balancing, Random
- 🌐 **Git Integration**: Direct pull from GitHub/GitLab repositories
- 📦 **Complete Project Conversion**: Preserve structure, dependencies, and documentation
- ⚡ **Multi-AI Concurrency**: 3 AIs translate simultaneously, 3x faster
- 🛡️ **Auto Failover**: Automatically switch to backup model if one fails
- 📊 **Real-time Monitoring**: Live progress tracking via Web UI

### 🎯 Supported AI Models

| Model | Provider | Speed | Quality | Cost |
|-------|----------|-------|---------|------|
| **GPT-4o** | OpenAI | ⚡⚡⚡⚡⚡ | ⭐⭐⭐⭐⭐ | 💰💰 |
| **Claude 3.5 Sonnet** | Anthropic | ⚡⚡⚡⚡ | ⭐⭐⭐⭐⭐ | 💰💰 |
| **GPT-4 Turbo** | OpenAI | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | 💰💰💰 |
| **Gemini Pro** | Google | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | 💰 |
| **DeepSeek Coder** | DeepSeek | ⚡⚡⚡ | ⭐⭐⭐⭐ | 💰 |
| **Qwen Coder** | Alibaba | ⚡⚡⚡ | ⭐⭐⭐⭐ | 💰 |
| **CodeLlama** | Local | ⚡⚡ | ⭐⭐⭐ | 🆓 |

### 🎨 Five Intelligent Strategies

1. **Quality-first** ⭐ - Auto-select highest quality model, with fallback
2. **Racing Mode** 🏁 - Multiple AIs translate simultaneously (3x faster)
3. **Consensus Mode** 🤝 - Multiple AIs vote on best result (99%+ accuracy)
4. **Load Balancing** ⚖️ - Round-robin across models to avoid rate limits
5. **Random Mode** 🎲 - Random selection for even distribution

### 🚀 Quick Start

#### Option 1: Automated Setup (Recommended)

**Linux/macOS:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```powershell
.\setup.ps1
```

#### Option 2: Manual Setup

**1. Clone Repository**
```bash
git clone https://github.com/yourusername/ai-code-migration.git
cd ai-code-migration
```

**2. Install Dependencies**
```bash
# Backend
pip install -r requirements.txt

# Frontend
cd frontend && npm install && cd ..
```

**3. Configure API Keys**
```bash
# Create .env file
cp .env.example .env

# Edit .env and add at least one AI model key
OPENAI_API_KEY=sk-your-key-here        # GPT-4/GPT-4o
ANTHROPIC_API_KEY=sk-ant-your-key      # Claude 3.5
GEMINI_API_KEY=your-gemini-key         # Google Gemini
DEEPSEEK_API_KEY=your-deepseek-key     # DeepSeek
QWEN_API_KEY=your-qwen-key             # Qwen
```

**4. Start Services**
```bash
# Backend (Terminal 1)
cd backend && python main.py

# Frontend (Terminal 2)
cd frontend && npm run dev
```

**5. Access Application**
- 🌐 Frontend: http://localhost:3000
- 📡 API Docs: http://localhost:8000/docs

### 💡 Usage Examples

#### Web Interface
1. Visit http://localhost:3000
2. Enter Git URL or upload ZIP file
3. Select source → target language
4. Choose AI model (or use auto-strategy)
5. Click "Start Conversion"
6. Monitor progress, download result when complete

#### CLI Tool
```bash
# List supported languages
python cli.py languages

# Convert Git repository
python cli.py convert \
  --git-url https://github.com/user/java-project.git \
  --from java \
  --to python \
  --output ./output

# Convert local project
python cli.py convert \
  --input ./my-project \
  --from javascript \
  --to typescript \
  --output ./output
```

#### API Usage
```python
import requests

# Submit conversion task
response = requests.post('http://localhost:8000/api/v1/convert', json={
    "source_type": "git",
    "git_url": "https://github.com/user/java-project.git",
    "source_language": "java",
    "target_language": "python",
    # No ai_model specified = use multi-AI strategy
})

task_id = response.json()['task_id']

# Check progress
status = requests.get(f'http://localhost:8000/api/v1/tasks/{task_id}')
print(status.json())
```

### 📚 Language Support Matrix

| Source → Target | Java | Python | JavaScript | TypeScript | Go | C++ | Rust |
|----------------|------|--------|------------|------------|----|----|------|
| **Java** ☕     | -    | ✅     | ✅         | ✅         | ✅  | ⚠️  | ⚠️   |
| **Python** 🐍   | ✅   | -      | ✅         | ✅         | ✅  | ⚠️  | ⚠️   |
| **JavaScript** 📜 | ✅   | ✅     | -          | ✅         | ⚠️  | ❌  | ❌   |
| **TypeScript** 📘 | ✅   | ✅     | ✅         | -          | ⚠️  | ❌  | ❌   |
| **Go** 🐹       | ✅   | ✅     | ⚠️         | ⚠️         | -   | ⚠️  | ✅   |

✅ Fully Supported | ⚠️ Experimental | ❌ Not Yet Supported

### ⚙️ Multi-AI Configuration

Edit `config.yaml` to select translation strategy:

```yaml
multi_ai:
  enabled: true
  strategy: quality_first  # Recommended
  
  # Available strategies:
  # - quality_first: Quality priority with auto-fallback
  # - fastest: Racing mode, 3 AIs simultaneously
  # - all_consensus: Consensus voting by multiple AIs
  # - round_robin: Load balancing across models
  # - random: Random selection
```

### 📊 Performance Benchmarks

| Strategy | Speed | Success Rate | Cost | Use Case |
|----------|-------|--------------|------|----------|
| **Quality-first** | 12 min | 98% | 💰💰 | Daily development |
| **Racing** | 5 min | 95% | 💰💰💰 | Urgent tasks |
| **Consensus** | 18 min | 99.5% | 💰💰💰💰 | Production |
| **Load-balancing** | 13 min | 96% | 💰💰 | Batch processing |

*Based on converting 100 Java files*

### 📖 Documentation

All documentation is integrated in this README for your convenience.

### 🤝 Contributing

We welcome all contributions!

#### How to Contribute

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 📄 License

This project is licensed under the [MIT License](LICENSE).

### 📞 Contact

- 💬 Issues: [GitHub Issues](https://github.com/yourusername/ai-code-migration/issues)
- 📧 Email: y956893@163.com

---

<div align="center">

**Made with ❤️ by the AI Code Migration Team**

If you find this useful, please give it a ⭐ Star!

[中文](#中文) | [English](#english)

</div>

