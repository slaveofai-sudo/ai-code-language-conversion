"""
AI Model Manager / AI模型管理器

Allows users to dynamically add, remove, and manage custom AI models.
允许用户动态添加、删除和管理自定义AI模型。

Features / 功能:
- Add custom AI models / 添加自定义AI模型
- Configure model parameters / 配置模型参数
- Test model connectivity / 测试模型连接
- Model validation / 模型验证
- Persistence / 持久化存储
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from loguru import logger
import requests
from datetime import datetime


@dataclass
class AIModelConfig:
    """
    AI Model Configuration / AI模型配置
    """
    model_id: str  # Unique identifier / 唯一标识符
    model_name: str  # Display name / 显示名称
    provider: str  # e.g., "openai", "anthropic", "custom" / 提供商
    api_base_url: str  # API base URL / API基础URL
    api_key_env_var: str  # Environment variable name for API key / API密钥的环境变量名
    model_type: str  # "chat", "completion", "custom" / 模型类型
    
    # Model parameters / 模型参数
    max_tokens: int = 4096
    temperature: float = 0.3
    top_p: float = 1.0
    
    # Custom headers / 自定义请求头
    custom_headers: Dict[str, str] = None
    
    # Request format / 请求格式
    request_format: str = "openai"  # "openai", "anthropic", "custom"
    
    # Custom request/response mapping / 自定义请求响应映射
    request_template: Optional[Dict[str, Any]] = None
    response_path: Optional[str] = None  # JSONPath to extract response
    
    # Metadata / 元数据
    description: str = ""
    tags: List[str] = None
    enabled: bool = True
    created_at: str = ""
    updated_at: str = ""
    
    def __post_init__(self):
        if self.custom_headers is None:
            self.custom_headers = {}
        if self.tags is None:
            self.tags = []
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.updated_at:
            self.updated_at = datetime.now().isoformat()


class AIModelManager:
    """
    AI Model Manager / AI模型管理器
    
    Manages custom AI models added by users.
    管理用户添加的自定义AI模型。
    """
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize AI Model Manager.
        初始化AI模型管理器。
        
        Args:
            config_file: Path to configuration file.
                        配置文件路径。
        """
        if config_file:
            self.config_file = Path(config_file)
        else:
            self.config_file = Path("./data/ai_models.json")
        
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Built-in models / 内置模型
        self.builtin_models = {
            "gpt-4o": AIModelConfig(
                model_id="gpt-4o",
                model_name="GPT-4o",
                provider="openai",
                api_base_url="https://api.openai.com/v1",
                api_key_env_var="OPENAI_API_KEY",
                model_type="chat",
                request_format="openai",
                description="OpenAI's GPT-4o model",
                tags=["openai", "gpt", "chat"]
            ),
            "claude-3.5-sonnet": AIModelConfig(
                model_id="claude-3.5-sonnet",
                model_name="Claude 3.5 Sonnet",
                provider="anthropic",
                api_base_url="https://api.anthropic.com/v1",
                api_key_env_var="ANTHROPIC_API_KEY",
                model_type="chat",
                request_format="anthropic",
                description="Anthropic's Claude 3.5 Sonnet",
                tags=["anthropic", "claude", "chat"]
            ),
            "gemini-pro": AIModelConfig(
                model_id="gemini-pro",
                model_name="Gemini Pro",
                provider="google",
                api_base_url="https://generativelanguage.googleapis.com/v1",
                api_key_env_var="GOOGLE_API_KEY",
                model_type="chat",
                request_format="google",
                description="Google's Gemini Pro model",
                tags=["google", "gemini", "chat"]
            ),
            "deepseek-coder": AIModelConfig(
                model_id="deepseek-coder",
                model_name="DeepSeek Coder",
                provider="deepseek",
                api_base_url="https://api.deepseek.com/v1",
                api_key_env_var="DEEPSEEK_API_KEY",
                model_type="chat",
                request_format="openai",
                description="DeepSeek Coder model",
                tags=["deepseek", "coder", "chat"]
            )
        }
        
        # Custom models added by users / 用户添加的自定义模型
        self.custom_models: Dict[str, AIModelConfig] = {}
        
        # Load saved models / 加载保存的模型
        self._load_models()
    
    def add_model(self, config: AIModelConfig) -> bool:
        """
        Add a custom AI model.
        添加自定义AI模型。
        
        Args:
            config: Model configuration.
                   模型配置。
        
        Returns:
            True if successful.
            成功返回True。
        """
        try:
            # Validate model ID / 验证模型ID
            if config.model_id in self.builtin_models:
                raise ValueError(f"Model ID '{config.model_id}' conflicts with built-in model")
            
            # Validate required fields / 验证必需字段
            if not config.model_name:
                raise ValueError("Model name is required")
            if not config.api_base_url:
                raise ValueError("API base URL is required")
            if not config.api_key_env_var:
                raise ValueError("API key environment variable is required")
            
            # Update timestamp / 更新时间戳
            config.updated_at = datetime.now().isoformat()
            
            # Add to custom models / 添加到自定义模型
            self.custom_models[config.model_id] = config
            
            # Save to file / 保存到文件
            self._save_models()
            
            logger.info(f"✅ 添加自定义AI模型: {config.model_name} ({config.model_id})")
            return True
        
        except Exception as e:
            logger.error(f"❌ 添加AI模型失败: {e}")
            return False
    
    def remove_model(self, model_id: str) -> bool:
        """
        Remove a custom AI model.
        删除自定义AI模型。
        
        Args:
            model_id: Model ID to remove.
                     要删除的模型ID。
        
        Returns:
            True if successful.
            成功返回True。
        """
        try:
            if model_id in self.builtin_models:
                raise ValueError(f"Cannot remove built-in model: {model_id}")
            
            if model_id not in self.custom_models:
                raise ValueError(f"Model not found: {model_id}")
            
            # Remove model / 删除模型
            del self.custom_models[model_id]
            
            # Save to file / 保存到文件
            self._save_models()
            
            logger.info(f"✅ 删除自定义AI模型: {model_id}")
            return True
        
        except Exception as e:
            logger.error(f"❌ 删除AI模型失败: {e}")
            return False
    
    def update_model(self, model_id: str, config: AIModelConfig) -> bool:
        """
        Update a custom AI model.
        更新自定义AI模型。
        
        Args:
            model_id: Model ID to update.
                     要更新的模型ID。
            config: New configuration.
                   新配置。
        
        Returns:
            True if successful.
            成功返回True。
        """
        try:
            if model_id in self.builtin_models:
                raise ValueError(f"Cannot update built-in model: {model_id}")
            
            if model_id not in self.custom_models:
                raise ValueError(f"Model not found: {model_id}")
            
            # Update timestamp / 更新时间戳
            config.updated_at = datetime.now().isoformat()
            
            # Update model / 更新模型
            self.custom_models[model_id] = config
            
            # Save to file / 保存到文件
            self._save_models()
            
            logger.info(f"✅ 更新自定义AI模型: {config.model_name} ({model_id})")
            return True
        
        except Exception as e:
            logger.error(f"❌ 更新AI模型失败: {e}")
            return False
    
    def get_model(self, model_id: str) -> Optional[AIModelConfig]:
        """
        Get model configuration.
        获取模型配置。
        
        Args:
            model_id: Model ID.
                     模型ID。
        
        Returns:
            Model configuration or None.
            模型配置或None。
        """
        # Check custom models first / 首先检查自定义模型
        if model_id in self.custom_models:
            return self.custom_models[model_id]
        
        # Then check built-in models / 然后检查内置模型
        if model_id in self.builtin_models:
            return self.builtin_models[model_id]
        
        return None
    
    def list_models(
        self,
        include_builtin: bool = True,
        include_custom: bool = True,
        enabled_only: bool = False
    ) -> List[AIModelConfig]:
        """
        List all available models.
        列出所有可用模型。
        
        Args:
            include_builtin: Include built-in models.
                           包含内置模型。
            include_custom: Include custom models.
                          包含自定义模型。
            enabled_only: Only include enabled models.
                         只包含启用的模型。
        
        Returns:
            List of model configurations.
            模型配置列表。
        """
        models = []
        
        if include_builtin:
            models.extend(self.builtin_models.values())
        
        if include_custom:
            models.extend(self.custom_models.values())
        
        if enabled_only:
            models = [m for m in models if m.enabled]
        
        return models
    
    def test_model(self, model_id: str, test_prompt: str = "Hello") -> Dict[str, Any]:
        """
        Test model connectivity and response.
        测试模型连接和响应。
        
        Args:
            model_id: Model ID to test.
                     要测试的模型ID。
            test_prompt: Test prompt.
                        测试提示词。
        
        Returns:
            Test result dictionary.
            测试结果字典。
        """
        result = {
            "model_id": model_id,
            "success": False,
            "response": None,
            "error": None,
            "latency_ms": 0
        }
        
        try:
            # Get model config / 获取模型配置
            config = self.get_model(model_id)
            if not config:
                raise ValueError(f"Model not found: {model_id}")
            
            # Get API key / 获取API密钥
            api_key = os.getenv(config.api_key_env_var)
            if not api_key:
                raise ValueError(f"API key not found in environment: {config.api_key_env_var}")
            
            # Prepare request / 准备请求
            start_time = datetime.now()
            
            if config.request_format == "openai":
                response = self._test_openai_format(config, api_key, test_prompt)
            elif config.request_format == "anthropic":
                response = self._test_anthropic_format(config, api_key, test_prompt)
            elif config.request_format == "google":
                response = self._test_google_format(config, api_key, test_prompt)
            elif config.request_format == "custom":
                response = self._test_custom_format(config, api_key, test_prompt)
            else:
                raise ValueError(f"Unsupported request format: {config.request_format}")
            
            end_time = datetime.now()
            latency = (end_time - start_time).total_seconds() * 1000
            
            result["success"] = True
            result["response"] = response
            result["latency_ms"] = round(latency, 2)
            
            logger.info(f"✅ 模型测试成功: {model_id} ({latency:.2f}ms)")
        
        except Exception as e:
            result["error"] = str(e)
            logger.error(f"❌ 模型测试失败: {model_id} - {e}")
        
        return result
    
    def _test_openai_format(self, config: AIModelConfig, api_key: str, prompt: str) -> str:
        """Test OpenAI-compatible API"""
        url = f"{config.api_base_url}/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            **config.custom_headers
        }
        
        data = {
            "model": config.model_id,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 100,
            "temperature": 0.3
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        return response.json()["choices"][0]["message"]["content"]
    
    def _test_anthropic_format(self, config: AIModelConfig, api_key: str, prompt: str) -> str:
        """Test Anthropic Claude API"""
        url = f"{config.api_base_url}/messages"
        
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
            **config.custom_headers
        }
        
        data = {
            "model": config.model_id,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 100
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        return response.json()["content"][0]["text"]
    
    def _test_google_format(self, config: AIModelConfig, api_key: str, prompt: str) -> str:
        """Test Google Gemini API"""
        url = f"{config.api_base_url}/models/{config.model_id}:generateContent?key={api_key}"
        
        headers = {
            "Content-Type": "application/json",
            **config.custom_headers
        }
        
        data = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    
    def _test_custom_format(self, config: AIModelConfig, api_key: str, prompt: str) -> str:
        """Test custom API format"""
        if not config.request_template:
            raise ValueError("Custom format requires request_template")
        
        # Build request from template / 从模板构建请求
        url = config.api_base_url
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            **config.custom_headers
        }
        
        # Replace placeholders in template / 替换模板中的占位符
        data = json.loads(json.dumps(config.request_template))
        self._replace_placeholders(data, {"prompt": prompt, "model": config.model_id})
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        # Extract response using JSONPath / 使用JSONPath提取响应
        response_data = response.json()
        if config.response_path:
            return self._extract_by_path(response_data, config.response_path)
        else:
            return str(response_data)
    
    def _replace_placeholders(self, obj: Any, replacements: Dict[str, str]):
        """Replace placeholders in object"""
        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, str):
                    for placeholder, replacement in replacements.items():
                        value = value.replace(f"{{{{{placeholder}}}}}", replacement)
                    obj[key] = value
                else:
                    self._replace_placeholders(value, replacements)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                if isinstance(item, str):
                    for placeholder, replacement in replacements.items():
                        item = item.replace(f"{{{{{placeholder}}}}}", replacement)
                    obj[i] = item
                else:
                    self._replace_placeholders(item, replacements)
    
    def _extract_by_path(self, data: Any, path: str) -> str:
        """Extract value from nested dict using dot notation"""
        keys = path.split(".")
        current = data
        
        for key in keys:
            if isinstance(current, dict):
                current = current.get(key)
            elif isinstance(current, list):
                try:
                    idx = int(key)
                    current = current[idx]
                except (ValueError, IndexError):
                    return None
            else:
                return None
        
        return str(current) if current is not None else None
    
    def _load_models(self):
        """Load models from configuration file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                for model_data in data.get("custom_models", []):
                    config = AIModelConfig(**model_data)
                    self.custom_models[config.model_id] = config
                
                logger.info(f"✅ 加载了 {len(self.custom_models)} 个自定义AI模型")
        
        except Exception as e:
            logger.warning(f"⚠️ 加载AI模型配置失败: {e}")
    
    def _save_models(self):
        """Save models to configuration file"""
        try:
            data = {
                "version": "1.0",
                "updated_at": datetime.now().isoformat(),
                "custom_models": [
                    asdict(config) for config in self.custom_models.values()
                ]
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✅ 保存了 {len(self.custom_models)} 个自定义AI模型")
        
        except Exception as e:
            logger.error(f"❌ 保存AI模型配置失败: {e}")
    
    def export_model(self, model_id: str) -> Optional[Dict[str, Any]]:
        """
        Export model configuration for sharing.
        导出模型配置用于分享。
        
        Args:
            model_id: Model ID to export.
                     要导出的模型ID。
        
        Returns:
            Model configuration dictionary.
            模型配置字典。
        """
        config = self.get_model(model_id)
        if not config:
            return None
        
        return asdict(config)
    
    def import_model(self, model_data: Dict[str, Any]) -> bool:
        """
        Import model configuration.
        导入模型配置。
        
        Args:
            model_data: Model configuration dictionary.
                       模型配置字典。
        
        Returns:
            True if successful.
            成功返回True。
        """
        try:
            config = AIModelConfig(**model_data)
            return self.add_model(config)
        
        except Exception as e:
            logger.error(f"❌ 导入AI模型失败: {e}")
            return False


# Global instance / 全局实例
_model_manager = None


def get_model_manager() -> AIModelManager:
    """Get global AI Model Manager instance"""
    global _model_manager
    if _model_manager is None:
        _model_manager = AIModelManager()
    return _model_manager

