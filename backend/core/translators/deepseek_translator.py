"""
DeepSeek 翻译器
支持 DeepSeek Coder 模型
"""

import os
from typing import Dict, Any
import httpx
from loguru import logger

from .base_translator import BaseTranslator


class DeepSeekTranslator(BaseTranslator):
    """DeepSeek Coder 翻译器"""
    
    def __init__(self, model_name: str = "deepseek-coder"):
        super().__init__(model_name)
        
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY 环境变量未设置")
        
        self.api_base = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com/v1")
        self.timeout = 120.0
    
    async def translate(
        self,
        source_code: str,
        source_language: str,
        target_language: str,
        context: Dict[str, Any] = None
    ) -> str:
        """使用 DeepSeek 翻译代码"""
        try:
            # 构建提示词
            prompt = self._build_prompt(
                source_code,
                source_language,
                target_language,
                context
            )
            
            # 调用 DeepSeek API
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.api_base}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model_name,
                        "messages": [
                            {
                                "role": "system",
                                "content": "You are an expert code translator specializing in converting code between programming languages."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        "temperature": 0.1,
                        "max_tokens": 4096
                    }
                )
                
                response.raise_for_status()
                result = response.json()
                
                # 提取响应
                translated_code = result["choices"][0]["message"]["content"]
                
                # 清理响应
                translated_code = self._extract_code_from_response(
                    translated_code,
                    target_language
                )
                
                logger.info(
                    f"DeepSeek翻译成功: {source_language} → {target_language}"
                )
                
                return translated_code
                
        except Exception as e:
            logger.error(f"DeepSeek 翻译失败: {str(e)}")
            raise

