"""
Multi-AI Code Optimizer / 多AI代码优化器

Uses multiple AI models to analyze code and provide optimization suggestions.
使用多个AI模型分析代码并提供优化建议。

Features / 功能:
- Multi-AI analysis / 多AI分析
- Suggestion aggregation / 建议聚合
- Priority ranking / 优先级排序
- Implementation roadmap / 实施路线图
"""

import asyncio
from pathlib import Path
from typing import List, Dict, Any, Optional
from loguru import logger
from dataclasses import dataclass, field
from collections import Counter
import json


@dataclass
class OptimizationSuggestion:
    """Single optimization suggestion / 单个优化建议"""
    category: str  # performance, readability, security, architecture, etc.
    title: str
    description: str
    priority: str  # critical, high, medium, low
    effort: str  # low, medium, high
    impact: str  # low, medium, high
    code_location: Optional[str] = None
    before_code: Optional[str] = None
    after_code: Optional[str] = None
    reasoning: Optional[str] = None
    suggested_by: List[str] = field(default_factory=list)  # Which AI models suggested this
    confidence_score: float = 0.0


@dataclass
class OptimizationReport:
    """Complete optimization report / 完整优化报告"""
    file_path: str
    language: str
    total_suggestions: int
    suggestions_by_category: Dict[str, int]
    suggestions_by_priority: Dict[str, int]
    consensus_suggestions: List[OptimizationSuggestion]  # Agreed by multiple AIs
    unique_suggestions: List[OptimizationSuggestion]  # From single AI
    implementation_roadmap: List[Dict[str, Any]]
    estimated_effort: str
    expected_impact: str


class CodeOptimizer:
    """
    Multi-AI Code Optimizer / 多AI代码优化器
    
    Coordinates multiple AI models to analyze code and provide optimization suggestions.
    协调多个AI模型分析代码并提供优化建议。
    """
    
    def __init__(self, ai_models: Optional[List[str]] = None):
        """
        Initialize optimizer with AI models.
        使用AI模型初始化优化器。
        
        Args:
            ai_models: List of AI model names to use.
                      要使用的AI模型名称列表。
        """
        self.ai_models = ai_models or ["gpt-4o", "claude-3.5-sonnet", "gemini-pro", "deepseek-coder"]
        
        self.category_weights = {
            "performance": 1.0,
            "security": 1.2,  # Security is more important
            "readability": 0.8,
            "maintainability": 0.9,
            "architecture": 1.0,
            "best_practices": 0.7,
            "error_handling": 1.1
        }
        
        self.priority_scores = {
            "critical": 10,
            "high": 7,
            "medium": 5,
            "low": 2
        }
        
        self.effort_multipliers = {
            "low": 1.0,
            "medium": 0.7,
            "high": 0.4
        }
    
    async def analyze_and_optimize(
        self,
        file_path: Path,
        language: str,
        use_multi_ai: bool = True,
        consensus_threshold: int = 2
    ) -> OptimizationReport:
        """
        Analyze code using multiple AIs and generate optimization suggestions.
        使用多个AI分析代码并生成优化建议。
        
        Args:
            file_path: Path to code file.
                      代码文件路径。
            language: Programming language.
                     编程语言。
            use_multi_ai: Whether to use multiple AI models.
                         是否使用多个AI模型。
            consensus_threshold: Minimum number of AIs that must agree for consensus.
                               达成共识所需的最少AI数量。
        
        Returns:
            OptimizationReport with all suggestions.
            包含所有建议的优化报告。
        """
        logger.info(f"开始多AI优化分析: {file_path}")
        
        # Read code file
        # 读取代码文件
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            code_content = f.read()
        
        if use_multi_ai:
            # Get suggestions from multiple AIs
            # 从多个AI获取建议
            all_suggestions = await self._get_multi_ai_suggestions(
                code_content,
                language,
                str(file_path)
            )
        else:
            # Use single AI
            # 使用单个AI
            suggestions = await self._get_single_ai_suggestions(
                code_content,
                language,
                str(file_path),
                self.ai_models[0]
            )
            all_suggestions = {self.ai_models[0]: suggestions}
        
        # Merge and analyze suggestions
        # 合并和分析建议
        consensus_suggestions, unique_suggestions = self._merge_suggestions(
            all_suggestions,
            consensus_threshold
        )
        
        # Rank suggestions by priority and impact
        # 按优先级和影响排序建议
        consensus_suggestions = self._rank_suggestions(consensus_suggestions)
        unique_suggestions = self._rank_suggestions(unique_suggestions)
        
        # Generate implementation roadmap
        # 生成实施路线图
        roadmap = self._generate_roadmap(consensus_suggestions, unique_suggestions)
        
        # Calculate statistics
        # 计算统计信息
        all_merged = consensus_suggestions + unique_suggestions
        
        suggestions_by_category = Counter(s.category for s in all_merged)
        suggestions_by_priority = Counter(s.priority for s in all_merged)
        
        # Estimate overall effort and impact
        # 估算总体工作量和影响
        estimated_effort = self._estimate_effort(all_merged)
        expected_impact = self._estimate_impact(all_merged)
        
        report = OptimizationReport(
            file_path=str(file_path),
            language=language,
            total_suggestions=len(all_merged),
            suggestions_by_category=dict(suggestions_by_category),
            suggestions_by_priority=dict(suggestions_by_priority),
            consensus_suggestions=consensus_suggestions,
            unique_suggestions=unique_suggestions,
            implementation_roadmap=roadmap,
            estimated_effort=estimated_effort,
            expected_impact=expected_impact
        )
        
        logger.info(f"优化分析完成: {len(all_merged)} 个建议")
        return report
    
    async def _get_multi_ai_suggestions(
        self,
        code: str,
        language: str,
        file_path: str
    ) -> Dict[str, List[OptimizationSuggestion]]:
        """
        Get optimization suggestions from multiple AI models.
        从多个AI模型获取优化建议。
        """
        tasks = []
        
        for model in self.ai_models:
            task = self._get_single_ai_suggestions(code, language, file_path, model)
            tasks.append(task)
        
        # Run all AI analyses in parallel
        # 并行运行所有AI分析
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Organize results by model
        # 按模型组织结果
        suggestions_by_model = {}
        
        for i, result in enumerate(results):
            model = self.ai_models[i]
            
            if isinstance(result, Exception):
                logger.error(f"AI模型 {model} 分析失败: {result}")
                suggestions_by_model[model] = []
            else:
                suggestions_by_model[model] = result
                logger.info(f"AI模型 {model} 提供了 {len(result)} 个建议")
        
        return suggestions_by_model
    
    async def _get_single_ai_suggestions(
        self,
        code: str,
        language: str,
        file_path: str,
        model: str
    ) -> List[OptimizationSuggestion]:
        """
        Get optimization suggestions from a single AI model.
        从单个AI模型获取优化建议。
        """
        # Build prompt for AI
        # 构建AI提示词
        prompt = self._build_optimization_prompt(code, language, file_path)
        
        try:
            # Call AI model (this would integrate with actual AI APIs)
            # 调用AI模型（这将与实际的AI API集成）
            response = await self._call_ai_model(model, prompt)
            
            # Parse AI response into structured suggestions
            # 将AI响应解析为结构化建议
            suggestions = self._parse_ai_response(response, model)
            
            return suggestions
        
        except Exception as e:
            logger.error(f"AI模型 {model} 调用失败: {e}")
            return []
    
    def _build_optimization_prompt(self, code: str, language: str, file_path: str) -> str:
        """
        Build optimization prompt for AI.
        为AI构建优化提示词。
        """
        prompt = f"""You are an expert code reviewer and optimization specialist.

Analyze the following {language} code and provide detailed optimization suggestions.

File: {file_path}

Code:
```{language}
{code}
```

Please provide optimization suggestions in the following categories:
1. Performance - Speed improvements, algorithm optimization
2. Security - Security vulnerabilities, input validation
3. Readability - Code clarity, naming conventions
4. Maintainability - Code structure, modularity
5. Architecture - Design patterns, SOLID principles
6. Best Practices - Language-specific best practices
7. Error Handling - Exception handling, edge cases

For each suggestion, provide:
- Category
- Title (brief description)
- Description (detailed explanation)
- Priority (critical, high, medium, low)
- Effort (low, medium, high)
- Impact (low, medium, high)
- Code location (line numbers or function name)
- Before code (current problematic code)
- After code (improved code)
- Reasoning (why this optimization is important)

Return your response as a JSON array of suggestions.

Example format:
[
  {{
    "category": "performance",
    "title": "Use list comprehension instead of loop",
    "description": "List comprehensions are faster and more Pythonic",
    "priority": "medium",
    "effort": "low",
    "impact": "medium",
    "code_location": "lines 45-50",
    "before_code": "result = []\\nfor item in items:\\n    result.append(item * 2)",
    "after_code": "result = [item * 2 for item in items]",
    "reasoning": "List comprehensions are optimized in Python and reduce code verbosity"
  }}
]

Important: Only provide actionable, specific suggestions. Avoid generic advice.
"""
        return prompt
    
    async def _call_ai_model(self, model: str, prompt: str) -> str:
        """
        Call AI model API.
        调用AI模型API。
        
        Note: This is a placeholder. In production, integrate with actual AI APIs.
        注意: 这是一个占位符。在生产环境中，需要集成实际的AI API。
        """
        # Simulate AI call
        # 模拟AI调用
        await asyncio.sleep(0.1)  # Simulate API call delay
        
        # Return mock response for demonstration
        # 返回模拟响应用于演示
        mock_response = json.dumps([
            {
                "category": "performance",
                "title": f"[{model}] Optimize loop iteration",
                "description": "Use more efficient iteration method",
                "priority": "medium",
                "effort": "low",
                "impact": "medium",
                "code_location": "function main",
                "before_code": "for i in range(len(items)):\\n    process(items[i])",
                "after_code": "for item in items:\\n    process(item)",
                "reasoning": "Direct iteration is more efficient and readable"
            },
            {
                "category": "security",
                "title": f"[{model}] Validate user input",
                "description": "Add input validation to prevent injection attacks",
                "priority": "high",
                "effort": "medium",
                "impact": "high",
                "code_location": "function process_input",
                "before_code": "query = f'SELECT * FROM users WHERE id = {user_id}'",
                "after_code": "query = 'SELECT * FROM users WHERE id = ?'\\ndb.execute(query, (user_id,))",
                "reasoning": "Prevents SQL injection vulnerabilities"
            }
        ])
        
        return mock_response
    
    def _parse_ai_response(self, response: str, model: str) -> List[OptimizationSuggestion]:
        """
        Parse AI response into structured suggestions.
        将AI响应解析为结构化建议。
        """
        try:
            suggestions_data = json.loads(response)
            
            suggestions = []
            for data in suggestions_data:
                suggestion = OptimizationSuggestion(
                    category=data.get("category", "general"),
                    title=data.get("title", ""),
                    description=data.get("description", ""),
                    priority=data.get("priority", "medium"),
                    effort=data.get("effort", "medium"),
                    impact=data.get("impact", "medium"),
                    code_location=data.get("code_location"),
                    before_code=data.get("before_code"),
                    after_code=data.get("after_code"),
                    reasoning=data.get("reasoning"),
                    suggested_by=[model],
                    confidence_score=0.8  # Base confidence
                )
                suggestions.append(suggestion)
            
            return suggestions
        
        except json.JSONDecodeError as e:
            logger.error(f"解析AI响应失败 ({model}): {e}")
            return []
    
    def _merge_suggestions(
        self,
        all_suggestions: Dict[str, List[OptimizationSuggestion]],
        consensus_threshold: int
    ) -> tuple[List[OptimizationSuggestion], List[OptimizationSuggestion]]:
        """
        Merge suggestions from multiple AIs.
        合并多个AI的建议。
        
        Returns:
            (consensus_suggestions, unique_suggestions)
            (共识建议, 独特建议)
        """
        # Group similar suggestions
        # 分组相似的建议
        suggestion_groups = {}
        
        for model, suggestions in all_suggestions.items():
            for suggestion in suggestions:
                # Create a key based on category and title similarity
                # 基于类别和标题相似性创建键
                key = self._create_suggestion_key(suggestion)
                
                if key not in suggestion_groups:
                    suggestion_groups[key] = []
                
                suggestion_groups[key].append(suggestion)
        
        # Separate consensus and unique suggestions
        # 分离共识和独特建议
        consensus_suggestions = []
        unique_suggestions = []
        
        for key, group in suggestion_groups.items():
            if len(group) >= consensus_threshold:
                # Multiple AIs agree - this is a consensus suggestion
                # 多个AI同意 - 这是共识建议
                merged = self._merge_similar_suggestions(group)
                merged.confidence_score = len(group) / len(self.ai_models)  # Confidence based on agreement
                consensus_suggestions.append(merged)
            else:
                # Unique suggestion from single AI
                # 来自单个AI的独特建议
                for suggestion in group:
                    suggestion.confidence_score = 1.0 / len(self.ai_models)  # Lower confidence
                    unique_suggestions.append(suggestion)
        
        logger.info(f"共识建议: {len(consensus_suggestions)}, 独特建议: {len(unique_suggestions)}")
        
        return consensus_suggestions, unique_suggestions
    
    def _create_suggestion_key(self, suggestion: OptimizationSuggestion) -> str:
        """
        Create a unique key for suggestion grouping.
        创建用于建议分组的唯一键。
        """
        # Normalize title for comparison
        # 规范化标题以进行比较
        normalized_title = suggestion.title.lower()
        
        # Remove model-specific prefixes
        # 移除模型特定的前缀
        for model in self.ai_models:
            normalized_title = normalized_title.replace(f"[{model}]", "")
        
        normalized_title = normalized_title.strip()
        
        return f"{suggestion.category}:{normalized_title}"
    
    def _merge_similar_suggestions(
        self,
        suggestions: List[OptimizationSuggestion]
    ) -> OptimizationSuggestion:
        """
        Merge similar suggestions from different AIs.
        合并来自不同AI的相似建议。
        """
        # Use the first suggestion as base
        # 使用第一个建议作为基础
        merged = suggestions[0]
        
        # Collect all AI models that suggested this
        # 收集所有建议此项的AI模型
        merged.suggested_by = []
        for s in suggestions:
            merged.suggested_by.extend(s.suggested_by)
        
        # Merge descriptions
        # 合并描述
        unique_descriptions = []
        for s in suggestions:
            if s.description not in unique_descriptions:
                unique_descriptions.append(s.description)
        
        merged.description = " | ".join(unique_descriptions)
        
        # Take highest priority
        # 取最高优先级
        priorities = [self.priority_scores.get(s.priority, 0) for s in suggestions]
        max_priority_idx = priorities.index(max(priorities))
        merged.priority = suggestions[max_priority_idx].priority
        
        # Merge reasoning
        # 合并推理
        unique_reasoning = []
        for s in suggestions:
            if s.reasoning and s.reasoning not in unique_reasoning:
                unique_reasoning.append(s.reasoning)
        
        if unique_reasoning:
            merged.reasoning = " | ".join(unique_reasoning)
        
        return merged
    
    def _rank_suggestions(
        self,
        suggestions: List[OptimizationSuggestion]
    ) -> List[OptimizationSuggestion]:
        """
        Rank suggestions by priority and impact.
        按优先级和影响排序建议。
        """
        def calculate_score(s: OptimizationSuggestion) -> float:
            priority_score = self.priority_scores.get(s.priority, 5)
            category_weight = self.category_weights.get(s.category, 1.0)
            effort_multiplier = self.effort_multipliers.get(s.effort, 1.0)
            
            # Impact score
            impact_scores = {"low": 1, "medium": 2, "high": 3}
            impact_score = impact_scores.get(s.impact, 2)
            
            # Final score = priority * category_weight * impact * effort_multiplier * confidence
            score = priority_score * category_weight * impact_score * effort_multiplier * s.confidence_score
            
            return score
        
        # Sort by score descending
        # 按分数降序排序
        ranked = sorted(suggestions, key=calculate_score, reverse=True)
        
        return ranked
    
    def _generate_roadmap(
        self,
        consensus_suggestions: List[OptimizationSuggestion],
        unique_suggestions: List[OptimizationSuggestion]
    ) -> List[Dict[str, Any]]:
        """
        Generate implementation roadmap.
        生成实施路线图。
        """
        roadmap = []
        
        # Phase 1: Critical and High Priority Consensus Items
        # 阶段1: 关键和高优先级共识项
        phase1_items = [
            s for s in consensus_suggestions
            if s.priority in ["critical", "high"]
        ]
        
        if phase1_items:
            roadmap.append({
                "phase": 1,
                "name": "关键优化 (Critical Fixes)",
                "priority": "立即执行",
                "estimated_time": self._estimate_phase_time(phase1_items),
                "items": [
                    {
                        "title": s.title,
                        "category": s.category,
                        "effort": s.effort,
                        "impact": s.impact
                    }
                    for s in phase1_items
                ]
            })
        
        # Phase 2: Medium Priority Consensus Items
        # 阶段2: 中优先级共识项
        phase2_items = [
            s for s in consensus_suggestions
            if s.priority == "medium"
        ]
        
        if phase2_items:
            roadmap.append({
                "phase": 2,
                "name": "重要改进 (Important Improvements)",
                "priority": "短期内执行",
                "estimated_time": self._estimate_phase_time(phase2_items),
                "items": [
                    {
                        "title": s.title,
                        "category": s.category,
                        "effort": s.effort,
                        "impact": s.impact
                    }
                    for s in phase2_items
                ]
            })
        
        # Phase 3: Low Priority and Unique Suggestions
        # 阶段3: 低优先级和独特建议
        phase3_items = (
            [s for s in consensus_suggestions if s.priority == "low"] +
            [s for s in unique_suggestions if s.priority in ["high", "medium"]]
        )
        
        if phase3_items:
            roadmap.append({
                "phase": 3,
                "name": "优化提升 (Enhancements)",
                "priority": "中长期规划",
                "estimated_time": self._estimate_phase_time(phase3_items),
                "items": [
                    {
                        "title": s.title,
                        "category": s.category,
                        "effort": s.effort,
                        "impact": s.impact
                    }
                    for s in phase3_items
                ]
            })
        
        return roadmap
    
    def _estimate_phase_time(self, suggestions: List[OptimizationSuggestion]) -> str:
        """
        Estimate time needed for a phase.
        估算阶段所需时间。
        """
        effort_hours = {
            "low": 2,
            "medium": 8,
            "high": 24
        }
        
        total_hours = sum(effort_hours.get(s.effort, 8) for s in suggestions)
        
        if total_hours <= 8:
            return "< 1 天"
        elif total_hours <= 40:
            return f"{total_hours // 8} 天"
        else:
            return f"{total_hours // 40} 周"
    
    def _estimate_effort(self, suggestions: List[OptimizationSuggestion]) -> str:
        """
        Estimate overall effort.
        估算总体工作量。
        """
        effort_counts = Counter(s.effort for s in suggestions)
        
        if effort_counts.get("high", 0) > 3:
            return "high"
        elif effort_counts.get("medium", 0) > 5:
            return "medium"
        else:
            return "low"
    
    def _estimate_impact(self, suggestions: List[OptimizationSuggestion]) -> str:
        """
        Estimate expected impact.
        估算预期影响。
        """
        impact_counts = Counter(s.impact for s in suggestions)
        
        if impact_counts.get("high", 0) >= 3:
            return "high"
        elif impact_counts.get("medium", 0) >= 5:
            return "medium"
        else:
            return "low"

