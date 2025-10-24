"""
翻译编排器
协调多个AI模型进行代码翻译
"""

import os
import asyncio
from pathlib import Path
from typing import List, Dict, Any, Callable, Optional
import yaml
from loguru import logger

from models.schemas import ProjectInfo, FileInfo, TranslationResult, SupportedLanguage
from core.translators.openai_translator import OpenAITranslator
from core.translators.anthropic_translator import AnthropicTranslator
from core.translators.local_translator import LocalTranslator
from core.generators.project_generator import ProjectGenerator

# 导入多 AI 编排器
try:
    from core.multi_ai_orchestrator import MultiAIOrchestrator
    MULTI_AI_AVAILABLE = True
except ImportError:
    MULTI_AI_AVAILABLE = False
    logger.warning("多 AI 编排器不可用")


class TranslationOrchestrator:
    """翻译编排器 - 管理整个项目的翻译流程"""
    
    def __init__(self, use_multi_ai: bool = True):
        # 加载配置
        config_path = Path(__file__).parent.parent.parent / "config.yaml"
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        # 是否使用多 AI 模式
        self.use_multi_ai = use_multi_ai and MULTI_AI_AVAILABLE
        
        if self.use_multi_ai:
            # 使用多 AI 编排器
            logger.info("🚀 启用多 AI 模式")
            self.multi_ai = MultiAIOrchestrator(self.config.get('multi_ai', {}))
            self.translators = None
        else:
            # 传统单 AI 模式
            logger.info("📌 使用传统单 AI 模式")
            self.multi_ai = None
            # 初始化翻译器
            self.translators = {
                "gpt-4": OpenAITranslator("gpt-4-turbo"),
                "gpt-4o": OpenAITranslator("gpt-4o"),
                "claude-3.5-sonnet": AnthropicTranslator("claude-3-5-sonnet-20241022"),
                "codellama": LocalTranslator("codellama:13b")
            }
        
        # 项目生成器
        self.generator = ProjectGenerator()
        
        # 并发控制
        self.max_concurrent = int(os.getenv("MAX_CONCURRENT_TASKS", 4))
    
    async def translate_project(
        self,
        project_info: ProjectInfo,
        source_language: SupportedLanguage,
        target_language: SupportedLanguage,
        ai_model: str,
        task_id: str,
        progress_callback: Optional[Callable[[float], None]] = None
    ) -> List[TranslationResult]:
        """
        翻译整个项目
        
        Args:
            project_info: 项目信息
            source_language: 源语言
            target_language: 目标语言
            ai_model: AI模型
            task_id: 任务ID
            progress_callback: 进度回调函数
            
        Returns:
            List[TranslationResult]: 翻译结果列表
        """
        logger.info(
            f"开始翻译项目: {source_language} → {target_language}, "
            f"文件数: {len(project_info.files)}"
        )
        
        # 获取翻译器
        translator = self.translators.get(ai_model)
        if not translator:
            raise ValueError(f"不支持的AI模型: {ai_model}")
        
        # 准备翻译任务
        files = project_info.files
        total_files = len(files)
        results = []
        
        # 批量处理（控制并发）
        for i in range(0, total_files, self.max_concurrent):
            batch = files[i:i + self.max_concurrent]
            
            # 并发翻译
            batch_tasks = [
                self._translate_file(
                    file_info,
                    source_language,
                    target_language,
                    translator
                )
                for file_info in batch
            ]
            
            batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)
            
            # 处理结果
            for result in batch_results:
                if isinstance(result, Exception):
                    logger.error(f"翻译失败: {str(result)}")
                else:
                    results.append(result)
            
            # 更新进度
            if progress_callback:
                progress = (i + len(batch)) / total_files
                progress_callback(progress)
        
        logger.info(f"翻译完成: {len(results)}/{total_files} 个文件")
        return results
    
    async def _translate_file(
        self,
        file_info: FileInfo,
        source_language: SupportedLanguage,
        target_language: SupportedLanguage,
        translator
    ) -> TranslationResult:
        """翻译单个文件"""
        try:
            # 读取源代码
            with open(file_info.path, 'r', encoding='utf-8', errors='ignore') as f:
                source_code = f.read()
            
            # 构建上下文
            context = {
                "file_path": file_info.path,
                "classes": file_info.classes,
                "functions": file_info.functions
            }
            
            # 执行翻译
            if self.use_multi_ai and self.multi_ai:
                # 使用多 AI 编排器
                translated_code = await self.multi_ai.translate_with_strategy(
                    source_code=source_code,
                    source_language=source_language.value,
                    target_language=target_language.value,
                    context=context
                )
            else:
                # 使用单个翻译器
                translated_code = await translator.translate(
                    source_code=source_code,
                    source_language=source_language.value,
                    target_language=target_language.value,
                    context=context
                )
            
            
            # 生成目标文件路径
            target_file = self._convert_file_path(
                file_info.path,
                source_language,
                target_language
            )
            
            return TranslationResult(
                source_file=file_info.path,
                target_file=target_file,
                source_code=source_code,
                translated_code=translated_code,
                success=True
            )
            
        except Exception as e:
            logger.error(f"文件翻译失败 {file_info.path}: {str(e)}")
            return TranslationResult(
                source_file=file_info.path,
                target_file="",
                source_code="",
                translated_code="",
                success=False,
                error=str(e)
            )
    
    def _convert_file_path(
        self,
        source_path: str,
        source_language: SupportedLanguage,
        target_language: SupportedLanguage
    ) -> str:
        """转换文件路径（修改扩展名）"""
        path = Path(source_path)
        
        # 获取目标语言的扩展名
        target_ext = self._get_default_extension(target_language)
        
        # 修改扩展名
        new_path = path.with_suffix(target_ext)
        
        return str(new_path)
    
    def _get_default_extension(self, language: SupportedLanguage) -> str:
        """获取语言的默认扩展名"""
        ext_map = {
            SupportedLanguage.JAVA: ".java",
            SupportedLanguage.PYTHON: ".py",
            SupportedLanguage.JAVASCRIPT: ".js",
            SupportedLanguage.TYPESCRIPT: ".ts",
            SupportedLanguage.GO: ".go",
            SupportedLanguage.CPP: ".cpp",
            SupportedLanguage.RUST: ".rs"
        }
        return ext_map.get(language, ".txt")
    
    async def generate_project(
        self,
        translation_results: List[TranslationResult],
        output_dir: Path,
        target_language: SupportedLanguage
    ):
        """生成目标项目"""
        await self.generator.generate(
            translation_results,
            output_dir,
            target_language
        )

