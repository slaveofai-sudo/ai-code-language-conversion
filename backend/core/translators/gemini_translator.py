"""
Google Gemini Translator / Google Gemini 翻译器

Uses Google's Gemini Pro model for code translation.
使用Google的Gemini Pro模型进行代码翻译。

Features / 特点:
- Multi-modal understanding / 多模态理解
- Fast inference / 快速推理
- Good code generation / 优秀的代码生成能力
"""

import os
from typing import Dict, Any
import httpx
from loguru import logger

from .base_translator import BaseTranslator


class GeminiTranslator(BaseTranslator):
    """Google Gemini 翻译器"""
    
    def __init__(self, model_name: str = "gemini-pro"):
        super().__init__(model_name)
        
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY 环境变量未设置")
        
        self.api_base = "https://generativelanguage.googleapis.com/v1beta"
        self.timeout = 120.0
    
    async def translate(
        self,
        source_code: str,
        source_language: str,
        target_language: str,
        context: Dict[str, Any] = None
    ) -> str:
        """使用 Gemini 翻译代码"""
        try:
            prompt = self._build_prompt(
                source_code,
                source_language,
                target_language,
                context
            )
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.api_base}/models/{self.model_name}:generateContent?key={self.api_key}",
                    headers={"Content-Type": "application/json"},
                    json={
                        "contents": [{
                            "parts": [{
                                "text": prompt
                            }]
                        }],
                        "generationConfig": {
                            "temperature": 0.1,
                            "maxOutputTokens": 4096
                        }
                    }
                )
                
                response.raise_for_status()
                result = response.json()
                
                translated_code = result["candidates"][0]["content"]["parts"][0]["text"]
                translated_code = self._extract_code_from_response(
                    translated_code,
                    target_language
                )
                
                logger.info(f"Gemini翻译成功: {source_language} → {target_language}")
                return translated_code
                
        except Exception as e:
            logger.error(f"Gemini 翻译失败: {str(e)}")
            raise

