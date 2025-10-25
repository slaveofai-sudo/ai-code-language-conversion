#!/bin/bash

# AI Code Migration Platform - Quick Start Script
# AI代码迁移平台 - 快速启动脚本

set -e

echo "🚀 Starting AI Code Migration Platform..."
echo "🚀 启动AI代码迁移平台..."
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Redis is installed
check_redis() {
    echo "🔍 Checking Redis..."
    if command -v redis-cli &> /dev/null; then
        if redis-cli ping &> /dev/null; then
            echo -e "${GREEN}✅ Redis is running${NC}"
            return 0
        else
            echo -e "${YELLOW}⚠️  Redis is installed but not running${NC}"
            echo "Starting Redis..."
            
            if [[ "$OSTYPE" == "darwin"* ]]; then
                brew services start redis
            elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
                sudo systemctl start redis-server
            fi
            
            sleep 2
            
            if redis-cli ping &> /dev/null; then
                echo -e "${GREEN}✅ Redis started successfully${NC}"
                return 0
            fi
        fi
    else
        echo -e "${RED}❌ Redis is not installed${NC}"
        echo ""
        echo "Please install Redis:"
        echo "  macOS:   brew install redis"
        echo "  Ubuntu:  sudo apt install redis-server"
        echo "  Or use Docker: docker run -d -p 6379:6379 redis:7-alpine"
        return 1
    fi
}

# Check if virtual environment exists
check_venv() {
    if [ ! -d "backend/venv" ]; then
        echo "📦 Creating Python virtual environment..."
        cd backend
        python3 -m venv venv
        source venv/bin/activate
        pip install -r ../requirements.txt
        cd ..
        echo -e "${GREEN}✅ Virtual environment created${NC}"
    else
        echo -e "${GREEN}✅ Virtual environment exists${NC}"
    fi
}

# Check if .env exists
check_env() {
    if [ ! -f "backend/.env" ]; then
        echo -e "${YELLOW}⚠️  .env file not found${NC}"
        echo "Creating .env from .env.example..."
        cp backend/.env.example backend/.env
        echo -e "${YELLOW}⚠️  Please edit backend/.env and add your API keys${NC}"
        echo ""
    else
        echo -e "${GREEN}✅ .env file exists${NC}"
    fi
}

# Check if frontend dependencies are installed
check_frontend() {
    if [ ! -d "frontend/node_modules" ]; then
        echo "📦 Installing frontend dependencies..."
        cd frontend
        npm install
        cd ..
        echo -e "${GREEN}✅ Frontend dependencies installed${NC}"
    else
        echo -e "${GREEN}✅ Frontend dependencies exist${NC}"
    fi
}

# Start backend
start_backend() {
    echo ""
    echo "🔷 Starting Backend (FastAPI)..."
    cd backend
    source venv/bin/activate
    python main.py &
    BACKEND_PID=$!
    cd ..
    echo -e "${GREEN}✅ Backend started (PID: $BACKEND_PID)${NC}"
}

# Start frontend
start_frontend() {
    echo ""
    echo "🔷 Starting Frontend (React + Vite)..."
    cd frontend
    npm run dev &
    FRONTEND_PID=$!
    cd ..
    echo -e "${GREEN}✅ Frontend started (PID: $FRONTEND_PID)${NC}"
}

# Cleanup function
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    echo "👋 Services stopped"
    exit 0
}

# Trap Ctrl+C
trap cleanup INT TERM

# Main execution
main() {
    echo "=================================="
    echo "  AI Code Migration Platform"
    echo "  AI代码迁移平台"
    echo "=================================="
    echo ""
    
    # Run checks
    check_redis || exit 1
    check_venv
    check_env
    check_frontend
    
    # Start services
    start_backend
    sleep 3
    start_frontend
    
    echo ""
    echo "=================================="
    echo -e "${GREEN}✅ All services started!${NC}"
    echo "=================================="
    echo ""
    echo "📍 Access URLs:"
    echo "   Frontend:  http://localhost:3000"
    echo "   Dashboard: http://localhost:3000/dashboard"
    echo "   Backend:   http://localhost:8000"
    echo "   API Docs:  http://localhost:8000/docs"
    echo ""
    echo "📊 Quick Links:"
    echo "   Cost Estimator: http://localhost:3000/dashboard"
    echo "   Cache Stats:    http://localhost:8000/api/v1/cache/stats"
    echo "   Cost Report:    http://localhost:8000/api/v1/cost/report"
    echo ""
    echo "Press Ctrl+C to stop all services"
    echo ""
    
    # Keep script running
    wait
}

# Run main function
main

