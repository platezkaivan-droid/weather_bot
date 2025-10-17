@echo off
echo 🚀 Запуск Weather Bot...
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

REM Создаем резервную копию БД если она существует
if exist "users.db" (
    echo 💾 Создаем резервную копию базы данных...
    copy "users.db" "users_backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%.db" >nul 2>&1
)

echo.
echo 🔧 Проверяем и исправляем базу данных...
python fix_database.py

echo.
echo 🎛️ Устанавливаем команды бота...
python setup_commands.py

echo.
echo ✅ Запускаем бота с автоперезапуском...
echo 💡 Для остановки нажмите Ctrl+C
echo.

REM Запускаем бота
python run_bot.py

echo.
echo 👋 Бот остановлен
pause