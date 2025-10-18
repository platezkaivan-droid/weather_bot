@echo off
echo 🚀 Weather Bot v2.1 - Полное обновление
echo ==================================================

echo.
echo 🔧 Шаг 1: Обновление команд меню...
python setup_commands.py
if %errorlevel% equ 0 (
    echo ✅ Команды меню обновлены
) else (
    echo ❌ Ошибка при обновлении команд
)

echo.
echo 📦 Шаг 2: Добавление файлов в git...
git add .
if %errorlevel% equ 0 (
    echo ✅ Файлы добавлены в git
) else (
    echo ❌ Ошибка при добавлении файлов
)

echo.
echo 💬 Шаг 3: Создание коммита...
git commit -m "🚀 Weather Bot v2.1: Добавлена информация о времени запуска и команда /status"
if %errorlevel% equ 0 (
    echo ✅ Коммит создан
) else (
    echo ⚠️ Коммит не создан (возможно, нет изменений)
)

echo.
echo 🌐 Шаг 4: Отправка на GitHub...
git push origin main
if %errorlevel% equ 0 (
    echo ✅ Изменения отправлены на GitHub
) else (
    echo ❌ Ошибка при отправке на GitHub
)

echo.
echo ==================================================
echo 🎉 Обновление завершено!
echo 🤖 Бот на Render обновится автоматически
echo 🌍 Web App: https://platezkaivan-droid.github.io/weather-bot-webapp/
echo.
pause