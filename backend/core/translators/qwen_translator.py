"""
阿里通义千问翻译器
"""

import os
from typing import Dict, Any
import httpx
from loguru import logger

from .base_translator import BaseTranslator


class QwenTranslator(BaseTranslator):
    """通义千问 Coder 翻译器"""
    
    def __init__(self, model_name: str = "qwen-coder-turbo"):
        super().__init__(model_name)
        
        self.api_key = os.getenv("QWEN_API_KEY")
        if not self.api_key:
            raise ValueError("QWEN_API_KEY 环境变量未设置")
        
        self.api_base = "https://dashscope.aliyuncs.com/api/v1"
        self.timeout = 120.0
    
    async def translate(
        self,
        source_code: str,
        source_language: str,
        target_language: str,
        context: Dict[str, Any] = None
    ) -> str:
        """使用通义千问翻译代码"""
        try:
            prompt = self._build_prompt(
                source_code,
                source_language,
                target_language,
                context
            )
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.api_base}/services/aigc/text-generation/generation",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model_name,
                        "input": {
                            "messages": [
                                {
                                    "role": "system",
                                    "content": "You are an expert code translator."
                                },
                                {
                                    "role": "user",
                                    "content": prompt
                                }
                            ]
                        },
                        "parameters": {
                            "temperature": 0.1,
                            "max_tokens": 4096
                        }
                    }
                )
                
                response.raise_for_status()
                result = response.json()
                
                translated_code = result["output"]["text"]
                translated_code = self._extract_code_from_response(
                    translated_code,
                    target_language
                )
                
                logger.info(f"通义千问翻译成功: {source_language} → {target_language}")
                return translated_code
                
        except Exception as e:
            logger.error(f"通义千问翻译失败: {str(e)}")
            raise

