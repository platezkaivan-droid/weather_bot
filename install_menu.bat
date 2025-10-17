@echo off
echo 🎛️ Установка панели команд для Weather Bot
echo ================================================
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

REM Устанавливаем зависимости если нужно
if not exist "requirements.txt" (
    echo 📦 Создаем requirements.txt...
    echo aiogram==3.4.1 > requirements.txt
    echo aiohttp==3.9.1 >> requirements.txt
)

echo 📦 Проверяем зависимости...
pip install -r requirements.txt --quiet

echo.
echo 🚀 Устанавливаем команды...
python setup_commands.py

echo.
echo ✅ Готово! Теперь запустите бота командой:
echo    start_bot.bat
echo.
pause