"""
JavaScript 代码解析器
使用正则表达式解析（可扩展使用 esprima）
"""

import re
from typing import Dict, List, Any
from loguru import logger

from .base_parser import BaseParser


class JavaScriptParser(BaseParser):
    """JavaScript解析器"""
    
    def parse(self, code: str) -> Dict[str, Any]:
        """解析JavaScript代码"""
        classes = self._extract_classes(code)
        functions = self._extract_functions(code)
        imports = self._extract_imports(code)
        
        return {
            "classes": classes,
            "functions": functions,
            "imports": imports
        }
    
    def _extract_classes(self, code: str) -> List[str]:
        """提取类定义"""
        # ES6 class 语法
        class_pattern = r'class\s+(\w+)'
        return re.findall(class_pattern, code)
    
    def _extract_functions(self, code: str) -> List[str]:
        """提取函数定义"""
        functions = []
        
        # 普通函数
        func_pattern = r'function\s+(\w+)\s*\('
        functions.extend(re.findall(func_pattern, code))
        
        # 箭头函数
        arrow_pattern = r'(?:const|let|var)\s+(\w+)\s*=\s*\([^)]*\)\s*=>'
        functions.extend(re.findall(arrow_pattern, code))
        
        return functions
    
    def _extract_imports(self, code: str) -> List[str]:
        """提取导入语句"""
        imports = []
        
        # ES6 import
        import_pattern = r"import\s+(?:{[^}]+}|\w+)\s+from\s+['\"]([^'\"]+)['\"]"
        imports.extend(re.findall(import_pattern, code))
        
        # require
        require_pattern = r"require\s*\(['\"]([^'\"]+)['\"]\)"
        imports.extend(re.findall(require_pattern, code))
        
        return imports
    
    def extract_structure(self, code: str) -> Dict[str, Any]:
        """提取JavaScript代码结构"""
        parsed = self.parse(code)
        
        return {
            "classes": parsed["classes"],
            "functions": parsed["functions"],
            "imports": parsed["imports"],
            "is_module": "export" in code or "module.exports" in code
        }

