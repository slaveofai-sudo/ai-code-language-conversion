"""
Project Analyzer / 项目分析器

Analyzes project structure for multiple programming languages.
解析多种编程语言的项目结构。

Features / 功能:
- Multi-language parsing / 多语言解析
- Dependency extraction / 依赖提取
- Project structure mapping / 项目结构映射
- Build system detection / 构建系统检测
"""

import os
from pathlib import Path
from typing import Dict, List, Any
import yaml
from loguru import logger

from models.schemas import ProjectInfo, FileInfo, SupportedLanguage

# Lazy import to avoid circular dependency / 延迟导入以避免循环依赖
_framework_detector = None

def get_framework_detector():
    """Get framework detector instance / 获取框架检测器实例"""
    global _framework_detector
    if _framework_detector is None:
        from .framework_detector import FrameworkDetector
        _framework_detector = FrameworkDetector()
    return _framework_detector


class ProjectAnalyzer:
    """项目结构分析器"""
    
    def __init__(self):
        # 加载配置
        config_path = Path(__file__).parent.parent.parent / "config.yaml"
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        # 语言扩展名映射
        self.language_extensions = self._build_extension_map()
        
        # 排除的目录
        self.excluded_dirs = set(self.config.get('git', {}).get('excluded_dirs', []))
    
    def _build_extension_map(self) -> Dict[str, str]:
        """构建文件扩展名到语言的映射"""
        ext_map = {}
        for lang in self.config.get('supported_languages', []):
            lang_id = lang['id']
            for ext in lang.get('extensions', []):
                ext_map[ext] = lang_id
        return ext_map
    
    async def analyze(
        self,
        project_path: Path,
        language: SupportedLanguage
    ) -> ProjectInfo:
        """
        Analyze project structure including frameworks / 分析项目结构（包括框架）
        
        Args:
            project_path: Project path / 项目路径
            language: Source language / 源语言
            
        Returns:
            ProjectInfo: Project information / 项目信息
        """
        logger.info(f"🔍 开始分析项目: {project_path}, 语言: {language}")
        
        # Detect frameworks / 检测框架
        logger.info("📦 检测项目框架...")
        framework_detector = get_framework_detector()
        detected_frameworks = framework_detector.detect_frameworks(project_path)
        primary_framework = framework_detector.get_primary_framework()
        
        if primary_framework:
            logger.info(
                f"✅ 主要框架: {primary_framework['name']} "
                f"(置信度: {primary_framework['confidence']:.0%})"
            )
        
        # 收集所有源文件
        files = self._collect_source_files(project_path, language)
        
        # 分析每个文件
        file_infos = []
        total_lines = 0
        
        for file_path in files:
            file_info = await self._analyze_file(file_path, language)
            file_infos.append(file_info)
            total_lines += file_info.lines
        
        # 分析项目结构
        structure = self._analyze_structure(project_path, language)
        
        # Add frameworks info to structure / 将框架信息添加到结构中
        structure['frameworks'] = {
            'detected': detected_frameworks,
            'primary': primary_framework,
            'count': len(detected_frameworks)
        }
        
        # 分析依赖
        dependencies = await self._analyze_dependencies(project_path, language)
        
        project_info = ProjectInfo(
            name=project_path.name,
            language=language,
            total_files=len(file_infos),
            total_lines=total_lines,
            files=file_infos,
            dependencies=dependencies,
            structure=structure
        )
        
        logger.info(
            f"✅ 项目分析完成: {len(file_infos)} 个文件, "
            f"{total_lines} 行代码, {len(detected_frameworks)} 个框架"
        )
        
        return project_info
    
    def _collect_source_files(
        self,
        project_path: Path,
        language: SupportedLanguage
    ) -> List[Path]:
        """收集源代码文件"""
        files = []
        
        # 获取该语言的扩展名
        lang_config = next(
            (l for l in self.config['supported_languages'] if l['id'] == language.value),
            None
        )
        
        if not lang_config:
            logger.warning(f"未找到语言配置: {language}")
            return files
        
        extensions = set(lang_config.get('extensions', []))
        
        # 遍历目录
        for root, dirs, filenames in os.walk(project_path):
            # 过滤排除的目录
            dirs[:] = [d for d in dirs if d not in self.excluded_dirs]
            
            # 收集匹配的文件
            for filename in filenames:
                file_ext = Path(filename).suffix
                if file_ext in extensions:
                    file_path = Path(root) / filename
                    files.append(file_path)
        
        logger.info(f"找到 {len(files)} 个 {language} 源文件")
        return files
    
    async def _analyze_file(
        self,
        file_path: Path,
        language: SupportedLanguage
    ) -> FileInfo:
        """分析单个文件"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            lines = content.count('\n') + 1
            size = file_path.stat().st_size
            
            # 使用对应语言的解析器
            parser = self._get_parser(language)
            parsed_info = parser.parse(content) if parser else {}
            
            return FileInfo(
                path=str(file_path),
                language=language.value,
                size=size,
                lines=lines,
                classes=parsed_info.get('classes', []),
                functions=parsed_info.get('functions', []),
                imports=parsed_info.get('imports', [])
            )
            
        except Exception as e:
            logger.warning(f"文件分析失败 {file_path}: {str(e)}")
            return FileInfo(
                path=str(file_path),
                language=language.value,
                size=0,
                lines=0
            )
    
    def _get_parser(self, language: SupportedLanguage):
        """获取语言解析器"""
        # 导入对应的解析器
        try:
            if language == SupportedLanguage.JAVA:
                from core.parsers.java_parser import JavaParser
                return JavaParser()
            elif language == SupportedLanguage.PYTHON:
                from core.parsers.python_parser import PythonParser
                return PythonParser()
            elif language == SupportedLanguage.JAVASCRIPT:
                from core.parsers.javascript_parser import JavaScriptParser
                return JavaScriptParser()
            # 添加更多语言...
        except ImportError as e:
            logger.warning(f"解析器导入失败 {language}: {str(e)}")
        
        return None
    
    def _analyze_structure(
        self,
        project_path: Path,
        language: SupportedLanguage
    ) -> Dict[str, Any]:
        """分析项目目录结构"""
        structure = {
            "root": str(project_path),
            "directories": [],
            "build_system": self._detect_build_system(project_path, language)
        }
        
        # 构建目录树
        for item in project_path.iterdir():
            if item.is_dir() and item.name not in self.excluded_dirs:
                structure["directories"].append(item.name)
        
        return structure
    
    def _detect_build_system(
        self,
        project_path: Path,
        language: SupportedLanguage
    ) -> str:
        """检测构建系统"""
        if language == SupportedLanguage.JAVA:
            if (project_path / "pom.xml").exists():
                return "maven"
            elif (project_path / "build.gradle").exists():
                return "gradle"
        elif language == SupportedLanguage.PYTHON:
            if (project_path / "setup.py").exists():
                return "setuptools"
            elif (project_path / "pyproject.toml").exists():
                return "poetry"
        elif language == SupportedLanguage.JAVASCRIPT:
            if (project_path / "package.json").exists():
                return "npm"
        elif language == SupportedLanguage.GO:
            if (project_path / "go.mod").exists():
                return "go-modules"
        
        return "unknown"
    
    async def _analyze_dependencies(
        self,
        project_path: Path,
        language: SupportedLanguage
    ) -> Dict[str, str]:
        """分析项目依赖"""
        dependencies = {}
        
        try:
            if language == SupportedLanguage.JAVA:
                # 解析 pom.xml 或 build.gradle
                pom_file = project_path / "pom.xml"
                if pom_file.exists():
                    dependencies = self._parse_maven_dependencies(pom_file)
                    
            elif language == SupportedLanguage.PYTHON:
                # 解析 requirements.txt
                req_file = project_path / "requirements.txt"
                if req_file.exists():
                    dependencies = self._parse_requirements(req_file)
                    
            elif language == SupportedLanguage.JAVASCRIPT:
                # 解析 package.json
                pkg_file = project_path / "package.json"
                if pkg_file.exists():
                    dependencies = self._parse_package_json(pkg_file)
                    
        except Exception as e:
            logger.warning(f"依赖分析失败: {str(e)}")
        
        return dependencies
    
    def _parse_requirements(self, req_file: Path) -> Dict[str, str]:
        """解析 Python requirements.txt"""
        deps = {}
        with open(req_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '==' in line:
                        name, version = line.split('==', 1)
                        deps[name.strip()] = version.strip()
                    else:
                        deps[line] = "latest"
        return deps
    
    def _parse_package_json(self, pkg_file: Path) -> Dict[str, str]:
        """解析 JavaScript package.json"""
        import json
        with open(pkg_file, 'r') as f:
            pkg_data = json.load(f)
        
        deps = {}
        deps.update(pkg_data.get('dependencies', {}))
        deps.update(pkg_data.get('devDependencies', {}))
        return deps
    
    def _parse_maven_dependencies(self, pom_file: Path) -> Dict[str, str]:
        """解析 Maven pom.xml (简化版)"""
        # 这里可以使用 XML 解析库
        # 简化实现
        return {}

