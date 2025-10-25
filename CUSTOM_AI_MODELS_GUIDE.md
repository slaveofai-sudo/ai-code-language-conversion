# 🤖 自定义AI模型完全指南

## 📖 目录

- [功能概述](#功能概述)
- [快速开始](#快速开始)
- [API接口说明](#api接口说明)
- [支持的请求格式](#支持的请求格式)
- [添加示例](#添加示例)
- [测试模型](#测试模型)
- [导入导出](#导入导出)
- [最佳实践](#最佳实践)
- [常见问题](#常见问题)

---

## 🎯 功能概述

**自定义AI模型系统**允许您添加任何AI模型到平台中，无需修改代码！

### ✨ 核心功能

| 功能 | 说明 |
|------|------|
| 🆕 **添加自定义模型** | 通过API添加任何AI模型 |
| 🔄 **更新模型配置** | 随时修改模型参数 |
| 🗑️ **删除模型** | 移除不需要的自定义模型 |
| 🧪 **测试模型** | 验证模型连接和响应 |
| 📤 **导出配置** | 分享模型配置给他人 |
| 📥 **导入配置** | 导入他人分享的配置 |
| 📋 **列出所有模型** | 查看内置和自定义模型 |

### 🌟 特色

- ✅ **零代码配置**: 无需修改源代码
- ✅ **热加载**: 添加后立即可用
- ✅ **持久化**: 配置自动保存
- ✅ **灵活性**: 支持多种API格式
- ✅ **安全性**: API密钥通过环境变量管理
- ✅ **可共享**: 轻松导出导入配置

---

## 🚀 快速开始

### 1. 列出现有模型

```bash
curl http://localhost:8000/api/v1/ai-models
```

响应示例:
```json
{
  "status": "success",
  "total": 4,
  "models": [
    {
      "model_id": "gpt-4o",
      "model_name": "GPT-4o",
      "provider": "openai",
      "model_type": "chat",
      "description": "OpenAI's GPT-4o model",
      "tags": ["openai", "gpt", "chat"],
      "enabled": true,
      "is_builtin": true
    },
    ...
  ]
}
```

### 2. 添加自定义模型

```bash
curl -X POST http://localhost:8000/api/v1/ai-models \
  -H "Content-Type: application/json" \
  -d '{
    "model_id": "my-custom-model",
    "model_name": "My Custom AI",
    "provider": "custom",
    "api_base_url": "https://api.example.com/v1",
    "api_key_env_var": "MY_CUSTOM_API_KEY",
    "model_type": "chat",
    "request_format": "openai",
    "description": "My custom AI model",
    "tags": ["custom", "experimental"]
  }'
```

### 3. 设置API密钥

```bash
# Linux/Mac
export MY_CUSTOM_API_KEY="your-api-key-here"

# Windows PowerShell
$env:MY_CUSTOM_API_KEY="your-api-key-here"

# 或添加到 .env 文件
echo "MY_CUSTOM_API_KEY=your-api-key-here" >> .env
```

### 4. 测试模型

```bash
curl -X POST "http://localhost:8000/api/v1/ai-models/my-custom-model/test?test_prompt=Hello"
```

响应示例:
```json
{
  "status": "success",
  "test_result": {
    "model_id": "my-custom-model",
    "success": true,
    "response": "Hello! How can I help you today?",
    "error": null,
    "latency_ms": 234.56
  }
}
```

### 5. 使用自定义模型

```bash
# 在代码转换中使用
curl -X POST http://localhost:8000/api/v1/convert \
  -d '{
    "source_code": "...",
    "source_language": "java",
    "target_language": "python",
    "ai_model": "my-custom-model"
  }'

# 在代码优化中使用
curl -X POST http://localhost:8000/api/v1/optimize-code \
  -d '{
    "file_path": "./app.py",
    "use_multi_ai": true,
    "ai_models": ["gpt-4o", "my-custom-model", "claude-3.5-sonnet"]
  }'
```

---

## 📡 API接口说明

### GET /api/v1/ai-models

**列出所有可用的AI模型**

**查询参数**:
- `include_builtin` (boolean, default: true) - 包含内置模型
- `include_custom` (boolean, default: true) - 包含自定义模型
- `enabled_only` (boolean, default: false) - 只返回启用的模型

**示例**:
```bash
# 只列出自定义模型
curl "http://localhost:8000/api/v1/ai-models?include_builtin=false"

# 只列出启用的模型
curl "http://localhost:8000/api/v1/ai-models?enabled_only=true"
```

### GET /api/v1/ai-models/{model_id}

**获取特定模型的详细信息**

**示例**:
```bash
curl http://localhost:8000/api/v1/ai-models/gpt-4o
```

### POST /api/v1/ai-models

**添加新的自定义AI模型**

**必需参数**:
- `model_id` (string) - 唯一标识符
- `model_name` (string) - 显示名称
- `provider` (string) - 提供商名称
- `api_base_url` (string) - API基础URL
- `api_key_env_var` (string) - API密钥环境变量名
- `model_type` (string) - 模型类型 (chat/completion/custom)

**可选参数**:
- `max_tokens` (int, default: 4096) - 最大token数
- `temperature` (float, default: 0.3) - 温度参数
- `top_p` (float, default: 1.0) - Top P参数
- `custom_headers` (object) - 自定义HTTP请求头
- `request_format` (string, default: "openai") - 请求格式
- `request_template` (object) - 自定义请求模板
- `response_path` (string) - 响应提取路径
- `description` (string) - 模型描述
- `tags` (array) - 标签
- `enabled` (boolean, default: true) - 是否启用

### PUT /api/v1/ai-models/{model_id}

**更新自定义AI模型配置**

所有参数都是可选的，只更新提供的字段。

**示例**:
```bash
curl -X PUT http://localhost:8000/api/v1/ai-models/my-custom-model \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": 0.5,
    "description": "Updated description",
    "enabled": true
  }'
```

### DELETE /api/v1/ai-models/{model_id}

**删除自定义AI模型**

注意: 不能删除内置模型。

**示例**:
```bash
curl -X DELETE http://localhost:8000/api/v1/ai-models/my-custom-model
```

### POST /api/v1/ai-models/{model_id}/test

**测试AI模型连接和响应**

**查询参数**:
- `test_prompt` (string, default: "Hello, how are you?") - 测试提示词

**示例**:
```bash
curl -X POST "http://localhost:8000/api/v1/ai-models/my-custom-model/test?test_prompt=Tell%20me%20a%20joke"
```

### POST /api/v1/ai-models/{model_id}/export

**导出AI模型配置用于分享**

**示例**:
```bash
curl -X POST http://localhost:8000/api/v1/ai-models/my-custom-model/export
```

### POST /api/v1/ai-models/import

**导入AI模型配置**

**示例**:
```bash
curl -X POST http://localhost:8000/api/v1/ai-models/import \
  -H "Content-Type: application/json" \
  -d @exported_model.json
```

---

## 🔧 支持的请求格式

### 1. OpenAI格式 (request_format: "openai")

最常见的格式，兼容OpenAI API。

**支持的模型**:
- OpenAI GPT系列
- DeepSeek
- 通义千问
- 许多OpenAI兼容的API

**示例配置**:
```json
{
  "model_id": "my-openai-compatible-model",
  "model_name": "My OpenAI Compatible Model",
  "provider": "custom",
  "api_base_url": "https://api.example.com/v1",
  "api_key_env_var": "MY_API_KEY",
  "model_type": "chat",
  "request_format": "openai"
}
```

### 2. Anthropic格式 (request_format: "anthropic")

用于Claude系列模型。

**示例配置**:
```json
{
  "model_id": "claude-custom",
  "model_name": "Custom Claude",
  "provider": "anthropic",
  "api_base_url": "https://api.anthropic.com/v1",
  "api_key_env_var": "ANTHROPIC_API_KEY",
  "model_type": "chat",
  "request_format": "anthropic"
}
```

### 3. Google格式 (request_format: "google")

用于Gemini系列模型。

**示例配置**:
```json
{
  "model_id": "gemini-custom",
  "model_name": "Custom Gemini",
  "provider": "google",
  "api_base_url": "https://generativelanguage.googleapis.com/v1",
  "api_key_env_var": "GOOGLE_API_KEY",
  "model_type": "chat",
  "request_format": "google"
}
```

### 4. 自定义格式 (request_format: "custom")

用于完全自定义的API格式。

**需要提供**:
- `request_template`: 请求模板
- `response_path`: 响应提取路径

**示例配置**:
```json
{
  "model_id": "fully-custom-model",
  "model_name": "Fully Custom Model",
  "provider": "custom",
  "api_base_url": "https://api.custom.com/generate",
  "api_key_env_var": "CUSTOM_API_KEY",
  "model_type": "custom",
  "request_format": "custom",
  "request_template": {
    "input": {
      "text": "{{prompt}}",
      "model_name": "{{model}}"
    },
    "parameters": {
      "max_length": 1000
    }
  },
  "response_path": "output.generated_text"
}
```

---

## 📝 添加示例

### 示例1: 添加Ollama本地模型

```bash
curl -X POST http://localhost:8000/api/v1/ai-models \
  -H "Content-Type: application/json" \
  -d '{
    "model_id": "ollama-llama3",
    "model_name": "Ollama Llama 3",
    "provider": "ollama",
    "api_base_url": "http://localhost:11434/api",
    "api_key_env_var": "OLLAMA_API_KEY",
    "model_type": "chat",
    "request_format": "openai",
    "description": "本地Ollama运行的Llama 3模型",
    "tags": ["local", "ollama", "llama"],
    "max_tokens": 2048
  }'

# Ollama通常不需要API密钥，设置一个虚拟值即可
export OLLAMA_API_KEY="not-needed"
```

### 示例2: 添加Azure OpenAI

```bash
curl -X POST http://localhost:8000/api/v1/ai-models \
  -H "Content-Type: application/json" \
  -d '{
    "model_id": "azure-gpt-4",
    "model_name": "Azure GPT-4",
    "provider": "azure",
    "api_base_url": "https://your-resource.openai.azure.com",
    "api_key_env_var": "AZURE_OPENAI_KEY",
    "model_type": "chat",
    "request_format": "openai",
    "custom_headers": {
      "api-key": "${AZURE_OPENAI_KEY}"
    },
    "description": "Azure OpenAI GPT-4",
    "tags": ["azure", "gpt", "enterprise"]
  }'
```

### 示例3: 添加智谱AI (GLM)

```bash
curl -X POST http://localhost:8000/api/v1/ai-models \
  -H "Content-Type: application/json" \
  -d '{
    "model_id": "zhipu-glm-4",
    "model_name": "智谱 GLM-4",
    "provider": "zhipu",
    "api_base_url": "https://open.bigmodel.cn/api/paas/v4",
    "api_key_env_var": "ZHIPU_API_KEY",
    "model_type": "chat",
    "request_format": "openai",
    "description": "智谱AI GLM-4模型",
    "tags": ["zhipu", "glm", "chinese"],
    "max_tokens": 4096
  }'
```

### 示例4: 添加百度文心一言

```bash
curl -X POST http://localhost:8000/api/v1/ai-models \
  -H "Content-Type: application/json" \
  -d '{
    "model_id": "ernie-bot-4",
    "model_name": "文心一言 4.0",
    "provider": "baidu",
    "api_base_url": "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat",
    "api_key_env_var": "BAIDU_API_KEY",
    "model_type": "chat",
    "request_format": "custom",
    "request_template": {
      "messages": [
        {"role": "user", "content": "{{prompt}}"}
      ]
    },
    "response_path": "result",
    "description": "百度文心一言4.0",
    "tags": ["baidu", "ernie", "chinese"]
  }'
```

### 示例5: 添加Hugging Face模型

```bash
curl -X POST http://localhost:8000/api/v1/ai-models \
  -H "Content-Type: application/json" \
  -d '{
    "model_id": "hf-codegen",
    "model_name": "HuggingFace CodeGen",
    "provider": "huggingface",
    "api_base_url": "https://api-inference.huggingface.co/models/Salesforce/codegen-16B-mono",
    "api_key_env_var": "HF_API_KEY",
    "model_type": "completion",
    "request_format": "custom",
    "request_template": {
      "inputs": "{{prompt}}",
      "parameters": {
        "max_new_tokens": 1000,
        "temperature": 0.7
      }
    },
    "response_path": "0.generated_text",
    "description": "HuggingFace CodeGen模型",
    "tags": ["huggingface", "codegen"]
  }'
```

---

## 🧪 测试模型

### 基本测试

```bash
curl -X POST "http://localhost:8000/api/v1/ai-models/my-model/test"
```

### 自定义提示词测试

```bash
curl -X POST "http://localhost:8000/api/v1/ai-models/my-model/test?test_prompt=Write%20a%20Python%20function%20to%20sort%20a%20list"
```

### Python测试脚本

```python
import requests

def test_model(model_id, test_prompts):
    """测试AI模型"""
    results = []
    
    for prompt in test_prompts:
        response = requests.post(
            f'http://localhost:8000/api/v1/ai-models/{model_id}/test',
            params={'test_prompt': prompt}
        )
        
        result = response.json()
        results.append({
            'prompt': prompt,
            'success': result['test_result']['success'],
            'latency_ms': result['test_result'].get('latency_ms', 0),
            'error': result['test_result'].get('error')
        })
    
    return results

# 使用
test_prompts = [
    "Hello, how are you?",
    "Write a Python function to calculate factorial",
    "Explain machine learning in simple terms"
]

results = test_model('my-custom-model', test_prompts)

for r in results:
    if r['success']:
        print(f"✅ {r['prompt'][:50]}... ({r['latency_ms']}ms)")
    else:
        print(f"❌ {r['prompt'][:50]}... Error: {r['error']}")
```

---

## 📤📥 导入导出

### 导出模型配置

```bash
curl -X POST http://localhost:8000/api/v1/ai-models/my-model/export > my_model.json
```

### 导入模型配置

```bash
# 1. 编辑导出的JSON文件，设置您自己的api_key_env_var
vi my_model.json

# 2. 导入
curl -X POST http://localhost:8000/api/v1/ai-models/import \
  -H "Content-Type: application/json" \
  -d @my_model.json
```

### 批量导入

```python
import requests
import json

def import_models_from_file(file_path):
    """从文件批量导入模型"""
    with open(file_path, 'r') as f:
        models = json.load(f)
    
    for model_config in models:
        response = requests.post(
            'http://localhost:8000/api/v1/ai-models/import',
            json=model_config
        )
        
        if response.status_code == 200:
            print(f"✅ 导入成功: {model_config['model_name']}")
        else:
            print(f"❌ 导入失败: {model_config['model_name']} - {response.text}")

# 使用
import_models_from_file('models_collection.json')
```

---

## 💡 最佳实践

### 1. API密钥管理

**推荐方式**:
```bash
# 使用 .env 文件
echo "MY_MODEL_API_KEY=xxx" >> .env

# 或使用环境变量
export MY_MODEL_API_KEY="xxx"
```

**不推荐**:
- ❌ 硬编码在代码中
- ❌ 直接在配置中暴露

### 2. 模型命名

**推荐**:
```json
{
  "model_id": "provider-model-version",
  "model_name": "Provider Model Version"
}
```

**示例**:
- `openai-gpt-4o` → "OpenAI GPT-4o"
- `anthropic-claude-3.5` → "Anthropic Claude 3.5"
- `local-llama-3-8b` → "Local Llama 3 8B"

### 3. 使用标签

```json
{
  "tags": [
    "provider-name",
    "model-type",
    "capability",
    "language"
  ]
}
```

**示例**:
```json
{
  "tags": ["openai", "gpt", "chat", "general"]
}
```

### 4. 测试流程

```
1. 添加模型
   ↓
2. 测试基本响应 (Hello test)
   ↓
3. 测试代码生成 (简单任务)
   ↓
4. 测试实际使用场景
   ↓
5. 性能监控
```

### 5. 错误处理

```python
def add_model_safely(config):
    """安全添加模型"""
    try:
        # 1. 验证必需字段
        required_fields = ['model_id', 'model_name', 'api_base_url', 'api_key_env_var']
        for field in required_fields:
            if not config.get(field):
                print(f"❌ 缺少必需字段: {field}")
                return False
        
        # 2. 验证API密钥存在
        import os
        if not os.getenv(config['api_key_env_var']):
            print(f"⚠️  警告: 环境变量 {config['api_key_env_var']} 未设置")
        
        # 3. 添加模型
        response = requests.post(
            'http://localhost:8000/api/v1/ai-models',
            json=config
        )
        
        if response.status_code == 200:
            print(f"✅ 模型添加成功: {config['model_name']}")
            
            # 4. 测试模型
            test_response = requests.post(
                f'http://localhost:8000/api/v1/ai-models/{config["model_id"]}/test'
            )
            
            if test_response.json()['test_result']['success']:
                print(f"✅ 模型测试成功")
            else:
                print(f"⚠️  模型测试失败: {test_response.json()['test_result']['error']}")
            
            return True
        else:
            print(f"❌ 添加失败: {response.text}")
            return False
    
    except Exception as e:
        print(f"❌ 异常: {e}")
        return False
```

---

## ❓ 常见问题

### Q1: 如何知道我的API使用的是什么格式？

A: 大多数现代AI API遵循以下格式之一：

1. **OpenAI格式** (最常见):
   - 如果API文档提到 "chat/completions" 端点
   - 请求格式: `{"model": "...", "messages": [...]}`

2. **Anthropic格式**:
   - Claude模型专用
   - 使用 `x-api-key` 头部

3. **Google格式**:
   - Gemini模型
   - API密钥在URL参数中

4. **自定义格式**:
   - 如果以上都不匹配，使用 `custom` 格式并提供模板

### Q2: API密钥如何安全存储？

A: 系统不存储API密钥本身，只存储环境变量名。实际密钥应该:
- 设置为环境变量
- 或添加到 `.env` 文件 (不要提交到Git)
- 使用密钥管理服务 (生产环境)

### Q3: 可以添加多少个自定义模型？

A: 没有硬性限制，但建议:
- 日常使用: 5-10个模型
- 测试环境: 20+个模型
- 根据实际需求添加

### Q4: 内置模型可以修改吗？

A: 不可以。内置模型是只读的，但您可以:
- 基于内置模型创建自定义版本
- 导出内置模型配置后修改并导入为新模型

### Q5: 模型添加后多久生效？

A: 立即生效！系统使用热加载，无需重启。

### Q6: 如何处理API速率限制？

A: 建议:
1. 在模型配置中添加适当的`max_tokens`
2. 调整`temperature`以控制输出长度
3. 使用多个API密钥并添加为不同的模型实例
4. 利用多AI策略中的"负载均衡"模式

### Q7: 测试失败怎么办？

A: 检查清单:
- ✅ API密钥是否正确设置？
- ✅ `api_base_url` 是否正确？
- ✅ `request_format` 是否匹配？
- ✅ 网络连接是否正常？
- ✅ 查看错误信息中的具体原因

### Q8: 可以使用本地模型吗？

A: 可以！支持:
- Ollama (推荐)
- vLLM
- LocalAI
- 其他支持OpenAI兼容API的本地服务

示例见上方"添加Ollama本地模型"。

---

## 🎉 开始使用

现在您已经了解了如何添加自定义AI模型！

**下一步**:
1. 列出现有模型: `GET /api/v1/ai-models`
2. 添加您的第一个自定义模型
3. 测试模型: `POST /api/v1/ai-models/{model_id}/test`
4. 在实际任务中使用

**需要帮助？**
- 查看API文档: http://localhost:8000/docs
- 查看示例: 本文档的"添加示例"部分
- 提issue: GitHub Issues

---

*📅 创建日期: 2025-10-25*  
*🤖 AI Code Migration Platform Team*

