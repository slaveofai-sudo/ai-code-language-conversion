"""
本地模型翻译器（使用 Ollama）
"""

import os
from typing import Dict, Any
import httpx
from loguru import logger

from .base_translator import BaseTranslator


class LocalTranslator(BaseTranslator):
    """本地模型翻译器（Ollama）"""
    
    def __init__(self, model_name: str = "codellama:13b"):
        super().__init__(model_name)
        
        self.endpoint = os.getenv("LOCAL_MODEL_URL", "http://localhost:11434")
        self.timeout = 120.0  # 本地模型可能较慢
    
    async def translate(
        self,
        source_code: str,
        source_language: str,
        target_language: str,
        context: Dict[str, Any] = None
    ) -> str:
        """使用本地模型翻译代码"""
        try:
            # 构建提示词
            prompt = self._build_prompt(
                source_code,
                source_language,
                target_language,
                context
            )
            
            # 调用 Ollama API
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.endpoint}/api/generate",
                    json={
                        "model": self.model_name,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.1,
                            "top_p": 0.95
                        }
                    }
                )
                
                response.raise_for_status()
                result = response.json()
                
                # 提取响应
                translated_code = result.get("response", "")
                
                # 清理响应
                translated_code = self._extract_code_from_response(
                    translated_code,
                    target_language
                )
                
                logger.info(
                    f"本地模型翻译成功: {source_language} → {target_language}"
                )
                
                return translated_code
                
        except Exception as e:
            logger.error(f"本地模型翻译失败: {str(e)}")
            raise

