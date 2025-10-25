# 🎉 V2.3 新功能：自定义AI模型系统

## 📖 概述

现在您可以**添加任何AI模型**到平台中，无需修改代码！系统支持完全自定义的AI模型配置，让您可以使用任何LLM服务。

---

## ✨ 核心功能

### 1. 零代码添加模型 ➕

通过简单的API调用即可添加新的AI模型：

```bash
curl -X POST http://localhost:8000/api/v1/ai-models \
  -H "Content-Type: application/json" \
  -d '{
    "model_id": "my-llm",
    "model_name": "My LLM",
    "provider": "custom",
    "api_base_url": "https://api.example.com/v1",
    "api_key_env_var": "MY_API_KEY",
    "request_format": "openai"
  }'
```

### 2. 支持多种API格式 🔧

- ✅ **OpenAI格式** - GPT、DeepSeek、通义千问等
- ✅ **Anthropic格式** - Claude系列
- ✅ **Google格式** - Gemini系列
- ✅ **完全自定义格式** - 任何其他API

### 3. 一键测试 🧪

```bash
curl -X POST "http://localhost:8000/api/v1/ai-models/my-llm/test"
```

返回：
```json
{
  "success": true,
  "response": "Hello! How can I help?",
  "latency_ms": 234.56
}
```

### 4. 配置分享 📤📥

**导出**：
```bash
curl -X POST http://localhost:8000/api/v1/ai-models/my-llm/export > config.json
```

**导入**：
```bash
curl -X POST http://localhost:8000/api/v1/ai-models/import -d @config.json
```

---

## 🌍 支持的AI模型

### 国内AI

| 模型 | 提供商 | 配置难度 |
|------|--------|---------|
| 智谱AI GLM-4 | 智谱AI | ⭐ |
| 百度文心一言 | 百度 | ⭐⭐ |
| 阿里通义千问 | 阿里云 | ⭐ |
| 字节豆包 | 字节跳动 | ⭐ |
| 讯飞星火 | 科大讯飞 | ⭐⭐ |

### 国际AI

| 模型 | 提供商 | 配置难度 |
|------|--------|---------|
| GPT-4/4o | OpenAI | ⭐ |
| Claude 3.5 | Anthropic | ⭐ |
| Gemini Pro | Google | ⭐ |
| Command R+ | Cohere | ⭐ |
| Mixtral | Mistral AI | ⭐ |

### 本地部署

| 工具 | 说明 | 配置难度 |
|------|------|---------|
| Ollama | 最简单的本地部署 | ⭐ |
| vLLM | 高性能推理 | ⭐⭐⭐ |
| LocalAI | OpenAI兼容 | ⭐⭐ |
| llama.cpp | 轻量级 | ⭐⭐ |

---

## 🚀 快速开始

### 示例1: 添加Ollama本地模型

```bash
# 1. 启动Ollama (假设已安装)
ollama serve

# 2. 添加模型到平台
curl -X POST http://localhost:8000/api/v1/ai-models \
  -H "Content-Type: application/json" \
  -d '{
    "model_id": "ollama-llama3",
    "model_name": "Ollama Llama 3",
    "provider": "ollama",
    "api_base_url": "http://localhost:11434/api",
    "api_key_env_var": "OLLAMA_KEY",
    "request_format": "openai",
    "description": "本地Llama 3模型"
  }'

# 3. 测试
curl -X POST "http://localhost:8000/api/v1/ai-models/ollama-llama3/test"

# 4. 使用
curl -X POST http://localhost:8000/api/v1/convert \
  -d '{
    "source_language": "java",
    "target_language": "python",
    "ai_model": "ollama-llama3"
  }'
```

### 示例2: 添加智谱AI

```bash
# 1. 添加模型
curl -X POST http://localhost:8000/api/v1/ai-models \
  -H "Content-Type: application/json" \
  -d '{
    "model_id": "zhipu-glm-4",
    "model_name": "智谱GLM-4",
    "provider": "zhipu",
    "api_base_url": "https://open.bigmodel.cn/api/paas/v4",
    "api_key_env_var": "ZHIPU_API_KEY",
    "request_format": "openai",
    "description": "智谱AI GLM-4"
  }'

# 2. 设置API密钥
export ZHIPU_API_KEY="your-api-key"

# 3. 测试
curl -X POST "http://localhost:8000/api/v1/ai-models/zhipu-glm-4/test"
```

### 示例3: 多AI协同（混合使用）

```bash
curl -X POST http://localhost:8000/api/v1/optimize-code \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "./app.py",
    "use_multi_ai": true,
    "ai_models": [
      "gpt-4o",              # OpenAI官方
      "ollama-llama3",        # 本地模型
      "zhipu-glm-4",          # 国产模型
      "claude-3.5-sonnet"     # Anthropic
    ],
    "consensus_threshold": 2
  }'
```

---

## 📊 完整API列表

| 端点 | 方法 | 功能 |
|------|------|------|
| `/api/v1/ai-models` | GET | 列出所有模型 |
| `/api/v1/ai-models` | POST | 添加新模型 |
| `/api/v1/ai-models/{id}` | GET | 获取模型详情 |
| `/api/v1/ai-models/{id}` | PUT | 更新模型配置 |
| `/api/v1/ai-models/{id}` | DELETE | 删除模型 |
| `/api/v1/ai-models/{id}/test` | POST | 测试模型 |
| `/api/v1/ai-models/{id}/export` | POST | 导出配置 |
| `/api/v1/ai-models/import` | POST | 导入配置 |

---

## 🎯 使用场景

### 场景1: 成本优化 💰

```python
# 使用便宜的本地模型处理简单任务
simple_tasks_model = "ollama-llama3"

# 使用强大的云端模型处理复杂任务
complex_tasks_model = "gpt-4o"

# 根据任务难度动态选择
if task_complexity < 5:
    model = simple_tasks_model
else:
    model = complex_tasks_model
```

### 场景2: 数据隐私 🔒

```python
# 敏感代码使用本地模型
if is_sensitive_code:
    model = "ollama-llama3"  # 不离开本地
else:
    model = "gpt-4o"  # 云端处理
```

### 场景3: 多区域部署 🌍

```python
# 国内用户使用国产模型（更快）
if user_region == "CN":
    models = ["zhipu-glm-4", "qwen-coder"]
else:
    models = ["gpt-4o", "claude-3.5-sonnet"]
```

### 场景4: A/B测试 🧪

```python
# 测试不同模型的效果
models_to_test = [
    "gpt-4o",
    "claude-3.5-sonnet",
    "my-fine-tuned-model"
]

for model in models_to_test:
    result = convert_code(model=model)
    evaluate_quality(result)
```

---

## 💡 高级功能

### 自定义请求格式

对于非标准API，可以使用自定义模板：

```json
{
  "model_id": "custom-api",
  "request_format": "custom",
  "request_template": {
    "input": {
      "text": "{{prompt}}",
      "config": {
        "model": "{{model}}",
        "max_length": 1000
      }
    }
  },
  "response_path": "output.result.text"
}
```

### 自定义请求头

```json
{
  "model_id": "enterprise-llm",
  "custom_headers": {
    "X-API-Version": "v2",
    "X-Tenant-ID": "my-company"
  }
}
```

---

## ⚙️ 配置持久化

所有自定义模型配置自动保存在：
```
data/ai_models.json
```

系统启动时自动加载，无需手动配置！

---

## 📚 完整文档

详细文档请查看：
- **`CUSTOM_AI_MODELS_GUIDE.md`** - 完整使用指南 (8000+字)
- **API文档** - http://localhost:8000/docs
- **README.md** - 快速开始

---

## 🎁 内置模型配置

系统内置以下模型配置（可直接使用）：

1. ✅ **GPT-4o** (OpenAI)
2. ✅ **Claude 3.5 Sonnet** (Anthropic)
3. ✅ **Gemini Pro** (Google)
4. ✅ **DeepSeek Coder** (DeepSeek)

只需设置相应的API密钥即可使用！

---

## 🆚 对比

### 之前 ❌

```python
# 要添加新模型，需要：
1. 修改源代码
2. 添加新的translator类
3. 重新部署
4. 只能使用预定义的几个模型
```

### 现在 ✅

```bash
# 添加新模型，只需：
curl -X POST /api/v1/ai-models -d '{...}'

# 1秒钟完成，立即可用！
```

---

## 🎉 开始使用

```bash
# 1. 查看现有模型
curl http://localhost:8000/api/v1/ai-models

# 2. 添加您的第一个自定义模型
curl -X POST http://localhost:8000/api/v1/ai-models \
  -H "Content-Type: application/json" \
  -d @my_model_config.json

# 3. 测试模型
curl -X POST "http://localhost:8000/api/v1/ai-models/my-model/test"

# 4. 开始使用
curl -X POST http://localhost:8000/api/v1/convert \
  -d '{"ai_model": "my-model", ...}'
```

---

**🚀 现在您可以使用任何AI模型了！无限可能！**

---

*📅 创建日期: 2025-10-25*  
*✨ 功能状态: ✅ 完整实现并可用*  
*📖 详细文档: CUSTOM_AI_MODELS_GUIDE.md*

