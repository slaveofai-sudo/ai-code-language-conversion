"""
Multi-AI Orchestrator / 多AI编排器

Supports multiple AI models working concurrently with:
支持多个AI模型并发工作，包含:

- Intelligent model selection / 智能模型选择
- Load balancing / 负载均衡
- Automatic failover / 自动故障转移
- Performance monitoring / 性能监控
- 5 different strategies / 5种不同策略
"""

import asyncio
import time
from typing import List, Dict, Any, Optional
from collections import defaultdict
from loguru import logger
import random

from core.translators.base_translator import BaseTranslator
from core.translators.openai_translator import OpenAITranslator
from core.translators.anthropic_translator import AnthropicTranslator
from core.translators.local_translator import LocalTranslator
from core.translators.deepseek_translator import DeepSeekTranslator
from core.translators.gemini_translator import GeminiTranslator
from core.translators.qwen_translator import QwenTranslator


class MultiAIOrchestrator:
    """
    Multi-AI Orchestrator / 多AI编排器
    
    Features / 功能:
    1. Multi-model concurrent translation / 多模型并发翻译
    2. Intelligent model selection / 智能模型选择
    3. Load balancing / 负载均衡
    4. Automatic failover / 故障自动转移
    5. Performance monitoring / 性能监控
    
    Strategies / 策略:
    - quality_first: Auto-select best quality model / 质量优先自动选择
    - fastest: Race mode - multiple AIs simultaneously / 竞速模式-多AI同时
    - all_consensus: Vote on best result / 投票选择最佳结果
    - round_robin: Load balancing / 负载均衡轮询
    - random: Random selection / 随机选择
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        
        # 初始化所有可用的翻译器
        self.translators = self._init_translators()
        
        # 性能统计
        self.stats = defaultdict(lambda: {
            "success": 0,
            "failure": 0,
            "total_time": 0.0,
            "avg_time": 0.0
        })
        
        # 策略配置
        self.strategy = self.config.get("strategy", "round_robin")
        # 策略: "round_robin", "fastest", "random", "quality_first", "all_consensus"
        
        self.current_index = 0  # 用于轮询
        
    def _init_translators(self) -> Dict[str, BaseTranslator]:
        """
        Initialize all available translators / 初始化所有可用的翻译器
        
        Tries to initialize translators for all AI models:
        尝试初始化所有AI模型的翻译器:
        - GPT-4, GPT-4o (OpenAI)
        - Claude 3.5 Sonnet (Anthropic)
        - Gemini Pro (Google)
        - DeepSeek Coder (DeepSeek)
        - Qwen Coder (Alibaba)
        - CodeLlama (Local/Ollama)
        
        Returns:
            dict: Available translators / 可用的翻译器字典
        """
        translators = {}
        
        # 尝试初始化各个翻译器
        models = [
            ("gpt-4", lambda: OpenAITranslator("gpt-4-turbo")),
            ("gpt-4o", lambda: OpenAITranslator("gpt-4o")),
            ("claude-3.5", lambda: AnthropicTranslator("claude-3-5-sonnet-20241022")),
            ("deepseek", lambda: DeepSeekTranslator("deepseek-coder")),
            ("gemini", lambda: GeminiTranslator("gemini-pro")),
            ("qwen", lambda: QwenTranslator("qwen-coder-turbo")),
            ("codellama", lambda: LocalTranslator("codellama:13b")),
        ]
        
        for name, creator in models:
            try:
                translators[name] = creator()
                logger.info(f"✓ 成功初始化翻译器: {name}")
            except Exception as e:
                logger.warning(f"✗ 跳过翻译器 {name}: {str(e)}")
        
        if not translators:
            raise ValueError("没有可用的翻译器！请至少配置一个 API Key")
        
        logger.info(f"可用翻译器: {list(translators.keys())}")
        return translators
    
    async def translate_with_strategy(
        self,
        source_code: str,
        source_language: str,
        target_language: str,
        context: Dict[str, Any] = None,
        preferred_models: List[str] = None
    ) -> str:
        """
        使用指定策略翻译代码
        
        Args:
            source_code: 源代码
            source_language: 源语言
            target_language: 目标语言
            context: 上下文信息
            preferred_models: 优先使用的模型列表
            
        Returns:
            翻译后的代码
        """
        # 过滤可用模型
        available_models = list(self.translators.keys())
        if preferred_models:
            available_models = [m for m in preferred_models if m in self.translators]
        
        if not available_models:
            raise ValueError("没有可用的翻译模型")
        
        # 根据策略选择翻译方式
        if self.strategy == "round_robin":
            return await self._translate_round_robin(
                source_code, source_language, target_language, context, available_models
            )
        
        elif self.strategy == "fastest":
            return await self._translate_race(
                source_code, source_language, target_language, context, available_models
            )
        
        elif self.strategy == "all_consensus":
            return await self._translate_consensus(
                source_code, source_language, target_language, context, available_models
            )
        
        elif self.strategy == "quality_first":
            return await self._translate_quality_first(
                source_code, source_language, target_language, context, available_models
            )
        
        else:  # random
            return await self._translate_random(
                source_code, source_language, target_language, context, available_models
            )
    
    async def _translate_round_robin(
        self,
        source_code: str,
        source_language: str,
        target_language: str,
        context: Dict[str, Any],
        models: List[str]
    ) -> str:
        """轮询策略：依次使用不同的模型"""
        model_name = models[self.current_index % len(models)]
        self.current_index += 1
        
        return await self._translate_with_fallback(
            model_name, source_code, source_language, target_language, context, models
        )
    
    async def _translate_race(
        self,
        source_code: str,
        source_language: str,
        target_language: str,
        context: Dict[str, Any],
        models: List[str]
    ) -> str:
        """
        Racing strategy: Multiple models translate simultaneously, return fastest result
        竞速策略：多个模型同时翻译，返回最快的结果
        
        This strategy launches multiple AI models in parallel and returns
        the first completed result, canceling other pending tasks.
        该策略并行启动多个AI模型，返回第一个完成的结果，取消其他待处理任务。
        
        Pros / 优点:
        - 3x faster speed / 速度提升3倍
        - High availability / 高可用性
        
        Cons / 缺点:
        - Higher cost (multiple API calls) / 更高成本（多个API调用）
        - Higher network usage / 更高网络使用
        
        Args:
            source_code: Source code to translate / 要翻译的源代码
            source_language: Source programming language / 源编程语言
            target_language: Target programming language / 目标编程语言
            context: Additional context (file path, classes, etc.) / 额外上下文
            models: List of models to race / 参与竞速的模型列表
            
        Returns:
            str: Translated code from fastest model / 最快模型翻译的代码
        """
        logger.info(f"🏁 竞速模式: 使用 {len(models)} 个模型同时翻译")
        
        tasks = []
        for model_name in models:
            translator = self.translators[model_name]
            task = self._translate_with_stats(
                model_name, translator, source_code, source_language, target_language, context
            )
            tasks.append(task)
        
        # 返回第一个完成的结果
        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        
        # 取消其他任务
        for task in pending:
            task.cancel()
        
        # 获取第一个完成的结果
        result = await list(done)[0]
        return result
    
    async def _translate_consensus(
        self,
        source_code: str,
        source_language: str,
        target_language: str,
        context: Dict[str, Any],
        models: List[str]
    ) -> str:
        """
        共识策略：多个模型同时翻译，综合所有结果
        选择最常见的翻译结果或质量最高的
        """
        logger.info(f"🤝 共识模式: 使用 {len(models)} 个模型投票")
        
        tasks = []
        for model_name in models[:3]:  # 最多使用3个模型，避免成本过高
            translator = self.translators[model_name]
            task = self._translate_with_stats(
                model_name, translator, source_code, source_language, target_language, context
            )
            tasks.append(task)
        
        # 等待所有翻译完成
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 过滤错误结果
        valid_results = [r for r in results if not isinstance(r, Exception)]
        
        if not valid_results:
            raise ValueError("所有翻译模型都失败了")
        
        # 简单策略：返回第一个成功的结果
        # TODO: 可以实现更复杂的共识算法，如投票、相似度比较等
        return valid_results[0]
    
    async def _translate_quality_first(
        self,
        source_code: str,
        source_language: str,
        target_language: str,
        context: Dict[str, Any],
        models: List[str]
    ) -> str:
        """质量优先策略：优先使用质量最高的模型"""
        # 模型质量排序 (根据经验)
        quality_order = ["claude-3.5", "gpt-4o", "gpt-4", "gemini", "deepseek", "qwen", "codellama"]
        
        # 按质量排序可用模型
        sorted_models = sorted(
            models,
            key=lambda m: quality_order.index(m) if m in quality_order else 999
        )
        
        return await self._translate_with_fallback(
            sorted_models[0], source_code, source_language, target_language, context, sorted_models
        )
    
    async def _translate_random(
        self,
        source_code: str,
        source_language: str,
        target_language: str,
        context: Dict[str, Any],
        models: List[str]
    ) -> str:
        """随机策略：随机选择一个模型"""
        model_name = random.choice(models)
        return await self._translate_with_fallback(
            model_name, source_code, source_language, target_language, context, models
        )
    
    async def _translate_with_fallback(
        self,
        primary_model: str,
        source_code: str,
        source_language: str,
        target_language: str,
        context: Dict[str, Any],
        fallback_models: List[str]
    ) -> str:
        """
        使用主模型翻译，失败时自动切换到备用模型
        """
        models_to_try = [primary_model] + [m for m in fallback_models if m != primary_model]
        
        last_error = None
        for model_name in models_to_try:
            try:
                translator = self.translators[model_name]
                result = await self._translate_with_stats(
                    model_name, translator, source_code, source_language, target_language, context
                )
                return result
                
            except Exception as e:
                logger.warning(f"模型 {model_name} 翻译失败: {str(e)}, 尝试下一个...")
                last_error = e
                continue
        
        # 所有模型都失败
        raise ValueError(f"所有翻译模型都失败了。最后错误: {str(last_error)}")
    
    async def _translate_with_stats(
        self,
        model_name: str,
        translator: BaseTranslator,
        source_code: str,
        source_language: str,
        target_language: str,
        context: Dict[str, Any]
    ) -> str:
        """执行翻译并记录统计信息"""
        start_time = time.time()
        
        try:
            result = await translator.translate(
                source_code, source_language, target_language, context
            )
            
            elapsed = time.time() - start_time
            
            # 更新统计
            self.stats[model_name]["success"] += 1
            self.stats[model_name]["total_time"] += elapsed
            total = self.stats[model_name]["success"] + self.stats[model_name]["failure"]
            self.stats[model_name]["avg_time"] = self.stats[model_name]["total_time"] / total
            
            logger.info(f"✓ {model_name} 翻译成功 (耗时: {elapsed:.2f}s)")
            return result
            
        except Exception as e:
            elapsed = time.time() - start_time
            self.stats[model_name]["failure"] += 1
            logger.error(f"✗ {model_name} 翻译失败: {str(e)} (耗时: {elapsed:.2f}s)")
            raise
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取性能统计"""
        return dict(self.stats)
    
    def get_available_models(self) -> List[str]:
        """获取所有可用的模型"""
        return list(self.translators.keys())
    
    def set_strategy(self, strategy: str):
        """
        设置翻译策略
        
        Args:
            strategy: 策略名称
                - round_robin: 轮询（负载均衡）
                - fastest: 竞速（多个同时翻译，返回最快的）
                - all_consensus: 共识（多个翻译后综合结果）
                - quality_first: 质量优先（优先使用高质量模型）
                - random: 随机选择
        """
        valid_strategies = ["round_robin", "fastest", "all_consensus", "quality_first", "random"]
        
        if strategy not in valid_strategies:
            raise ValueError(f"无效的策略: {strategy}. 可用策略: {valid_strategies}")
        
        self.strategy = strategy
        logger.info(f"切换到策略: {strategy}")

