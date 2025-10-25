"""
Code Inspector / 代码检测器

Analyzes code quality, complexity, and structure for learning purposes.
分析代码质量、复杂度和结构以供学习使用。

Features / 功能:
- Code complexity analysis / 代码复杂度分析
- Design pattern detection / 设计模式检测
- Code smell detection / 代码异味检测
- Dependency analysis / 依赖分析
- Security vulnerability detection / 安全漏洞检测
"""

import ast
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Set
from dataclasses import dataclass, field
from loguru import logger
import os


@dataclass
class FunctionMetrics:
    """Function-level metrics / 函数级指标"""
    name: str
    lines_of_code: int
    cyclomatic_complexity: int  # 圈复杂度
    cognitive_complexity: int    # 认知复杂度
    num_parameters: int
    num_returns: int
    num_branches: int
    max_nesting_depth: int
    dependencies: List[str] = field(default_factory=list)
    is_recursive: bool = False
    difficulty_level: str = "medium"  # easy, medium, hard, expert


@dataclass
class ClassMetrics:
    """Class-level metrics / 类级指标"""
    name: str
    lines_of_code: int
    num_methods: int
    num_attributes: int
    inheritance_depth: int
    coupling: int  # 耦合度
    cohesion: float  # 内聚度
    design_patterns: List[str] = field(default_factory=list)
    responsibilities: List[str] = field(default_factory=list)


@dataclass
class FileMetrics:
    """File-level metrics / 文件级指标"""
    file_path: str
    language: str
    lines_of_code: int
    num_functions: int
    num_classes: int
    num_imports: int
    complexity_score: float
    maintainability_index: float  # 可维护性指数
    code_smells: List[Dict[str, Any]] = field(default_factory=list)
    security_issues: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class ProjectMetrics:
    """Project-level metrics / 项目级指标"""
    project_name: str
    total_files: int
    total_lines: int
    total_functions: int
    total_classes: int
    languages: Dict[str, int]  # language -> line count
    avg_complexity: float
    overall_difficulty: str
    architecture_patterns: List[str] = field(default_factory=list)
    tech_stack: List[str] = field(default_factory=list)


class CodeInspector:
    """
    Code Inspector / 代码检测器
    
    Performs comprehensive code analysis for learning and documentation.
    执行全面的代码分析以供学习和文档使用。
    """
    
    def __init__(self):
        self.complexity_thresholds = {
            "easy": (0, 5),
            "medium": (6, 10),
            "hard": (11, 20),
            "expert": (21, float('inf'))
        }
        
        self.design_patterns = {
            "singleton": ["getInstance", "__new__", "instance"],
            "factory": ["create", "factory", "build"],
            "observer": ["subscribe", "notify", "observer", "listener"],
            "strategy": ["strategy", "algorithm"],
            "decorator": ["@", "wrapper", "decorate"],
            "adapter": ["adapt", "adapter"],
            "repository": ["repository", "findBy", "save"],
            "service": ["service", "process"],
            "mvc": ["controller", "model", "view"],
            "dependency_injection": ["inject", "Autowired", "Depends"]
        }
    
    def inspect_project(self, project_path: Path) -> Dict[str, Any]:
        """
        Inspect entire project and generate metrics.
        检测整个项目并生成指标。
        
        Args:
            project_path: Path to project directory.
                         项目目录路径。
        
        Returns:
            Dictionary containing all metrics and analysis.
            包含所有指标和分析的字典。
        """
        logger.info(f"开始检测项目: {project_path}")
        
        file_metrics = []
        all_functions = []
        all_classes = []
        language_stats = {}
        
        # Analyze all source files
        # 分析所有源文件
        for file_path in self._get_source_files(project_path):
            try:
                metrics = self._inspect_file(file_path)
                file_metrics.append(metrics)
                
                # Update language statistics
                # 更新语言统计
                lang = metrics.language
                language_stats[lang] = language_stats.get(lang, 0) + metrics.lines_of_code
                
            except Exception as e:
                logger.warning(f"检测文件失败 {file_path}: {e}")
        
        # Calculate project-level metrics
        # 计算项目级指标
        project_metrics = self._calculate_project_metrics(
            project_path,
            file_metrics,
            language_stats
        )
        
        # Detect architecture patterns
        # 检测架构模式
        architecture = self._detect_architecture(project_path, file_metrics)
        
        # Detect tech stack
        # 检测技术栈
        tech_stack = self._detect_tech_stack(project_path)
        
        return {
            "project_metrics": project_metrics,
            "file_metrics": file_metrics,
            "architecture": architecture,
            "tech_stack": tech_stack,
            "summary": self._generate_summary(project_metrics, file_metrics)
        }
    
    def _get_source_files(self, project_path: Path) -> List[Path]:
        """
        Get all source code files in project.
        获取项目中的所有源代码文件。
        """
        extensions = {'.py', '.java', '.js', '.ts', '.go', '.cpp', '.c', '.h', '.rs'}
        exclude_dirs = {'node_modules', 'venv', '__pycache__', '.git', 'build', 'dist'}
        
        source_files = []
        
        for root, dirs, files in os.walk(project_path):
            # Remove excluded directories
            # 移除排除的目录
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix in extensions:
                    source_files.append(file_path)
        
        return source_files
    
    def _inspect_file(self, file_path: Path) -> FileMetrics:
        """
        Inspect a single file and calculate metrics.
        检测单个文件并计算指标。
        """
        language = self._detect_language(file_path)
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        if language == "python":
            return self._inspect_python_file(file_path, content)
        elif language == "java":
            return self._inspect_java_file(file_path, content)
        elif language in ["javascript", "typescript"]:
            return self._inspect_javascript_file(file_path, content)
        else:
            return self._inspect_generic_file(file_path, content, language)
    
    def _inspect_python_file(self, file_path: Path, content: str) -> FileMetrics:
        """
        Inspect Python file using AST.
        使用AST检测Python文件。
        """
        try:
            tree = ast.parse(content)
            
            functions = []
            classes = []
            imports = []
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    func_metrics = self._analyze_python_function(node, content)
                    functions.append(func_metrics)
                
                elif isinstance(node, ast.ClassDef):
                    class_metrics = self._analyze_python_class(node, content)
                    classes.append(class_metrics)
                
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    imports.append(node)
            
            # Calculate file complexity
            # 计算文件复杂度
            avg_complexity = sum(f.cyclomatic_complexity for f in functions) / len(functions) if functions else 0
            
            # Calculate maintainability index
            # 计算可维护性指数
            lines = content.count('\n') + 1
            maintainability = self._calculate_maintainability_index(
                lines,
                avg_complexity,
                len(functions) + len(classes)
            )
            
            # Detect code smells
            # 检测代码异味
            code_smells = self._detect_code_smells_python(functions, classes)
            
            # Detect security issues
            # 检测安全问题
            security_issues = self._detect_security_issues_python(content)
            
            return FileMetrics(
                file_path=str(file_path),
                language="python",
                lines_of_code=lines,
                num_functions=len(functions),
                num_classes=len(classes),
                num_imports=len(imports),
                complexity_score=avg_complexity,
                maintainability_index=maintainability,
                code_smells=code_smells,
                security_issues=security_issues
            )
        
        except Exception as e:
            logger.error(f"解析Python文件失败 {file_path}: {e}")
            return self._inspect_generic_file(file_path, content, "python")
    
    def _analyze_python_function(self, node: ast.FunctionDef, content: str) -> FunctionMetrics:
        """
        Analyze Python function and calculate metrics.
        分析Python函数并计算指标。
        """
        # Calculate lines of code
        # 计算代码行数
        start_line = node.lineno
        end_line = node.end_lineno if node.end_lineno else start_line
        loc = end_line - start_line + 1
        
        # Calculate cyclomatic complexity
        # 计算圈复杂度
        cyclomatic = self._calculate_cyclomatic_complexity(node)
        
        # Calculate cognitive complexity
        # 计算认知复杂度
        cognitive = self._calculate_cognitive_complexity(node)
        
        # Count parameters
        # 计算参数数量
        num_params = len(node.args.args)
        
        # Count returns
        # 计算返回语句数量
        num_returns = sum(1 for n in ast.walk(node) if isinstance(n, ast.Return))
        
        # Count branches
        # 计算分支数量
        num_branches = sum(1 for n in ast.walk(node) if isinstance(n, (ast.If, ast.For, ast.While)))
        
        # Calculate max nesting depth
        # 计算最大嵌套深度
        max_depth = self._calculate_max_nesting_depth(node)
        
        # Check if recursive
        # 检查是否递归
        is_recursive = self._is_recursive(node)
        
        # Determine difficulty level
        # 确定难度级别
        difficulty = self._determine_difficulty(cyclomatic, cognitive, max_depth)
        
        return FunctionMetrics(
            name=node.name,
            lines_of_code=loc,
            cyclomatic_complexity=cyclomatic,
            cognitive_complexity=cognitive,
            num_parameters=num_params,
            num_returns=num_returns,
            num_branches=num_branches,
            max_nesting_depth=max_depth,
            is_recursive=is_recursive,
            difficulty_level=difficulty
        )
    
    def _analyze_python_class(self, node: ast.ClassDef, content: str) -> ClassMetrics:
        """
        Analyze Python class and calculate metrics.
        分析Python类并计算指标。
        """
        # Calculate lines of code
        # 计算代码行数
        start_line = node.lineno
        end_line = node.end_lineno if node.end_lineno else start_line
        loc = end_line - start_line + 1
        
        # Count methods
        # 计算方法数量
        methods = [n for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
        num_methods = len(methods)
        
        # Count attributes
        # 计算属性数量
        attributes = set()
        for n in ast.walk(node):
            if isinstance(n, ast.Assign):
                for target in n.targets:
                    if isinstance(target, ast.Attribute):
                        attributes.add(target.attr)
        
        # Calculate inheritance depth
        # 计算继承深度
        inheritance_depth = len(node.bases)
        
        # Detect design patterns
        # 检测设计模式
        patterns = self._detect_class_patterns(node)
        
        return ClassMetrics(
            name=node.name,
            lines_of_code=loc,
            num_methods=num_methods,
            num_attributes=len(attributes),
            inheritance_depth=inheritance_depth,
            coupling=0,  # Simplified
            cohesion=0.0,  # Simplified
            design_patterns=patterns
        )
    
    def _calculate_cyclomatic_complexity(self, node: ast.AST) -> int:
        """
        Calculate cyclomatic complexity (McCabe).
        计算圈复杂度（McCabe）。
        
        Formula: CC = E - N + 2P
        Where:
        - E = number of edges
        - N = number of nodes
        - P = number of connected components (usually 1)
        
        Simplified: Count decision points + 1
        """
        complexity = 1  # Base complexity
        
        for n in ast.walk(node):
            # Decision points / 决策点
            if isinstance(n, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(n, ast.BoolOp):
                complexity += len(n.values) - 1
            elif isinstance(n, (ast.ListComp, ast.DictComp, ast.SetComp)):
                complexity += 1
        
        return complexity
    
    def _calculate_cognitive_complexity(self, node: ast.AST) -> int:
        """
        Calculate cognitive complexity (SonarSource).
        计算认知复杂度（SonarSource）。
        
        Focuses on how difficult code is to understand.
        关注代码理解的难度。
        """
        complexity = 0
        nesting_level = 0
        
        def visit(n, level):
            nonlocal complexity
            
            # Increment for control flow structures
            # 控制流结构增加复杂度
            if isinstance(n, (ast.If, ast.While, ast.For)):
                complexity += 1 + level
            
            # Increment for boolean operators in conditions
            # 条件中的布尔运算符增加复杂度
            elif isinstance(n, ast.BoolOp):
                complexity += len(n.values) - 1
            
            # Increment for nested functions
            # 嵌套函数增加复杂度
            elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and level > 0:
                complexity += 1
            
            # Recursively visit children with increased nesting
            # 递归访问子节点并增加嵌套级别
            new_level = level + 1 if isinstance(n, (ast.If, ast.While, ast.For)) else level
            for child in ast.iter_child_nodes(n):
                visit(child, new_level)
        
        visit(node, 0)
        return complexity
    
    def _calculate_max_nesting_depth(self, node: ast.AST) -> int:
        """
        Calculate maximum nesting depth.
        计算最大嵌套深度。
        """
        max_depth = 0
        
        def visit(n, depth):
            nonlocal max_depth
            max_depth = max(max_depth, depth)
            
            new_depth = depth + 1 if isinstance(n, (ast.If, ast.While, ast.For, ast.With)) else depth
            
            for child in ast.iter_child_nodes(n):
                visit(child, new_depth)
        
        visit(node, 0)
        return max_depth
    
    def _is_recursive(self, node: ast.FunctionDef) -> bool:
        """
        Check if function is recursive.
        检查函数是否递归。
        """
        func_name = node.name
        
        for n in ast.walk(node):
            if isinstance(n, ast.Call):
                if isinstance(n.func, ast.Name) and n.func.id == func_name:
                    return True
        
        return False
    
    def _determine_difficulty(self, cyclomatic: int, cognitive: int, max_depth: int) -> str:
        """
        Determine difficulty level based on complexity metrics.
        根据复杂度指标确定难度级别。
        """
        # Calculate weighted score
        # 计算加权分数
        score = (cyclomatic * 0.4) + (cognitive * 0.4) + (max_depth * 0.2)
        
        if score <= 5:
            return "easy"
        elif score <= 10:
            return "medium"
        elif score <= 20:
            return "hard"
        else:
            return "expert"
    
    def _calculate_maintainability_index(
        self,
        lines: int,
        complexity: float,
        halstead_volume: float
    ) -> float:
        """
        Calculate maintainability index.
        计算可维护性指数。
        
        MI = max(0, (171 - 5.2 * ln(V) - 0.23 * G - 16.2 * ln(L)) * 100 / 171)
        Where:
        - V = Halstead Volume (simplified as module size)
        - G = Cyclomatic Complexity
        - L = Lines of Code
        """
        import math
        
        try:
            if lines == 0:
                return 100.0
            
            # Simplified calculation
            # 简化计算
            mi = 171 - 5.2 * math.log(halstead_volume + 1) - 0.23 * complexity - 16.2 * math.log(lines)
            mi = max(0, mi * 100 / 171)
            return round(mi, 2)
        except:
            return 50.0  # Default middle value
    
    def _detect_code_smells_python(
        self,
        functions: List[FunctionMetrics],
        classes: List[ClassMetrics]
    ) -> List[Dict[str, Any]]:
        """
        Detect common code smells.
        检测常见的代码异味。
        """
        smells = []
        
        # Long method / 过长方法
        for func in functions:
            if func.lines_of_code > 50:
                smells.append({
                    "type": "long_method",
                    "severity": "medium",
                    "location": func.name,
                    "message": f"方法过长 ({func.lines_of_code} 行)，建议拆分"
                })
            
            # Too many parameters / 参数过多
            if func.num_parameters > 5:
                smells.append({
                    "type": "too_many_parameters",
                    "severity": "medium",
                    "location": func.name,
                    "message": f"参数过多 ({func.num_parameters} 个)，考虑使用对象封装"
                })
            
            # High complexity / 高复杂度
            if func.cyclomatic_complexity > 10:
                smells.append({
                    "type": "high_complexity",
                    "severity": "high",
                    "location": func.name,
                    "message": f"圈复杂度过高 ({func.cyclomatic_complexity})，难以理解和测试"
                })
        
        # Large class / 过大类
        for cls in classes:
            if cls.num_methods > 20:
                smells.append({
                    "type": "large_class",
                    "severity": "high",
                    "location": cls.name,
                    "message": f"类过大 ({cls.num_methods} 个方法)，违反单一职责原则"
                })
        
        return smells
    
    def _detect_security_issues_python(self, content: str) -> List[Dict[str, Any]]:
        """
        Detect potential security issues.
        检测潜在的安全问题。
        """
        issues = []
        
        # Check for eval usage / 检查eval使用
        if 'eval(' in content:
            issues.append({
                "type": "dangerous_function",
                "severity": "critical",
                "message": "使用了 eval()，存在代码注入风险"
            })
        
        # Check for exec usage / 检查exec使用
        if 'exec(' in content:
            issues.append({
                "type": "dangerous_function",
                "severity": "critical",
                "message": "使用了 exec()，存在代码注入风险"
            })
        
        # Check for hardcoded secrets / 检查硬编码密钥
        secret_patterns = [
            (r'password\s*=\s*["\'][^"\']+["\']', "硬编码密码"),
            (r'api_key\s*=\s*["\'][^"\']+["\']', "硬编码API密钥"),
            (r'secret\s*=\s*["\'][^"\']+["\']', "硬编码密钥")
        ]
        
        for pattern, message in secret_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                issues.append({
                    "type": "hardcoded_secret",
                    "severity": "high",
                    "message": message
                })
        
        return issues
    
    def _inspect_java_file(self, file_path: Path, content: str) -> FileMetrics:
        """Inspect Java file (simplified)"""
        return self._inspect_generic_file(file_path, content, "java")
    
    def _inspect_javascript_file(self, file_path: Path, content: str) -> FileMetrics:
        """Inspect JavaScript/TypeScript file (simplified)"""
        return self._inspect_generic_file(file_path, content, "javascript")
    
    def _inspect_generic_file(self, file_path: Path, content: str, language: str) -> FileMetrics:
        """
        Generic file inspection for unsupported languages.
        不支持语言的通用文件检测。
        """
        lines = content.count('\n') + 1
        
        # Simple heuristics / 简单启发式
        num_functions = content.count('def ') + content.count('function ') + content.count('func ')
        num_classes = content.count('class ')
        num_imports = content.count('import ') + content.count('require(')
        
        return FileMetrics(
            file_path=str(file_path),
            language=language,
            lines_of_code=lines,
            num_functions=num_functions,
            num_classes=num_classes,
            num_imports=num_imports,
            complexity_score=5.0,  # Default
            maintainability_index=70.0  # Default
        )
    
    def _detect_language(self, file_path: Path) -> str:
        """Detect programming language from file extension"""
        extension_map = {
            '.py': 'python',
            '.java': 'java',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.go': 'go',
            '.cpp': 'cpp',
            '.c': 'c',
            '.rs': 'rust'
        }
        return extension_map.get(file_path.suffix, 'unknown')
    
    def _calculate_project_metrics(
        self,
        project_path: Path,
        file_metrics: List[FileMetrics],
        language_stats: Dict[str, int]
    ) -> ProjectMetrics:
        """Calculate project-level metrics"""
        total_files = len(file_metrics)
        total_lines = sum(f.lines_of_code for f in file_metrics)
        total_functions = sum(f.num_functions for f in file_metrics)
        total_classes = sum(f.num_classes for f in file_metrics)
        
        avg_complexity = sum(f.complexity_score for f in file_metrics) / total_files if total_files else 0
        
        # Determine overall difficulty
        # 确定整体难度
        if avg_complexity <= 5:
            difficulty = "beginner"
        elif avg_complexity <= 10:
            difficulty = "intermediate"
        elif avg_complexity <= 15:
            difficulty = "advanced"
        else:
            difficulty = "expert"
        
        return ProjectMetrics(
            project_name=project_path.name,
            total_files=total_files,
            total_lines=total_lines,
            total_functions=total_functions,
            total_classes=total_classes,
            languages=language_stats,
            avg_complexity=round(avg_complexity, 2),
            overall_difficulty=difficulty
        )
    
    def _detect_architecture(self, project_path: Path, file_metrics: List[FileMetrics]) -> Dict[str, Any]:
        """Detect architecture patterns"""
        patterns = []
        
        # Check for common directory structures
        # 检查常见目录结构
        dirs = set()
        for f in file_metrics:
            parts = Path(f.file_path).parts
            dirs.update(parts)
        
        if 'controller' in dirs or 'controllers' in dirs:
            patterns.append("MVC")
        
        if 'service' in dirs or 'services' in dirs:
            patterns.append("Service Layer")
        
        if 'repository' in dirs or 'repositories' in dirs:
            patterns.append("Repository Pattern")
        
        if 'model' in dirs or 'models' in dirs:
            patterns.append("Domain Model")
        
        return {
            "patterns": patterns,
            "structure": "layered" if len(patterns) > 2 else "simple"
        }
    
    def _detect_tech_stack(self, project_path: Path) -> List[str]:
        """Detect technology stack from project files"""
        tech_stack = []
        
        # Check for common files
        # 检查常见文件
        if (project_path / "requirements.txt").exists():
            tech_stack.append("Python/pip")
        
        if (project_path / "package.json").exists():
            tech_stack.append("Node.js/npm")
        
        if (project_path / "pom.xml").exists():
            tech_stack.append("Java/Maven")
        
        if (project_path / "build.gradle").exists():
            tech_stack.append("Java/Gradle")
        
        if (project_path / "go.mod").exists():
            tech_stack.append("Go")
        
        if (project_path / "Cargo.toml").exists():
            tech_stack.append("Rust/Cargo")
        
        return tech_stack
    
    def _detect_class_patterns(self, node: ast.ClassDef) -> List[str]:
        """Detect design patterns in class"""
        patterns = []
        class_name_lower = node.name.lower()
        
        for pattern, keywords in self.design_patterns.items():
            if any(keyword.lower() in class_name_lower for keyword in keywords):
                patterns.append(pattern)
        
        return patterns
    
    def _generate_summary(
        self,
        project_metrics: ProjectMetrics,
        file_metrics: List[FileMetrics]
    ) -> Dict[str, Any]:
        """Generate project summary"""
        # Count code smells and security issues
        # 统计代码异味和安全问题
        total_smells = sum(len(f.code_smells) for f in file_metrics)
        total_security = sum(len(f.security_issues) for f in file_metrics)
        
        # Calculate average maintainability
        # 计算平均可维护性
        avg_maintainability = sum(f.maintainability_index for f in file_metrics) / len(file_metrics) if file_metrics else 0
        
        return {
            "health_score": self._calculate_health_score(project_metrics, total_smells, total_security, avg_maintainability),
            "total_code_smells": total_smells,
            "total_security_issues": total_security,
            "avg_maintainability": round(avg_maintainability, 2),
            "recommendation": self._generate_recommendation(project_metrics, total_smells, total_security)
        }
    
    def _calculate_health_score(
        self,
        project_metrics: ProjectMetrics,
        total_smells: int,
        total_security: int,
        avg_maintainability: float
    ) -> float:
        """Calculate overall project health score (0-100)"""
        score = 100.0
        
        # Deduct for complexity
        # 复杂度扣分
        score -= min(project_metrics.avg_complexity * 2, 30)
        
        # Deduct for code smells
        # 代码异味扣分
        score -= min(total_smells * 2, 30)
        
        # Deduct for security issues
        # 安全问题扣分
        score -= min(total_security * 5, 30)
        
        # Add for maintainability
        # 可维护性加分
        score += (avg_maintainability - 50) * 0.2
        
        return max(0, min(100, round(score, 2)))
    
    def _generate_recommendation(
        self,
        project_metrics: ProjectMetrics,
        total_smells: int,
        total_security: int
    ) -> str:
        """Generate recommendation based on metrics"""
        if total_security > 0:
            return "⚠️ 发现安全问题，建议立即修复"
        elif total_smells > 10:
            return "⚠️ 代码异味较多，建议重构"
        elif project_metrics.avg_complexity > 15:
            return "⚠️ 整体复杂度过高，建议简化逻辑"
        else:
            return "✅ 代码质量良好"

