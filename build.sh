#!/bin/bash

# Build script for Easypanel deployment
# This script prepares the project for deployment on Easypanel

set -e

echo "🚀 Building TradingView API for Easypanel"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "webapp/app.py" ]; then
    echo -e "${RED}❌ Error: webapp/app.py not found!${NC}"
    echo "Please run this script from the project root directory."
    exit 1
fi

echo -e "${YELLOW}📋 Checking project structure...${NC}"

# Verify required files exist
required_files=(
    "Dockerfile"
    "webapp/app.py"
    "webapp/requirements.production.txt"
    "webapp/api_database.py"
)

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo -e "${RED}❌ Required file not found: $file${NC}"
        exit 1
    fi
done

echo -e "${GREEN}✅ All required files found${NC}"

# Create logs directory if it doesn't exist
echo -e "${YELLOW}📁 Creating directories...${NC}"
mkdir -p logs
mkdir -p export

# Set proper permissions
chmod 755 logs
chmod 755 export

echo -e "${GREEN}✅ Directories created${NC}"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env file not found, creating from template...${NC}"
    if [ -f ".env.easypanel" ]; then
        cp .env.easypanel .env
        echo -e "${GREEN}✅ .env file created from .env.easypanel${NC}"
    else
        echo -e "${YELLOW}⚠️  Creating basic .env file...${NC}"
        cat > .env << EOF
# Database Configuration
DATABASE_URL=postgres://postgres:password@localhost:5432/tradingview

# API Configuration
API_HOST=0.0.0.0
API_PORT=5000
FLASK_ENV=production
SECRET_KEY=your-secret-key-here

# Worker Configuration
WORKER_ENABLED=True
SYNC_INTERVAL_CATEGORIES=3600
SYNC_INTERVAL_ASSETS=1800
SYNC_INTERVAL_CANDLES=60
SYNC_INTERVAL_CURRENT=1

# Cache Configuration
CACHE_ENABLED=True
CACHE_TTL=300

# Logging
LOG_LEVEL=INFO
EOF
        echo -e "${GREEN}✅ Basic .env file created${NC}"
    fi
fi

# Test Docker build locally (optional)
if command -v docker &> /dev/null; then
    echo -e "${YELLOW}🐳 Testing Docker build locally...${NC}"
    if docker build -t tradingview-api-test . > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Docker build test successful${NC}"
        docker rmi tradingview-api-test > /dev/null 2>&1
    else
        echo -e "${YELLOW}⚠️  Docker build test failed, but continuing...${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Docker not found, skipping build test${NC}"
fi

# Create .dockerignore if it doesn't exist
if [ ! -f ".dockerignore" ]; then
    echo -e "${YELLOW}📝 Creating .dockerignore...${NC}"
    cat > .dockerignore << EOF
# Git
.git
.gitignore

# Documentation
*.md
docs/

# Python
__pycache__/
*.py[cod]
*.so
.Python
build/
dist/
*.egg-info/

# Virtual environments
venv/
env/
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
logs/
*.log

# Test files
test_*.py
*_test.py
tests/

# Development files
.env.local
.env.development
.env.test

# Temporary files
tmp/
temp/
*.tmp
EOF
    echo -e "${GREEN}✅ .dockerignore created${NC}"
fi

echo ""
echo -e "${GREEN}🎉 Build preparation completed successfully!${NC}"
echo "=========================================="
echo ""
echo -e "${YELLOW}📋 Next steps:${NC}"
echo "1. Commit and push your changes:"
echo "   git add ."
echo "   git commit -m 'Ajuste docker para Easypanel'"
echo "   git push origin main"
echo ""
echo "2. Deploy on Easypanel:"
echo "   - Go to your Easypanel dashboard"
echo "   - Create new project from Git repository"
echo "   - Configure environment variables"
echo "   - Deploy!"
echo ""
echo "3. Test your API:"
echo "   curl https://your-domain.com/api/health"
echo ""
echo -e "${GREEN}🚀 Your TradingView API is ready for Easypanel deployment!${NC}"
