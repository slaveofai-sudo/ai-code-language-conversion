"""
Learning Document Generator / 学习文档生成器

Generates comprehensive learning documentation for code projects.
为代码项目生成全面的学习文档。

Features / 功能:
- Learning roadmap / 学习路线图
- Difficulty analysis / 难度分析
- Design pattern explanation / 设计模式解释
- Implementation flow / 实现流程
- Detailed code analysis / 详细代码分析
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
from loguru import logger
from datetime import datetime
import json


class LearningDocGenerator:
    """
    Learning Document Generator / 学习文档生成器
    
    Generates detailed learning documentation based on code inspection results.
    基于代码检测结果生成详细的学习文档。
    """
    
    def __init__(self):
        self.difficulty_descriptions = {
            "easy": {
                "zh": "初级 - 适合编程新手",
                "en": "Beginner - Suitable for programming newcomers",
                "learning_time": "1-2 天",
                "prerequisites": "基本编程概念"
            },
            "medium": {
                "zh": "中级 - 需要一定编程经验",
                "en": "Intermediate - Requires some programming experience",
                "learning_time": "3-5 天",
                "prerequisites": "熟悉基本语法和数据结构"
            },
            "hard": {
                "zh": "高级 - 需要扎实的编程基础",
                "en": "Advanced - Requires solid programming foundation",
                "learning_time": "1-2 周",
                "prerequisites": "熟悉设计模式和高级概念"
            },
            "expert": {
                "zh": "专家级 - 需要丰富的实战经验",
                "en": "Expert - Requires extensive practical experience",
                "learning_time": "2-4 周",
                "prerequisites": "深入理解架构和最佳实践"
            }
        }
        
        self.pattern_explanations = {
            "singleton": {
                "zh": "单例模式 - 确保一个类只有一个实例",
                "en": "Singleton Pattern - Ensures a class has only one instance",
                "use_case": "全局配置、数据库连接池",
                "difficulty": "easy"
            },
            "factory": {
                "zh": "工厂模式 - 创建对象的接口",
                "en": "Factory Pattern - Interface for creating objects",
                "use_case": "对象创建逻辑复杂时",
                "difficulty": "medium"
            },
            "observer": {
                "zh": "观察者模式 - 定义对象间的一对多依赖",
                "en": "Observer Pattern - Defines one-to-many dependency",
                "use_case": "事件处理、消息订阅",
                "difficulty": "medium"
            },
            "strategy": {
                "zh": "策略模式 - 定义算法族并可互换",
                "en": "Strategy Pattern - Defines family of algorithms",
                "use_case": "不同算法实现可替换",
                "difficulty": "medium"
            },
            "decorator": {
                "zh": "装饰器模式 - 动态添加功能",
                "en": "Decorator Pattern - Adds functionality dynamically",
                "use_case": "在不修改原代码情况下扩展功能",
                "difficulty": "medium"
            },
            "repository": {
                "zh": "仓储模式 - 封装数据访问逻辑",
                "en": "Repository Pattern - Encapsulates data access",
                "use_case": "数据持久化层",
                "difficulty": "medium"
            },
            "mvc": {
                "zh": "MVC模式 - 模型-视图-控制器分离",
                "en": "MVC Pattern - Model-View-Controller separation",
                "use_case": "Web应用架构",
                "difficulty": "hard"
            }
        }
    
    def generate_learning_doc(
        self,
        inspection_results: Dict[str, Any],
        project_path: Path,
        output_format: str = "markdown"
    ) -> str:
        """
        Generate comprehensive learning documentation.
        生成全面的学习文档。
        
        Args:
            inspection_results: Results from CodeInspector.
                               代码检测器的结果。
            project_path: Path to the project.
                         项目路径。
            output_format: Output format (markdown, html, json).
                          输出格式。
        
        Returns:
            Generated documentation string.
            生成的文档字符串。
        """
        logger.info(f"开始生成学习文档: {project_path}")
        
        if output_format == "markdown":
            return self._generate_markdown_doc(inspection_results, project_path)
        elif output_format == "json":
            return json.dumps(self._generate_json_doc(inspection_results, project_path), indent=2, ensure_ascii=False)
        else:
            raise ValueError(f"Unsupported output format: {output_format}")
    
    def _generate_markdown_doc(self, results: Dict[str, Any], project_path: Path) -> str:
        """Generate Markdown format documentation"""
        project_metrics = results['project_metrics']
        file_metrics = results['file_metrics']
        architecture = results['architecture']
        tech_stack = results['tech_stack']
        summary = results['summary']
        
        doc = []
        
        # Title and metadata
        # 标题和元数据
        doc.append(f"# 📚 {project_metrics['project_name']} - 学习文档")
        doc.append("")
        doc.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        doc.append(f"**项目路径**: `{project_path}`")
        doc.append("")
        doc.append("---")
        doc.append("")
        
        # Table of Contents
        # 目录
        doc.append("## 📖 目录")
        doc.append("")
        doc.append("1. [项目概览](#项目概览)")
        doc.append("2. [学习路线图](#学习路线图)")
        doc.append("3. [难度分析](#难度分析)")
        doc.append("4. [技术栈分析](#技术栈分析)")
        doc.append("5. [架构设计](#架构设计)")
        doc.append("6. [设计模式](#设计模式)")
        doc.append("7. [代码复杂度](#代码复杂度)")
        doc.append("8. [文件结构分析](#文件结构分析)")
        doc.append("9. [学习建议](#学习建议)")
        doc.append("10. [代码质量报告](#代码质量报告)")
        doc.append("")
        doc.append("---")
        doc.append("")
        
        # 1. Project Overview
        # 项目概览
        doc.append("## 🎯 项目概览")
        doc.append("")
        doc.append("### 基本信息")
        doc.append("")
        doc.append(f"- **项目名称**: {project_metrics['project_name']}")
        doc.append(f"- **代码文件数**: {project_metrics['total_files']} 个")
        doc.append(f"- **代码总行数**: {project_metrics['total_lines']:,} 行")
        doc.append(f"- **函数数量**: {project_metrics['total_functions']} 个")
        doc.append(f"- **类数量**: {project_metrics['total_classes']} 个")
        doc.append(f"- **整体难度**: {project_metrics['overall_difficulty'].upper()}")
        doc.append(f"- **健康分数**: {summary['health_score']}/100 {'🟢' if summary['health_score'] >= 80 else '🟡' if summary['health_score'] >= 60 else '🔴'}")
        doc.append("")
        
        # Language distribution
        # 语言分布
        doc.append("### 编程语言分布")
        doc.append("")
        doc.append("| 语言 | 代码行数 | 占比 |")
        doc.append("|------|---------|------|")
        
        total_lines = sum(project_metrics['languages'].values())
        for lang, lines in sorted(project_metrics['languages'].items(), key=lambda x: x[1], reverse=True):
            percentage = (lines / total_lines * 100) if total_lines > 0 else 0
            doc.append(f"| {lang.title()} | {lines:,} | {percentage:.1f}% |")
        
        doc.append("")
        doc.append("---")
        doc.append("")
        
        # 2. Learning Roadmap
        # 学习路线图
        doc.append("## 🗺️ 学习路线图")
        doc.append("")
        doc.append(self._generate_learning_roadmap(project_metrics, file_metrics))
        doc.append("")
        doc.append("---")
        doc.append("")
        
        # 3. Difficulty Analysis
        # 难度分析
        doc.append("## 📊 难度分析")
        doc.append("")
        doc.append(self._generate_difficulty_analysis(project_metrics, file_metrics))
        doc.append("")
        doc.append("---")
        doc.append("")
        
        # 4. Tech Stack
        # 技术栈
        doc.append("## 🛠️ 技术栈分析")
        doc.append("")
        doc.append("### 使用的技术")
        doc.append("")
        
        if tech_stack:
            for tech in tech_stack:
                doc.append(f"- ✅ **{tech}**")
        else:
            doc.append("- ℹ️ 未检测到明确的技术栈标识")
        
        doc.append("")
        doc.append("### 学习资源推荐")
        doc.append("")
        doc.append(self._generate_tech_resources(tech_stack))
        doc.append("")
        doc.append("---")
        doc.append("")
        
        # 5. Architecture Design
        # 架构设计
        doc.append("## 🏛️ 架构设计")
        doc.append("")
        doc.append(self._generate_architecture_analysis(architecture, file_metrics))
        doc.append("")
        doc.append("---")
        doc.append("")
        
        # 6. Design Patterns
        # 设计模式
        doc.append("## 🎨 设计模式")
        doc.append("")
        doc.append(self._generate_pattern_analysis(file_metrics))
        doc.append("")
        doc.append("---")
        doc.append("")
        
        # 7. Complexity Analysis
        # 复杂度分析
        doc.append("## 🧮 代码复杂度")
        doc.append("")
        doc.append(self._generate_complexity_analysis(project_metrics, file_metrics))
        doc.append("")
        doc.append("---")
        doc.append("")
        
        # 8. File Structure Analysis
        # 文件结构分析
        doc.append("## 📁 文件结构分析")
        doc.append("")
        doc.append(self._generate_file_analysis(file_metrics))
        doc.append("")
        doc.append("---")
        doc.append("")
        
        # 9. Learning Recommendations
        # 学习建议
        doc.append("## 💡 学习建议")
        doc.append("")
        doc.append(self._generate_learning_recommendations(project_metrics, file_metrics, summary))
        doc.append("")
        doc.append("---")
        doc.append("")
        
        # 10. Code Quality Report
        # 代码质量报告
        doc.append("## 🔍 代码质量报告")
        doc.append("")
        doc.append(self._generate_quality_report(file_metrics, summary))
        doc.append("")
        doc.append("---")
        doc.append("")
        
        # Footer
        # 页脚
        doc.append("## 📝 附录")
        doc.append("")
        doc.append("### 术语解释")
        doc.append("")
        doc.append("- **圈复杂度 (Cyclomatic Complexity)**: 衡量代码分支和循环的数量，值越高代码越复杂")
        doc.append("- **认知复杂度 (Cognitive Complexity)**: 衡量代码理解的难度，考虑嵌套和控制流")
        doc.append("- **可维护性指数 (Maintainability Index)**: 0-100的分数，表示代码的可维护性")
        doc.append("- **代码异味 (Code Smell)**: 代码中可能存在的设计或实现问题")
        doc.append("")
        doc.append("### 相关链接")
        doc.append("")
        doc.append("- [Clean Code原则](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)")
        doc.append("- [设计模式](https://refactoring.guru/design-patterns)")
        doc.append("- [代码复杂度](https://en.wikipedia.org/wiki/Cyclomatic_complexity)")
        doc.append("")
        doc.append("---")
        doc.append("")
        doc.append(f"*📅 文档生成于 {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}*")
        doc.append("")
        doc.append("*🤖 由 AI Code Migration Platform 自动生成*")
        
        return "\n".join(doc)
    
    def _generate_learning_roadmap(
        self,
        project_metrics: Dict[str, Any],
        file_metrics: List[Dict[str, Any]]
    ) -> str:
        """Generate learning roadmap"""
        difficulty = project_metrics['overall_difficulty']
        difficulty_info = self.difficulty_descriptions.get(difficulty, self.difficulty_descriptions['medium'])
        
        roadmap = []
        
        roadmap.append(f"### 推荐学习时间")
        roadmap.append("")
        roadmap.append(f"**{difficulty_info['learning_time']}**")
        roadmap.append("")
        roadmap.append(f"### 前置知识要求")
        roadmap.append("")
        roadmap.append(f"- {difficulty_info['prerequisites']}")
        roadmap.append("")
        
        roadmap.append("### 学习阶段")
        roadmap.append("")
        roadmap.append("#### 阶段1: 项目结构理解 (20%)")
        roadmap.append("")
        roadmap.append("- 📂 了解项目目录结构")
        roadmap.append("- 📋 阅读主要配置文件")
        roadmap.append("- 🔗 理解模块间的依赖关系")
        roadmap.append("")
        roadmap.append("**建议时长**: 1-2小时")
        roadmap.append("")
        
        roadmap.append("#### 阶段2: 核心功能学习 (40%)")
        roadmap.append("")
        
        # Find most important files
        # 找到最重要的文件
        important_files = sorted(
            file_metrics,
            key=lambda f: f['num_functions'] + f['num_classes'],
            reverse=True
        )[:5]
        
        roadmap.append("**重点学习文件**:")
        roadmap.append("")
        for i, f in enumerate(important_files, 1):
            file_name = Path(f['file_path']).name
            roadmap.append(f"{i}. `{file_name}` - {f['num_functions']} 个函数, {f['num_classes']} 个类")
        
        roadmap.append("")
        roadmap.append("**建议时长**: 根据难度而定")
        roadmap.append("")
        
        roadmap.append("#### 阶段3: 设计模式理解 (20%)")
        roadmap.append("")
        roadmap.append("- 🎨 识别代码中使用的设计模式")
        roadmap.append("- 🔄 理解模式的应用场景")
        roadmap.append("- 💡 学习最佳实践")
        roadmap.append("")
        roadmap.append("**建议时长**: 2-4小时")
        roadmap.append("")
        
        roadmap.append("#### 阶段4: 实践与优化 (20%)")
        roadmap.append("")
        roadmap.append("- ✍️ 尝试修改和扩展功能")
        roadmap.append("- 🧪 编写单元测试")
        roadmap.append("- 🔧 重构和优化代码")
        roadmap.append("")
        roadmap.append("**建议时长**: 根据项目复杂度而定")
        
        return "\n".join(roadmap)
    
    def _generate_difficulty_analysis(
        self,
        project_metrics: Dict[str, Any],
        file_metrics: List[Dict[str, Any]]
    ) -> str:
        """Generate difficulty analysis"""
        analysis = []
        
        difficulty = project_metrics['overall_difficulty']
        avg_complexity = project_metrics['avg_complexity']
        
        analysis.append(f"### 整体难度等级: **{difficulty.upper()}**")
        analysis.append("")
        
        difficulty_info = self.difficulty_descriptions.get(difficulty, self.difficulty_descriptions['medium'])
        analysis.append(f"- **中文说明**: {difficulty_info['zh']}")
        analysis.append(f"- **English**: {difficulty_info['en']}")
        analysis.append("")
        
        analysis.append("### 难度构成分析")
        analysis.append("")
        analysis.append("| 维度 | 评分 | 说明 |")
        analysis.append("|------|------|------|")
        
        # Code volume / 代码量
        code_volume_score = min(10, project_metrics['total_lines'] / 1000)
        analysis.append(f"| 代码量 | {code_volume_score:.1f}/10 | {project_metrics['total_lines']:,} 行代码 |")
        
        # Complexity / 复杂度
        complexity_score = min(10, avg_complexity)
        analysis.append(f"| 复杂度 | {complexity_score:.1f}/10 | 平均圈复杂度 {avg_complexity:.1f} |")
        
        # Architecture / 架构
        arch_score = 5.0 + (project_metrics['total_classes'] / 20)
        analysis.append(f"| 架构设计 | {min(10, arch_score):.1f}/10 | {project_metrics['total_classes']} 个类 |")
        
        # Dependencies / 依赖
        dep_score = 5.0
        analysis.append(f"| 依赖管理 | {dep_score:.1f}/10 | 中等复杂度 |")
        
        analysis.append("")
        
        # Difficulty distribution
        # 难度分布
        analysis.append("### 文件难度分布")
        analysis.append("")
        
        # Count files by difficulty (we need to add this to file metrics)
        # 按难度统计文件（需要在文件指标中添加）
        easy_count = sum(1 for f in file_metrics if f['complexity_score'] <= 5)
        medium_count = sum(1 for f in file_metrics if 5 < f['complexity_score'] <= 10)
        hard_count = sum(1 for f in file_metrics if 10 < f['complexity_score'] <= 15)
        expert_count = sum(1 for f in file_metrics if f['complexity_score'] > 15)
        
        total = len(file_metrics)
        
        analysis.append("```")
        analysis.append(f"简单 (Easy):    {'█' * int(easy_count / total * 20) if total > 0 else ''} {easy_count} 个文件")
        analysis.append(f"中等 (Medium):  {'█' * int(medium_count / total * 20) if total > 0 else ''} {medium_count} 个文件")
        analysis.append(f"困难 (Hard):    {'█' * int(hard_count / total * 20) if total > 0 else ''} {hard_count} 个文件")
        analysis.append(f"专家 (Expert):  {'█' * int(expert_count / total * 20) if total > 0 else ''} {expert_count} 个文件")
        analysis.append("```")
        
        return "\n".join(analysis)
    
    def _generate_tech_resources(self, tech_stack: List[str]) -> str:
        """Generate technology learning resources"""
        resources = []
        
        resource_map = {
            "Python/pip": "- [Python官方文档](https://docs.python.org/zh-cn/3/)\n- [Python教程](https://www.runoob.com/python3/python3-tutorial.html)",
            "Node.js/npm": "- [Node.js官方文档](https://nodejs.org/zh-cn/docs/)\n- [JavaScript教程](https://javascript.info/)",
            "Java/Maven": "- [Java官方文档](https://docs.oracle.com/en/java/)\n- [Maven教程](https://maven.apache.org/guides/)",
            "Java/Gradle": "- [Gradle官方文档](https://docs.gradle.org/)\n- [Gradle教程](https://www.tutorialspoint.com/gradle/index.htm)",
            "Go": "- [Go官方文档](https://go.dev/doc/)\n- [Go语言之旅](https://tour.go-zh.org/)",
            "Rust/Cargo": "- [Rust官方文档](https://www.rust-lang.org/zh-CN/learn)\n- [Rust程序设计语言](https://kaisery.github.io/trpl-zh-cn/)"
        }
        
        for tech in tech_stack:
            if tech in resource_map:
                resources.append(f"**{tech}**:")
                resources.append(resource_map[tech])
                resources.append("")
        
        if not resources:
            resources.append("- 通用编程资源: [GitHub](https://github.com)")
        
        return "\n".join(resources)
    
    def _generate_architecture_analysis(
        self,
        architecture: Dict[str, Any],
        file_metrics: List[Dict[str, Any]]
    ) -> str:
        """Generate architecture analysis"""
        analysis = []
        
        patterns = architecture.get('patterns', [])
        structure = architecture.get('structure', 'simple')
        
        analysis.append(f"### 架构类型: **{structure.upper()}**")
        analysis.append("")
        
        if patterns:
            analysis.append("### 检测到的架构模式")
            analysis.append("")
            for pattern in patterns:
                analysis.append(f"- ✅ **{pattern}**")
            analysis.append("")
        
        analysis.append("### 项目结构")
        analysis.append("")
        analysis.append("```")
        
        # Group files by directory
        # 按目录分组文件
        dir_structure = {}
        for f in file_metrics[:10]:  # Show top 10 files
            parts = Path(f['file_path']).parts
            if len(parts) > 1:
                dir_name = parts[-2] if len(parts) > 1 else "root"
                file_name = parts[-1]
                if dir_name not in dir_structure:
                    dir_structure[dir_name] = []
                dir_structure[dir_name].append(file_name)
        
        for dir_name, files in sorted(dir_structure.items()):
            analysis.append(f"📁 {dir_name}/")
            for file_name in files[:5]:  # Show top 5 files per directory
                analysis.append(f"  ├─ {file_name}")
            if len(files) > 5:
                analysis.append(f"  └─ ... 还有 {len(files) - 5} 个文件")
        
        analysis.append("```")
        
        return "\n".join(analysis)
    
    def _generate_pattern_analysis(self, file_metrics: List[Dict[str, Any]]) -> str:
        """Generate design pattern analysis"""
        analysis = []
        
        # This would need to be extracted from file metrics if we add pattern detection
        # 这需要从文件指标中提取（如果我们添加了模式检测）
        analysis.append("### 常见设计模式")
        analysis.append("")
        analysis.append("以下是项目中可能使用的设计模式：")
        analysis.append("")
        
        # Check file names for pattern hints
        # 检查文件名中的模式提示
        detected_patterns = set()
        for f in file_metrics:
            file_name_lower = Path(f['file_path']).name.lower()
            
            if 'factory' in file_name_lower:
                detected_patterns.add('factory')
            if 'service' in file_name_lower:
                detected_patterns.add('service')
            if 'repository' in file_name_lower:
                detected_patterns.add('repository')
            if 'controller' in file_name_lower:
                detected_patterns.add('mvc')
            if 'observer' in file_name_lower or 'listener' in file_name_lower:
                detected_patterns.add('observer')
        
        if detected_patterns:
            for pattern in detected_patterns:
                if pattern in self.pattern_explanations:
                    info = self.pattern_explanations[pattern]
                    analysis.append(f"#### {pattern.upper()}")
                    analysis.append("")
                    analysis.append(f"- **说明**: {info['zh']}")
                    analysis.append(f"- **English**: {info['en']}")
                    analysis.append(f"- **使用场景**: {info['use_case']}")
                    analysis.append(f"- **难度**: {info['difficulty'].upper()}")
                    analysis.append("")
        else:
            analysis.append("- ℹ️ 未检测到明显的设计模式标识")
            analysis.append("")
            analysis.append("这并不意味着代码质量不好，可能使用了更简单直接的实现方式。")
        
        return "\n".join(analysis)
    
    def _generate_complexity_analysis(
        self,
        project_metrics: Dict[str, Any],
        file_metrics: List[Dict[str, Any]]
    ) -> str:
        """Generate complexity analysis"""
        analysis = []
        
        avg_complexity = project_metrics['avg_complexity']
        
        analysis.append(f"### 整体复杂度指标")
        analysis.append("")
        analysis.append(f"- **平均圈复杂度**: {avg_complexity:.2f}")
        analysis.append(f"- **复杂度评级**: {'🟢 低' if avg_complexity <= 5 else '🟡 中' if avg_complexity <= 10 else '🔴 高'}")
        analysis.append("")
        
        # Find most complex files
        # 找到最复杂的文件
        complex_files = sorted(
            file_metrics,
            key=lambda f: f['complexity_score'],
            reverse=True
        )[:5]
        
        analysis.append("### 最复杂的文件 (Top 5)")
        analysis.append("")
        analysis.append("| 文件 | 复杂度 | 可维护性 | 建议 |")
        analysis.append("|------|--------|---------|------|")
        
        for f in complex_files:
            file_name = Path(f['file_path']).name
            complexity = f['complexity_score']
            maintainability = f['maintainability_index']
            
            suggestion = "✅ 良好" if complexity <= 5 else "⚠️ 考虑重构" if complexity <= 10 else "🔴 需要重构"
            
            analysis.append(f"| `{file_name}` | {complexity:.1f} | {maintainability:.1f}/100 | {suggestion} |")
        
        analysis.append("")
        
        analysis.append("### 复杂度理解指南")
        analysis.append("")
        analysis.append("- **1-5**: 简单易懂，适合新手学习")
        analysis.append("- **6-10**: 中等复杂，需要一定经验")
        analysis.append("- **11-20**: 较复杂，需要深入理解")
        analysis.append("- **20+**: 非常复杂，建议重构")
        
        return "\n".join(analysis)
    
    def _generate_file_analysis(self, file_metrics: List[Dict[str, Any]]) -> str:
        """Generate file structure analysis"""
        analysis = []
        
        analysis.append("### 文件统计")
        analysis.append("")
        analysis.append("| 文件 | 行数 | 函数 | 类 | 复杂度 |")
        analysis.append("|------|------|------|-----|--------|")
        
        # Show top 10 files by lines of code
        # 显示代码行数最多的前10个文件
        top_files = sorted(
            file_metrics,
            key=lambda f: f['lines_of_code'],
            reverse=True
        )[:10]
        
        for f in top_files:
            file_name = Path(f['file_path']).name
            analysis.append(f"| `{file_name}` | {f['lines_of_code']} | {f['num_functions']} | {f['num_classes']} | {f['complexity_score']:.1f} |")
        
        analysis.append("")
        
        if len(file_metrics) > 10:
            analysis.append(f"*... 还有 {len(file_metrics) - 10} 个文件*")
        
        return "\n".join(analysis)
    
    def _generate_learning_recommendations(
        self,
        project_metrics: Dict[str, Any],
        file_metrics: List[Dict[str, Any]],
        summary: Dict[str, Any]
    ) -> str:
        """Generate personalized learning recommendations"""
        recommendations = []
        
        difficulty = project_metrics['overall_difficulty']
        avg_complexity = project_metrics['avg_complexity']
        
        recommendations.append("### 学习策略建议")
        recommendations.append("")
        
        if difficulty == "beginner":
            recommendations.append("#### 💚 适合初学者")
            recommendations.append("")
            recommendations.append("这个项目非常适合作为学习入门：")
            recommendations.append("")
            recommendations.append("1. **从简单文件开始**: 先阅读复杂度低的文件")
            recommendations.append("2. **逐步深入**: 理解一个功能后再学习下一个")
            recommendations.append("3. **动手实践**: 尝试修改代码并观察结果")
            recommendations.append("4. **添加注释**: 用自己的话解释代码逻辑")
        
        elif difficulty == "intermediate":
            recommendations.append("#### 💛 中级学习建议")
            recommendations.append("")
            recommendations.append("1. **理解架构**: 先理清模块间的关系")
            recommendations.append("2. **学习模式**: 识别和理解使用的设计模式")
            recommendations.append("3. **阅读测试**: 如果有测试代码，它们是很好的文档")
            recommendations.append("4. **重构练习**: 尝试优化复杂的代码")
        
        elif difficulty == "advanced":
            recommendations.append("#### 🧡 高级学习建议")
            recommendations.append("")
            recommendations.append("1. **系统性学习**: 从架构层面理解整体设计")
            recommendations.append("2. **深入分析**: 研究关键算法和数据结构")
            recommendations.append("3. **性能优化**: 思考代码的性能瓶颈")
            recommendations.append("4. **扩展功能**: 尝试添加新功能")
        
        else:  # expert
            recommendations.append("#### ❤️ 专家级学习建议")
            recommendations.append("")
            recommendations.append("1. **架构演进**: 理解架构的演化过程")
            recommendations.append("2. **最佳实践**: 识别和学习高级编程技巧")
            recommendations.append("3. **源码研究**: 深入研究核心实现")
            recommendations.append("4. **贡献代码**: 参与项目开发和优化")
        
        recommendations.append("")
        recommendations.append("### 学习资源")
        recommendations.append("")
        recommendations.append("- 📖 阅读项目文档（如果有）")
        recommendations.append("- 🎥 搜索相关技术的视频教程")
        recommendations.append("- 💬 加入相关技术社区讨论")
        recommendations.append("- 🔧 使用调试器逐步执行代码")
        
        return "\n".join(recommendations)
    
    def _generate_quality_report(
        self,
        file_metrics: List[Dict[str, Any]],
        summary: Dict[str, Any]
    ) -> str:
        """Generate code quality report"""
        report = []
        
        total_smells = summary['total_code_smells']
        total_security = summary['total_security_issues']
        avg_maintainability = summary['avg_maintainability']
        health_score = summary['health_score']
        
        report.append(f"### 整体健康分数: {health_score}/100")
        report.append("")
        report.append(self._get_health_emoji(health_score))
        report.append("")
        
        report.append("### 质量指标")
        report.append("")
        report.append("| 指标 | 值 | 状态 |")
        report.append("|------|----|----|")
        report.append(f"| 平均可维护性 | {avg_maintainability:.1f}/100 | {self._get_status_emoji(avg_maintainability)} |")
        report.append(f"| 代码异味数量 | {total_smells} | {self._get_smell_status(total_smells)} |")
        report.append(f"| 安全问题数量 | {total_security} | {self._get_security_status(total_security)} |")
        report.append("")
        
        # List code smells if any
        # 列出代码异味（如果有）
        if total_smells > 0:
            report.append("### 检测到的代码异味")
            report.append("")
            
            smell_count = 0
            for f in file_metrics:
                if f['code_smells']:
                    for smell in f['code_smells'][:3]:  # Show top 3 smells per file
                        file_name = Path(f['file_path']).name
                        report.append(f"- **{smell['type']}** in `{file_name}`: {smell['message']}")
                        smell_count += 1
                        if smell_count >= 10:  # Limit to 10 smells total
                            break
                if smell_count >= 10:
                    break
            
            if total_smells > 10:
                report.append(f"- *... 还有 {total_smells - 10} 个问题*")
            report.append("")
        
        # List security issues if any
        # 列出安全问题（如果有）
        if total_security > 0:
            report.append("### ⚠️ 检测到的安全问题")
            report.append("")
            
            sec_count = 0
            for f in file_metrics:
                if f['security_issues']:
                    for issue in f['security_issues']:
                        file_name = Path(f['file_path']).name
                        report.append(f"- **{issue['severity'].upper()}** in `{file_name}`: {issue['message']}")
                        sec_count += 1
                        if sec_count >= 10:
                            break
                if sec_count >= 10:
                    break
            
            report.append("")
            report.append("**建议**: 立即修复安全问题，避免潜在风险！")
            report.append("")
        
        report.append("### 改进建议")
        report.append("")
        report.append(f"- {summary['recommendation']}")
        
        return "\n".join(report)
    
    def _get_health_emoji(self, score: float) -> str:
        """Get health emoji based on score"""
        if score >= 90:
            return "🎉 优秀！代码质量非常高"
        elif score >= 80:
            return "✅ 良好！代码质量不错"
        elif score >= 70:
            return "⚠️ 一般，有改进空间"
        elif score >= 60:
            return "🔴 较差，需要重点优化"
        else:
            return "💥 严重问题，建议全面重构"
    
    def _get_status_emoji(self, value: float) -> str:
        """Get status emoji for maintainability"""
        if value >= 80:
            return "🟢 优秀"
        elif value >= 60:
            return "🟡 良好"
        else:
            return "🔴 需改进"
    
    def _get_smell_status(self, count: int) -> str:
        """Get status for code smells"""
        if count == 0:
            return "🟢 无"
        elif count <= 5:
            return "🟡 少量"
        elif count <= 15:
            return "🟠 较多"
        else:
            return "🔴 很多"
    
    def _get_security_status(self, count: int) -> str:
        """Get status for security issues"""
        if count == 0:
            return "🟢 无"
        else:
            return f"🔴 {count} 个"
    
    def _generate_json_doc(self, results: Dict[str, Any], project_path: Path) -> Dict[str, Any]:
        """Generate JSON format documentation"""
        return {
            "project_name": results['project_metrics']['project_name'],
            "generated_at": datetime.now().isoformat(),
            "metrics": results['project_metrics'],
            "files": results['file_metrics'],
            "architecture": results['architecture'],
            "tech_stack": results['tech_stack'],
            "summary": results['summary']
        }

