@echo off
title ShopFlow
color 0A
echo.
echo  ============================================
echo   SHOPFLOW - Sistema de Gestao de Lojas
echo  ============================================
echo.
echo  [1/2] Instalando dependencias...
pip install flask --quiet
if %errorlevel% neq 0 (
    echo.
    echo  ERRO: pip nao encontrado. Instale Python em python.org
    pause
    exit /b 1
)
echo  Flask OK.
echo.
echo  [2/2] Iniciando servidor em http://localhost:5000
echo.
echo  Pressione Ctrl+C para parar o servidor.
echo  ============================================
echo.
timeout /t 1 /nobreak >nul
start "" "http://localhost:5000"
python app.py
pause
