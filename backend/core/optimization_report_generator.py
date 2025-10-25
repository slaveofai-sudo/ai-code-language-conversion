"""
Optimization Report Generator / 优化报告生成器

Generates detailed optimization reports from multi-AI analysis.
从多AI分析生成详细的优化报告。

Features / 功能:
- Markdown report generation / Markdown报告生成
- Consensus analysis / 共识分析
- Implementation guidance / 实施指导
- Visual priority matrix / 可视化优先级矩阵
"""

from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
from loguru import logger


class OptimizationReportGenerator:
    """
    Optimization Report Generator / 优化报告生成器
    
    Generates comprehensive optimization reports.
    生成全面的优化报告。
    """
    
    def __init__(self):
        self.priority_emojis = {
            "critical": "🔴",
            "high": "🟠",
            "medium": "🟡",
            "low": "🟢"
        }
        
        self.category_emojis = {
            "performance": "⚡",
            "security": "🔒",
            "readability": "📖",
            "maintainability": "🔧",
            "architecture": "🏛️",
            "best_practices": "✨",
            "error_handling": "⚠️"
        }
    
    def generate_report(
        self,
        optimization_report: Any,  # OptimizationReport
        output_format: str = "markdown"
    ) -> str:
        """
        Generate optimization report.
        生成优化报告。
        
        Args:
            optimization_report: OptimizationReport object.
                                优化报告对象。
            output_format: Output format (markdown/json).
                          输出格式。
        
        Returns:
            Generated report string.
            生成的报告字符串。
        """
        if output_format == "markdown":
            return self._generate_markdown_report(optimization_report)
        elif output_format == "json":
            return self._generate_json_report(optimization_report)
        else:
            raise ValueError(f"Unsupported format: {output_format}")
    
    def _generate_markdown_report(self, report: Any) -> str:
        """
        Generate Markdown format report.
        生成Markdown格式报告。
        """
        doc = []
        
        # Title
        # 标题
        doc.append(f"# 🚀 代码优化建议报告")
        doc.append("")
        doc.append(f"**文件**: `{report.file_path}`")
        doc.append(f"**语言**: {report.language}")
        doc.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        doc.append("")
        doc.append("---")
        doc.append("")
        
        # Executive Summary
        # 执行摘要
        doc.append("## 📊 执行摘要")
        doc.append("")
        doc.append(f"- **总建议数**: {report.total_suggestions}")
        doc.append(f"- **共识建议**: {len(report.consensus_suggestions)} (多个AI认同)")
        doc.append(f"- **独特建议**: {len(report.unique_suggestions)} (单个AI提出)")
        doc.append(f"- **预估工作量**: {self._format_effort(report.estimated_effort)}")
        doc.append(f"- **预期影响**: {self._format_impact(report.expected_impact)}")
        doc.append("")
        
        # Priority Distribution
        # 优先级分布
        doc.append("### 优先级分布")
        doc.append("")
        for priority, count in sorted(report.suggestions_by_priority.items(), 
                                     key=lambda x: self._priority_order(x[0])):
            emoji = self.priority_emojis.get(priority, "⚪")
            bar = "█" * min(count, 20)
            doc.append(f"{emoji} **{priority.title()}**: {bar} {count} 项")
        doc.append("")
        
        # Category Distribution
        # 类别分布
        doc.append("### 类别分布")
        doc.append("")
        for category, count in sorted(report.suggestions_by_category.items(), 
                                     key=lambda x: x[1], reverse=True):
            emoji = self.category_emojis.get(category, "📋")
            doc.append(f"{emoji} **{category.title()}**: {count} 项")
        doc.append("")
        doc.append("---")
        doc.append("")
        
        # Consensus Suggestions
        # 共识建议
        doc.append("## 🤝 共识优化建议")
        doc.append("")
        doc.append("以下建议得到多个AI模型的一致认可，建议优先实施。")
        doc.append("")
        
        if report.consensus_suggestions:
            for i, suggestion in enumerate(report.consensus_suggestions, 1):
                doc.append(self._format_suggestion(i, suggestion, is_consensus=True))
        else:
            doc.append("*暂无共识建议*")
            doc.append("")
        
        doc.append("---")
        doc.append("")
        
        # Unique Suggestions
        # 独特建议
        doc.append("## 💡 独特优化建议")
        doc.append("")
        doc.append("以下建议由单个AI模型提出，可作为参考或进一步验证。")
        doc.append("")
        
        if report.unique_suggestions:
            for i, suggestion in enumerate(report.unique_suggestions, 1):
                doc.append(self._format_suggestion(i, suggestion, is_consensus=False))
        else:
            doc.append("*暂无独特建议*")
            doc.append("")
        
        doc.append("---")
        doc.append("")
        
        # Implementation Roadmap
        # 实施路线图
        doc.append("## 🗺️ 实施路线图")
        doc.append("")
        doc.append("根据优先级和影响，建议按以下阶段实施优化：")
        doc.append("")
        
        for phase in report.implementation_roadmap:
            doc.append(f"### 阶段 {phase['phase']}: {phase['name']}")
            doc.append("")
            doc.append(f"- **优先级**: {phase['priority']}")
            doc.append(f"- **预估时间**: {phase['estimated_time']}")
            doc.append(f"- **优化项数**: {len(phase['items'])}")
            doc.append("")
            doc.append("**具体项目**:")
            doc.append("")
            
            for item in phase['items']:
                emoji = self.category_emojis.get(item['category'], "📋")
                doc.append(f"- {emoji} {item['title']}")
                doc.append(f"  - 工作量: {item['effort']} | 影响: {item['impact']}")
            
            doc.append("")
        
        doc.append("---")
        doc.append("")
        
        # Priority Matrix
        # 优先级矩阵
        doc.append("## 📈 优先级矩阵")
        doc.append("")
        doc.append("根据影响和工作量的优先级矩阵：")
        doc.append("")
        doc.append("```")
        doc.append("              影响 (Impact)")
        doc.append("               High  |  Medium  |  Low")
        doc.append("          --------------------------------")
        doc.append(" 工作量  Low   |  ★★★  |   ★★   |   ★")
        doc.append(" (Effort) Med  |  ★★   |   ★★   |   ★")
        doc.append("         High  |  ★★   |   ★    |   ☆")
        doc.append("")
        doc.append("★★★ = 最高优先级 (Quick Wins)")
        doc.append("★★  = 高优先级")
        doc.append("★   = 中优先级")
        doc.append("☆   = 低优先级")
        doc.append("```")
        doc.append("")
        
        # Generate distribution
        # 生成分布
        doc.append(self._generate_priority_matrix(report))
        doc.append("")
        doc.append("---")
        doc.append("")
        
        # Recommendations
        # 建议
        doc.append("## 💬 实施建议")
        doc.append("")
        doc.append("### ✅ 立即行动项 (Quick Wins)")
        doc.append("")
        
        quick_wins = [
            s for s in report.consensus_suggestions
            if s.effort == "low" and s.impact in ["high", "medium"]
        ]
        
        if quick_wins:
            for s in quick_wins:
                doc.append(f"- {s.title}")
        else:
            doc.append("- 暂无立即可执行的Quick Wins项")
        
        doc.append("")
        doc.append("### ⚠️ 需要注意的风险")
        doc.append("")
        
        critical_items = [
            s for s in report.consensus_suggestions + report.unique_suggestions
            if s.priority == "critical" or s.category == "security"
        ]
        
        if critical_items:
            for s in critical_items:
                doc.append(f"- **{s.title}**: {s.description}")
        else:
            doc.append("- 未发现关键风险")
        
        doc.append("")
        doc.append("### 📚 学习和研究项")
        doc.append("")
        doc.append("以下建议需要进一步学习或研究：")
        doc.append("")
        
        research_items = [
            s for s in report.unique_suggestions
            if s.effort == "high" or s.category == "architecture"
        ]
        
        if research_items:
            for s in research_items[:5]:  # Top 5
                doc.append(f"- {s.title}")
        else:
            doc.append("- 暂无需要深入研究的项目")
        
        doc.append("")
        doc.append("---")
        doc.append("")
        
        # Footer
        # 页脚
        doc.append("## 📝 附录")
        doc.append("")
        doc.append("### AI模型贡献分析")
        doc.append("")
        
        # Count contributions by AI model
        # 统计AI模型的贡献
        ai_contributions = {}
        for s in report.consensus_suggestions + report.unique_suggestions:
            for ai in s.suggested_by:
                ai_contributions[ai] = ai_contributions.get(ai, 0) + 1
        
        doc.append("| AI模型 | 建议数 | 贡献度 |")
        doc.append("|--------|--------|--------|")
        
        total_suggestions = sum(ai_contributions.values())
        for ai, count in sorted(ai_contributions.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_suggestions * 100) if total_suggestions > 0 else 0
            doc.append(f"| {ai} | {count} | {percentage:.1f}% |")
        
        doc.append("")
        doc.append("### 术语解释")
        doc.append("")
        doc.append("- **共识建议**: 至少2个AI模型提出的相似建议，可信度更高")
        doc.append("- **独特建议**: 仅由1个AI模型提出的建议，需要进一步评估")
        doc.append("- **工作量**: 实施该优化所需的时间和精力")
        doc.append("- **影响**: 该优化对代码质量或性能的改善程度")
        doc.append("- **置信度分数**: 基于AI模型一致性的可信度评分")
        doc.append("")
        doc.append("---")
        doc.append("")
        doc.append(f"*🤖 报告由多AI协同分析生成 | 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        
        return "\n".join(doc)
    
    def _format_suggestion(self, index: int, suggestion: Any, is_consensus: bool) -> str:
        """
        Format a single suggestion.
        格式化单个建议。
        """
        lines = []
        
        # Header
        # 标题
        priority_emoji = self.priority_emojis.get(suggestion.priority, "⚪")
        category_emoji = self.category_emojis.get(suggestion.category, "📋")
        
        lines.append(f"### {index}. {priority_emoji} {suggestion.title}")
        lines.append("")
        
        # Metadata
        # 元数据
        lines.append(f"**类别**: {category_emoji} {suggestion.category.title()}")
        lines.append(f"**优先级**: {suggestion.priority.upper()}")
        lines.append(f"**工作量**: {suggestion.effort} | **影响**: {suggestion.impact}")
        
        if is_consensus:
            lines.append(f"**建议来源**: {', '.join(suggestion.suggested_by)}")
            lines.append(f"**置信度**: {suggestion.confidence_score:.0%}")
        else:
            lines.append(f"**建议来源**: {suggestion.suggested_by[0]}")
        
        if suggestion.code_location:
            lines.append(f"**代码位置**: {suggestion.code_location}")
        
        lines.append("")
        
        # Description
        # 描述
        lines.append("**说明**:")
        lines.append(f"{suggestion.description}")
        lines.append("")
        
        # Code comparison
        # 代码对比
        if suggestion.before_code and suggestion.after_code:
            lines.append("**优化前**:")
            lines.append("```python")
            lines.append(suggestion.before_code)
            lines.append("```")
            lines.append("")
            lines.append("**优化后**:")
            lines.append("```python")
            lines.append(suggestion.after_code)
            lines.append("```")
            lines.append("")
        
        # Reasoning
        # 推理
        if suggestion.reasoning:
            lines.append("**原因**:")
            lines.append(f"{suggestion.reasoning}")
            lines.append("")
        
        lines.append("---")
        lines.append("")
        
        return "\n".join(lines)
    
    def _generate_priority_matrix(self, report: Any) -> str:
        """
        Generate priority matrix distribution.
        生成优先级矩阵分布。
        """
        lines = []
        
        # Count suggestions by effort and impact
        # 按工作量和影响统计建议
        matrix = {
            "low": {"high": [], "medium": [], "low": []},
            "medium": {"high": [], "medium": [], "low": []},
            "high": {"high": [], "medium": [], "low": []}
        }
        
        all_suggestions = report.consensus_suggestions + report.unique_suggestions
        
        for s in all_suggestions:
            effort = s.effort if s.effort in ["low", "medium", "high"] else "medium"
            impact = s.impact if s.impact in ["low", "medium", "high"] else "medium"
            matrix[effort][impact].append(s)
        
        lines.append("**分布详情**:")
        lines.append("")
        
        for effort in ["low", "medium", "high"]:
            for impact in ["high", "medium", "low"]:
                items = matrix[effort][impact]
                if items:
                    lines.append(f"**工作量={effort.title()}, 影响={impact.title()}**: {len(items)} 项")
                    for item in items[:3]:  # Show top 3
                        lines.append(f"  - {item.title}")
                    if len(items) > 3:
                        lines.append(f"  - ... 还有 {len(items) - 3} 项")
                    lines.append("")
        
        return "\n".join(lines)
    
    def _format_effort(self, effort: str) -> str:
        """Format effort string"""
        effort_map = {
            "low": "🟢 低 (< 1天)",
            "medium": "🟡 中 (1-3天)",
            "high": "🔴 高 (> 3天)"
        }
        return effort_map.get(effort, effort)
    
    def _format_impact(self, impact: str) -> str:
        """Format impact string"""
        impact_map = {
            "low": "🟢 低",
            "medium": "🟡 中",
            "high": "🔴 高"
        }
        return impact_map.get(impact, impact)
    
    def _priority_order(self, priority: str) -> int:
        """Get priority order for sorting"""
        order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        return order.get(priority, 4)
    
    def _generate_json_report(self, report: Any) -> str:
        """
        Generate JSON format report.
        生成JSON格式报告。
        """
        import json
        
        def suggestion_to_dict(s):
            return {
                "category": s.category,
                "title": s.title,
                "description": s.description,
                "priority": s.priority,
                "effort": s.effort,
                "impact": s.impact,
                "code_location": s.code_location,
                "before_code": s.before_code,
                "after_code": s.after_code,
                "reasoning": s.reasoning,
                "suggested_by": s.suggested_by,
                "confidence_score": s.confidence_score
            }
        
        report_dict = {
            "file_path": report.file_path,
            "language": report.language,
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_suggestions": report.total_suggestions,
                "consensus_suggestions": len(report.consensus_suggestions),
                "unique_suggestions": len(report.unique_suggestions),
                "estimated_effort": report.estimated_effort,
                "expected_impact": report.expected_impact
            },
            "suggestions_by_category": report.suggestions_by_category,
            "suggestions_by_priority": report.suggestions_by_priority,
            "consensus_suggestions": [suggestion_to_dict(s) for s in report.consensus_suggestions],
            "unique_suggestions": [suggestion_to_dict(s) for s in report.unique_suggestions],
            "implementation_roadmap": report.implementation_roadmap
        }
        
        return json.dumps(report_dict, indent=2, ensure_ascii=False)

