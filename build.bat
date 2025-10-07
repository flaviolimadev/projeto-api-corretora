@echo off
setlocal enabledelayedexpansion

REM Build script for Easypanel deployment (Windows)
REM This script prepares the project for deployment on Easypanel

echo.
echo ==========================================
echo 🚀 Building TradingView API for Easypanel
echo ==========================================
echo.

REM Check if we're in the right directory
if not exist "webapp\app.py" (
    echo ❌ Error: webapp\app.py not found!
    echo Please run this script from the project root directory.
    pause
    exit /b 1
)

echo 📋 Checking project structure...

REM Verify required files exist
set required_files=Dockerfile webapp\app.py webapp\requirements.production.txt webapp\api_database.py

for %%f in (%required_files%) do (
    if not exist "%%f" (
        echo ❌ Required file not found: %%f
        pause
        exit /b 1
    )
)

echo ✅ All required files found

REM Create directories if they don't exist
echo 📁 Creating directories...
if not exist "logs" mkdir logs
if not exist "export" mkdir export

echo ✅ Directories created

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  .env file not found, creating from template...
    if exist ".env.easypanel" (
        copy ".env.easypanel" ".env" >nul
        echo ✅ .env file created from .env.easypanel
    ) else (
        echo ⚠️  Creating basic .env file...
        (
            echo # Database Configuration
            echo DATABASE_URL=postgres://postgres:password@localhost:5432/tradingview
            echo.
            echo # API Configuration
            echo API_HOST=0.0.0.0
            echo API_PORT=5000
            echo FLASK_ENV=production
            echo SECRET_KEY=your-secret-key-here
            echo.
            echo # Worker Configuration
            echo WORKER_ENABLED=True
            echo SYNC_INTERVAL_CATEGORIES=3600
            echo SYNC_INTERVAL_ASSETS=1800
            echo SYNC_INTERVAL_CANDLES=60
            echo SYNC_INTERVAL_CURRENT=1
            echo.
            echo # Cache Configuration
            echo CACHE_ENABLED=True
            echo CACHE_TTL=300
            echo.
            echo # Logging
            echo LOG_LEVEL=INFO
        ) > .env
        echo ✅ Basic .env file created
    )
)

REM Test Docker build locally (optional)
docker --version >nul 2>&1
if !errorlevel! equ 0 (
    echo 🐳 Testing Docker build locally...
    docker build -t tradingview-api-test . >nul 2>&1
    if !errorlevel! equ 0 (
        echo ✅ Docker build test successful
        docker rmi tradingview-api-test >nul 2>&1
    ) else (
        echo ⚠️  Docker build test failed, but continuing...
    )
) else (
    echo ⚠️  Docker not found, skipping build test
)

REM Create .dockerignore if it doesn't exist
if not exist ".dockerignore" (
    echo 📝 Creating .dockerignore...
    (
        echo # Git
        echo .git
        echo .gitignore
        echo.
        echo # Documentation
        echo *.md
        echo docs/
        echo.
        echo # Python
        echo __pycache__/
        echo *.py[cod]
        echo *.so
        echo .Python
        echo build/
        echo dist/
        echo *.egg-info/
        echo.
        echo # Virtual environments
        echo venv/
        echo env/
        echo .venv/
        echo.
        echo # IDE
        echo .vscode/
        echo .idea/
        echo *.swp
        echo *.swo
        echo.
        echo # OS
        echo .DS_Store
        echo Thumbs.db
        echo.
        echo # Logs
        echo logs/
        echo *.log
        echo.
        echo # Test files
        echo test_*.py
        echo *_test.py
        echo tests/
        echo.
        echo # Development files
        echo .env.local
        echo .env.development
        echo .env.test
        echo.
        echo # Temporary files
        echo tmp/
        echo temp/
        echo *.tmp
    ) > .dockerignore
    echo ✅ .dockerignore created
)

echo.
echo ==========================================
echo 🎉 Build preparation completed successfully!
echo ==========================================
echo.
echo 📋 Next steps:
echo 1. Commit and push your changes:
echo    git add .
echo    git commit -m "Ajuste docker para Easypanel"
echo    git push origin main
echo.
echo 2. Deploy on Easypanel:
echo    - Go to your Easypanel dashboard
echo    - Create new project from Git repository
echo    - Configure environment variables
echo    - Deploy!
echo.
echo 3. Test your API:
echo    curl https://your-domain.com/api/health
echo.
echo 🚀 Your TradingView API is ready for Easypanel deployment!
echo.
pause
