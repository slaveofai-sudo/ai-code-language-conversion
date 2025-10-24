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

from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, HttpUrl
from typing import Optional, List
import uvicorn
from pathlib import Path
import os
from dotenv import load_dotenv

from core.git_manager import GitManager
from core.project_analyzer import ProjectAnalyzer
from core.translation_orchestrator import TranslationOrchestrator
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


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "false").lower() == "true"
    )

