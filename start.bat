@echo off
echo Iniciando backend...
start cmd /k "cd backend && uvicorn app.main:app --reload"

echo Aguardando 2 segundos...
timeout /t 2 /nobreak >nul

echo Iniciando frontend...
start cmd /k "cd frontend && npm run dev"

echo Servidores iniciados!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173

