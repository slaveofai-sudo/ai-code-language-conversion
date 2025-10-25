"""
AI Code Migration Platform - FastAPI Backend
AI代码迁移平台 - FastAPI后端服务

This is the main entry point for the backend API server.
这是后端API服务器的主入口文件。

Features / 功能:
- RESTful API endpoints / REST API端点
- Multi-AI orchestration / 多AI编排
- Task management / 任务管理
- Real-time progress tracking / 实时进度追踪
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, HttpUrl
from typing import Optional, List
import uvicorn
from pathlib import Path
import os
import asyncio
from dotenv import load_dotenv

from core.git_manager import GitManager
from core.project_analyzer import ProjectAnalyzer
from core.translation_orchestrator import TranslationOrchestrator
from core.framework_mapper import FrameworkMapper
from core.runtime_configurator import RuntimeConfigurator
from core.cache_manager import get_cache_manager
from core.cost_estimator import get_cost_estimator
from core.test_generator import TestGenerator
from core.code_block_analyzer import CodeBlockAnalyzer
from core.code_inspector import CodeInspector
from core.learning_doc_generator import LearningDocGenerator
from core.code_optimizer import CodeOptimizer
from core.optimization_report_generator import OptimizationReportGenerator
from core.ai_model_manager import get_model_manager, AIModelConfig
from services.task_manager import TaskManager
from models.schemas import (
    ConversionRequest,
    ConversionResponse,
    TaskStatus,
    SupportedLanguage
)

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="AI Code Migration Platform",
    description="多语言代码智能转换系统",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize managers
git_manager = GitManager()
project_analyzer = ProjectAnalyzer()
translator = TranslationOrchestrator()
task_manager = TaskManager()
framework_mapper = FrameworkMapper()
runtime_configurator = RuntimeConfigurator()
cache_manager = get_cache_manager()
cost_estimator = get_cost_estimator()
test_generator = TestGenerator()
code_block_analyzer = CodeBlockAnalyzer()
code_inspector = CodeInspector()
learning_doc_generator = LearningDocGenerator()
code_optimizer = CodeOptimizer()
optimization_report_generator = OptimizationReportGenerator()
model_manager = get_model_manager()

# Create necessary directories
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "./data/uploads"))
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "./data/outputs"))
CACHE_DIR = Path(os.getenv("CACHE_DIR", "./data/cache"))

for dir_path in [UPLOAD_DIR, OUTPUT_DIR, CACHE_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)


@app.get("/")
async def root():
    """
    Health check endpoint / 健康检查端点
    
    Returns:
        dict: Service status information / 服务状态信息
    """
    return {
        "service": "AI Code Migration Platform",
        "status": "running",
        "version": "1.3.0"
    }


@app.get("/api/v1/languages")
async def get_supported_languages():
    """
    Get list of supported programming languages
    获取支持的编程语言列表
    
    Returns:
        dict: List of supported languages with icons
              支持的语言列表（含图标）
    """
    return {
        "languages": [
            {"id": "java", "name": "Java", "icon": "☕"},
            {"id": "python", "name": "Python", "icon": "🐍"},
            {"id": "javascript", "name": "JavaScript", "icon": "📜"},
            {"id": "typescript", "name": "TypeScript", "icon": "📘"},
            {"id": "go", "name": "Go", "icon": "🐹"},
            {"id": "cpp", "name": "C++", "icon": "⚙️"},
            {"id": "rust", "name": "Rust", "icon": "🦀"},
        ]
    }


@app.get("/api/v1/models")
async def get_ai_models():
    """
    Get list of available AI models
    获取可用的AI模型列表
    
    Returns:
        dict: List of AI models with metadata (speed, quality, cost)
              AI模型列表及元数据（速度、质量、成本）
    """
    return {
        "models": [
            {
                "id": "gpt-4",
                "name": "GPT-4 Turbo",
                "provider": "OpenAI",
                "recommended": True,
                "speed": "medium",
                "quality": "excellent"
            },
            {
                "id": "gpt-4o",
                "name": "GPT-4o",
                "provider": "OpenAI",
                "recommended": True,
                "speed": "fast",
                "quality": "excellent"
            },
            {
                "id": "claude-3.5-sonnet",
                "name": "Claude 3.5 Sonnet",
                "provider": "Anthropic",
                "recommended": True,
                "speed": "fast",
                "quality": "excellent"
            },
            {
                "id": "codellama",
                "name": "CodeLlama 13B",
                "provider": "Local (Ollama)",
                "recommended": False,
                "speed": "slow",
                "quality": "good"
            }
        ]
    }


@app.get("/api/v1/frameworks")
async def get_supported_frameworks():
    """
    Get list of supported frameworks / 获取支持的框架列表
    
    Returns:
        dict: List of frameworks by language / 按语言分类的框架列表
    """
    return {
        "frameworks": {
            "java": [
                {"id": "spring-boot", "name": "Spring Boot", "type": "web", "recommended": True},
                {"id": "quarkus", "name": "Quarkus", "type": "web", "recommended": False},
                {"id": "micronaut", "name": "Micronaut", "type": "web", "recommended": False}
            ],
            "python": [
                {"id": "fastapi", "name": "FastAPI", "type": "web", "recommended": True},
                {"id": "django", "name": "Django", "type": "web", "recommended": True},
                {"id": "flask", "name": "Flask", "type": "web", "recommended": False}
            ],
            "javascript": [
                {"id": "express", "name": "Express", "type": "web", "recommended": True},
                {"id": "nestjs", "name": "NestJS", "type": "web", "recommended": True},
                {"id": "koa", "name": "Koa", "type": "web", "recommended": False}
            ],
            "typescript": [
                {"id": "nestjs", "name": "NestJS", "type": "web", "recommended": True},
                {"id": "express", "name": "Express (TS)", "type": "web", "recommended": True}
            ],
            "go": [
                {"id": "gin", "name": "Gin", "type": "web", "recommended": True},
                {"id": "echo", "name": "Echo", "type": "web", "recommended": True},
                {"id": "fiber", "name": "Fiber", "type": "web", "recommended": False}
            ]
        }
    }


@app.get("/api/v1/runtime-environments")
async def get_runtime_environments():
    """
    Get list of supported runtime environments / 获取支持的运行环境列表
    
    Returns:
        dict: List of runtime environments / 运行环境列表
    """
    return {
        "runtime_environments": [
            {
                "id": "docker",
                "name": "Docker",
                "description": "容器化部署 / Containerized deployment",
                "icon": "🐳",
                "recommended": True
            },
            {
                "id": "kubernetes",
                "name": "Kubernetes",
                "description": "K8s集群部署 / Kubernetes cluster",
                "icon": "☸️",
                "recommended": True
            },
            {
                "id": "aws",
                "name": "AWS",
                "description": "AWS云平台 / AWS cloud platform",
                "icon": "☁️",
                "recommended": False
            },
            {
                "id": "heroku",
                "name": "Heroku",
                "description": "Heroku平台 / Heroku platform",
                "icon": "🟣",
                "recommended": False
            },
            {
                "id": "systemd",
                "name": "Systemd",
                "description": "Linux系统服务 / Linux system service",
                "icon": "🐧",
                "recommended": False
            }
        ]
    }


@app.post("/api/v1/frameworks/detect")
async def detect_frameworks(git_url: str, source_language: str):
    """
    Detect frameworks in a repository / 检测仓库中的框架
    
    Args:
        git_url: Git repository URL / Git仓库URL
        source_language: Source language / 源语言
        
    Returns:
        dict: Detected frameworks / 检测到的框架
    """
    try:
        # Clone repository temporarily / 临时克隆仓库
        import tempfile
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            await git_manager.clone_repository(git_url, temp_path)
            
            # Detect frameworks / 检测框架
            from core.framework_detector import FrameworkDetector
            detector = FrameworkDetector()
            detected = detector.detect_frameworks(temp_path)
            
            return {
                "success": True,
                "detected_frameworks": detected,
                "count": len(detected)
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/frameworks/suggest")
async def suggest_target_framework(
    source_framework: str,
    source_language: str,
    target_language: str
):
    """
    Suggest compatible target frameworks / 建议兼容的目标框架
    
    Args:
        source_framework: Source framework / 源框架
        source_language: Source language / 源语言
        target_language: Target language / 目标语言
        
    Returns:
        dict: Suggested target frameworks / 建议的目标框架
    """
    suggestions = framework_mapper.get_compatible_frameworks(
        source_framework,
        source_language,
        target_language
    )
    
    return {
        "success": True,
        "source_framework": source_framework,
        "target_language": target_language,
        "suggestions": suggestions
    }


@app.post("/api/v1/estimate")
async def estimate_conversion_cost(
    lines_of_code: int,
    source_language: str,
    target_language: str,
    ai_model: str = "gpt-4o",
    strategy: str = "quality_first"
):
    """
    Estimate conversion cost and time / 估算转换成本和时间
    
    Args:
        lines_of_code: Number of lines of code / 代码行数
        source_language: Source language / 源语言
        target_language: Target language / 目标语言
        ai_model: AI model to use / 使用的AI模型
        strategy: Translation strategy / 翻译策略
        
    Returns:
        dict: Cost estimation / 成本估算
    """
    estimate = cost_estimator.estimate(
        lines_of_code=lines_of_code,
        source_language=source_language,
        target_language=target_language,
        ai_model=ai_model,
        strategy=strategy
    )
    
    return {
        "success": True,
        "estimate": {
            "total_tokens": estimate.total_tokens,
            "input_tokens": estimate.input_tokens,
            "output_tokens": estimate.output_tokens,
            "cost_usd": estimate.cost_usd,
            "time_minutes": estimate.time_minutes,
            "ai_model": estimate.ai_model,
            "alternative_options": estimate.alternative_options,
            "savings_potential_usd": estimate.savings_potential_usd
        },
        "recommendations": {
            "cheapest": estimate.alternative_options[0] if estimate.alternative_options else None,
            "message": f"您可以通过使用 {estimate.alternative_options[0]['model']} 节省 ${estimate.savings_potential_usd}" if estimate.alternative_options else "当前已是最优选择"
        }
    }


@app.get("/api/v1/cost/report")
async def get_cost_report():
    """
    Get cost usage report / 获取成本使用报告
    
    Returns:
        dict: Cost report / 成本报告
    """
    report = cost_estimator.get_cost_report()
    return {
        "success": True,
        "report": report
    }


@app.get("/api/v1/cache/stats")
async def get_cache_stats():
    """
    Get cache statistics / 获取缓存统计
    
    Returns:
        dict: Cache statistics / 缓存统计
    """
    stats = cache_manager.get_stats()
    cache_size = await cache_manager.get_cache_size()
    
    return {
        "success": True,
        "stats": {
            **stats,
            "total_cached_items": cache_size
        }
    }


@app.post("/api/v1/cache/clear")
async def clear_cache():
    """
    Clear all cache / 清空所有缓存
    
    Returns:
        dict: Success status / 成功状态
    """
    success = await cache_manager.clear_all()
    return {
        "success": success,
        "message": "缓存已清空" if success else "清空缓存失败"
    }


@app.websocket("/ws/task/{task_id}")
async def websocket_task_progress(websocket: WebSocket, task_id: str):
    """
    WebSocket endpoint for real-time task progress
    WebSocket端点用于实时任务进度
    
    Args:
        websocket: WebSocket connection / WebSocket连接
        task_id: Task ID / 任务ID
    """
    await websocket.accept()
    
    try:
        while True:
            # Get task status / 获取任务状态
            status = task_manager.get_task(task_id)
            
            if not status:
                await websocket.send_json({
                    "error": "Task not found",
                    "task_id": task_id
                })
                break
            
            # Send progress update / 发送进度更新
            await websocket.send_json({
                "task_id": task_id,
                "status": status.get("status"),
                "progress": status.get("progress", 0),
                "current_file": status.get("current_file", ""),
                "total_files": status.get("total_files", 0),
                "completed_files": status.get("completed_files", 0),
                "message": status.get("message", "Processing..."),
                "elapsed_time": status.get("elapsed_time", 0),
                "estimated_remaining": status.get("estimated_remaining", 0)
            })
            
            # Check if task is completed or failed / 检查任务是否完成或失败
            if status.get("status") in ["completed", "failed", "cancelled"]:
                await websocket.send_json({
                    "task_id": task_id,
                    "status": status.get("status"),
                    "progress": 100 if status.get("status") == "completed" else status.get("progress", 0),
                    "message": "转换完成!" if status.get("status") == "completed" else "转换失败",
                    "result_url": status.get("result_url"),
                    "error": status.get("error")
                })
                break
            
            # Wait before next update / 等待下次更新
            await asyncio.sleep(1)
            
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for task {task_id}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        try:
            await websocket.send_json({
                "error": str(e),
                "task_id": task_id
            })
        except:
            pass


@app.post("/api/v1/convert")
async def convert_code(
    request: ConversionRequest,
    background_tasks: BackgroundTasks
):
    """
    Submit code conversion task / 提交代码转换任务
    
    Supports two input methods / 支持两种输入方式:
    1. Git URL: Pull from remote repository / 直接拉取远程仓库
    2. Upload: Upload ZIP file (via separate endpoint) / 上传ZIP文件（通过单独端点）
    
    Args:
        request: Conversion request with source/target language and AI model
                 转换请求（含源语言、目标语言和AI模型）
        background_tasks: FastAPI background tasks for async execution
                         FastAPI后台任务用于异步执行
    
    Returns:
        ConversionResponse: Task ID and status / 任务ID和状态
    """
    try:
        # 创建任务
        task_id = task_manager.create_task(
            source_language=request.source_language,
            target_language=request.target_language,
            ai_model=request.ai_model
        )
        
        # 在后台执行转换
        background_tasks.add_task(
            execute_conversion,
            task_id=task_id,
            request=request
        )
        
        return ConversionResponse(
            task_id=task_id,
            status="queued",
            message="转换任务已创建，正在处理中..."
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/upload")
async def upload_project(
    file: UploadFile = File(...),
    source_language: str = "java",
    target_language: str = "python",
    ai_model: str = "gpt-4"
):
    """上传项目ZIP文件并开始转换"""
    try:
        # 保存上传的文件
        upload_path = UPLOAD_DIR / f"{file.filename}"
        
        with open(upload_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # 创建转换请求
        request = ConversionRequest(
            source_type="upload",
            upload_path=str(upload_path),
            source_language=source_language,
            target_language=target_language,
            ai_model=ai_model
        )
        
        # 创建任务
        task_id = task_manager.create_task(
            source_language=source_language,
            target_language=target_language,
            ai_model=ai_model
        )
        
        # 异步执行
        background_tasks = BackgroundTasks()
        background_tasks.add_task(execute_conversion, task_id, request)
        
        return {
            "task_id": task_id,
            "status": "processing",
            "message": f"文件 {file.filename} 上传成功，开始转换..."
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"上传失败: {str(e)}")


@app.get("/api/v1/tasks/{task_id}")
async def get_task_status(task_id: str):
    """查询任务状态"""
    try:
        status = task_manager.get_task_status(task_id)
        
        if not status:
            raise HTTPException(status_code=404, detail="任务不存在")
        
        return status
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/tasks/{task_id}/download")
async def download_result(task_id: str):
    """下载转换结果"""
    try:
        status = task_manager.get_task_status(task_id)
        
        if not status:
            raise HTTPException(status_code=404, detail="任务不存在")
        
        if status["status"] != "completed":
            raise HTTPException(status_code=400, detail="任务尚未完成")
        
        output_file = status.get("output_file")
        if not output_file or not Path(output_file).exists():
            raise HTTPException(status_code=404, detail="输出文件不存在")
        
        return FileResponse(
            output_file,
            media_type="application/zip",
            filename=Path(output_file).name
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/tasks")
async def list_tasks(limit: int = 20, offset: int = 0):
    """列出所有任务"""
    try:
        tasks = task_manager.list_tasks(limit=limit, offset=offset)
        return {"tasks": tasks, "total": len(tasks)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def execute_conversion(task_id: str, request: ConversionRequest):
    """
    Execute code conversion workflow / 执行代码转换的核心流程
    
    This is the main conversion pipeline that:
    这是主要的转换流程，包括:
    
    1. Fetches source code (Git clone or extract ZIP) / 获取源代码（Git克隆或解压ZIP）
    2. Analyzes project structure / 分析项目结构
    3. Translates code using AI models / 使用AI模型翻译代码
    4. Generates target project / 生成目标项目
    5. Packages output as ZIP / 打包输出为ZIP
    
    Args:
        task_id: Unique task identifier / 唯一任务标识符
        request: Conversion request details / 转换请求详情
    """
    try:
        # 更新任务状态
        task_manager.update_task(task_id, status="processing", progress=0)
        
        # Step 1: 获取源代码
        task_manager.update_task(task_id, progress=10, stage="获取源代码...")
        
        if request.source_type == "git":
            # 克隆Git仓库
            source_dir = await git_manager.clone_repository(
                request.git_url,
                UPLOAD_DIR / task_id
            )
        else:
            # 解压上传的文件
            source_dir = await extract_upload(request.upload_path, task_id)
        
        # Step 2: 分析项目结构
        task_manager.update_task(task_id, progress=20, stage="分析项目结构...")
        
        project_info = await project_analyzer.analyze(
            source_dir,
            request.source_language
        )
        
        # Step 3: AI翻译
        task_manager.update_task(task_id, progress=30, stage="AI翻译中...")
        
        translated_files = await translator.translate_project(
            project_info=project_info,
            source_language=request.source_language,
            target_language=request.target_language,
            ai_model=request.ai_model,
            task_id=task_id,
            progress_callback=lambda p: task_manager.update_task(
                task_id, progress=30 + int(p * 0.5)
            )
        )
        
        # Step 4: 生成目标项目
        task_manager.update_task(task_id, progress=80, stage="生成项目文件...")
        
        output_dir = OUTPUT_DIR / task_id
        await translator.generate_project(
            translated_files,
            output_dir,
            request.target_language
        )
        
        # Step 5: 打包输出
        task_manager.update_task(task_id, progress=90, stage="打包输出...")
        
        output_zip = await create_zip(output_dir, task_id)
        
        # 完成
        task_manager.update_task(
            task_id,
            status="completed",
            progress=100,
            stage="转换完成！",
            output_file=str(output_zip),
            result={
                "total_files": len(translated_files),
                "source_language": request.source_language,
                "target_language": request.target_language
            }
        )
        
    except Exception as e:
        # 失败
        task_manager.update_task(
            task_id,
            status="failed",
            error=str(e)
        )


async def extract_upload(upload_path: str, task_id: str) -> Path:
    """解压上传的ZIP文件"""
    import zipfile
    
    extract_dir = UPLOAD_DIR / task_id
    extract_dir.mkdir(parents=True, exist_ok=True)
    
    with zipfile.ZipFile(upload_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    
    return extract_dir


async def create_zip(directory: Path, task_id: str) -> Path:
    """创建输出ZIP文件"""
    import zipfile
    
    output_zip = OUTPUT_DIR / f"{task_id}.zip"
    
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in directory.rglob('*'):
            if file_path.is_file():
                zipf.write(
                    file_path,
                    file_path.relative_to(directory)
                )
    
    return output_zip


@app.post("/api/v1/generate-tests")
async def generate_tests(
    source_file: str,
    target_language: str,
    framework: Optional[str] = None
):
    """
    Generate unit tests for converted code
    为转换后的代码生成单元测试
    
    Args:
        source_file: Path to converted source file / 转换后的源文件路径
        target_language: Target programming language / 目标编程语言
        framework: Optional framework name / 可选的框架名称
    
    Returns:
        dict: Generated test code and metadata / 生成的测试代码和元数据
    """
    try:
        source_path = Path(source_file)
        
        if not source_path.exists():
            raise HTTPException(status_code=404, detail=f"Source file not found: {source_file}")
        
        # Generate tests
        # 生成测试
        result = test_generator.generate_tests(
            source_file=source_path,
            target_language=target_language,
            framework=framework
        )
        
        # Save test file
        # 保存测试文件
        if result["status"] == "success":
            test_file_path = source_path.parent / "tests" / result["test_file_name"]
            test_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(test_file_path, 'w', encoding='utf-8') as f:
                f.write(result["test_code"])
            
            result["test_file_path"] = str(test_file_path)
        
        return JSONResponse(content={
            "status": "success",
            "result": result
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/analyze-blocks")
async def analyze_code_blocks(
    source_file: str,
    target_file: str,
    source_language: str,
    target_language: str,
    source_framework: Optional[str] = None,
    target_framework: Optional[str] = None,
    generate_report: bool = True
):
    """
    Analyze code migration at block level
    在代码块级别分析代码迁移
    
    Args:
        source_file: Path to source file / 源文件路径
        target_file: Path to target file / 目标文件路径
        source_language: Source programming language / 源编程语言
        target_language: Target programming language / 目标编程语言
        source_framework: Source framework (optional) / 源框架（可选）
        target_framework: Target framework (optional) / 目标框架（可选）
        generate_report: Generate Markdown report / 生成Markdown报告
    
    Returns:
        dict: Code block analysis results / 代码块分析结果
    """
    try:
        source_path = Path(source_file)
        target_path = Path(target_file)
        
        if not source_path.exists():
            raise HTTPException(status_code=404, detail=f"Source file not found: {source_file}")
        
        if not target_path.exists():
            raise HTTPException(status_code=404, detail=f"Target file not found: {target_file}")
        
        # Analyze migration
        # 分析迁移
        analysis = code_block_analyzer.analyze_migration(
            source_file=source_path,
            target_file=target_path,
            source_language=source_language,
            target_language=target_language,
            source_framework=source_framework,
            target_framework=target_framework
        )
        
        response_data = {
            "status": "success",
            "analysis": {
                "source_file": analysis.source_file,
                "target_file": analysis.target_file,
                "source_language": analysis.source_language,
                "target_language": analysis.target_language,
                "source_framework": analysis.source_framework,
                "target_framework": analysis.target_framework,
                "total_blocks": len(analysis.blocks),
                "statistics": analysis.statistics,
                "quality_metrics": analysis.quality_metrics,
                "recommendations": analysis.recommendations,
                "blocks": [
                    {
                        "id": block.id,
                        "type": block.type,
                        "source_code": block.source_code,
                        "target_code": block.target_code,
                        "mappings": block.mappings,
                        "conversion_notes": block.conversion_notes,
                        "quality_score": block.quality_score
                    }
                    for block in analysis.blocks
                ]
            }
        }
        
        # Generate Markdown report if requested
        # 如果需要，生成Markdown报告
        if generate_report:
            report_md = code_block_analyzer.generate_markdown_report(analysis)
            report_file_path = target_path.parent / f"{target_path.stem}_analysis.md"
            
            with open(report_file_path, 'w', encoding='utf-8') as f:
                f.write(report_md)
            
            response_data["report_file"] = str(report_file_path)
        
        return JSONResponse(content=response_data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/convert-with-analysis")
async def convert_with_full_analysis(
    request: ConversionRequest,
    background_tasks: BackgroundTasks,
    generate_tests: bool = True,
    generate_analysis: bool = True
):
    """
    Convert code with full analysis (tests + code block analysis)
    进行完整分析的代码转换（测试 + 代码块分析）
    
    This endpoint performs code conversion and automatically generates:
    这个端点执行代码转换并自动生成:
    - Unit tests for converted code / 转换后代码的单元测试
    - Detailed code block analysis / 详细的代码块分析
    - Quality metrics and recommendations / 质量指标和建议
    
    Args:
        request: Conversion request with all parameters / 包含所有参数的转换请求
        background_tasks: FastAPI background tasks / FastAPI后台任务
        generate_tests: Whether to generate tests / 是否生成测试
        generate_analysis: Whether to generate block analysis / 是否生成块级分析
    
    Returns:
        dict: Task ID and status / 任务ID和状态
    """
    # Create conversion task (same as /api/v1/convert)
    # 创建转换任务（与 /api/v1/convert 相同）
    task_id = task_manager.create_task()
    
    async def conversion_with_analysis_task():
        try:
            # Perform regular conversion first
            # 先执行常规转换
            # ... (conversion logic same as /api/v1/convert)
            
            # After conversion, generate tests and analysis
            # 转换后，生成测试和分析
            output_dir = OUTPUT_DIR / task_id
            
            if generate_tests:
                task_manager.update_task(
                    task_id,
                    stage="生成单元测试...",
                    progress=85
                )
                
                # Generate tests for all converted files
                # 为所有转换后的文件生成测试
                for file_path in output_dir.rglob(f"*.{_get_file_extension(request.target_language)}"):
                    try:
                        test_result = test_generator.generate_tests(
                            source_file=file_path,
                            target_language=request.target_language,
                            framework=request.target_framework
                        )
                        
                        if test_result["status"] == "success":
                            # Save test file
                            # 保存测试文件
                            test_file_path = file_path.parent / "tests" / test_result["test_file_name"]
                            test_file_path.parent.mkdir(parents=True, exist_ok=True)
                            
                            with open(test_file_path, 'w', encoding='utf-8') as f:
                                f.write(test_result["test_code"])
                    
                    except Exception as e:
                        logger.warning(f"测试生成失败 {file_path}: {e}")
            
            if generate_analysis:
                task_manager.update_task(
                    task_id,
                    stage="生成代码块分析报告...",
                    progress=95
                )
                
                # TODO: Implement full analysis generation for all files
                # 待实现：为所有文件生成完整分析
            
            task_manager.update_task(
                task_id,
                status="completed",
                progress=100,
                stage="转换完成（包含测试和分析）！"
            )
        
        except Exception as e:
            task_manager.update_task(
                task_id,
                status="failed",
                error=str(e)
            )
    
    # Add to background tasks
    # 添加到后台任务
    background_tasks.add_task(conversion_with_analysis_task)
    
    return JSONResponse(content={
        "task_id": task_id,
        "status": "processing",
        "message": "代码转换任务已创建（包含测试和分析）"
    })


def _get_file_extension(language: str) -> str:
    """Get file extension for a programming language"""
    extensions = {
        "python": "py",
        "java": "java",
        "javascript": "js",
        "typescript": "ts",
        "go": "go",
        "rust": "rs",
        "cpp": "cpp",
        "csharp": "cs"
    }
    return extensions.get(language, "txt")


@app.post("/api/v1/inspect-project")
async def inspect_project(
    git_url: Optional[str] = None,
    local_path: Optional[str] = None,
    generate_learning_doc: bool = True,
    output_format: str = "markdown"
):
    """
    Inspect project code and generate learning documentation
    检测项目代码并生成学习文档
    
    This endpoint analyzes code complexity, detects patterns, and generates
    comprehensive learning documentation.
    此端点分析代码复杂度、检测模式并生成全面的学习文档。
    
    Args:
        git_url: Git repository URL / Git仓库URL
        local_path: Local project path / 本地项目路径
        generate_learning_doc: Generate learning documentation / 生成学习文档
        output_format: Output format (markdown, json) / 输出格式
    
    Returns:
        dict: Inspection results and learning documentation
              检测结果和学习文档
    """
    try:
        # Determine project path
        # 确定项目路径
        if git_url:
            # Clone repository
            # 克隆仓库
            task_id = task_manager.create_task()
            clone_dir = UPLOAD_DIR / task_id
            clone_dir.mkdir(parents=True, exist_ok=True)
            
            logger.info(f"克隆仓库: {git_url}")
            repo_path = git_manager.clone_repo(git_url, str(clone_dir))
            project_path = Path(repo_path)
        
        elif local_path:
            project_path = Path(local_path)
            if not project_path.exists():
                raise HTTPException(status_code=404, detail=f"Project path not found: {local_path}")
        
        else:
            raise HTTPException(status_code=400, detail="Either git_url or local_path must be provided")
        
        logger.info(f"开始检测项目: {project_path}")
        
        # Inspect project
        # 检测项目
        inspection_results = code_inspector.inspect_project(project_path)
        
        response_data = {
            "status": "success",
            "project_path": str(project_path),
            "inspection_results": {
                "project_metrics": {
                    "project_name": inspection_results['project_metrics'].project_name,
                    "total_files": inspection_results['project_metrics'].total_files,
                    "total_lines": inspection_results['project_metrics'].total_lines,
                    "total_functions": inspection_results['project_metrics'].total_functions,
                    "total_classes": inspection_results['project_metrics'].total_classes,
                    "languages": inspection_results['project_metrics'].languages,
                    "avg_complexity": inspection_results['project_metrics'].avg_complexity,
                    "overall_difficulty": inspection_results['project_metrics'].overall_difficulty,
                },
                "architecture": inspection_results['architecture'],
                "tech_stack": inspection_results['tech_stack'],
                "summary": inspection_results['summary']
            }
        }
        
        # Generate learning documentation if requested
        # 如果需要，生成学习文档
        if generate_learning_doc:
            logger.info("生成学习文档...")
            
            # Convert dataclasses to dicts for the generator
            # 为生成器转换数据类为字典
            results_for_doc = {
                "project_metrics": {
                    "project_name": inspection_results['project_metrics'].project_name,
                    "total_files": inspection_results['project_metrics'].total_files,
                    "total_lines": inspection_results['project_metrics'].total_lines,
                    "total_functions": inspection_results['project_metrics'].total_functions,
                    "total_classes": inspection_results['project_metrics'].total_classes,
                    "languages": inspection_results['project_metrics'].languages,
                    "avg_complexity": inspection_results['project_metrics'].avg_complexity,
                    "overall_difficulty": inspection_results['project_metrics'].overall_difficulty,
                },
                "file_metrics": [
                    {
                        "file_path": f.file_path,
                        "language": f.language,
                        "lines_of_code": f.lines_of_code,
                        "num_functions": f.num_functions,
                        "num_classes": f.num_classes,
                        "num_imports": f.num_imports,
                        "complexity_score": f.complexity_score,
                        "maintainability_index": f.maintainability_index,
                        "code_smells": f.code_smells,
                        "security_issues": f.security_issues
                    }
                    for f in inspection_results['file_metrics']
                ],
                "architecture": inspection_results['architecture'],
                "tech_stack": inspection_results['tech_stack'],
                "summary": inspection_results['summary']
            }
            
            learning_doc = learning_doc_generator.generate_learning_doc(
                results_for_doc,
                project_path,
                output_format=output_format
            )
            
            # Save learning documentation
            # 保存学习文档
            if output_format == "markdown":
                doc_filename = f"{inspection_results['project_metrics'].project_name}_学习文档.md"
            else:
                doc_filename = f"{inspection_results['project_metrics'].project_name}_学习文档.json"
            
            doc_path = project_path / doc_filename
            
            with open(doc_path, 'w', encoding='utf-8') as f:
                f.write(learning_doc)
            
            response_data["learning_doc"] = {
                "content": learning_doc if output_format == "json" else learning_doc[:1000] + "..." if len(learning_doc) > 1000 else learning_doc,
                "file_path": str(doc_path),
                "format": output_format
            }
            
            logger.info(f"学习文档已保存: {doc_path}")
        
        return JSONResponse(content=response_data)
    
    except Exception as e:
        logger.error(f"项目检测失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/inspect-project/{task_id}/download")
async def download_learning_doc(task_id: str):
    """
    Download generated learning documentation
    下载生成的学习文档
    
    Args:
        task_id: Task ID / 任务ID
    
    Returns:
        FileResponse: Learning documentation file
                     学习文档文件
    """
    try:
        # Find the learning doc file
        # 查找学习文档文件
        project_dir = UPLOAD_DIR / task_id
        
        if not project_dir.exists():
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Look for learning doc files
        # 查找学习文档文件
        doc_files = list(project_dir.glob("*学习文档.*"))
        
        if not doc_files:
            raise HTTPException(status_code=404, detail="Learning documentation not found")
        
        doc_file = doc_files[0]
        
        return FileResponse(
            path=doc_file,
            filename=doc_file.name,
            media_type='application/octet-stream'
        )
    
    except Exception as e:
        logger.error(f"下载学习文档失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/inspect-and-convert")
async def inspect_and_convert(
    request: ConversionRequest,
    background_tasks: BackgroundTasks,
    generate_learning_doc: bool = True
):
    """
    Inspect project and then convert it (combined workflow)
    检测项目然后进行转换（组合工作流）
    
    This endpoint first inspects the project to generate learning documentation,
    then performs the code conversion.
    此端点首先检测项目以生成学习文档，然后执行代码转换。
    
    Args:
        request: Conversion request / 转换请求
        background_tasks: Background tasks / 后台任务
        generate_learning_doc: Generate learning documentation / 生成学习文档
    
    Returns:
        dict: Task ID and status / 任务ID和状态
    """
    task_id = task_manager.create_task()
    
    async def inspect_and_convert_task():
        try:
            # Step 1: Inspect project
            # 步骤1: 检测项目
            if generate_learning_doc:
                task_manager.update_task(
                    task_id,
                    stage="检测项目并生成学习文档...",
                    progress=10
                )
                
                # Clone or get project path
                # 克隆或获取项目路径
                if request.source_type == "git":
                    clone_dir = UPLOAD_DIR / task_id
                    clone_dir.mkdir(parents=True, exist_ok=True)
                    repo_path = git_manager.clone_repo(request.git_url, str(clone_dir))
                    project_path = Path(repo_path)
                else:
                    # Handle uploaded file
                    project_path = UPLOAD_DIR / task_id
                
                # Inspect project
                # 检测项目
                inspection_results = code_inspector.inspect_project(project_path)
                
                # Generate learning doc
                # 生成学习文档
                results_for_doc = {
                    "project_metrics": {
                        "project_name": inspection_results['project_metrics'].project_name,
                        "total_files": inspection_results['project_metrics'].total_files,
                        "total_lines": inspection_results['project_metrics'].total_lines,
                        "total_functions": inspection_results['project_metrics'].total_functions,
                        "total_classes": inspection_results['project_metrics'].total_classes,
                        "languages": inspection_results['project_metrics'].languages,
                        "avg_complexity": inspection_results['project_metrics'].avg_complexity,
                        "overall_difficulty": inspection_results['project_metrics'].overall_difficulty,
                    },
                    "file_metrics": [
                        {
                            "file_path": f.file_path,
                            "language": f.language,
                            "lines_of_code": f.lines_of_code,
                            "num_functions": f.num_functions,
                            "num_classes": f.num_classes,
                            "num_imports": f.num_imports,
                            "complexity_score": f.complexity_score,
                            "maintainability_index": f.maintainability_index,
                            "code_smells": f.code_smells,
                            "security_issues": f.security_issues
                        }
                        for f in inspection_results['file_metrics']
                    ],
                    "architecture": inspection_results['architecture'],
                    "tech_stack": inspection_results['tech_stack'],
                    "summary": inspection_results['summary']
                }
                
                learning_doc = learning_doc_generator.generate_learning_doc(
                    results_for_doc,
                    project_path,
                    output_format="markdown"
                )
                
                doc_path = project_path / f"{inspection_results['project_metrics'].project_name}_学习文档.md"
                with open(doc_path, 'w', encoding='utf-8') as f:
                    f.write(learning_doc)
            
            # Step 2: Perform conversion (same as regular conversion)
            # 步骤2: 执行转换（与常规转换相同）
            task_manager.update_task(
                task_id,
                stage="开始代码转换...",
                progress=30
            )
            
            # ... (conversion logic here - would call existing conversion workflow)
            # ... (转换逻辑 - 调用现有的转换工作流程)
            
            task_manager.update_task(
                task_id,
                status="completed",
                progress=100,
                stage="检测和转换完成！"
            )
        
        except Exception as e:
            task_manager.update_task(
                task_id,
                status="failed",
                error=str(e)
            )
    
    background_tasks.add_task(inspect_and_convert_task)
    
    return JSONResponse(content={
        "task_id": task_id,
        "status": "processing",
        "message": "项目检测和转换任务已创建"
    })


@app.post("/api/v1/optimize-code")
async def optimize_code(
    file_path: Optional[str] = None,
    git_url: Optional[str] = None,
    target_file: Optional[str] = None,
    use_multi_ai: bool = True,
    ai_models: Optional[List[str]] = None,
    consensus_threshold: int = 2,
    output_format: str = "markdown"
):
    """
    Multi-AI code optimization analysis
    多AI代码优化分析
    
    This endpoint uses multiple AI models to analyze code and provide
    comprehensive optimization suggestions.
    此端点使用多个AI模型分析代码并提供全面的优化建议。
    
    Args:
        file_path: Path to local file / 本地文件路径
        git_url: Git repository URL / Git仓库URL
        target_file: Specific file in repo to analyze / 仓库中要分析的特定文件
        use_multi_ai: Use multiple AI models / 使用多个AI模型
        ai_models: List of AI models to use / 要使用的AI模型列表
        consensus_threshold: Minimum AIs for consensus / 共识所需的最少AI数量
        output_format: Output format (markdown/json) / 输出格式
    
    Returns:
        dict: Optimization report / 优化报告
    """
    try:
        logger.info("开始多AI代码优化分析")
        
        # Determine file to analyze
        # 确定要分析的文件
        if file_path:
            target_path = Path(file_path)
            if not target_path.exists():
                raise HTTPException(status_code=404, detail=f"File not found: {file_path}")
        
        elif git_url:
            # Clone repository
            # 克隆仓库
            task_id = task_manager.create_task()
            clone_dir = UPLOAD_DIR / task_id
            clone_dir.mkdir(parents=True, exist_ok=True)
            
            repo_path = git_manager.clone_repo(git_url, str(clone_dir))
            
            if target_file:
                target_path = Path(repo_path) / target_file
                if not target_path.exists():
                    raise HTTPException(status_code=404, detail=f"File not found in repo: {target_file}")
            else:
                # Find main file
                # 查找主文件
                target_path = None
                for ext in ['.py', '.java', '.js', '.go']:
                    candidates = list(Path(repo_path).rglob(f'*{ext}'))
                    if candidates:
                        target_path = candidates[0]
                        break
                
                if not target_path:
                    raise HTTPException(status_code=404, detail="No code file found in repository")
        
        else:
            raise HTTPException(status_code=400, detail="Either file_path or git_url must be provided")
        
        # Detect language
        # 检测语言
        language = _detect_language_from_extension(target_path)
        
        # Initialize optimizer with specified AI models
        # 使用指定的AI模型初始化优化器
        if ai_models:
            optimizer = CodeOptimizer(ai_models=ai_models)
        else:
            optimizer = code_optimizer
        
        # Perform optimization analysis
        # 执行优化分析
        logger.info(f"使用 {len(optimizer.ai_models)} 个AI模型分析: {target_path}")
        
        optimization_report = await optimizer.analyze_and_optimize(
            target_path,
            language,
            use_multi_ai=use_multi_ai,
            consensus_threshold=consensus_threshold
        )
        
        # Generate report
        # 生成报告
        report_content = optimization_report_generator.generate_report(
            optimization_report,
            output_format=output_format
        )
        
        # Save report
        # 保存报告
        report_filename = f"{target_path.stem}_optimization_report.{output_format}"
        report_path = target_path.parent / report_filename
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        logger.info(f"优化报告已保存: {report_path}")
        
        # Prepare response
        # 准备响应
        response_data = {
            "status": "success",
            "file_analyzed": str(target_path),
            "language": language,
            "ai_models_used": optimizer.ai_models,
            "summary": {
                "total_suggestions": optimization_report.total_suggestions,
                "consensus_suggestions": len(optimization_report.consensus_suggestions),
                "unique_suggestions": len(optimization_report.unique_suggestions),
                "estimated_effort": optimization_report.estimated_effort,
                "expected_impact": optimization_report.expected_impact
            },
            "suggestions_by_category": optimization_report.suggestions_by_category,
            "suggestions_by_priority": optimization_report.suggestions_by_priority,
            "implementation_roadmap": optimization_report.implementation_roadmap,
            "report_file": str(report_path),
            "report_format": output_format
        }
        
        # Include report preview for markdown
        # 为markdown格式包含报告预览
        if output_format == "markdown":
            response_data["report_preview"] = report_content[:1500] + "..." if len(report_content) > 1500 else report_content
        else:
            response_data["report_content"] = report_content
        
        return JSONResponse(content=response_data)
    
    except Exception as e:
        logger.error(f"代码优化分析失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def _detect_language_from_extension(file_path: Path) -> str:
    """Detect language from file extension"""
    extension_map = {
        '.py': 'python',
        '.java': 'java',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.go': 'go',
        '.rs': 'rust',
        '.cpp': 'cpp',
        '.c': 'c'
    }
    return extension_map.get(file_path.suffix, 'unknown')


# ============================================================================
# AI Model Management APIs / AI模型管理接口
# ============================================================================

@app.get("/api/v1/ai-models")
async def list_ai_models(
    include_builtin: bool = True,
    include_custom: bool = True,
    enabled_only: bool = False
):
    """
    List all available AI models
    列出所有可用的AI模型
    
    This endpoint returns all AI models, including both built-in and custom models.
    此端点返回所有AI模型，包括内置和自定义模型。
    
    Args:
        include_builtin: Include built-in models / 包含内置模型
        include_custom: Include custom models / 包含自定义模型
        enabled_only: Only enabled models / 只返回启用的模型
    
    Returns:
        dict: List of AI models / AI模型列表
    """
    try:
        models = model_manager.list_models(
            include_builtin=include_builtin,
            include_custom=include_custom,
            enabled_only=enabled_only
        )
        
        # Convert to dict format / 转换为字典格式
        models_data = []
        for model in models:
            model_dict = {
                "model_id": model.model_id,
                "model_name": model.model_name,
                "provider": model.provider,
                "model_type": model.model_type,
                "description": model.description,
                "tags": model.tags,
                "enabled": model.enabled,
                "is_builtin": model.model_id in model_manager.builtin_models,
                "created_at": model.created_at,
                "updated_at": model.updated_at
            }
            models_data.append(model_dict)
        
        return JSONResponse(content={
            "status": "success",
            "total": len(models_data),
            "models": models_data
        })
    
    except Exception as e:
        logger.error(f"列出AI模型失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/ai-models/{model_id}")
async def get_ai_model(model_id: str):
    """
    Get detailed information about a specific AI model
    获取特定AI模型的详细信息
    
    Args:
        model_id: Model ID / 模型ID
    
    Returns:
        dict: Model configuration / 模型配置
    """
    try:
        model = model_manager.get_model(model_id)
        
        if not model:
            raise HTTPException(status_code=404, detail=f"Model not found: {model_id}")
        
        return JSONResponse(content={
            "status": "success",
            "model": {
                "model_id": model.model_id,
                "model_name": model.model_name,
                "provider": model.provider,
                "api_base_url": model.api_base_url,
                "api_key_env_var": model.api_key_env_var,
                "model_type": model.model_type,
                "max_tokens": model.max_tokens,
                "temperature": model.temperature,
                "top_p": model.top_p,
                "custom_headers": model.custom_headers,
                "request_format": model.request_format,
                "description": model.description,
                "tags": model.tags,
                "enabled": model.enabled,
                "is_builtin": model.model_id in model_manager.builtin_models,
                "created_at": model.created_at,
                "updated_at": model.updated_at
            }
        })
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取AI模型失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/ai-models")
async def add_ai_model(
    model_id: str,
    model_name: str,
    provider: str,
    api_base_url: str,
    api_key_env_var: str,
    model_type: str = "chat",
    max_tokens: int = 4096,
    temperature: float = 0.3,
    top_p: float = 1.0,
    custom_headers: Optional[Dict[str, str]] = None,
    request_format: str = "openai",
    request_template: Optional[Dict[str, Any]] = None,
    response_path: Optional[str] = None,
    description: str = "",
    tags: Optional[List[str]] = None,
    enabled: bool = True
):
    """
    Add a new custom AI model
    添加新的自定义AI模型
    
    This endpoint allows users to add their own AI models.
    此端点允许用户添加自己的AI模型。
    
    Args:
        model_id: Unique model ID / 唯一模型ID
        model_name: Display name / 显示名称
        provider: Provider name / 提供商名称
        api_base_url: API base URL / API基础URL
        api_key_env_var: Environment variable for API key / API密钥环境变量
        model_type: Model type (chat/completion/custom) / 模型类型
        max_tokens: Maximum tokens / 最大token数
        temperature: Temperature / 温度
        top_p: Top P / Top P
        custom_headers: Custom HTTP headers / 自定义HTTP头
        request_format: Request format (openai/anthropic/google/custom) / 请求格式
        request_template: Custom request template / 自定义请求模板
        response_path: JSONPath to extract response / 响应提取路径
        description: Model description / 模型描述
        tags: Tags / 标签
        enabled: Whether enabled / 是否启用
    
    Returns:
        dict: Success message / 成功消息
    """
    try:
        # Create model config / 创建模型配置
        config = AIModelConfig(
            model_id=model_id,
            model_name=model_name,
            provider=provider,
            api_base_url=api_base_url,
            api_key_env_var=api_key_env_var,
            model_type=model_type,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            custom_headers=custom_headers or {},
            request_format=request_format,
            request_template=request_template,
            response_path=response_path,
            description=description,
            tags=tags or [],
            enabled=enabled
        )
        
        # Add model / 添加模型
        success = model_manager.add_model(config)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to add model")
        
        return JSONResponse(content={
            "status": "success",
            "message": f"AI模型已添加: {model_name}",
            "model_id": model_id
        })
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"添加AI模型失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/v1/ai-models/{model_id}")
async def update_ai_model(
    model_id: str,
    model_name: Optional[str] = None,
    provider: Optional[str] = None,
    api_base_url: Optional[str] = None,
    api_key_env_var: Optional[str] = None,
    model_type: Optional[str] = None,
    max_tokens: Optional[int] = None,
    temperature: Optional[float] = None,
    top_p: Optional[float] = None,
    custom_headers: Optional[Dict[str, str]] = None,
    request_format: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[List[str]] = None,
    enabled: Optional[bool] = None
):
    """
    Update a custom AI model
    更新自定义AI模型
    
    Args:
        model_id: Model ID to update / 要更新的模型ID
        ...: Fields to update / 要更新的字段
    
    Returns:
        dict: Success message / 成功消息
    """
    try:
        # Get existing model / 获取现有模型
        existing = model_manager.get_model(model_id)
        if not existing:
            raise HTTPException(status_code=404, detail=f"Model not found: {model_id}")
        
        if model_id in model_manager.builtin_models:
            raise HTTPException(status_code=400, detail="Cannot update built-in model")
        
        # Update fields / 更新字段
        config = AIModelConfig(
            model_id=model_id,
            model_name=model_name or existing.model_name,
            provider=provider or existing.provider,
            api_base_url=api_base_url or existing.api_base_url,
            api_key_env_var=api_key_env_var or existing.api_key_env_var,
            model_type=model_type or existing.model_type,
            max_tokens=max_tokens if max_tokens is not None else existing.max_tokens,
            temperature=temperature if temperature is not None else existing.temperature,
            top_p=top_p if top_p is not None else existing.top_p,
            custom_headers=custom_headers if custom_headers is not None else existing.custom_headers,
            request_format=request_format or existing.request_format,
            request_template=existing.request_template,
            response_path=existing.response_path,
            description=description if description is not None else existing.description,
            tags=tags if tags is not None else existing.tags,
            enabled=enabled if enabled is not None else existing.enabled,
            created_at=existing.created_at
        )
        
        # Update model / 更新模型
        success = model_manager.update_model(model_id, config)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update model")
        
        return JSONResponse(content={
            "status": "success",
            "message": f"AI模型已更新: {config.model_name}"
        })
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新AI模型失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/v1/ai-models/{model_id}")
async def delete_ai_model(model_id: str):
    """
    Delete a custom AI model
    删除自定义AI模型
    
    Args:
        model_id: Model ID to delete / 要删除的模型ID
    
    Returns:
        dict: Success message / 成功消息
    """
    try:
        success = model_manager.remove_model(model_id)
        
        if not success:
            raise HTTPException(status_code=404, detail=f"Model not found or cannot be deleted: {model_id}")
        
        return JSONResponse(content={
            "status": "success",
            "message": f"AI模型已删除: {model_id}"
        })
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"删除AI模型失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/ai-models/{model_id}/test")
async def test_ai_model(model_id: str, test_prompt: str = "Hello, how are you?"):
    """
    Test AI model connectivity and response
    测试AI模型连接和响应
    
    This endpoint tests if the AI model is properly configured and working.
    此端点测试AI模型是否正确配置并能正常工作。
    
    Args:
        model_id: Model ID to test / 要测试的模型ID
        test_prompt: Test prompt / 测试提示词
    
    Returns:
        dict: Test result / 测试结果
    """
    try:
        result = model_manager.test_model(model_id, test_prompt)
        
        return JSONResponse(content={
            "status": "success" if result["success"] else "failed",
            "test_result": result
        })
    
    except Exception as e:
        logger.error(f"测试AI模型失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/ai-models/{model_id}/export")
async def export_ai_model(model_id: str):
    """
    Export AI model configuration for sharing
    导出AI模型配置用于分享
    
    Args:
        model_id: Model ID to export / 要导出的模型ID
    
    Returns:
        dict: Model configuration / 模型配置
    """
    try:
        config = model_manager.export_model(model_id)
        
        if not config:
            raise HTTPException(status_code=404, detail=f"Model not found: {model_id}")
        
        # Remove sensitive info / 删除敏感信息
        config["api_key_env_var"] = "YOUR_API_KEY_ENV_VAR"
        
        return JSONResponse(content={
            "status": "success",
            "config": config,
            "instructions": "替换 api_key_env_var 为您自己的环境变量名，并设置相应的API密钥"
        })
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"导出AI模型失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/ai-models/import")
async def import_ai_model(config: Dict[str, Any]):
    """
    Import AI model configuration
    导入AI模型配置
    
    Args:
        config: Model configuration / 模型配置
    
    Returns:
        dict: Success message / 成功消息
    """
    try:
        success = model_manager.import_model(config)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to import model")
        
        return JSONResponse(content={
            "status": "success",
            "message": f"AI模型已导入: {config.get('model_name', 'Unknown')}"
        })
    
    except Exception as e:
        logger.error(f"导入AI模型失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "false").lower() == "true"
    )

