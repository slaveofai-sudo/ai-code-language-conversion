"""
Java 代码解析器
使用 javalang 解析 Java 代码
"""

import re
from typing import Dict, List, Any
from loguru import logger

from .base_parser import BaseParser


class JavaParser(BaseParser):
    """Java解析器"""
    
    def parse(self, code: str) -> Dict[str, Any]:
        """解析Java代码"""
        try:
            # 尝试使用 javalang
            import javalang
            
            tree = javalang.parse.parse(code)
            
            classes = []
            functions = []
            imports = []
            
            # 提取类
            for _, node in tree.filter(javalang.tree.ClassDeclaration):
                classes.append(node.name)
                
                # 提取方法
                for method in node.methods:
                    functions.append(f"{node.name}.{method.name}")
            
            # 提取导入
            for imp in tree.imports:
                imports.append(imp.path)
            
            return {
                "classes": classes,
                "functions": functions,
                "imports": imports,
                "ast": tree
            }
            
        except ImportError:
            # 回退到正则解析
            logger.warning("javalang 未安装，使用正则表达式解析")
            return self._parse_with_regex(code)
        except Exception as e:
            logger.warning(f"Java 解析失败: {str(e)}")
            return self._parse_with_regex(code)
    
    def _parse_with_regex(self, code: str) -> Dict[str, Any]:
        """使用正则表达式解析（简化版）"""
        # 提取类名
        class_pattern = r'(?:public\s+)?(?:abstract\s+)?class\s+(\w+)'
        classes = re.findall(class_pattern, code)
        
        # 提取方法名
        method_pattern = r'(?:public|private|protected)\s+(?:static\s+)?[\w<>\[\]]+\s+(\w+)\s*\('
        functions = re.findall(method_pattern, code)
        
        # 提取导入
        import_pattern = r'import\s+([\w.]+);'
        imports = re.findall(import_pattern, code)
        
        return {
            "classes": classes,
            "functions": functions,
            "imports": imports
        }
    
    def extract_structure(self, code: str) -> Dict[str, Any]:
        """提取Java代码结构"""
        parsed = self.parse(code)
        
        return {
            "package": self._extract_package(code),
            "classes": parsed["classes"],
            "methods": parsed["functions"],
            "imports": parsed["imports"]
        }
    
    def _extract_package(self, code: str) -> str:
        """提取包名"""
        match = re.search(r'package\s+([\w.]+);', code)
        return match.group(1) if match else ""

