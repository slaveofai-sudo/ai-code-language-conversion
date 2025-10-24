"""
Git Repository Manager / Git仓库管理器

Supports cloning and analyzing remote Git repositories.
支持克隆和分析远程Git仓库。

Features / 功能:
- Clone from GitHub/GitLab / 从GitHub/GitLab克隆
- Shallow clone for faster speed / 浅克隆提升速度
- Repository size validation / 仓库大小验证
- Branch selection / 分支选择
"""

import os
import shutil
from pathlib import Path
from typing import Optional
import git
from git import Repo
from loguru import logger


class GitManager:
    """
    Git Repository Manager / Git仓库管理类
    
    Handles all Git operations including:
    处理所有Git操作，包括:
    - Repository cloning / 仓库克隆
    - Size validation / 大小验证
    - Branch management / 分支管理
    """
    
    def __init__(self):
        self.max_repo_size = int(os.getenv("GIT_MAX_REPO_SIZE", 524288000))  # 500MB
        self.clone_timeout = int(os.getenv("GIT_CLONE_TIMEOUT", 300))
        self.clone_depth = int(os.getenv("GIT_CLONE_DEPTH", 1))
        
    async def clone_repository(
        self,
        git_url: str,
        target_dir: Path,
        branch: Optional[str] = None
    ) -> Path:
        """
        克隆Git仓库
        
        Args:
            git_url: Git仓库URL
            target_dir: 目标目录
            branch: 分支名称 (默认为main/master)
            
        Returns:
            Path: 克隆后的目录路径
        """
        try:
            logger.info(f"开始克隆仓库: {git_url}")
            
            # 清理目标目录
            if target_dir.exists():
                shutil.rmtree(target_dir)
            target_dir.mkdir(parents=True, exist_ok=True)
            
            # 克隆参数
            clone_kwargs = {
                'depth': self.clone_depth,  # 浅克隆
                'single_branch': True,
            }
            
            if branch:
                clone_kwargs['branch'] = branch
            
            # 执行克隆
            repo = Repo.clone_from(
                git_url,
                target_dir,
                **clone_kwargs
            )
            
            logger.info(f"仓库克隆成功: {target_dir}")
            
            # 检查仓库大小
            repo_size = self._get_directory_size(target_dir)
            if repo_size > self.max_repo_size:
                shutil.rmtree(target_dir)
                raise ValueError(
                    f"仓库大小 ({repo_size / 1024 / 1024:.2f}MB) "
                    f"超过限制 ({self.max_repo_size / 1024 / 1024:.2f}MB)"
                )
            
            # 获取仓库信息
            repo_info = self._get_repo_info(repo)
            logger.info(f"仓库信息: {repo_info}")
            
            return target_dir
            
        except git.GitCommandError as e:
            logger.error(f"Git克隆失败: {str(e)}")
            raise ValueError(f"无法克隆仓库: {str(e)}")
        except Exception as e:
            logger.error(f"克隆过程出错: {str(e)}")
            raise
    
    def _get_directory_size(self, path: Path) -> int:
        """计算目录大小"""
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if os.path.exists(filepath):
                    total_size += os.path.getsize(filepath)
        return total_size
    
    def _get_repo_info(self, repo: Repo) -> dict:
        """获取仓库信息"""
        try:
            return {
                "branch": repo.active_branch.name,
                "commit": repo.head.commit.hexsha[:7],
                "commit_message": repo.head.commit.message.strip(),
                "author": str(repo.head.commit.author),
                "commit_date": repo.head.commit.committed_datetime.isoformat(),
            }
        except Exception as e:
            logger.warning(f"无法获取仓库信息: {str(e)}")
            return {}
    
    async def validate_git_url(self, git_url: str) -> bool:
        """验证Git URL是否有效"""
        try:
            # 简单检查URL格式
            if not (git_url.startswith("https://") or git_url.startswith("git@")):
                return False
            
            # 可以添加更多验证逻辑，如检查仓库是否可访问
            return True
            
        except Exception:
            return False
    
    def get_default_branch(self, repo: Repo) -> str:
        """获取默认分支名称"""
        try:
            return repo.active_branch.name
        except Exception:
            # 尝试常见的默认分支名
            for branch_name in ['main', 'master', 'develop']:
                try:
                    repo.git.checkout(branch_name)
                    return branch_name
                except:
                    continue
            return "main"

