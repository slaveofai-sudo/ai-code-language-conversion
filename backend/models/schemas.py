"""
Data Models / 数据模型定义

Pydantic models for API request/response schemas.
用于API请求/响应的Pydantic模型。

Includes / 包括:
- ConversionRequest: Code conversion request / 代码转换请求
- ConversionResponse: Conversion response / 转换响应
- TaskStatus: Task status tracking / 任务状态追踪
- SupportedLanguage: Language metadata / 语言元数据
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List, Dict, Any, Literal
from datetime import datetime
from enum import Enum


class SourceType(str, Enum):
    """输入源类型"""
    GIT = "git"
    UPLOAD = "upload"


class TaskStatusEnum(str, Enum):
    """任务状态"""
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class SupportedLanguage(str, Enum):
    """支持的编程语言"""
    JAVA = "java"
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    GO = "go"
    CPP = "cpp"
    RUST = "rust"


class AIModel(str, Enum):
    """AI模型选项"""
    GPT4 = "gpt-4"
    GPT4O = "gpt-4o"
    CLAUDE = "claude-3.5-sonnet"
    CODELLAMA = "codellama"


class ConversionRequest(BaseModel):
    """
    Code Conversion Request / 代码转换请求
    
    Request payload for code conversion API.
    代码转换API的请求负载。
    
    Fields / 字段:
    - source_language: Source programming language / 源编程语言
    - target_language: Target programming language / 目标编程语言
    - git_url: Git repository URL (optional) / Git仓库URL（可选）
    - ai_model: AI model to use / 使用的AI模型
    - multi_ai_strategy: Multi-AI strategy (optional) / 多AI策略（可选）
    """
    source_type: SourceType = Field(..., description="输入源类型: git 或 upload")
    git_url: Optional[HttpUrl] = Field(None, description="Git仓库URL (source_type=git时必填)")
    git_branch: Optional[str] = Field("main", description="Git分支名称")
    upload_path: Optional[str] = Field(None, description="上传文件路径 (source_type=upload时必填)")
    
    source_language: SupportedLanguage = Field(..., description="源语言")
    target_language: SupportedLanguage = Field(..., description="目标语言")
    ai_model: AIModel = Field(AIModel.GPT4, description="使用的AI模型")
    
    preserve_comments: bool = Field(True, description="保留代码注释")
    preserve_structure: bool = Field(True, description="保持项目结构")
    add_type_hints: bool = Field(True, description="添加类型提示（如果目标语言支持）")
    optimize_code: bool = Field(False, description="优化代码质量")
    
    custom_rules: Optional[Dict[str, Any]] = Field(None, description="自定义转换规则")
    
    class Config:
        json_schema_extra = {
            "example": {
                "source_type": "git",
                "git_url": "https://github.com/user/java-project.git",
                "git_branch": "main",
                "source_language": "java",
                "target_language": "python",
                "ai_model": "gpt-4",
                "preserve_comments": True,
                "preserve_structure": True
            }
        }


class ConversionResponse(BaseModel):
    """代码转换响应"""
    task_id: str = Field(..., description="任务ID")
    status: TaskStatusEnum = Field(..., description="任务状态")
    message: str = Field(..., description="响应消息")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")


class TaskStatus(BaseModel):
    """任务状态详情"""
    task_id: str
    status: TaskStatusEnum
    progress: int = Field(0, ge=0, le=100, description="完成进度 0-100")
    stage: str = Field("", description="当前阶段描述")
    
    source_language: Optional[SupportedLanguage] = None
    target_language: Optional[SupportedLanguage] = None
    ai_model: Optional[AIModel] = None
    
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    
    total_files: int = Field(0, description="总文件数")
    processed_files: int = Field(0, description="已处理文件数")
    
    output_file: Optional[str] = Field(None, description="输出文件路径")
    error: Optional[str] = Field(None, description="错误信息")
    
    result: Optional[Dict[str, Any]] = Field(None, description="转换结果详情")
    
    class Config:
        json_schema_extra = {
            "example": {
                "task_id": "abc-123-def-456",
                "status": "processing",
                "progress": 45,
                "stage": "AI翻译中...",
                "source_language": "java",
                "target_language": "python",
                "total_files": 50,
                "processed_files": 23
            }
        }


class FileInfo(BaseModel):
    """文件信息"""
    path: str
    language: str
    size: int
    lines: int
    classes: List[str] = []
    functions: List[str] = []
    imports: List[str] = []


class ProjectInfo(BaseModel):
    """项目信息"""
    name: str
    language: SupportedLanguage
    total_files: int
    total_lines: int
    files: List[FileInfo]
    dependencies: Dict[str, str] = {}
    structure: Dict[str, Any] = {}
    
    
class TranslationResult(BaseModel):
    """翻译结果"""
    source_file: str
    target_file: str
    source_code: str
    translated_code: str
    success: bool
    error: Optional[str] = None
    warnings: List[str] = []


class LanguageInfo(BaseModel):
    """语言信息"""
    id: str
    name: str
    icon: str
    extensions: List[str]
    parser: str
    package_manager: str

