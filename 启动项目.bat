@echo off
chcp 65001 >nul
title CampusFlow AI - 启动中...
echo ========================================
echo   CampusFlow AI 启动器
echo ========================================
echo.

REM 获取批处理文件所在目录
set "PROJECT_DIR=%~dp0"
echo 项目目录: %PROJECT_DIR%
echo.

REM 检查后端目录
if not exist "%PROJECT_DIR%backend\venv\Scripts\activate" (
    echo [错误] 找不到后端虚拟环境！
    echo 请先运行: cd backend ^&^& python -m venv venv ^&^& pip install -e .
    pause
    exit /b 1
)

REM 检查前端目录
if not exist "%PROJECT_DIR%frontend\node_modules" (
    echo [错误] 找不到前端依赖！
    echo 请先运行: cd frontend ^&^& npm install
    pause
    exit /b 1
)

echo [1/2] 正在启动后端...
start "CampusFlow Backend" cmd /k "cd /d "%PROJECT_DIR%backend" && call venv\Scripts\activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

echo [2/2] 等待5秒后启动前端...
timeout /t 5 /nobreak >nul

start "CampusFlow Frontend" cmd /k "cd /d "%PROJECT_DIR%frontend" && npm run dev"

echo.
echo ========================================
echo   启动完成！
echo.
echo   请等待约10秒后打开浏览器访问：
echo   前端: http://localhost:3000
echo   后端: http://localhost:8000/docs
echo ========================================
echo.
echo 关闭此窗口不影响运行
echo 要停止服务请关闭那两个黑色窗口
pause
