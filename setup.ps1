# AI Code Migration Platform - Windows 快速设置脚本
# PowerShell 版本

Write-Host "🚀 AI Code Migration Platform - 快速设置" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# 检查 Python
Write-Host "检查 Python..." -ForegroundColor Yellow
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonVersion = python --version
    Write-Host "✓ 找到 $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "✗ 未找到 Python" -ForegroundColor Red
    Write-Host "请先安装 Python 3.10 或更高版本"
    exit 1
}

# 检查 Node.js
Write-Host "检查 Node.js..." -ForegroundColor Yellow
if (Get-Command node -ErrorAction SilentlyContinue) {
    $nodeVersion = node --version
    Write-Host "✓ 找到 Node.js $nodeVersion" -ForegroundColor Green
} else {
    Write-Host "✗ 未找到 Node.js" -ForegroundColor Red
    Write-Host "请先安装 Node.js 16 或更高版本"
    exit 1
}

# 创建虚拟环境
Write-Host ""
Write-Host "创建 Python 虚拟环境..." -ForegroundColor Yellow
python -m venv venv
Write-Host "✓ 虚拟环境已创建" -ForegroundColor Green

# 激活虚拟环境
Write-Host "激活虚拟环境..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1
Write-Host "✓ 虚拟环境已激活" -ForegroundColor Green

# 安装 Python 依赖
Write-Host ""
Write-Host "安装 Python 依赖..." -ForegroundColor Yellow
python -m pip install --upgrade pip | Out-Null
pip install -r requirements.txt
Write-Host "✓ Python 依赖安装完成" -ForegroundColor Green

# 安装前端依赖
Write-Host ""
Write-Host "安装前端依赖..." -ForegroundColor Yellow
Set-Location frontend
npm install
Set-Location ..
Write-Host "✓ 前端依赖安装完成" -ForegroundColor Green

# 创建必要的目录
Write-Host ""
Write-Host "创建数据目录..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path data\uploads | Out-Null
New-Item -ItemType Directory -Force -Path data\outputs | Out-Null
New-Item -ItemType Directory -Force -Path data\cache | Out-Null
New-Item -ItemType Directory -Force -Path data\tasks | Out-Null
New-Item -ItemType Directory -Force -Path logs | Out-Null
Write-Host "✓ 目录已创建" -ForegroundColor Green

# 创建 .env 文件
Write-Host ""
if (-not (Test-Path .env)) {
    Write-Host "创建 .env 配置文件..." -ForegroundColor Yellow
    @"
# Application Settings
APP_NAME=AI Code Migration Platform
DEBUG=true
ENVIRONMENT=development

# Server
HOST=0.0.0.0
PORT=8000

# Database (SQLite for development)
DATABASE_URL=sqlite:///./data/migration.db

# Redis (optional)
REDIS_URL=redis://localhost:6379/0

# AI Models - 请填写你的 API Keys
OPENAI_API_KEY=your-openai-api-key-here
ANTHROPIC_API_KEY=your-anthropic-api-key-here

# Local Model (Ollama)
LOCAL_MODEL_ENABLED=false
LOCAL_MODEL_URL=http://localhost:11434

# Git Configuration
GIT_MAX_REPO_SIZE=524288000
GIT_CLONE_TIMEOUT=300

# File Storage
UPLOAD_DIR=./data/uploads
OUTPUT_DIR=./data/outputs
CACHE_DIR=./data/cache
MAX_UPLOAD_SIZE=104857600

# Conversion Settings
MAX_CONCURRENT_TASKS=4
CONVERSION_TIMEOUT=3600

# Security
SECRET_KEY=change-this-in-production
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log
"@ | Out-File -FilePath .env -Encoding UTF8
    Write-Host "✓ .env 文件已创建" -ForegroundColor Green
    Write-Host "⚠️  请编辑 .env 文件并添加你的 API Keys" -ForegroundColor Yellow
} else {
    Write-Host "✓ .env 文件已存在" -ForegroundColor Green
}

# 创建启动脚本
Write-Host ""
Write-Host "创建启动脚本..." -ForegroundColor Yellow

@"
# 启动 AI Code Migration Platform

Write-Host "🚀 启动 AI Code Migration Platform..." -ForegroundColor Cyan
Write-Host ""

# 启动后端
Write-Host "启动后端服务..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; python main.py"

# 等待后端启动
Start-Sleep -Seconds 3

# 启动前端
Write-Host "启动前端服务..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"

Write-Host ""
Write-Host "✅ 服务已启动！" -ForegroundColor Green
Write-Host ""
Write-Host "📍 访问地址：" -ForegroundColor Cyan
Write-Host "   前端: http://localhost:3000"
Write-Host "   API:  http://localhost:8000/docs"
Write-Host ""
Write-Host "💡 关闭 PowerShell 窗口以停止服务" -ForegroundColor Yellow
"@ | Out-File -FilePath start.ps1 -Encoding UTF8

Write-Host "✓ 启动脚本已创建 (start.ps1)" -ForegroundColor Green

# 运行健康检查
Write-Host ""
Write-Host "运行健康检查..." -ForegroundColor Yellow
python cli.py doctor

# 完成
Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host "✨ 设置完成！" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""
Write-Host "📝 下一步："
Write-Host "   1. 编辑 .env 文件，添加你的 API Keys"
Write-Host "   2. 运行 .\start.ps1 启动服务"
Write-Host "   3. 访问 http://localhost:3000"
Write-Host ""
Write-Host "📚 文档："
Write-Host "   - 快速开始: Get-Content QUICKSTART.md"
Write-Host "   - 使用教程: Get-Content TUTORIAL.md"
Write-Host "   - API 文档: http://localhost:8000/docs"
Write-Host ""
Write-Host "🎉 祝你使用愉快！" -ForegroundColor Cyan

