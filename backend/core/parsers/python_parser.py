"""
Python 代码解析器
使用 ast 模块解析 Python 代码
"""

import ast
from typing import Dict, List, Any
from loguru import logger

from .base_parser import BaseParser


class PythonParser(BaseParser):
    """Python解析器"""
    
    def parse(self, code: str) -> Dict[str, Any]:
        """解析Python代码"""
        try:
            tree = ast.parse(code)
            
            classes = []
            functions = []
            imports = []
            
            for node in ast.walk(tree):
                # 提取类
                if isinstance(node, ast.ClassDef):
                    classes.append(node.name)
                
                # 提取函数
                elif isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
                
                # 提取导入
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
            
            return {
                "classes": classes,
                "functions": functions,
                "imports": imports,
                "ast": tree
            }
            
        except SyntaxError as e:
            logger.warning(f"Python 语法错误: {str(e)}")
            return {
                "classes": [],
                "functions": [],
                "imports": [],
                "error": str(e)
            }
        except Exception as e:
            logger.warning(f"Python 解析失败: {str(e)}")
            return {
                "classes": [],
                "functions": [],
                "imports": []
            }
    
    def extract_structure(self, code: str) -> Dict[str, Any]:
        """提取Python代码结构"""
        parsed = self.parse(code)
        
        return {
            "classes": parsed["classes"],
            "functions": parsed["functions"],
            "imports": parsed["imports"],
            "has_main": "__main__" in code
        }
    
    def get_docstrings(self, code: str) -> List[str]:
        """提取文档字符串"""
        try:
            tree = ast.parse(code)
            docstrings = []
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
                    docstring = ast.get_docstring(node)
                    if docstring:
                        docstrings.append(docstring)
            
            return docstrings
        except:
            return []

