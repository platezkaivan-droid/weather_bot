@echo off
echo 🔧 Исправление базы данных Weather Bot
echo ==========================================
echo.

REM Проверяем наличие Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не найден! Установите Python 3.8+
    pause
    exit /b 1
)

REM Переходим в папку с ботом
cd /d "%~dp0"

echo 🚀 Исправляем базу данных...
python fix_database.py

echo.
echo ✅ Готово! Теперь можно запускать бота.
echo.
pause