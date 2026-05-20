@echo off
title CampusFlow AI - 启动中...
echo ========================================
echo   CampusFlow AI 启动器
echo ========================================
echo.
echo 正在启动后端...
start "CampusFlow Backend" cmd /k "cd /d %~dp0backend && call venv\Scripts\activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
timeout /t 5 /nobreak >nul
echo 正在启动前端...
start "CampusFlow Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"
echo.
echo ========================================
echo   启动完成！
echo   前端: http://localhost:3000
echo   后端: http://localhost:8000/docs
echo ========================================
echo.
echo 关闭此窗口不影响运行
echo 要停止服务请关闭那两个黑色窗口
pause
