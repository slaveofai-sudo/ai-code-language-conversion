"""
Anthropic Claude 翻译器
"""

import os
from typing import Dict, Any
from anthropic import AsyncAnthropic
from loguru import logger

from .base_translator import BaseTranslator


class AnthropicTranslator(BaseTranslator):
    """Claude翻译器"""
    
    def __init__(self, model_name: str = "claude-3-5-sonnet-20241022"):
        super().__init__(model_name)
        
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY 环境变量未设置")
        
        self.client = AsyncAnthropic(api_key=api_key)
        self.max_tokens = 8192
    
    async def translate(
        self,
        source_code: str,
        source_language: str,
        target_language: str,
        context: Dict[str, Any] = None
    ) -> str:
        """使用 Claude 翻译代码"""
        try:
            # 构建提示词
            prompt = self._build_prompt(
                source_code,
                source_language,
                target_language,
                context
            )
            
            # 调用 Anthropic API
            response = await self.client.messages.create(
                model=self.model_name,
                max_tokens=self.max_tokens,
                temperature=0.1,
                system="You are an expert code translator. Convert code between programming languages while preserving functionality, structure, and best practices.",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # 提取响应
            translated_code = response.content[0].text
            
            # 清理响应
            translated_code = self._extract_code_from_response(
                translated_code,
                target_language
            )
            
            logger.info(
                f"Claude翻译成功: {source_language} → {target_language}"
            )
            
            return translated_code
            
        except Exception as e:
            logger.error(f"Anthropic 翻译失败: {str(e)}")
            raise

