"""
Framework Detector / 框架检测器

Automatically detects which framework is used in the source code.
自动检测源代码中使用的框架。

Supports / 支持:
- Java: Spring Boot, Spring MVC, Quarkus, Micronaut
- Python: Django, Flask, FastAPI, Tornado
- JavaScript/TypeScript: Express, NestJS, Koa, Fastify
- Go: Gin, Echo, Fiber, Beego
- Ruby: Rails, Sinatra
- PHP: Laravel, Symfony, CodeIgniter
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Any
from loguru import logger


class FrameworkDetector:
    """
    Framework Detector / 框架检测器
    
    Analyzes project files to detect the framework being used.
    分析项目文件以检测正在使用的框架。
    """
    
    # Framework detection patterns / 框架检测模式
    FRAMEWORK_PATTERNS = {
        # Java Frameworks
        "spring-boot": {
            "files": ["pom.xml", "build.gradle"],
            "patterns": [
                r"spring-boot-starter",
                r"@SpringBootApplication",
                r"org\.springframework\.boot"
            ],
            "language": "java",
            "type": "web",
            "version_pattern": r"spring-boot-starter-parent.*?(\d+\.\d+\.\d+)"
        },
        "spring-mvc": {
            "files": ["pom.xml", "build.gradle", "web.xml"],
            "patterns": [
                r"spring-webmvc",
                r"@Controller",
                r"DispatcherServlet"
            ],
            "language": "java",
            "type": "web"
        },
        "quarkus": {
            "files": ["pom.xml", "build.gradle"],
            "patterns": [
                r"quarkus-universe-bom",
                r"io\.quarkus",
                r"@QuarkusApplication"
            ],
            "language": "java",
            "type": "web"
        },
        
        # Python Frameworks
        "django": {
            "files": ["requirements.txt", "Pipfile", "pyproject.toml", "manage.py"],
            "patterns": [
                r"django==",
                r"from django",
                r"INSTALLED_APPS",
                r"settings\.py"
            ],
            "language": "python",
            "type": "web",
            "version_pattern": r"django==(\d+\.\d+\.\d+)"
        },
        "flask": {
            "files": ["requirements.txt", "Pipfile", "app.py"],
            "patterns": [
                r"flask==",
                r"from flask import",
                r"@app\.route",
                r"Flask\(__name__\)"
            ],
            "language": "python",
            "type": "web",
            "version_pattern": r"flask==(\d+\.\d+\.\d+)"
        },
        "fastapi": {
            "files": ["requirements.txt", "Pipfile", "main.py"],
            "patterns": [
                r"fastapi==",
                r"from fastapi import",
                r"@app\.get",
                r"FastAPI\("
            ],
            "language": "python",
            "type": "web",
            "version_pattern": r"fastapi==(\d+\.\d+\.\d+)"
        },
        
        # JavaScript/TypeScript Frameworks
        "express": {
            "files": ["package.json"],
            "patterns": [
                r'"express"',
                r"require\('express'\)",
                r"import.*express",
                r"app\.listen"
            ],
            "language": "javascript",
            "type": "web",
            "version_pattern": r'"express":\s*"[\^~]?(\d+\.\d+\.\d+)"'
        },
        "nestjs": {
            "files": ["package.json"],
            "patterns": [
                r'"@nestjs/core"',
                r"@Module\(",
                r"@Controller\(",
                r"NestFactory"
            ],
            "language": "typescript",
            "type": "web"
        },
        "nextjs": {
            "files": ["package.json", "next.config.js"],
            "patterns": [
                r'"next"',
                r"import.*next",
                r"export default.*Page"
            ],
            "language": "typescript",
            "type": "frontend"
        },
        "react": {
            "files": ["package.json"],
            "patterns": [
                r'"react"',
                r"import React",
                r"from 'react'"
            ],
            "language": "javascript",
            "type": "frontend"
        },
        "vue": {
            "files": ["package.json"],
            "patterns": [
                r'"vue"',
                r"import Vue",
                r"createApp"
            ],
            "language": "javascript",
            "type": "frontend"
        },
        
        # Go Frameworks
        "gin": {
            "files": ["go.mod", "main.go"],
            "patterns": [
                r"github\.com/gin-gonic/gin",
                r"gin\.Default\(",
                r"router\.GET"
            ],
            "language": "go",
            "type": "web"
        },
        "echo": {
            "files": ["go.mod"],
            "patterns": [
                r"github\.com/labstack/echo",
                r"echo\.New\(",
                r"e\.GET"
            ],
            "language": "go",
            "type": "web"
        },
        
        # Database ORMs
        "hibernate": {
            "files": ["pom.xml", "build.gradle"],
            "patterns": [
                r"hibernate-core",
                r"@Entity",
                r"javax\.persistence"
            ],
            "language": "java",
            "type": "orm"
        },
        "sqlalchemy": {
            "files": ["requirements.txt"],
            "patterns": [
                r"sqlalchemy==",
                r"from sqlalchemy import",
                r"declarative_base"
            ],
            "language": "python",
            "type": "orm"
        },
        "typeorm": {
            "files": ["package.json"],
            "patterns": [
                r'"typeorm"',
                r"@Entity\(",
                r"createConnection"
            ],
            "language": "typescript",
            "type": "orm"
        }
    }
    
    def __init__(self):
        """Initialize framework detector / 初始化框架检测器"""
        self.detected_frameworks = []
    
    def detect_frameworks(self, project_path: Path) -> List[Dict[str, Any]]:
        """
        Detect all frameworks used in the project / 检测项目中使用的所有框架
        
        Args:
            project_path: Path to the project directory / 项目目录路径
            
        Returns:
            List of detected frameworks with metadata / 检测到的框架列表及元数据
        """
        detected = []
        
        logger.info(f"🔍 开始检测框架: {project_path}")
        
        for framework_name, config in self.FRAMEWORK_PATTERNS.items():
            if self._check_framework(project_path, framework_name, config):
                framework_info = {
                    "name": framework_name,
                    "language": config["language"],
                    "type": config["type"],
                    "version": self._detect_version(project_path, config),
                    "confidence": self._calculate_confidence(project_path, config)
                }
                detected.append(framework_info)
                logger.info(f"✅ 检测到框架: {framework_name} ({config['language']})")
        
        # Sort by confidence / 按置信度排序
        detected.sort(key=lambda x: x["confidence"], reverse=True)
        
        self.detected_frameworks = detected
        return detected
    
    def _check_framework(
        self,
        project_path: Path,
        framework_name: str,
        config: Dict[str, Any]
    ) -> bool:
        """
        Check if a specific framework is used / 检查是否使用特定框架
        
        Args:
            project_path: Project path / 项目路径
            framework_name: Framework name / 框架名称
            config: Framework configuration / 框架配置
            
        Returns:
            bool: True if framework is detected / 如果检测到框架则返回True
        """
        matches = 0
        required_matches = 2  # Need at least 2 pattern matches / 至少需要2个模式匹配
        
        # Check for required files / 检查必需文件
        for filename in config.get("files", []):
            file_path = self._find_file(project_path, filename)
            if file_path:
                matches += 1
                
                # Check patterns in the file / 检查文件中的模式
                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    for pattern in config.get("patterns", []):
                        if re.search(pattern, content, re.IGNORECASE):
                            matches += 1
                except Exception as e:
                    logger.warning(f"⚠️ 读取文件失败 {file_path}: {e}")
        
        return matches >= required_matches
    
    def _find_file(self, project_path: Path, filename: str) -> Optional[Path]:
        """
        Find a file in the project / 在项目中查找文件
        
        Args:
            project_path: Project path / 项目路径
            filename: File name to find / 要查找的文件名
            
        Returns:
            Path to file if found, None otherwise / 如果找到则返回文件路径，否则返回None
        """
        # First check root directory / 首先检查根目录
        root_file = project_path / filename
        if root_file.exists():
            return root_file
        
        # Search in subdirectories (up to 3 levels) / 在子目录中搜索（最多3层）
        for path in project_path.rglob(filename):
            if path.is_file() and len(path.relative_to(project_path).parts) <= 3:
                return path
        
        return None
    
    def _detect_version(self, project_path: Path, config: Dict[str, Any]) -> Optional[str]:
        """
        Detect framework version / 检测框架版本
        
        Args:
            project_path: Project path / 项目路径
            config: Framework configuration / 框架配置
            
        Returns:
            Version string if found / 如果找到则返回版本字符串
        """
        version_pattern = config.get("version_pattern")
        if not version_pattern:
            return None
        
        for filename in config.get("files", []):
            file_path = self._find_file(project_path, filename)
            if file_path:
                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    match = re.search(version_pattern, content)
                    if match:
                        return match.group(1)
                except Exception:
                    pass
        
        return None
    
    def _calculate_confidence(self, project_path: Path, config: Dict[str, Any]) -> float:
        """
        Calculate detection confidence / 计算检测置信度
        
        Args:
            project_path: Project path / 项目路径
            config: Framework configuration / 框架配置
            
        Returns:
            Confidence score (0.0 to 1.0) / 置信度分数（0.0到1.0）
        """
        total_checks = len(config.get("files", [])) + len(config.get("patterns", []))
        matches = 0
        
        for filename in config.get("files", []):
            if self._find_file(project_path, filename):
                matches += 1
        
        for filename in config.get("files", []):
            file_path = self._find_file(project_path, filename)
            if file_path:
                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    for pattern in config.get("patterns", []):
                        if re.search(pattern, content, re.IGNORECASE):
                            matches += 1
                except Exception:
                    pass
        
        return min(matches / total_checks, 1.0) if total_checks > 0 else 0.0
    
    def get_primary_framework(self) -> Optional[Dict[str, Any]]:
        """
        Get the primary (most confident) framework / 获取主要（最有信心的）框架
        
        Returns:
            Primary framework info / 主要框架信息
        """
        return self.detected_frameworks[0] if self.detected_frameworks else None
    
    def get_frameworks_by_type(self, framework_type: str) -> List[Dict[str, Any]]:
        """
        Get frameworks by type (web, orm, frontend, etc.) / 按类型获取框架
        
        Args:
            framework_type: Type of framework / 框架类型
            
        Returns:
            List of frameworks of the specified type / 指定类型的框架列表
        """
        return [
            fw for fw in self.detected_frameworks
            if fw["type"] == framework_type
        ]

