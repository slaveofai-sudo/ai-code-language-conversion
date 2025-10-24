


#!/bin/bash

# AI Code Migration Platform - 快速设置脚本
# 适用于 macOS 和 Linux

set -e

echo "🚀 AI Code Migration Platform - 快速设置"
echo "========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查 Python
echo -e "${YELLOW}检查 Python...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓ 找到 $PYTHON_VERSION${NC}"
else
    echo -e "${RED}✗ 未找到 Python 3${NC}"
    echo "请先安装 Python 3.10 或更高版本"
    exit 1
fi

# 检查 Node.js
echo -e "${YELLOW}检查 Node.js...${NC}"
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓ 找到 Node.js $NODE_VERSION${NC}"
else
    echo -e "${RED}✗ 未找到 Node.js${NC}"
    echo "请先安装 Node.js 16 或更高版本"
    exit 1
fi

# 创建虚拟环境
echo ""
echo -e "${YELLOW}创建 Python 虚拟环境...${NC}"
python3 -m venv venv
echo -e "${GREEN}✓ 虚拟环境已创建${NC}"

# 激活虚拟环境
echo -e "${YELLOW}激活虚拟环境...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ 虚拟环境已激活${NC}"

# 安装 Python 依赖
echo ""
echo -e "${YELLOW}安装 Python 依赖...${NC}"
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt
echo -e "${GREEN}✓ Python 依赖安装完成${NC}"

# 安装前端依赖
echo ""
echo -e "${YELLOW}安装前端依赖...${NC}"
cd frontend
npm install
cd ..
echo -e "${GREEN}✓ 前端依赖安装完成${NC}"

# 创建必要的目录
echo ""
echo -e "${YELLOW}创建数据目录...${NC}"
mkdir -p data/uploads data/outputs data/cache data/tasks logs
echo -e "${GREEN}✓ 目录已创建${NC}"

# 创建 .env 文件
echo ""
if [ ! -f .env ]; then
    echo -e "${YELLOW}创建 .env 配置文件...${NC}"
    cat > .env << 'EOF'
# Application Settings
APP_NAME=AI Code Migration Platform
DEBUG=true
ENVIRONMENT=development

# Server
HOST=0.0.0.0
PORT=8000

# Database (SQLite for development)
DATABASE_URL=sqlite:///./data/migration.db

# Redis (optional for development)
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
EOF
    echo -e "${GREEN}✓ .env 文件已创建${NC}"
    echo -e "${YELLOW}⚠️  请编辑 .env 文件并添加你的 API Keys${NC}"
else
    echo -e "${GREEN}✓ .env 文件已存在${NC}"
fi

# 创建启动脚本
echo ""
echo -e "${YELLOW}创建启动脚本...${NC}"

cat > start.sh << 'EOF'
#!/bin/bash

# 启动 AI Code Migration Platform

echo "🚀 启动 AI Code Migration Platform..."
echo ""

# 启动后端
echo "启动后端服务..."
source venv/bin/activate
cd backend
python main.py &
BACKEND_PID=$!
cd ..

# 等待后端启动
sleep 3

# 启动前端
echo "启动前端服务..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ 服务已启动！"
echo ""
echo "📍 访问地址："
echo "   前端: http://localhost:3000"
echo "   API:  http://localhost:8000/docs"
echo ""
echo "💡 按 Ctrl+C 停止服务"
echo ""

# 等待用户停止
trap "echo ''; echo '🛑 停止服务...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
EOF

chmod +x start.sh
echo -e "${GREEN}✓ 启动脚本已创建 (start.sh)${NC}"

# 运行健康检查
echo ""
echo -e "${YELLOW}运行健康检查...${NC}"
python cli.py doctor

# 完成
echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}✨ 设置完成！${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo "📝 下一步："
echo "   1. 编辑 .env 文件，添加你的 API Keys"
echo "   2. 运行 ./start.sh 启动服务"
echo "   3. 访问 http://localhost:3000"
echo ""
echo "📚 文档："
echo "   - 快速开始: cat QUICKSTART.md"
echo "   - 使用教程: cat TUTORIAL.md"
echo "   - API 文档: http://localhost:8000/docs"
echo ""
echo "🎉 祝你使用愉快！"

