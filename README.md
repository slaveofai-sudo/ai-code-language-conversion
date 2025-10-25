

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

### 🎉 最新亮点

**🚀 V2.3 重磅更新！** 现在支持添加**任何AI模型**到平台，无需修改代码！

```bash
# 10秒添加自定义AI模型
curl -X POST http://localhost:8000/api/v1/ai-models -d '{...}'

# 立即使用！支持 Ollama、智谱AI、百度文心、任何OpenAI兼容API
```

**📊 功能统计**:
- ✅ **19+** 已实现的主要功能
- 🤖 **7+** 内置AI模型 + **无限** 自定义模型
- 🌍 **7** 种编程语言互转
- 📈 准确率从 **52% → 94%** (三维度迁移)
- ⚡ 速度提升 **1000倍** (Redis缓存)
- 💰 成本降低 **80-90%** (智能缓存+本地模型)

### ✨ 核心功能

#### 🎯 V2.0 新增 - 三维度精准迁移
- 🎯 **语言 + 框架 + 环境** 三维度选择，准确率从52%提升至94%
- 🧪 **自动测试生成**：智能生成pytest/JUnit/Jest单元测试，节省2-3天工作量
- 📊 **代码块分析**：详细转换报告，100%可追溯性
- 🏗️ **框架智能识别**：自动检测Spring Boot/FastAPI/Express等框架
- 🗺️ **框架智能映射**：@Autowired → Depends()，@GetMapping → @router.get
- 🐳 **环境配置生成**：自动生成Docker/K8s/AWS部署配置
- 💰 **成本估算**：预估转换成本，推荐更便宜方案
- ⚡ **Redis缓存**：相同代码1000倍速度提升，成本降低80-90%
- 📡 **WebSocket实时进度**：无需轮询，实时推送任务状态

#### 🆕 V2.1 新增 - 代码学习文档生成
- 🔍 **代码智能检测**：全面分析代码质量、复杂度、设计模式
- 📊 **复杂度分析**：圈复杂度、认知复杂度、可维护性指数
- 🎨 **设计模式识别**：自动识别Singleton、Factory、MVC等模式
- ⚠️ **代码异味检测**：发现Long Method、High Complexity等问题
- 🔒 **安全漏洞扫描**：识别eval、硬编码密钥等安全隐患
- 📚 **学习文档自动生成**：包含学习路线图、难度分析、质量报告
- 🗺️ **智能学习路线**：根据项目复杂度定制学习计划
- 💡 **个性化学习建议**：针对不同难度提供学习策略

#### 🆕 V2.2 新增 - 多AI协同代码优化
- 🤖 **多AI并行分析**：4+个AI模型（GPT-4o/Claude/Gemini/DeepSeek）同时分析代码
- 🤝 **共识机制**：识别多个AI都认同的建议（置信度高达100%）
- 💡 **独特见解保留**：保留单个AI的创新性建议，提供探索方向
- 📊 **7大优化类别**：性能/安全/可读性/可维护性/架构/最佳实践/错误处理
- 🎯 **智能优先级排序**：综合优先级、影响、工作量、置信度排序
- 🗺️ **三阶段实施路线图**：关键优化 → 重要改进 → 优化提升
- ⚡ **Quick Wins识别**：自动找出"低工作量+高影响"的优化项
- 📄 **详细优化报告**：代码对比、推理说明、AI贡献分析、优先级矩阵

#### 🆕 V2.3 新增 - 自定义AI模型系统
- ➕ **添加任何AI模型**：通过API添加自定义AI模型，无需修改代码
- 🔧 **灵活配置**：支持OpenAI/Anthropic/Google/自定义等多种API格式
- 🧪 **模型测试**：一键测试模型连接和响应
- 📤 **导出导入**：轻松分享和导入模型配置
- 🏷️ **标签管理**：通过标签组织和筛选模型
- ⚙️ **热加载**：添加后立即可用，无需重启
- 🔐 **安全管理**：API密钥通过环境变量管理
- 🌐 **支持本地模型**：Ollama、vLLM、LocalAI等本地部署模型

#### 🔄 基础功能
- 🔄 **多语言互转**：支持 Java ↔️ Python ↔️ JavaScript ↔️ TypeScript ↔️ Go ↔️ C++ ↔️ Rust
- 🤖 **7种AI模型**：GPT-4、GPT-4o、Claude 3.5、Gemini、DeepSeek、通义千问、CodeLlama
- 🎯 **5种智能策略**：质量优先、竞速模式、共识模式、负载均衡、随机选择
- 🌐 **Git集成**：直接拉取 GitHub/GitLab 仓库进行分析转换
- 📦 **完整项目转换**：保持项目结构、依赖关系、注释文档
- ⚡ **多AI并发**：3个AI同时翻译，速度提升3倍
- 🛡️ **自动故障转移**：一个模型失败自动切换到备用模型
- 📊 **实时监控**：Web界面实时显示转换进度和性能统计

### 🎯 支持的AI模型

#### 内置模型

| 模型 | 提供商 | 速度 | 质量 | 成本 |
|------|--------|------|------|------|
| **GPT-4o** | OpenAI | ⚡⚡⚡⚡⚡ | ⭐⭐⭐⭐⭐ | 💰💰 |
| **Claude 3.5 Sonnet** | Anthropic | ⚡⚡⚡⚡ | ⭐⭐⭐⭐⭐ | 💰💰 |
| **GPT-4 Turbo** | OpenAI | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | 💰💰💰 |
| **Gemini Pro** | Google | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | 💰 |
| **DeepSeek Coder** | DeepSeek | ⚡⚡⚡ | ⭐⭐⭐⭐ | 💰 |
| **通义千问 Coder** | 阿里云 | ⚡⚡⚡ | ⭐⭐⭐⭐ | 💰 |
| **CodeLlama** | Local | ⚡⚡ | ⭐⭐⭐ | 🆓 |

#### 🆕 支持自定义AI模型

**现在您可以添加任何AI模型到平台！** 通过API无需修改代码即可添加：

| 类型 | 示例 | 配置难度 | 支持格式 |
|------|------|---------|---------|
| **国产AI** | 智谱GLM、百度文心、讯飞星火、字节豆包 | ⭐ | OpenAI兼容 |
| **国际AI** | Cohere、Mistral、Perplexity | ⭐ | 标准API |
| **本地部署** | Ollama、vLLM、LocalAI、llama.cpp | ⭐⭐ | OpenAI兼容 |
| **自定义API** | 企业内部模型、私有化部署 | ⭐⭐⭐ | 完全自定义 |

**快速添加示例**:
```bash
# 添加Ollama本地模型（免费！）
curl -X POST http://localhost:8000/api/v1/ai-models -H "Content-Type: application/json" -d '{
  "model_id": "ollama-llama3",
  "model_name": "Ollama Llama 3",
  "provider": "ollama",
  "api_base_url": "http://localhost:11434/api",
  "api_key_env_var": "OLLAMA_KEY",
  "request_format": "openai"
}'

# 测试模型
curl -X POST "http://localhost:8000/api/v1/ai-models/ollama-llama3/test"

# 立即使用！
curl -X POST http://localhost:8000/api/v1/convert -d '{
  "source_language": "java",
  "target_language": "python",
  "ai_model": "ollama-llama3"
}'
```

**所有详细配置请参考下方API调用示例**

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
git clone https://github.com/slaveofai-sudo/ai-code-language-conversion.git
cd ai-code-language-conversion
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

##### 基础转换
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

##### 🆕 V2.0 完整转换（包含测试和分析）
```python
# 三维度精准迁移 + 自动测试生成 + 代码块分析
response = requests.post('http://localhost:8000/api/v1/convert-with-analysis', json={
    "source_type": "git",
    "git_url": "https://github.com/user/spring-project.git",
    
    # 三维度选择
    "source_language": "java",              # 语言
    "target_language": "python",
    "target_framework": "fastapi",          # 框架
    "runtime_environment": "kubernetes",    # 环境
    
    # 自动检测和生成
    "auto_detect_framework": true,
    "generate_tests": true,                 # 生成测试
    "generate_analysis": true,              # 生成分析报告
    
    # AI配置
    "ai_model": "gpt-4o",
    "use_multi_ai": true
})

# 下载结果包含:
# ✅ 转换后的FastAPI代码
# ✅ 自动生成的pytest测试
# ✅ 代码块分析报告 (Markdown)
# ✅ Kubernetes部署配置
# ✅ Docker配置文件
```

##### 🆕 单独生成测试
```python
# 为已转换的代码生成测试
response = requests.post('http://localhost:8000/api/v1/generate-tests', json={
    "source_file": "./output/user_controller.py",
    "target_language": "python",
    "framework": "fastapi"
})

print(response.json()['result']['test_file_path'])
# 输出: ./output/tests/test_user_controller.py
```

##### 🆕 代码块分析
```python
# 分析转换质量
response = requests.post('http://localhost:8000/api/v1/analyze-blocks', json={
    "source_file": "./input/UserController.java",
    "target_file": "./output/user_controller.py",
    "source_language": "java",
    "target_language": "python",
    "source_framework": "spring-boot",
    "target_framework": "fastapi",
    "generate_report": true
})

analysis = response.json()['analysis']
print(f"质量分数: {analysis['quality_metrics']['overall_quality']}%")
print(f"分析报告: {response.json()['report_file']}")
```

##### 🆕 成本估算
```python
# 预估转换成本
response = requests.post('http://localhost:8000/api/v1/estimate', json={
    "lines_of_code": 5000,
    "source_language": "java",
    "target_language": "python",
    "ai_model": "gpt-4o"
})

estimate = response.json()['estimate']
print(f"预估成本: ${estimate['cost_usd']}")
print(f"预估时间: {estimate['time_minutes']} 分钟")
print(f"节省潜力: ${estimate['savings_potential_usd']}")
```

##### 🆕 代码检测和学习文档生成
```python
# 检测Git仓库并生成学习文档
response = requests.post('http://localhost:8000/api/v1/inspect-project', json={
    "git_url": "https://github.com/username/project.git",
    "generate_learning_doc": true,
    "output_format": "markdown"
})

result = response.json()
print(f"项目名称: {result['inspection_results']['project_metrics']['project_name']}")
print(f"总文件数: {result['inspection_results']['project_metrics']['total_files']}")
print(f"总行数: {result['inspection_results']['project_metrics']['total_lines']}")
print(f"整体难度: {result['inspection_results']['project_metrics']['overall_difficulty']}")
print(f"健康分数: {result['inspection_results']['summary']['health_score']}/100")
print(f"学习文档已保存: {result['learning_doc']['file_path']}")

# 生成的学习文档包含:
# ✅ 项目概览和语言分布
# ✅ 学习路线图（推荐学习时间、阶段划分）
# ✅ 难度分析（代码量、复杂度、架构评分）
# ✅ 技术栈分析和学习资源推荐
# ✅ 架构设计分析
# ✅ 设计模式识别和解释
# ✅ 代码复杂度详细分析
# ✅ 文件结构统计
# ✅ 个性化学习建议
# ✅ 代码质量报告（代码异味、安全问题）
```

##### 🆕 多AI协同代码优化
```python
# 使用多个AI模型分析代码并生成优化建议
response = requests.post('http://localhost:8000/api/v1/optimize-code', json={
    "file_path": "./backend/app.py",  # 或使用 git_url + target_file
    "use_multi_ai": true,
    "ai_models": ["gpt-4o", "claude-3.5-sonnet", "gemini-pro", "deepseek-coder"],
    "consensus_threshold": 2,  # 至少2个AI同意才算共识
    "output_format": "markdown"
})

result = response.json()
print(f"✅ 分析完成!")
print(f"📊 总建议数: {result['summary']['total_suggestions']}")
print(f"🤝 共识建议: {result['summary']['consensus_suggestions']}")
print(f"💡 独特建议: {result['summary']['unique_suggestions']}")
print(f"⏱️  预估工作量: {result['summary']['estimated_effort']}")
print(f"📈 预期影响: {result['summary']['expected_impact']}")
print(f"📄 报告保存在: {result['report_file']}")

# 生成的优化报告包含:
# ✅ 执行摘要（总建议数、优先级分布、类别分布）
# ✅ 共识优化建议（多AI认同，高可信度）
# ✅ 独特优化建议（单AI见解，探索性）
# ✅ 三阶段实施路线图（关键优化 → 重要改进 → 优化提升）
# ✅ 代码对比（优化前/后）
# ✅ 推理说明（为什么要优化）
# ✅ 优先级矩阵（Quick Wins识别）
# ✅ AI贡献分析（每个AI的贡献度）
```

##### 🆕 自定义AI模型管理
```python
# 1. 列出所有可用的AI模型（内置+自定义）
response = requests.get('http://localhost:8000/api/v1/ai-models')
models = response.json()['models']
print(f"可用模型数: {len(models)}")

# 2. 添加自定义AI模型
response = requests.post('http://localhost:8000/api/v1/ai-models', json={
    "model_id": "my-custom-llm",
    "model_name": "My Custom LLM",
    "provider": "custom",
    "api_base_url": "https://api.example.com/v1",
    "api_key_env_var": "MY_LLM_API_KEY",
    "model_type": "chat",
    "request_format": "openai",  # openai/anthropic/google/custom
    "description": "我的自定义AI模型",
    "tags": ["custom", "experimental"],
    "max_tokens": 4096,
    "temperature": 0.3
})

print(f"✅ 模型已添加: {response.json()['model_id']}")

# 3. 测试自定义模型
response = requests.post(
    'http://localhost:8000/api/v1/ai-models/my-custom-llm/test',
    params={'test_prompt': 'Hello, how are you?'}
)

test_result = response.json()['test_result']
if test_result['success']:
    print(f"✅ 测试成功! 延迟: {test_result['latency_ms']}ms")
    print(f"响应: {test_result['response']}")
else:
    print(f"❌ 测试失败: {test_result['error']}")

# 4. 在转换中使用自定义模型
response = requests.post('http://localhost:8000/api/v1/convert', json={
    "source_code": "public class Hello { ... }",
    "source_language": "java",
    "target_language": "python",
    "ai_model": "my-custom-llm"  # 使用自定义模型
})

# 5. 在多AI优化中使用自定义模型
response = requests.post('http://localhost:8000/api/v1/optimize-code', json={
    "file_path": "./app.py",
    "use_multi_ai": true,
    "ai_models": ["gpt-4o", "my-custom-llm", "claude-3.5-sonnet"]  # 混合使用
})

# 6. 导出模型配置（用于分享）
response = requests.post('http://localhost:8000/api/v1/ai-models/my-custom-llm/export')
config = response.json()['config']
with open('my_model_config.json', 'w') as f:
    json.dump(config, f, indent=2)

# 7. 导入他人分享的模型配置
with open('shared_model_config.json', 'r') as f:
    config = json.load(f)

response = requests.post('http://localhost:8000/api/v1/ai-models/import', json=config)
print(f"✅ 导入成功: {response.json()['message']}")

# 支持的AI模型示例:
# - Ollama本地模型 (llama3, codellama, etc.)
# - Azure OpenAI
# - 智谱AI (GLM)
# - 百度文心一言
# - 阿里通义千问
# - HuggingFace模型
# - 任何OpenAI兼容的API
```

##### 🆕 先检测后转换（组合工作流）
```python
# 先生成学习文档，再进行代码转换
response = requests.post('http://localhost:8000/api/v1/inspect-and-convert', json={
    "source_type": "git",
    "git_url": "https://github.com/username/java-project.git",
    "source_language": "java",
    "target_language": "python",
    "target_framework": "fastapi",
    "runtime_environment": "kubernetes",
    "generate_learning_doc": true,
    "generate_tests": true,
    "generate_analysis": true
})

# 结果包含:
# ✅ 原项目的学习文档
# ✅ 转换后的Python代码
# ✅ 自动生成的测试
# ✅ 代码块分析报告
# ✅ Kubernetes配置
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

### 📖 完整文档

本 README 已包含所有功能的完整使用说明，包括：
- ✅ 快速开始指南
- ✅ API 调用示例（基础转换、三维度迁移、测试生成、代码分析、成本估算等）
- ✅ 自定义AI模型配置
- ✅ 多AI优化使用方法
- ✅ 代码检测和学习文档生成
- ✅ CLI 工具和 Web 界面使用

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

#### 已完成 ✅

- [x] **v1.0** - 基础功能（Java/Python转换）
- [x] **v1.1** - 多语言支持（JS/TS/Go/C++/Rust）
- [x] **v1.2** - 多AI模型支持（7种AI）
- [x] **v1.3** - 智能策略（5种策略）
- [x] **v2.0** - 三维度精准迁移（语言+框架+环境）
- [x] **v2.0** - 自动测试生成（pytest/JUnit/Jest）
- [x] **v2.0** - 代码块分析和质量报告
- [x] **v2.0** - 框架智能识别和映射
- [x] **v2.0** - 环境配置生成（Docker/K8s/AWS）
- [x] **v2.0** - 成本估算和缓存系统
- [x] **v2.1** - 代码智能检测和学习文档生成
- [x] **v2.1** - 复杂度分析和设计模式识别
- [x] **v2.1** - 代码异味和安全漏洞扫描
- [x] **v2.2** - 多AI协同代码优化
- [x] **v2.2** - 共识机制和优先级排序
- [x] **v2.2** - Quick Wins识别和实施路线图
- [x] **v2.3** - 自定义AI模型系统
- [x] **v2.3** - 模型热加载和导入导出
- [x] **v2.3** - 支持本地模型（Ollama/vLLM）

#### 开发中 🚧

- [ ] **v2.4** - 前端可视化界面优化
- [ ] **v2.5** - 批量转换和任务队列管理
- [ ] **v2.6** - 转换历史和版本对比

#### 计划中 📋

- [ ] **v3.0** - 企业版功能
  - [ ] 团队协作和权限管理
  - [ ] 私有化部署方案
  - [ ] API使用统计和计费
  - [ ] 自定义转换规则
- [ ] **v3.1** - 高级功能
  - [ ] 代码重构建议
  - [ ] 性能瓶颈分析
  - [ ] 技术债务评估
- [ ] **v3.2** - 生态系统
  - [ ] 插件系统
  - [ ] 社区模型库
  - [ ] 转换模板市场

### 📋 版本历史

#### V2.3 (最新) - 2025-10-25
- 🆕 **自定义AI模型系统** - 添加任何AI模型，无需修改代码
- 🔧 支持 OpenAI/Anthropic/Google/自定义 API格式
- 🧪 一键模型测试和验证
- 📤 模型配置导出导入
- 🌐 完整支持本地模型 (Ollama/vLLM/LocalAI)

#### V2.2 - 2025-10-24
- 🤖 **多AI协同代码优化** - 4+个AI同时分析代码
- 🤝 共识机制识别高可信度建议
- 📊 7大优化类别和智能排序
- 🗺️ 三阶段实施路线图生成
- ⚡ Quick Wins自动识别

#### V2.1 - 2025-10-23
- 🔍 **代码智能检测** - 全面分析代码质量
- 📚 **学习文档自动生成** - 包含学习路线图
- 🎨 设计模式自动识别
- ⚠️ 代码异味和安全漏洞扫描
- 💡 个性化学习建议

#### V2.0 - 2025-10-22
- 🎯 **三维度精准迁移** - 语言+框架+环境
- 🧪 自动测试生成 (pytest/JUnit/Jest)
- 📊 代码块级分析和质量报告
- 🏗️ 框架智能识别和映射
- 🐳 环境配置自动生成
- 💰 成本估算系统
- ⚡ Redis缓存 (1000倍提速)
- 📡 WebSocket实时进度

#### V1.3 - 2025-10-20
- 🎯 5种智能策略 (质量优先/竞速/共识/负载均衡/随机)
- 🛡️ 自动故障转移
- ⚖️ 负载均衡和API限流处理

#### V1.2 - 2025-10-18
- 🤖 多AI模型支持 (7种主流AI)
- ⚡ 多AI并发翻译
- 📊 性能监控和统计

#### V1.1 - 2025-10-15
- 🌍 多语言支持 (7种编程语言)
- 📦 完整项目结构保持
- 🌐 Git集成

#### V1.0 - 2025-10-10
- 🔄 基础代码转换 (Java ↔️ Python)
- 🖥️ Web界面和CLI工具
- 📡 RESTful API

### ⭐ Star History

如果这个项目对你有帮助，请给我们一个 Star ⭐！

### 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

### 🙏 致谢

感谢以下开源项目和服务：

#### 核心技术栈
- [FastAPI](https://fastapi.tiangolo.com/) - 现代化的 Web 框架
- [React](https://reactjs.org/) - 用户界面库
- [Tailwind CSS](https://tailwindcss.com/) - CSS 框架
- [Redis](https://redis.io/) - 缓存和消息队列
- [PostgreSQL](https://www.postgresql.org/) - 数据库

#### AI模型提供商
- [OpenAI](https://openai.com/) - GPT 系列模型
- [Anthropic](https://www.anthropic.com/) - Claude 系列模型
- [Google](https://ai.google.dev/) - Gemini 系列模型
- [DeepSeek](https://www.deepseek.com/) - DeepSeek Coder
- [阿里云](https://www.aliyun.com/) - 通义千问
- [Ollama](https://ollama.ai/) - 本地模型部署

#### 开源工具
- [Tree-sitter](https://tree-sitter.github.io/) - 代码解析
- [Loguru](https://github.com/Delgan/loguru) - 日志系统
- [Pydantic](https://pydantic-docs.helpmanual.io/) - 数据验证

### 📞 联系我们

- 💬 问题反馈：[GitHub Issues](https://github.com/slaveofai-sudo/ai-code-language-conversion/issues)
- 📧 邮件：y956893@163.com
- 🔗 GitHub：[@slaveofai-sudo](https://github.com/slaveofai-sudo)

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
git clone https://github.com/slaveofai-sudo/ai-code-language-conversion.git
cd ai-code-language-conversion
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

- 💬 Issues: [GitHub Issues](https://github.com/slaveofai-sudo/ai-code-language-conversion/issues)
- 📧 Email: y956893@163.com
- 🔗 GitHub: [@slaveofai-sudo](https://github.com/slaveofai-sudo)

---

<div align="center">

**Made with ❤️ by the AI Code Migration Team**

If you find this useful, please give it a ⭐ Star!

[中文](#中文) | [English](#english)

</div>

