# AI Code Migration Platform - Quick Start Script (Windows)
# AI代码迁移平台 - 快速启动脚本 (Windows)

Write-Host "🚀 Starting AI Code Migration Platform..." -ForegroundColor Cyan
Write-Host "🚀 启动AI代码迁移平台..." -ForegroundColor Cyan
Write-Host ""

# Check if Redis is running
function Check-Redis {
    Write-Host "🔍 Checking Redis..." -ForegroundColor Yellow
    
    try {
        $redisTest = redis-cli ping 2>$null
        if ($redisTest -eq "PONG") {
            Write-Host "✅ Redis is running" -ForegroundColor Green
            return $true
        }
    } catch {
        Write-Host "❌ Redis is not running" -ForegroundColor Red
        Write-Host ""
        Write-Host "Please install and start Redis:" -ForegroundColor Yellow
        Write-Host "  Option 1: Use Docker" -ForegroundColor White
        Write-Host "    docker run -d -p 6379:6379 --name redis redis:7-alpine" -ForegroundColor Gray
        Write-Host ""
        Write-Host "  Option 2: Use WSL2" -ForegroundColor White
        Write-Host "    wsl --install" -ForegroundColor Gray
        Write-Host "    wsl" -ForegroundColor Gray
        Write-Host "    sudo apt install redis-server" -ForegroundColor Gray
        Write-Host "    sudo service redis-server start" -ForegroundColor Gray
        Write-Host ""
        return $false
    }
}

# Check if virtual environment exists
function Check-Venv {
    if (-not (Test-Path "backend\venv")) {
        Write-Host "📦 Creating Python virtual environment..." -ForegroundColor Yellow
        Push-Location backend
        python -m venv venv
        .\venv\Scripts\Activate.ps1
        pip install -r ..\requirements.txt
        Pop-Location
        Write-Host "✅ Virtual environment created" -ForegroundColor Green
    } else {
        Write-Host "✅ Virtual environment exists" -ForegroundColor Green
    }
}

# Check if .env exists
function Check-Env {
    if (-not (Test-Path "backend\.env")) {
        Write-Host "⚠️  .env file not found" -ForegroundColor Yellow
        Write-Host "Creating .env from .env.example..." -ForegroundColor Yellow
        Copy-Item "backend\.env.example" "backend\.env"
        Write-Host "⚠️  Please edit backend\.env and add your API keys" -ForegroundColor Yellow
        Write-Host ""
    } else {
        Write-Host "✅ .env file exists" -ForegroundColor Green
    }
}

# Check if frontend dependencies are installed
function Check-Frontend {
    if (-not (Test-Path "frontend\node_modules")) {
        Write-Host "📦 Installing frontend dependencies..." -ForegroundColor Yellow
        Push-Location frontend
        npm install
        Pop-Location
        Write-Host "✅ Frontend dependencies installed" -ForegroundColor Green
    } else {
        Write-Host "✅ Frontend dependencies exist" -ForegroundColor Green
    }
}

# Main execution
try {
    Write-Host "==================================" -ForegroundColor Cyan
    Write-Host "  AI Code Migration Platform" -ForegroundColor Cyan
    Write-Host "  AI代码迁移平台" -ForegroundColor Cyan
    Write-Host "==================================" -ForegroundColor Cyan
    Write-Host ""
    
    # Run checks
    if (-not (Check-Redis)) {
        exit 1
    }
    Check-Venv
    Check-Env
    Check-Frontend
    
    Write-Host ""
    Write-Host "🔷 Starting Backend (FastAPI)..." -ForegroundColor Cyan
    
    # Start backend in new window
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\backend'; .\venv\Scripts\Activate.ps1; python main.py"
    
    Start-Sleep -Seconds 3
    
    Write-Host "🔷 Starting Frontend (React + Vite)..." -ForegroundColor Cyan
    
    # Start frontend in new window
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\frontend'; npm run dev"
    
    Write-Host ""
    Write-Host "==================================" -ForegroundColor Green
    Write-Host "✅ All services started!" -ForegroundColor Green
    Write-Host "==================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "📍 Access URLs:" -ForegroundColor Cyan
    Write-Host "   Frontend:  http://localhost:3000" -ForegroundColor White
    Write-Host "   Dashboard: http://localhost:3000/dashboard" -ForegroundColor White
    Write-Host "   Backend:   http://localhost:8000" -ForegroundColor White
    Write-Host "   API Docs:  http://localhost:8000/docs" -ForegroundColor White
    Write-Host ""
    Write-Host "📊 Quick Links:" -ForegroundColor Cyan
    Write-Host "   Cost Estimator: http://localhost:3000/dashboard" -ForegroundColor White
    Write-Host "   Cache Stats:    http://localhost:8000/api/v1/cache/stats" -ForegroundColor White
    Write-Host "   Cost Report:    http://localhost:8000/api/v1/cost/report" -ForegroundColor White
    Write-Host ""
    Write-Host "💡 Tip: Close the PowerShell windows to stop the services" -ForegroundColor Yellow
    Write-Host ""
    
    # Open browser
    Start-Sleep -Seconds 5
    Start-Process "http://localhost:3000/dashboard"
    
} catch {
    Write-Host "❌ Error: $_" -ForegroundColor Red
    exit 1
}

