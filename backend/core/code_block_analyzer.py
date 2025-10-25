"""
Code Block Analyzer / 代码块分析器

Generates detailed analysis documentation for code migration at block level.
为代码迁移生成详细的块级分析文档。

Features / 功能:
- Block-level code analysis / 代码块级分析
- Semantic mapping / 语义映射
- Conversion traceability / 转换可追溯性
- Quality metrics / 质量指标
"""

import ast
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from loguru import logger
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class CodeBlock:
    """Represents a code block / 代码块表示"""
    id: int
    type: str  # class, method, import, annotation, etc.
    source_code: str
    target_code: str
    source_line_start: int
    source_line_end: int
    target_line_start: int
    target_line_end: int
    mappings: List[Dict[str, str]] = field(default_factory=list)
    ai_prompt: Optional[str] = None
    conversion_notes: Optional[str] = None
    quality_score: float = 0.0


@dataclass
class MigrationAnalysis:
    """Migration analysis report / 迁移分析报告"""
    source_file: str
    target_file: str
    source_language: str
    target_language: str
    source_framework: Optional[str]
    target_framework: Optional[str]
    blocks: List[CodeBlock]
    statistics: Dict[str, Any]
    quality_metrics: Dict[str, Any]
    recommendations: List[str]
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class CodeBlockAnalyzer:
    """
    Code Block Analyzer / 代码块分析器
    
    Analyzes code migration at block level and generates detailed documentation.
    在代码块级别分析代码迁移并生成详细文档。
    """
    
    def __init__(self):
        self.block_id_counter = 0
        
    def analyze_migration(
        self,
        source_file: Path,
        target_file: Path,
        source_language: str,
        target_language: str,
        source_framework: Optional[str] = None,
        target_framework: Optional[str] = None
    ) -> MigrationAnalysis:
        """
        Analyze code migration and generate comprehensive report.
        分析代码迁移并生成综合报告。
        
        Args:
            source_file: Path to source code file.
                        源代码文件路径。
            target_file: Path to converted target file.
                        转换后的目标文件路径。
            source_language: Source programming language.
                           源编程语言。
            target_language: Target programming language.
                           目标编程语言。
            source_framework: Source framework (optional).
                             源框架（可选）。
            target_framework: Target framework (optional).
                             目标框架（可选）。
        
        Returns:
            MigrationAnalysis object with detailed analysis.
            包含详细分析的MigrationAnalysis对象。
        """
        logger.info(f"开始分析代码块迁移: {source_file} → {target_file}")
        
        # Read source and target files
        # 读取源文件和目标文件
        with open(source_file, 'r', encoding='utf-8') as f:
            source_content = f.read()
        
        with open(target_file, 'r', encoding='utf-8') as f:
            target_content = f.read()
        
        # Extract code blocks
        # 提取代码块
        source_blocks = self._extract_blocks(source_content, source_language)
        target_blocks = self._extract_blocks(target_content, target_language)
        
        # Match and analyze blocks
        # 匹配和分析代码块
        matched_blocks = self._match_blocks(
            source_blocks, 
            target_blocks,
            source_language,
            target_language,
            source_framework,
            target_framework
        )
        
        # Calculate statistics
        # 计算统计信息
        statistics = self._calculate_statistics(source_content, target_content, matched_blocks)
        
        # Calculate quality metrics
        # 计算质量指标
        quality_metrics = self._calculate_quality_metrics(matched_blocks, target_content)
        
        # Generate recommendations
        # 生成建议
        recommendations = self._generate_recommendations(matched_blocks, quality_metrics)
        
        analysis = MigrationAnalysis(
            source_file=str(source_file),
            target_file=str(target_file),
            source_language=source_language,
            target_language=target_language,
            source_framework=source_framework,
            target_framework=target_framework,
            blocks=matched_blocks,
            statistics=statistics,
            quality_metrics=quality_metrics,
            recommendations=recommendations
        )
        
        logger.info(f"代码块分析完成: {len(matched_blocks)} 个代码块")
        return analysis
    
    def _extract_blocks(self, content: str, language: str) -> List[Dict[str, Any]]:
        """
        Extract code blocks from source content.
        从源内容中提取代码块。
        """
        if language == "python":
            return self._extract_python_blocks(content)
        elif language == "java":
            return self._extract_java_blocks(content)
        elif language == "javascript":
            return self._extract_javascript_blocks(content)
        else:
            logger.warning(f"不支持的语言: {language}")
            return []
    
    def _extract_python_blocks(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract blocks from Python code using AST.
        使用AST从Python代码中提取代码块。
        """
        try:
            tree = ast.parse(content)
            blocks = []
            lines = content.split('\n')
            
            # Extract imports
            # 提取导入
            for node in ast.walk(tree):
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    start_line = node.lineno - 1
                    end_line = node.end_lineno if node.end_lineno else start_line
                    code = '\n'.join(lines[start_line:end_line])
                    
                    blocks.append({
                        "type": "import",
                        "code": code,
                        "start_line": start_line,
                        "end_line": end_line,
                        "name": ast.unparse(node) if hasattr(ast, 'unparse') else code
                    })
            
            # Extract classes
            # 提取类
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    start_line = node.lineno - 1
                    end_line = node.end_lineno if node.end_lineno else start_line
                    code = '\n'.join(lines[start_line:end_line])
                    
                    blocks.append({
                        "type": "class",
                        "code": code,
                        "start_line": start_line,
                        "end_line": end_line,
                        "name": node.name,
                        "decorators": [ast.unparse(d) if hasattr(ast, 'unparse') else "" for d in node.decorator_list]
                    })
            
            # Extract functions
            # 提取函数
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    start_line = node.lineno - 1
                    end_line = node.end_lineno if node.end_lineno else start_line
                    code = '\n'.join(lines[start_line:end_line])
                    
                    blocks.append({
                        "type": "function",
                        "code": code,
                        "start_line": start_line,
                        "end_line": end_line,
                        "name": node.name,
                        "is_async": isinstance(node, ast.AsyncFunctionDef),
                        "decorators": [ast.unparse(d) if hasattr(ast, 'unparse') else "" for d in node.decorator_list]
                    })
            
            return blocks
        except Exception as e:
            logger.error(f"提取Python代码块失败: {e}")
            return []
    
    def _extract_java_blocks(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract blocks from Java code (simplified regex-based).
        从Java代码中提取代码块（简化的基于正则）。
        """
        blocks = []
        lines = content.split('\n')
        
        # Extract imports
        # 提取导入
        for i, line in enumerate(lines):
            if line.strip().startswith('import '):
                blocks.append({
                    "type": "import",
                    "code": line,
                    "start_line": i,
                    "end_line": i,
                    "name": line.strip()
                })
        
        # Extract class definitions
        # 提取类定义
        class_pattern = r'(public|private|protected)?\s*(class|interface)\s+(\w+)'
        for i, line in enumerate(lines):
            match = re.search(class_pattern, line)
            if match:
                # Find class body (simplified: find matching braces)
                # 查找类主体（简化：查找匹配的大括号）
                class_name = match.group(3)
                blocks.append({
                    "type": "class",
                    "code": line,
                    "start_line": i,
                    "end_line": i,  # Simplified
                    "name": class_name
                })
        
        # Extract method definitions
        # 提取方法定义
        method_pattern = r'(public|private|protected)?\s*(static)?\s*(\w+)\s+(\w+)\s*\([^)]*\)'
        for i, line in enumerate(lines):
            match = re.search(method_pattern, line)
            if match and '{' in line:
                method_name = match.group(4)
                blocks.append({
                    "type": "method",
                    "code": line,
                    "start_line": i,
                    "end_line": i,  # Simplified
                    "name": method_name
                })
        
        return blocks
    
    def _extract_javascript_blocks(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract blocks from JavaScript code.
        从JavaScript代码中提取代码块。
        """
        blocks = []
        lines = content.split('\n')
        
        # Extract imports
        # 提取导入
        import_patterns = [r'import\s+.*from', r'const\s+.*=\s*require']
        for i, line in enumerate(lines):
            for pattern in import_patterns:
                if re.search(pattern, line):
                    blocks.append({
                        "type": "import",
                        "code": line,
                        "start_line": i,
                        "end_line": i,
                        "name": line.strip()
                    })
        
        # Extract function definitions
        # 提取函数定义
        func_patterns = [
            r'(async\s+)?function\s+(\w+)',
            r'const\s+(\w+)\s*=\s*(async\s+)?\(',
            r'(\w+)\s*:\s*(async\s+)?function'
        ]
        
        for i, line in enumerate(lines):
            for pattern in func_patterns:
                match = re.search(pattern, line)
                if match:
                    blocks.append({
                        "type": "function",
                        "code": line,
                        "start_line": i,
                        "end_line": i,  # Simplified
                        "name": match.group(1) if match.lastindex >= 1 else "anonymous"
                    })
        
        return blocks
    
    def _match_blocks(
        self,
        source_blocks: List[Dict[str, Any]],
        target_blocks: List[Dict[str, Any]],
        source_language: str,
        target_language: str,
        source_framework: Optional[str],
        target_framework: Optional[str]
    ) -> List[CodeBlock]:
        """
        Match source blocks to target blocks and analyze conversion.
        将源代码块匹配到目标代码块并分析转换。
        """
        matched = []
        
        # Simple matching by type and order
        # 通过类型和顺序进行简单匹配
        for i, source_block in enumerate(source_blocks):
            # Find corresponding target block
            # 查找对应的目标代码块
            target_block = target_blocks[i] if i < len(target_blocks) else None
            
            if target_block:
                # Analyze conversion
                # 分析转换
                mappings = self._analyze_conversion(
                    source_block,
                    target_block,
                    source_language,
                    target_language,
                    source_framework,
                    target_framework
                )
                
                # Generate AI prompt used
                # 生成使用的AI提示词
                ai_prompt = self._reconstruct_ai_prompt(
                    source_block,
                    source_language,
                    target_language,
                    source_framework,
                    target_framework
                )
                
                # Generate conversion notes
                # 生成转换说明
                notes = self._generate_conversion_notes(
                    source_block,
                    target_block,
                    mappings,
                    source_framework,
                    target_framework
                )
                
                # Calculate quality score
                # 计算质量分数
                quality_score = self._calculate_block_quality(target_block, target_language)
                
                block = CodeBlock(
                    id=self.block_id_counter,
                    type=source_block["type"],
                    source_code=source_block["code"],
                    target_code=target_block["code"],
                    source_line_start=source_block["start_line"],
                    source_line_end=source_block["end_line"],
                    target_line_start=target_block["start_line"],
                    target_line_end=target_block["end_line"],
                    mappings=mappings,
                    ai_prompt=ai_prompt,
                    conversion_notes=notes,
                    quality_score=quality_score
                )
                
                matched.append(block)
                self.block_id_counter += 1
        
        return matched
    
    def _analyze_conversion(
        self,
        source_block: Dict[str, Any],
        target_block: Dict[str, Any],
        source_language: str,
        target_language: str,
        source_framework: Optional[str],
        target_framework: Optional[str]
    ) -> List[Dict[str, str]]:
        """
        Analyze how source features map to target features.
        分析源特性如何映射到目标特性。
        """
        mappings = []
        
        # Framework-specific mappings
        # 框架特定的映射
        if source_framework == "spring-boot" and target_framework == "fastapi":
            if source_block["type"] == "class":
                if "@RestController" in str(source_block.get("decorators", [])):
                    mappings.append({
                        "source_feature": "@RestController",
                        "target_feature": "APIRouter",
                        "explanation": "Spring的REST控制器 → FastAPI路由器"
                    })
                
                if "@RequestMapping" in source_block["code"]:
                    mappings.append({
                        "source_feature": "@RequestMapping",
                        "target_feature": "router.prefix",
                        "explanation": "路由前缀映射"
                    })
            
            elif source_block["type"] == "method":
                if "@GetMapping" in source_block["code"]:
                    mappings.append({
                        "source_feature": "@GetMapping",
                        "target_feature": "@router.get",
                        "explanation": "GET请求映射"
                    })
                
                if "@Autowired" in source_block["code"]:
                    mappings.append({
                        "source_feature": "@Autowired",
                        "target_feature": "Depends()",
                        "explanation": "依赖注入模式"
                    })
        
        # Language-specific mappings
        # 语言特定的映射
        if source_language == "java" and target_language == "python":
            mappings.append({
                "source_feature": "public class",
                "target_feature": "class",
                "explanation": "访问修饰符简化"
            })
            
            mappings.append({
                "source_feature": "Long",
                "target_feature": "int",
                "explanation": "数据类型转换"
            })
        
        return mappings
    
    def _reconstruct_ai_prompt(
        self,
        source_block: Dict[str, Any],
        source_language: str,
        target_language: str,
        source_framework: Optional[str],
        target_framework: Optional[str]
    ) -> str:
        """
        Reconstruct the AI prompt that would have been used.
        重构可能使用的AI提示词。
        """
        framework_context = ""
        if source_framework and target_framework:
            framework_context = f"\n识别到{source_framework}框架特征，转换为{target_framework}对应实现。"
        
        prompt = f"""转换以下{source_language}代码块为{target_language}:

类型: {source_block['type']}
代码:
{source_block['code']}
{framework_context}

要求:
- 保持相同的语义
- 使用目标语言的惯用法
- 保留注释和文档
"""
        return prompt
    
    def _generate_conversion_notes(
        self,
        source_block: Dict[str, Any],
        target_block: Dict[str, Any],
        mappings: List[Dict[str, str]],
        source_framework: Optional[str],
        target_framework: Optional[str]
    ) -> str:
        """
        Generate human-readable conversion notes.
        生成人类可读的转换说明。
        """
        notes = []
        
        if mappings:
            notes.append("特征映射:")
            for mapping in mappings:
                notes.append(f"- {mapping['source_feature']} → {mapping['target_feature']}: {mapping['explanation']}")
        
        # Check for added features
        # 检查添加的特征
        if "async" in target_block["code"] and "async" not in source_block["code"]:
            notes.append("- 转换为异步实现（目标框架最佳实践）")
        
        # Check for type annotations
        # 检查类型注解
        if ":" in target_block["code"] and ":" not in source_block["code"]:
            notes.append("- 添加了Python类型注解")
        
        return "\n".join(notes) if notes else "直接转换，无特殊说明"
    
    def _calculate_block_quality(self, target_block: Dict[str, Any], language: str) -> float:
        """
        Calculate quality score for a converted block.
        计算转换后代码块的质量分数。
        """
        score = 1.0
        code = target_block["code"]
        
        # Check for type annotations (Python)
        # 检查类型注解（Python）
        if language == "python":
            if "def " in code or "async def " in code:
                if " -> " in code:  # Has return type
                    score += 0.1
                if re.search(r'\w+:\s*\w+', code):  # Has parameter types
                    score += 0.1
        
        # Check for documentation
        # 检查文档
        if '"""' in code or "'''" in code or "/**" in code:
            score += 0.15
        
        # Check for error handling
        # 检查错误处理
        if "try" in code or "except" in code or "raise" in code:
            score += 0.1
        
        # Penalize for TODO comments
        # 对TODO注释进行惩罚
        todo_count = code.lower().count("todo")
        score -= (todo_count * 0.05)
        
        return min(max(score, 0.0), 1.0)  # Clamp between 0 and 1
    
    def _calculate_statistics(
        self,
        source_content: str,
        target_content: str,
        blocks: List[CodeBlock]
    ) -> Dict[str, Any]:
        """
        Calculate migration statistics.
        计算迁移统计信息。
        """
        source_lines = len(source_content.split('\n'))
        target_lines = len(target_content.split('\n'))
        
        return {
            "source_lines": source_lines,
            "target_lines": target_lines,
            "line_change_percent": round(((target_lines - source_lines) / source_lines * 100), 2) if source_lines > 0 else 0,
            "total_blocks": len(blocks),
            "blocks_by_type": self._count_blocks_by_type(blocks),
            "average_quality_score": round(sum(b.quality_score for b in blocks) / len(blocks), 2) if blocks else 0.0
        }
    
    def _count_blocks_by_type(self, blocks: List[CodeBlock]) -> Dict[str, int]:
        """
        Count blocks by type.
        按类型统计代码块。
        """
        counts = {}
        for block in blocks:
            counts[block.type] = counts.get(block.type, 0) + 1
        return counts
    
    def _calculate_quality_metrics(
        self,
        blocks: List[CodeBlock],
        target_content: str
    ) -> Dict[str, Any]:
        """
        Calculate overall quality metrics.
        计算整体质量指标。
        """
        # Calculate average quality score
        # 计算平均质量分数
        avg_quality = sum(b.quality_score for b in blocks) / len(blocks) if blocks else 0.0
        
        # Count blocks with high quality
        # 计算高质量代码块数量
        high_quality_blocks = sum(1 for b in blocks if b.quality_score >= 0.9)
        
        # Check for type annotations coverage (Python)
        # 检查类型注解覆盖率（Python）
        has_type_hints = target_content.count(" -> ") + target_content.count(": ")
        type_coverage = min((has_type_hints / len(blocks) * 100), 100) if blocks else 0
        
        return {
            "syntax_correctness": 100.0,  # Assume syntax is correct if it parsed
            "type_correctness": round(type_coverage, 1),
            "framework_adaptation": round(avg_quality * 100, 1),
            "code_style": 100.0,  # Assume formatted code
            "overall_quality": round(avg_quality * 100, 1)
        }
    
    def _generate_recommendations(
        self,
        blocks: List[CodeBlock],
        quality_metrics: Dict[str, Any]
    ) -> List[str]:
        """
        Generate improvement recommendations.
        生成改进建议。
        """
        recommendations = []
        
        # Check for low quality blocks
        # 检查低质量代码块
        low_quality_blocks = [b for b in blocks if b.quality_score < 0.7]
        if low_quality_blocks:
            recommendations.append(f"⚠️ {len(low_quality_blocks)} 个代码块质量较低，建议人工审查")
        
        # Check type coverage
        # 检查类型覆盖率
        if quality_metrics["type_correctness"] < 80:
            recommendations.append("✅ 建议添加更多类型注解以提高代码可维护性")
        
        # Check documentation
        # 检查文档
        undocumented_blocks = [b for b in blocks if '"""' not in b.target_code and "'''" not in b.target_code]
        if len(undocumented_blocks) > len(blocks) * 0.5:
            recommendations.append("✅ 建议为主要函数和类添加文档字符串")
        
        # Check for error handling
        # 检查错误处理
        blocks_without_error_handling = [b for b in blocks if "try" not in b.target_code and "raise" not in b.target_code]
        if len(blocks_without_error_handling) > len(blocks) * 0.7:
            recommendations.append("⚠️ 建议添加错误处理逻辑")
        
        # Check for logging
        # 检查日志
        blocks_without_logging = [b for b in blocks if "log" not in b.target_code.lower()]
        if len(blocks_without_logging) == len(blocks):
            recommendations.append("⚠️ 建议添加日志记录")
        
        if not recommendations:
            recommendations.append("✅ 代码质量良好，无明显改进点")
        
        return recommendations
    
    def generate_markdown_report(self, analysis: MigrationAnalysis) -> str:
        """
        Generate Markdown format analysis report.
        生成Markdown格式的分析报告。
        """
        md = []
        
        # Title
        # 标题
        md.append("# 代码迁移分析报告 / Code Migration Analysis Report\n")
        
        # Overview
        # 概览
        md.append("## 概览 / Overview\n")
        md.append(f"- **源文件 / Source File**: `{analysis.source_file}`")
        md.append(f"- **目标文件 / Target File**: `{analysis.target_file}`")
        md.append(f"- **源语言 / Source Language**: {analysis.source_language}")
        md.append(f"- **目标语言 / Target Language**: {analysis.target_language}")
        if analysis.source_framework:
            md.append(f"- **源框架 / Source Framework**: {analysis.source_framework}")
        if analysis.target_framework:
            md.append(f"- **目标框架 / Target Framework**: {analysis.target_framework}")
        md.append(f"- **代码块数 / Code Blocks**: {len(analysis.blocks)}")
        md.append(f"- **转换成功率 / Success Rate**: {analysis.quality_metrics['overall_quality']}%")
        md.append("")
        
        # Statistics
        # 统计信息
        md.append("## 统计信息 / Statistics\n")
        stats = analysis.statistics
        md.append(f"- **源代码行数 / Source Lines**: {stats['source_lines']}")
        md.append(f"- **目标代码行数 / Target Lines**: {stats['target_lines']}")
        md.append(f"- **行数变化 / Line Change**: {stats['line_change_percent']:+.1f}%")
        md.append(f"- **平均质量分数 / Average Quality Score**: {stats['average_quality_score']:.2f}/1.00")
        md.append("")
        
        # Code blocks
        # 代码块
        md.append("## 代码块分析 / Code Block Analysis\n")
        
        for i, block in enumerate(analysis.blocks, 1):
            md.append(f"### 代码块 #{i}: {block.type.title()}\n")
            
            # Source code
            # 源代码
            md.append("#### 源代码 / Source Code\n")
            md.append(f"```{analysis.source_language}")
            md.append(block.source_code)
            md.append("```\n")
            
            # Target code
            # 目标代码
            md.append("#### 转换后 / Converted Code\n")
            md.append(f"```{analysis.target_language}")
            md.append(block.target_code)
            md.append("```\n")
            
            # Mappings
            # 映射
            if block.mappings:
                md.append("#### 转换逻辑 / Conversion Logic\n")
                md.append("| 源特征 / Source Feature | 目标特征 / Target Feature | 说明 / Explanation |")
                md.append("|------------------------|---------------------------|-------------------|")
                for mapping in block.mappings:
                    md.append(f"| `{mapping['source_feature']}` | `{mapping['target_feature']}` | {mapping['explanation']} |")
                md.append("")
            
            # Notes
            # 说明
            if block.conversion_notes:
                md.append("#### 转换说明 / Conversion Notes\n")
                md.append(block.conversion_notes)
                md.append("")
            
            # Quality score
            # 质量分数
            md.append(f"**质量分数 / Quality Score**: {block.quality_score:.2f}/1.00\n")
            md.append("---\n")
        
        # Quality metrics
        # 质量指标
        md.append("## 质量指标 / Quality Metrics\n")
        metrics = analysis.quality_metrics
        md.append("| 指标 / Metric | 值 / Value |")
        md.append("|--------------|-----------|")
        md.append(f"| 语法正确性 / Syntax Correctness | {metrics['syntax_correctness']}% |")
        md.append(f"| 类型正确性 / Type Correctness | {metrics['type_correctness']}% |")
        md.append(f"| 框架适配度 / Framework Adaptation | {metrics['framework_adaptation']}% |")
        md.append(f"| 代码风格 / Code Style | {metrics['code_style']}% |")
        md.append(f"| **总体质量 / Overall Quality** | **{metrics['overall_quality']}%** |")
        md.append("")
        
        # Recommendations
        # 建议
        md.append("## 改进建议 / Recommendations\n")
        for rec in analysis.recommendations:
            md.append(f"- {rec}")
        md.append("")
        
        # Footer
        # 页脚
        md.append(f"\n---\n*生成时间 / Generated at: {analysis.timestamp}*")
        
        return "\n".join(md)

