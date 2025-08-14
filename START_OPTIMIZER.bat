@echo off
title UltraOptimizer v1.0
color 0A
cls

echo =========================================
echo    UltraOptimizer - Gaming Performance
echo =========================================
echo.

:: Verificar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no esta instalado!
    echo Por favor, ejecuta install_python.ps1 primero
    pause
    exit /b 1
)

:: Activar venv si existe
if exist ".venv\Scripts\activate.bat" (
    echo Activando entorno virtual...
    call .venv\Scripts\activate.bat
) else (
    echo Usando Python del sistema...
)

:: Cambiar al directorio app
cd app

:: Ejecutar el launcher
echo.
echo Iniciando UltraOptimizer...
echo.
python run_optimizer.py

pause