"""
Test Generator / 测试生成器

Automatically generates unit tests for converted code.
自动为转换后的代码生成单元测试。

Features / 功能:
- Analyze function signatures / 分析函数签名
- Generate test scenarios / 生成测试场景
- Create mock objects / 创建模拟对象
- Generate assertions / 生成断言
"""

import ast
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from loguru import logger
from dataclasses import dataclass


@dataclass
class FunctionInfo:
    """Function information / 函数信息"""
    name: str
    params: List[Dict[str, Any]]
    return_type: Optional[str]
    is_async: bool
    decorators: List[str]
    docstring: Optional[str]
    class_name: Optional[str] = None


class TestGenerator:
    """
    Test Generator / 测试生成器
    
    Generates comprehensive unit tests for converted code.
    为转换后的代码生成全面的单元测试。
    """
    
    def __init__(self, ai_model: str = "gpt-4o"):
        self.ai_model = ai_model
        self.test_frameworks = {
            "python": "pytest",
            "java": "junit",
            "javascript": "jest",
            "go": "testing"
        }
        
    def generate_tests(
        self,
        source_file: Path,
        target_language: str,
        framework: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate tests for a converted source file.
        为转换后的源文件生成测试。
        
        Args:
            source_file: Path to the converted source file.
                        转换后源文件的路径。
            target_language: Target programming language.
                           目标编程语言。
            framework: Optional framework name (e.g., "fastapi").
                      可选的框架名称。
        
        Returns:
            Dictionary containing test code and metadata.
            包含测试代码和元数据的字典。
        """
        logger.info(f"开始为文件生成测试: {source_file}")
        
        # Parse source file and extract functions
        # 解析源文件并提取函数
        functions = self._parse_source_file(source_file, target_language)
        
        if not functions:
            logger.warning(f"未在文件中找到可测试的函数: {source_file}")
            return {"status": "no_functions", "test_code": "", "functions_tested": 0}
        
        # Generate test code for each function
        # 为每个函数生成测试代码
        test_code_sections = []
        
        # Add imports
        # 添加导入
        imports = self._generate_imports(target_language, framework, functions)
        test_code_sections.append(imports)
        
        # Generate test class or functions
        # 生成测试类或函数
        for func in functions:
            test_code = self._generate_function_tests(func, target_language, framework)
            test_code_sections.append(test_code)
        
        final_test_code = "\n\n".join(test_code_sections)
        
        # Format test code
        # 格式化测试代码
        final_test_code = self._format_test_code(final_test_code, target_language)
        
        return {
            "status": "success",
            "test_code": final_test_code,
            "functions_tested": len(functions),
            "test_file_name": self._get_test_filename(source_file, target_language),
            "framework": self.test_frameworks.get(target_language, "unknown")
        }
    
    def _parse_source_file(self, source_file: Path, language: str) -> List[FunctionInfo]:
        """
        Parse source file and extract function information.
        解析源文件并提取函数信息。
        """
        if language == "python":
            return self._parse_python_file(source_file)
        elif language == "java":
            return self._parse_java_file(source_file)
        elif language == "javascript":
            return self._parse_javascript_file(source_file)
        else:
            logger.warning(f"不支持的语言: {language}")
            return []
    
    def _parse_python_file(self, source_file: Path) -> List[FunctionInfo]:
        """
        Parse Python file using AST.
        使用AST解析Python文件。
        """
        try:
            with open(source_file, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
            
            functions = []
            current_class = None
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    current_class = node.name
                    
                if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                    # Skip private methods (starting with _)
                    # 跳过私有方法（以_开头）
                    if node.name.startswith('_') and node.name != '__init__':
                        continue
                    
                    params = []
                    for arg in node.args.args:
                        param_info = {"name": arg.arg}
                        if arg.annotation:
                            param_info["type"] = ast.unparse(arg.annotation)
                        params.append(param_info)
                    
                    return_type = None
                    if node.returns:
                        return_type = ast.unparse(node.returns)
                    
                    decorators = [ast.unparse(d) for d in node.decorator_list]
                    
                    docstring = ast.get_docstring(node)
                    
                    func_info = FunctionInfo(
                        name=node.name,
                        params=params,
                        return_type=return_type,
                        is_async=isinstance(node, ast.AsyncFunctionDef),
                        decorators=decorators,
                        docstring=docstring,
                        class_name=current_class
                    )
                    
                    functions.append(func_info)
                    logger.debug(f"提取函数: {func_info.name} (类: {current_class})")
            
            return functions
        except Exception as e:
            logger.error(f"解析Python文件失败 {source_file}: {e}")
            return []
    
    def _parse_java_file(self, source_file: Path) -> List[FunctionInfo]:
        """
        Parse Java file (simplified regex-based parsing).
        解析Java文件（简化的基于正则的解析）。
        """
        try:
            with open(source_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            functions = []
            
            # Simple regex to find public methods
            # 简单正则查找公共方法
            method_pattern = r'public\s+(?:static\s+)?(\w+)\s+(\w+)\s*\((.*?)\)'
            
            for match in re.finditer(method_pattern, content):
                return_type = match.group(1)
                method_name = match.group(2)
                params_str = match.group(3)
                
                # Parse parameters
                # 解析参数
                params = []
                if params_str.strip():
                    for param in params_str.split(','):
                        param = param.strip()
                        if param:
                            parts = param.split()
                            if len(parts) >= 2:
                                params.append({
                                    "name": parts[-1],
                                    "type": ' '.join(parts[:-1])
                                })
                
                func_info = FunctionInfo(
                    name=method_name,
                    params=params,
                    return_type=return_type,
                    is_async=False,
                    decorators=[],
                    docstring=None
                )
                
                functions.append(func_info)
                logger.debug(f"提取Java方法: {method_name}")
            
            return functions
        except Exception as e:
            logger.error(f"解析Java文件失败 {source_file}: {e}")
            return []
    
    def _parse_javascript_file(self, source_file: Path) -> List[FunctionInfo]:
        """
        Parse JavaScript/TypeScript file (simplified).
        解析JavaScript/TypeScript文件（简化）。
        """
        try:
            with open(source_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            functions = []
            
            # Find async function declarations
            # 查找async函数声明
            async_pattern = r'async\s+function\s+(\w+)\s*\((.*?)\)'
            for match in re.finditer(async_pattern, content):
                func_name = match.group(1)
                params_str = match.group(2)
                
                params = []
                if params_str.strip():
                    for param in params_str.split(','):
                        param = param.strip()
                        if param:
                            params.append({"name": param.split(':')[0].strip()})
                
                func_info = FunctionInfo(
                    name=func_name,
                    params=params,
                    return_type=None,
                    is_async=True,
                    decorators=[],
                    docstring=None
                )
                functions.append(func_info)
            
            # Find regular function declarations
            # 查找常规函数声明
            func_pattern = r'function\s+(\w+)\s*\((.*?)\)'
            for match in re.finditer(func_pattern, content):
                func_name = match.group(1)
                params_str = match.group(2)
                
                params = []
                if params_str.strip():
                    for param in params_str.split(','):
                        param = param.strip()
                        if param:
                            params.append({"name": param.split(':')[0].strip()})
                
                func_info = FunctionInfo(
                    name=func_name,
                    params=params,
                    return_type=None,
                    is_async=False,
                    decorators=[],
                    docstring=None
                )
                functions.append(func_info)
            
            return functions
        except Exception as e:
            logger.error(f"解析JavaScript文件失败 {source_file}: {e}")
            return []
    
    def _generate_imports(
        self,
        language: str,
        framework: Optional[str],
        functions: List[FunctionInfo]
    ) -> str:
        """
        Generate import statements for test file.
        为测试文件生成导入语句。
        """
        if language == "python":
            imports = ["import pytest", "from unittest.mock import Mock, AsyncMock, patch"]
            
            # Check if any function is async
            # 检查是否有异步函数
            has_async = any(f.is_async for f in functions)
            if has_async:
                imports.append("import asyncio")
            
            # Framework-specific imports
            # 框架特定的导入
            if framework == "fastapi":
                imports.append("from fastapi import HTTPException")
                imports.append("from fastapi.testclient import TestClient")
            elif framework == "django":
                imports.append("from django.test import TestCase")
            elif framework == "flask":
                imports.append("from flask import Flask")
            
            return "\n".join(imports)
        
        elif language == "java":
            return """import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;"""
        
        elif language == "javascript":
            return """const { describe, it, expect, beforeEach, jest } = require('@jest/globals');"""
        
        return ""
    
    def _generate_function_tests(
        self,
        func: FunctionInfo,
        language: str,
        framework: Optional[str]
    ) -> str:
        """
        Generate test code for a single function.
        为单个函数生成测试代码。
        """
        if language == "python":
            return self._generate_python_tests(func, framework)
        elif language == "java":
            return self._generate_java_tests(func)
        elif language == "javascript":
            return self._generate_javascript_tests(func)
        return ""
    
    def _generate_python_tests(self, func: FunctionInfo, framework: Optional[str]) -> str:
        """
        Generate pytest test code for Python function.
        为Python函数生成pytest测试代码。
        """
        test_class_name = f"Test{func.class_name or func.name.title()}"
        test_func_name = f"test_{func.name}"
        
        # Determine test scenarios
        # 确定测试场景
        scenarios = self._identify_test_scenarios(func)
        
        test_code = f'class {test_class_name}:\n'
        test_code += f'    """{func.class_name or func.name}的测试类"""\n\n'
        
        # Generate fixture for mocks if needed
        # 如果需要，生成模拟对象的fixture
        if func.params and len(func.params) > 1:  # Assuming first param might be 'self'
            test_code += '    @pytest.fixture\n'
            test_code += '    def mock_dependencies(self):\n'
            test_code += '        """Mock dependencies / 模拟依赖项"""\n'
            test_code += '        return {\n'
            for param in func.params[1:]:  # Skip 'self'
                if param["name"] != "self":
                    test_code += f'            "{param["name"]}": Mock(),\n'
            test_code += '        }\n\n'
        
        # Generate test for success scenario
        # 生成成功场景的测试
        async_marker = "@pytest.mark.asyncio\n    " if func.is_async else ""
        async_keyword = "async " if func.is_async else ""
        await_keyword = "await " if func.is_async else ""
        
        test_code += f'    {async_marker}async def {test_func_name}_success(self):\n'
        test_code += f'        """测试 {func.name} - 正常情况"""\n'
        test_code += '        # Arrange / 准备\n'
        
        # Generate mock setup
        # 生成模拟设置
        for param in func.params[1:]:  # Skip 'self'
            if param["name"] != "self":
                param_name = param["name"]
                test_code += f'        mock_{param_name} = Mock()\n'
        
        test_code += '\n        # Act / 执行\n'
        
        # Generate function call
        # 生成函数调用
        param_names = [p["name"] for p in func.params if p["name"] != "self"]
        params_str = ", ".join([f"mock_{p}" if i > 0 else p for i, p in enumerate(param_names)])
        
        if func.class_name:
            test_code += f'        instance = {func.class_name}()\n'
            test_code += f'        result = {await_keyword}instance.{func.name}({params_str})\n'
        else:
            test_code += f'        result = {await_keyword}{func.name}({params_str})\n'
        
        test_code += '\n        # Assert / 断言\n'
        test_code += '        assert result is not None\n'
        
        if func.return_type:
            test_code += f'        # TODO: 添加更具体的断言来验证返回类型 {func.return_type}\n'
        
        test_code += '\n'
        
        # Generate test for exception scenario
        # 生成异常场景的测试
        if framework == "fastapi" or "HTTPException" in str(func.decorators):
            test_code += f'    {async_marker}async def {test_func_name}_not_found(self):\n'
            test_code += f'        """测试 {func.name} - 异常情况（未找到）"""\n'
            test_code += '        # Arrange / 准备\n'
            test_code += '        # TODO: 设置导致HTTPException的条件\n\n'
            test_code += '        # Act & Assert / 执行和断言\n'
            test_code += '        with pytest.raises(HTTPException) as exc_info:\n'
            test_code += f'            {await_keyword}{func.name}(invalid_param)\n'
            test_code += '        assert exc_info.value.status_code == 404\n\n'
        
        # Generate parametrized test
        # 生成参数化测试
        if func.params:
            test_code += '    @pytest.mark.parametrize("test_input,expected", [\n'
            test_code += '        (1, "expected_output_1"),\n'
            test_code += '        (2, "expected_output_2"),\n'
            test_code += '        (3, "expected_output_3"),\n'
            test_code += '    ])\n'
            test_code += f'    {async_marker}async def {test_func_name}_parametrized(self, test_input, expected):\n'
            test_code += f'        """测试 {func.name} - 参数化测试（边界情况）"""\n'
            test_code += '        # TODO: 实现参数化测试逻辑\n'
            test_code += f'        result = {await_keyword}{func.name}(test_input)\n'
            test_code += '        # assert result == expected\n\n'
        
        return test_code
    
    def _generate_java_tests(self, func: FunctionInfo) -> str:
        """
        Generate JUnit test code for Java method.
        为Java方法生成JUnit测试代码。
        """
        test_class_name = f"{func.name.title()}Test"
        
        test_code = f'public class {test_class_name} {{\n\n'
        test_code += '    @BeforeEach\n'
        test_code += '    void setUp() {\n'
        test_code += '        MockitoAnnotations.openMocks(this);\n'
        test_code += '    }\n\n'
        
        test_code += '    @Test\n'
        test_code += f'    void test{func.name.title()}Success() {{\n'
        test_code += '        // Arrange\n'
        test_code += '        // TODO: Set up test data\n\n'
        test_code += '        // Act\n'
        params_str = ", ".join([f'mock{p["name"].title()}' for p in func.params])
        test_code += f'        {func.return_type} result = {func.name}({params_str});\n\n'
        test_code += '        // Assert\n'
        test_code += '        assertNotNull(result);\n'
        test_code += '        // TODO: Add more specific assertions\n'
        test_code += '    }\n\n'
        
        test_code += '    @Test\n'
        test_code += f'    void test{func.name.title()}ThrowsException() {{\n'
        test_code += '        // TODO: Test exception scenario\n'
        test_code += '    }\n'
        test_code += '}\n'
        
        return test_code
    
    def _generate_javascript_tests(self, func: FunctionInfo) -> str:
        """
        Generate Jest test code for JavaScript function.
        为JavaScript函数生成Jest测试代码。
        """
        test_code = f"describe('{func.name}', () => {{\n"
        test_code += "    beforeEach(() => {\n"
        test_code += "        // Set up test environment\n"
        test_code += "    });\n\n"
        
        test_code += f"    it('should execute successfully', {'async ' if func.is_async else ''}() => {{\n"
        test_code += "        // Arrange\n"
        test_code += "        const mockData = {};\n\n"
        test_code += "        // Act\n"
        await_keyword = "await " if func.is_async else ""
        test_code += f"        const result = {await_keyword}{func.name}(mockData);\n\n"
        test_code += "        // Assert\n"
        test_code += "        expect(result).toBeDefined();\n"
        test_code += "    });\n\n"
        
        test_code += f"    it('should handle errors', {'async ' if func.is_async else ''}() => {{\n"
        test_code += "        // TODO: Test error scenario\n"
        test_code += "    });\n"
        test_code += "});\n"
        
        return test_code
    
    def _identify_test_scenarios(self, func: FunctionInfo) -> List[str]:
        """
        Identify test scenarios based on function signature.
        根据函数签名识别测试场景。
        """
        scenarios = ["success"]  # Always test success case
        
        # Check for potential exception scenarios
        # 检查潜在的异常场景
        if func.return_type and ("Optional" in func.return_type or "None" in str(func.return_type)):
            scenarios.append("not_found")
        
        # Check for input validation scenarios
        # 检查输入验证场景
        if func.params:
            scenarios.append("invalid_input")
        
        # Check for boundary scenarios
        # 检查边界场景
        if any(p.get("type") in ["int", "Integer", "long", "Long"] for p in func.params):
            scenarios.append("boundary_values")
        
        return scenarios
    
    def _format_test_code(self, test_code: str, language: str) -> str:
        """
        Format test code using language-specific formatters.
        使用特定语言的格式化工具格式化测试代码。
        """
        if language == "python":
            try:
                import black
                return black.format_str(test_code, mode=black.FileMode())
            except ImportError:
                logger.warning("black未安装，跳过代码格式化")
                return test_code
        
        return test_code
    
    def _get_test_filename(self, source_file: Path, language: str) -> str:
        """
        Generate test filename based on source file.
        根据源文件生成测试文件名。
        """
        stem = source_file.stem
        
        if language == "python":
            return f"test_{stem}.py"
        elif language == "java":
            return f"{stem}Test.java"
        elif language == "javascript":
            return f"{stem}.test.js"
        
        return f"test_{stem}"

