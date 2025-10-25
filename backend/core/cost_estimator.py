"""
Cost Estimator / 成本估算器

Estimates the cost and time for code conversion before execution.
在执行前估算代码转换的成本和时间。

Features / 功能:
- Cost estimation by AI model / 按AI模型估算成本
- Time estimation / 时间估算
- Alternative suggestions / 替代方案建议
- Budget tracking / 预算追踪
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from loguru import logger


@dataclass
class CostEstimate:
    """
    Cost estimation result / 成本估算结果
    
    Attributes:
        total_tokens: Estimated total tokens / 估算的总token数
        input_tokens: Input tokens / 输入token数
        output_tokens: Output tokens / 输出token数
        cost_usd: Estimated cost in USD / 估算成本（美元）
        time_minutes: Estimated time in minutes / 估算时间（分钟）
        ai_model: AI model used / 使用的AI模型
        alternative_options: Cheaper alternatives / 更便宜的替代方案
        savings_potential_usd: Potential savings / 潜在节省金额
    """
    total_tokens: int
    input_tokens: int
    output_tokens: int
    cost_usd: float
    time_minutes: float
    ai_model: str
    alternative_options: List[Dict[str, Any]]
    savings_potential_usd: float


class CostEstimator:
    """
    Cost Estimator / 成本估算器
    
    Provides cost and time estimates for code conversion.
    为代码转换提供成本和时间估算。
    """
    
    # AI Model pricing (per 1K tokens) / AI模型定价（每1K tokens）
    # Updated as of 2024
    MODEL_PRICES = {
        "gpt-4": {
            "input": 0.03,
            "output": 0.06,
            "speed_factor": 1.0,
            "quality": 0.95
        },
        "gpt-4o": {
            "input": 0.005,
            "output": 0.015,
            "speed_factor": 1.5,
            "quality": 0.95
        },
        "claude-3.5-sonnet": {
            "input": 0.003,
            "output": 0.015,
            "speed_factor": 1.3,
            "quality": 0.96
        },
        "gemini-pro": {
            "input": 0.00025,
            "output": 0.0005,
            "speed_factor": 1.4,
            "quality": 0.88
        },
        "deepseek-coder": {
            "input": 0.0002,
            "output": 0.0002,
            "speed_factor": 1.0,
            "quality": 0.85
        },
        "qwen-coder": {
            "input": 0.0002,
            "output": 0.0002,
            "speed_factor": 1.1,
            "quality": 0.86
        },
        "codellama": {
            "input": 0.0,
            "output": 0.0,
            "speed_factor": 0.5,
            "quality": 0.75
        }
    }
    
    def __init__(self):
        """Initialize cost estimator / 初始化成本估算器"""
        self.conversion_history = []
    
    def estimate(
        self,
        lines_of_code: int,
        source_language: str,
        target_language: str,
        ai_model: str = "gpt-4o",
        strategy: str = "quality_first"
    ) -> CostEstimate:
        """
        Estimate conversion cost and time / 估算转换成本和时间
        
        Calculation formula / 计算公式:
        - Average tokens per line: 10-15 (depends on language)
        - Translation requires: input tokens + output tokens
        - Output is typically 1.2x input size (code expansion)
        
        Args:
            lines_of_code: Number of lines of code / 代码行数
            source_language: Source language / 源语言
            target_language: Target language / 目标语言
            ai_model: AI model to use / 使用的AI模型
            strategy: Translation strategy / 翻译策略
            
        Returns:
            CostEstimate: Cost estimation result / 成本估算结果
        """
        # Get model pricing / 获取模型定价
        if ai_model not in self.MODEL_PRICES:
            logger.warning(f"Unknown model {ai_model}, using default pricing")
            ai_model = "gpt-4o"
        
        model_info = self.MODEL_PRICES[ai_model]
        
        # Calculate tokens / 计算token数
        # Different languages have different token densities
        # 不同语言有不同的token密度
        token_multipliers = {
            "java": 12,      # Java is verbose
            "python": 10,
            "javascript": 11,
            "typescript": 12,
            "go": 10,
            "cpp": 13,
            "rust": 12
        }
        
        tokens_per_line = token_multipliers.get(source_language, 10)
        input_tokens = lines_of_code * tokens_per_line
        
        # Output is typically 1.2x input (code expansion during translation)
        # 输出通常是输入的1.2倍（翻译过程中的代码扩展）
        output_tokens = int(input_tokens * 1.2)
        
        total_tokens = input_tokens + output_tokens
        
        # Calculate cost / 计算成本
        input_cost = (input_tokens / 1000) * model_info["input"]
        output_cost = (output_tokens / 1000) * model_info["output"]
        total_cost = input_cost + output_cost
        
        # Adjust for strategy / 根据策略调整
        if strategy == "fastest":
            # Racing mode uses 3 models / 竞速模式使用3个模型
            total_cost *= 3
        elif strategy == "all_consensus":
            # Consensus mode uses 3 models / 共识模式使用3个模型
            total_cost *= 3
        
        # Estimate time / 估算时间
        # Base: 2 minutes per 1000 lines / 基础：每1000行2分钟
        base_time = (lines_of_code / 1000) * 2
        speed_factor = model_info["speed_factor"]
        estimated_time = base_time / speed_factor
        
        # Find cheaper alternatives / 找到更便宜的替代方案
        alternatives = self._find_alternatives(
            input_tokens,
            output_tokens,
            ai_model,
            total_cost
        )
        
        # Calculate savings potential / 计算节省潜力
        if alternatives:
            cheapest_cost = min(alt["cost_usd"] for alt in alternatives)
            savings_potential = max(0, total_cost - cheapest_cost)
        else:
            savings_potential = 0.0
        
        estimate = CostEstimate(
            total_tokens=total_tokens,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_usd=round(total_cost, 2),
            time_minutes=round(estimated_time, 1),
            ai_model=ai_model,
            alternative_options=alternatives,
            savings_potential_usd=round(savings_potential, 2)
        )
        
        logger.info(
            f"💰 Cost estimate: ${estimate.cost_usd} "
            f"({estimate.total_tokens:,} tokens, ~{estimate.time_minutes}min)"
        )
        
        return estimate
    
    def _find_alternatives(
        self,
        input_tokens: int,
        output_tokens: int,
        current_model: str,
        current_cost: float
    ) -> List[Dict[str, Any]]:
        """
        Find cheaper alternative models / 找到更便宜的替代模型
        
        Args:
            input_tokens: Input tokens / 输入token数
            output_tokens: Output tokens / 输出token数
            current_model: Current model / 当前模型
            current_cost: Current cost / 当前成本
            
        Returns:
            List of alternative options / 替代方案列表
        """
        alternatives = []
        
        for model_name, model_info in self.MODEL_PRICES.items():
            if model_name == current_model:
                continue
            
            # Calculate cost for this model / 计算此模型的成本
            alt_cost = (
                (input_tokens / 1000) * model_info["input"] +
                (output_tokens / 1000) * model_info["output"]
            )
            
            if alt_cost < current_cost:
                savings = current_cost - alt_cost
                savings_percent = (savings / current_cost) * 100
                
                alternatives.append({
                    "model": model_name,
                    "cost_usd": round(alt_cost, 2),
                    "savings_usd": round(savings, 2),
                    "savings_percent": round(savings_percent, 1),
                    "quality_score": model_info["quality"],
                    "speed_factor": model_info["speed_factor"],
                    "recommendation": self._get_recommendation(
                        savings_percent,
                        model_info["quality"]
                    )
                })
        
        # Sort by savings / 按节省金额排序
        alternatives.sort(key=lambda x: x["savings_usd"], reverse=True)
        
        return alternatives[:3]  # Return top 3 alternatives
    
    def _get_recommendation(self, savings_percent: float, quality: float) -> str:
        """
        Get recommendation text / 获取推荐文本
        
        Args:
            savings_percent: Savings percentage / 节省百分比
            quality: Quality score / 质量分数
            
        Returns:
            str: Recommendation text / 推荐文本
        """
        if savings_percent > 80 and quality > 0.8:
            return "⭐ 强烈推荐：大幅节省成本，质量仍然很好"
        elif savings_percent > 50:
            return "✅ 推荐：节省成本明显"
        elif quality > 0.9:
            return "💎 高质量选项"
        else:
            return "⚖️ 平衡选项"
    
    def estimate_batch(
        self,
        projects: List[Dict[str, Any]],
        ai_model: str = "gpt-4o"
    ) -> Dict[str, Any]:
        """
        Estimate cost for batch conversion / 估算批量转换成本
        
        Args:
            projects: List of projects with metadata / 项目列表及元数据
            ai_model: AI model to use / 使用的AI模型
            
        Returns:
            dict: Batch estimation result / 批量估算结果
        """
        total_cost = 0.0
        total_time = 0.0
        project_estimates = []
        
        for project in projects:
            estimate = self.estimate(
                lines_of_code=project["lines_of_code"],
                source_language=project["source_language"],
                target_language=project["target_language"],
                ai_model=ai_model
            )
            
            total_cost += estimate.cost_usd
            total_time += estimate.time_minutes
            
            project_estimates.append({
                "project_name": project.get("name", "Unknown"),
                "estimate": estimate
            })
        
        return {
            "total_projects": len(projects),
            "total_cost_usd": round(total_cost, 2),
            "total_time_minutes": round(total_time, 1),
            "total_time_hours": round(total_time / 60, 1),
            "average_cost_per_project": round(total_cost / len(projects), 2),
            "project_estimates": project_estimates
        }
    
    def track_actual_cost(
        self,
        task_id: str,
        actual_tokens: int,
        actual_cost: float,
        actual_time: float
    ):
        """
        Track actual conversion cost for learning / 追踪实际转换成本用于学习
        
        Args:
            task_id: Task ID / 任务ID
            actual_tokens: Actual tokens used / 实际使用的token数
            actual_cost: Actual cost / 实际成本
            actual_time: Actual time / 实际时间
        """
        self.conversion_history.append({
            "task_id": task_id,
            "timestamp": datetime.now().isoformat(),
            "actual_tokens": actual_tokens,
            "actual_cost": actual_cost,
            "actual_time": actual_time
        })
        
        logger.info(
            f"📊 Actual cost tracked: ${actual_cost} "
            f"({actual_tokens:,} tokens, {actual_time}min)"
        )
    
    def get_cost_report(self) -> Dict[str, Any]:
        """
        Get cost usage report / 获取成本使用报告
        
        Returns:
            dict: Cost report / 成本报告
        """
        if not self.conversion_history:
            return {
                "total_conversions": 0,
                "total_cost_usd": 0.0,
                "total_tokens": 0,
                "average_cost": 0.0
            }
        
        total_cost = sum(h["actual_cost"] for h in self.conversion_history)
        total_tokens = sum(h["actual_tokens"] for h in self.conversion_history)
        
        return {
            "total_conversions": len(self.conversion_history),
            "total_cost_usd": round(total_cost, 2),
            "total_tokens": total_tokens,
            "average_cost": round(total_cost / len(self.conversion_history), 2),
            "average_tokens": int(total_tokens / len(self.conversion_history)),
            "recent_conversions": self.conversion_history[-5:]  # Last 5
        }


# Global cost estimator instance / 全局成本估算器实例
_cost_estimator_instance = None

def get_cost_estimator() -> CostEstimator:
    """
    Get global cost estimator instance / 获取全局成本估算器实例
    
    Returns:
        CostEstimator: Cost estimator instance / 成本估算器实例
    """
    global _cost_estimator_instance
    if _cost_estimator_instance is None:
        _cost_estimator_instance = CostEstimator()
    return _cost_estimator_instance

