"""
OpenAI GPT Translator / OpenAI GPT 翻译器

Uses OpenAI's GPT models (GPT-4, GPT-4o) for code translation.
使用OpenAI的GPT模型（GPT-4、GPT-4o）进行代码翻译。

Supported models / 支持的模型:
- gpt-4-turbo: High quality, slower / 高质量，较慢
- gpt-4o: High quality, faster / 高质量，更快
"""

import os
from typing import Dict, Any
from openai import AsyncOpenAI
from loguru import logger

from .base_translator import BaseTranslator


class OpenAITranslator(BaseTranslator):
    """
    OpenAI GPT Translator / OpenAI GPT翻译器
    
    Translates code using OpenAI's GPT models with:
    使用OpenAI的GPT模型翻译代码，具有:
    - High translation quality / 高翻译质量
    - Good context understanding / 良好的上下文理解
    - Support for multiple languages / 支持多种语言
    """
    
    def __init__(self, model_name: str = "gpt-4-turbo"):
        super().__init__(model_name)
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY 环境变量未设置")
        
        self.client = AsyncOpenAI(api_key=api_key)
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", 4096))
    
    async def translate(
        self,
        source_code: str,
        source_language: str,
        target_language: str,
        context: Dict[str, Any] = None
    ) -> str:
        """
        Translate code using GPT / 使用GPT翻译代码
        
        Args:
            source_code: Source code to translate / 要翻译的源代码
            source_language: Source language (e.g., 'java') / 源语言
            target_language: Target language (e.g., 'python') / 目标语言
            context: Additional context (file path, classes, etc.) / 额外上下文
            
        Returns:
            str: Translated code / 翻译后的代码
            
        Raises:
            Exception: If translation fails / 翻译失败时抛出异常
        """
        try:
            # 构建提示词
            prompt = self._build_prompt(
                source_code,
                source_language,
                target_language,
                context
            )
            
            # 调用 OpenAI API
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert code translator specializing in converting code between programming languages while preserving functionality and best practices."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=self.max_tokens,
                temperature=0.1,  # 低温度以保持一致性
                top_p=0.95
            )
            
            # 提取响应
            translated_code = response.choices[0].message.content
            
            # 清理响应
            translated_code = self._extract_code_from_response(
                translated_code,
                target_language
            )
            
            logger.info(
                f"GPT翻译成功: {source_language} → {target_language}, "
                f"源码长度: {len(source_code)}, 译码长度: {len(translated_code)}"
            )
            
            return translated_code
            
        except Exception as e:
            logger.error(f"OpenAI 翻译失败: {str(e)}")
            raise
    
    def _build_prompt(
        self,
        source_code: str,
        source_language: str,
        target_language: str,
        context: Dict[str, Any] = None
    ) -> str:
        """构建增强的提示词"""
        context_info = ""
        if context:
            file_path = context.get("file_path", "")
            classes = context.get("classes", [])
            functions = context.get("functions", [])
            
            if file_path:
                context_info += f"\nFile: {file_path}"
            if classes:
                context_info += f"\nClasses: {', '.join(classes)}"
            if functions:
                context_info += f"\nFunctions: {', '.join(functions[:5])}"  # 限制数量
        
        prompt = f"""Convert the following {source_language} code to {target_language}.
{context_info}

Requirements:
1. Maintain exact functionality and logic
2. Follow {target_language} naming conventions (e.g., camelCase vs snake_case)
3. Use appropriate {target_language} libraries and idioms
4. Preserve all comments and documentation
5. Handle errors appropriately for {target_language}
6. Add type hints if {target_language} supports them

{source_language} code:
```{source_language}
{source_code}
```

Translated {target_language} code:
"""
        return prompt

