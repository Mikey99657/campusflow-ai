@echo off
title CampusFlow AI Backend
cd /d "%~dp0backend"
call venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
pause
