"""
Task Manager / 任务管理器

Manages the lifecycle and status of conversion tasks.
管理转换任务的生命周期和状态。

Features / 功能:
- Task creation and tracking / 任务创建和追踪
- Status updates / 状态更新
- Progress monitoring / 进度监控
- Result storage / 结果存储
"""

import uuid
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path
import json
from loguru import logger

from models.schemas import TaskStatus, TaskStatusEnum, SupportedLanguage


class TaskManager:
    """任务管理器"""
    
    def __init__(self):
        # 内存存储（生产环境应使用数据库）
        self.tasks: Dict[str, TaskStatus] = {}
        
        # 持久化存储目录
        self.storage_dir = Path("./data/tasks")
        self.storage_dir.mkdir(parents=True, exist_ok=True)
    
    def create_task(
        self,
        source_language: str,
        target_language: str,
        ai_model: str
    ) -> str:
        """
        创建新任务
        
        Returns:
            str: 任务ID
        """
        task_id = str(uuid.uuid4())
        
        task = TaskStatus(
            task_id=task_id,
            status=TaskStatusEnum.QUEUED,
            source_language=SupportedLanguage(source_language),
            target_language=SupportedLanguage(target_language),
            ai_model=ai_model,
            progress=0,
            stage="任务已创建"
        )
        
        self.tasks[task_id] = task
        self._save_task(task)
        
        logger.info(f"创建任务: {task_id}, {source_language} → {target_language}")
        
        return task_id
    
    def get_task_status(self, task_id: str) -> Optional[Dict]:
        """获取任务状态"""
        task = self.tasks.get(task_id)
        
        if not task:
            # 尝试从存储加载
            task = self._load_task(task_id)
        
        if task:
            return task.model_dump()
        
        return None
    
    def update_task(
        self,
        task_id: str,
        status: Optional[str] = None,
        progress: Optional[int] = None,
        stage: Optional[str] = None,
        total_files: Optional[int] = None,
        processed_files: Optional[int] = None,
        output_file: Optional[str] = None,
        error: Optional[str] = None,
        result: Optional[Dict] = None
    ):
        """更新任务状态"""
        task = self.tasks.get(task_id)
        
        if not task:
            logger.warning(f"任务不存在: {task_id}")
            return
        
        # 更新字段
        if status:
            task.status = TaskStatusEnum(status)
        if progress is not None:
            task.progress = progress
        if stage:
            task.stage = stage
        if total_files is not None:
            task.total_files = total_files
        if processed_files is not None:
            task.processed_files = processed_files
        if output_file:
            task.output_file = output_file
        if error:
            task.error = error
        if result:
            task.result = result
        
        # 更新时间
        task.updated_at = datetime.now()
        
        # 如果完成或失败，设置完成时间
        if status in [TaskStatusEnum.COMPLETED.value, TaskStatusEnum.FAILED.value]:
            task.completed_at = datetime.now()
        
        # 保存
        self._save_task(task)
        
        logger.info(
            f"任务更新: {task_id}, 状态: {task.status}, "
            f"进度: {task.progress}%, 阶段: {task.stage}"
        )
    
    def list_tasks(
        self,
        limit: int = 20,
        offset: int = 0,
        status: Optional[str] = None
    ) -> List[Dict]:
        """列出任务"""
        tasks = list(self.tasks.values())
        
        # 按状态过滤
        if status:
            tasks = [t for t in tasks if t.status == status]
        
        # 排序（最新的在前）
        tasks.sort(key=lambda t: t.created_at, reverse=True)
        
        # 分页
        tasks = tasks[offset:offset + limit]
        
        return [t.model_dump() for t in tasks]
    
    def delete_task(self, task_id: str) -> bool:
        """删除任务"""
        if task_id in self.tasks:
            del self.tasks[task_id]
            
            # 删除存储文件
            task_file = self.storage_dir / f"{task_id}.json"
            if task_file.exists():
                task_file.unlink()
            
            logger.info(f"删除任务: {task_id}")
            return True
        
        return False
    
    def _save_task(self, task: TaskStatus):
        """保存任务到存储"""
        task_file = self.storage_dir / f"{task.task_id}.json"
        
        with open(task_file, 'w', encoding='utf-8') as f:
            json.dump(task.model_dump(), f, indent=2, default=str)
    
    def _load_task(self, task_id: str) -> Optional[TaskStatus]:
        """从存储加载任务"""
        task_file = self.storage_dir / f"{task_id}.json"
        
        if not task_file.exists():
            return None
        
        try:
            with open(task_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            task = TaskStatus(**data)
            self.tasks[task_id] = task
            return task
            
        except Exception as e:
            logger.error(f"加载任务失败 {task_id}: {str(e)}")
            return None
    
    def get_statistics(self) -> Dict:
        """获取统计信息"""
        total = len(self.tasks)
        
        stats = {
            "total": total,
            "queued": 0,
            "processing": 0,
            "completed": 0,
            "failed": 0
        }
        
        for task in self.tasks.values():
            if task.status == TaskStatusEnum.QUEUED:
                stats["queued"] += 1
            elif task.status == TaskStatusEnum.PROCESSING:
                stats["processing"] += 1
            elif task.status == TaskStatusEnum.COMPLETED:
                stats["completed"] += 1
            elif task.status == TaskStatusEnum.FAILED:
                stats["failed"] += 1
        
        return stats

