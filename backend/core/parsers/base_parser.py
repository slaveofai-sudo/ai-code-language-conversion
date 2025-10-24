"""
基础解析器接口
所有语言解析器的抽象基类
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any


class BaseParser(ABC):
    """解析器基类"""
    
    @abstractmethod
    def parse(self, code: str) -> Dict[str, Any]:
        """
        解析代码
        
        Args:
            code: 源代码字符串
            
        Returns:
            Dict包含:
            - classes: 类名列表
            - functions: 函数名列表  
            - imports: 导入语句列表
            - ast: 抽象语法树(可选)
        """
        pass
    
    @abstractmethod
    def extract_structure(self, code: str) -> Dict[str, Any]:
        """提取代码结构信息"""
        pass
    
    def get_imports(self, code: str) -> List[str]:
        """提取导入语句"""
        return []
    
    def get_classes(self, code: str) -> List[str]:
        """提取类定义"""
        return []
    
    def get_functions(self, code: str) -> List[str]:
        """提取函数定义"""
        return []

