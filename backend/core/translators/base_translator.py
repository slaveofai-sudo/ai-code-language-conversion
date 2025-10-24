"""
翻译器基类
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseTranslator(ABC):
    """AI翻译器基类"""
    
    def __init__(self, model_name: str):
        self.model_name = model_name
    
    @abstractmethod
    async def translate(
        self,
        source_code: str,
        source_language: str,
        target_language: str,
        context: Dict[str, Any] = None
    ) -> str:
        """
        翻译代码
        
        Args:
            source_code: 源代码
            source_language: 源语言
            target_language: 目标语言
            context: 上下文信息（文件路径、类名、函数名等）
            
        Returns:
            str: 翻译后的代码
        """
        pass
    
    def _build_prompt(
        self,
        source_code: str,
        source_language: str,
        target_language: str,
        context: Dict[str, Any] = None
    ) -> str:
        """构建提示词"""
        prompt = f"""You are an expert code translator. Convert the following {source_language} code to {target_language}.

Requirements:
1. Preserve the original logic and functionality exactly
2. Follow {target_language} naming conventions and best practices
3. Maintain all comments and documentation
4. Use idiomatic {target_language} patterns
5. Ensure proper error handling
6. Add type hints/annotations where applicable

{source_language} Source Code:
```{source_language}
{source_code}
```

Provide ONLY the translated {target_language} code without explanations:
```{target_language}
"""
        return prompt
    
    def _extract_code_from_response(self, response: str, language: str) -> str:
        """从响应中提取代码"""
        import re
        
        # 尝试提取代码块
        pattern = rf"```{language}?\s*(.*?)\s*```"
        match = re.search(pattern, response, re.DOTALL | re.IGNORECASE)
        
        if match:
            return match.group(1).strip()
        
        # 如果没有代码块标记，返回原始响应
        return response.strip()

