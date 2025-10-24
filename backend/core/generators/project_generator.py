"""
项目生成器
根据翻译结果生成完整的目标语言项目
"""

import os
import shutil
from pathlib import Path
from typing import List, Dict
import yaml
from loguru import logger

from models.schemas import TranslationResult, SupportedLanguage


class ProjectGenerator:
    """项目生成器"""
    
    def __init__(self):
        # 加载配置
        config_path = Path(__file__).parent.parent.parent.parent / "config.yaml"
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
    
    async def generate(
        self,
        translation_results: List[TranslationResult],
        output_dir: Path,
        target_language: SupportedLanguage
    ):
        """
        生成目标项目
        
        Args:
            translation_results: 翻译结果列表
            output_dir: 输出目录
            target_language: 目标语言
        """
        logger.info(f"开始生成 {target_language} 项目，输出目录: {output_dir}")
        
        # 创建输出目录
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 1. 创建项目结构
        await self._create_project_structure(output_dir, target_language)
        
        # 2. 写入翻译后的代码
        for result in translation_results:
            if result.success:
                await self._write_translated_file(
                    output_dir,
                    result,
                    target_language
                )
        
        # 3. 生成配置文件
        await self._generate_config_files(output_dir, target_language)
        
        # 4. 生成依赖文件
        await self._generate_dependency_files(output_dir, target_language)
        
        # 5. 生成 README
        await self._generate_readme(output_dir, target_language, len(translation_results))
        
        logger.info(f"项目生成完成: {output_dir}")
    
    async def _create_project_structure(
        self,
        output_dir: Path,
        language: SupportedLanguage
    ):
        """创建项目目录结构"""
        templates = self.config.get('project_templates', {})
        lang_template = templates.get(language.value, {})
        
        # 创建目录
        for dir_path in lang_template.get('structure', []):
            (output_dir / dir_path).mkdir(parents=True, exist_ok=True)
    
    async def _write_translated_file(
        self,
        output_dir: Path,
        result: TranslationResult,
        language: SupportedLanguage
    ):
        """写入翻译后的文件"""
        # 计算相对路径
        source_path = Path(result.source_file)
        
        # 生成目标路径
        if language == SupportedLanguage.PYTHON:
            target_path = output_dir / "src" / Path(result.target_file).name
        elif language == SupportedLanguage.JAVA:
            target_path = output_dir / "src" / "main" / "java" / Path(result.target_file).name
        elif language == SupportedLanguage.JAVASCRIPT:
            target_path = output_dir / "src" / Path(result.target_file).name
        else:
            target_path = output_dir / Path(result.target_file).name
        
        # 确保目录存在
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 写入文件
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(result.translated_code)
        
        logger.debug(f"已写入: {target_path}")
    
    async def _generate_config_files(
        self,
        output_dir: Path,
        language: SupportedLanguage
    ):
        """生成配置文件"""
        if language == SupportedLanguage.PYTHON:
            # 生成 .env 示例
            env_content = "# Environment Variables\nDEBUG=true\n"
            (output_dir / ".env.example").write_text(env_content)
            
        elif language == SupportedLanguage.JAVA:
            # 生成 application.properties
            props_content = "# Application Properties\nserver.port=8080\n"
            config_dir = output_dir / "src" / "main" / "resources"
            config_dir.mkdir(parents=True, exist_ok=True)
            (config_dir / "application.properties").write_text(props_content)
    
    async def _generate_dependency_files(
        self,
        output_dir: Path,
        language: SupportedLanguage
    ):
        """生成依赖管理文件"""
        if language == SupportedLanguage.PYTHON:
            # requirements.txt
            requirements = "# Python Dependencies\n# Add your dependencies here\n"
            (output_dir / "requirements.txt").write_text(requirements)
            
            # setup.py
            setup_content = '''from setuptools import setup, find_packages

setup(
    name="translated_project",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        # Add dependencies
    ],
)
'''
            (output_dir / "setup.py").write_text(setup_content)
            
        elif language == SupportedLanguage.JAVA:
            # pom.xml (Maven)
            pom_content = '''<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    
    <groupId>com.translated</groupId>
    <artifactId>translated-project</artifactId>
    <version>1.0.0</version>
    
    <properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
    </properties>
    
    <dependencies>
        <!-- Add dependencies -->
    </dependencies>
</project>
'''
            (output_dir / "pom.xml").write_text(pom_content)
            
        elif language in [SupportedLanguage.JAVASCRIPT, SupportedLanguage.TYPESCRIPT]:
            # package.json
            package_json = '''{
  "name": "translated-project",
  "version": "1.0.0",
  "description": "Translated project",
  "main": "src/index.js",
  "scripts": {
    "start": "node src/index.js",
    "test": "echo \\"No tests specified\\""
  },
  "dependencies": {}
}
'''
            (output_dir / "package.json").write_text(package_json)
            
        elif language == SupportedLanguage.GO:
            # go.mod
            go_mod = '''module translated-project

go 1.21

require (
    // Add dependencies
)
'''
            (output_dir / "go.mod").write_text(go_mod)
    
    async def _generate_readme(
        self,
        output_dir: Path,
        language: SupportedLanguage,
        file_count: int
    ):
        """生成 README 文件"""
        readme_content = f'''# Translated Project

This project was automatically translated to {language.value.upper()}.

## 📊 Statistics

- **Language**: {language.value}
- **Files**: {file_count}
- **Generated by**: AI Code Migration Platform

## 🚀 Getting Started

### Prerequisites

'''
        
        if language == SupportedLanguage.PYTHON:
            readme_content += '''- Python 3.8+

### Installation

```bash
pip install -r requirements.txt
```

### Running

```bash
python src/main.py
```
'''
        elif language == SupportedLanguage.JAVA:
            readme_content += '''- Java 17+
- Maven

### Build

```bash
mvn clean install
```

### Run

```bash
mvn exec:java
```
'''
        elif language in [SupportedLanguage.JAVASCRIPT, SupportedLanguage.TYPESCRIPT]:
            readme_content += '''- Node.js 16+

### Installation

```bash
npm install
```

### Run

```bash
npm start
```
'''
        
        readme_content += '''
## ⚠️ Note

This is an AI-generated translation. Please review and test the code before using in production.

## 📝 TODO

- [ ] Review translated code
- [ ] Add tests
- [ ] Update dependencies
- [ ] Add documentation
'''
        
        (output_dir / "README.md").write_text(readme_content)

