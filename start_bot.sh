#!/bin/bash

echo "🚀 Запуск Weather Bot..."
echo

# Проверяем наличие Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден! Установите Python 3.8+"
    exit 1
fi

# Переходим в папку с ботом
cd "$(dirname "$0")"

# Создаем виртуальное окружение если его нет
if [ ! -d "venv" ]; then
    echo "📦 Создаем виртуальное окружение..."
    python3 -m venv venv
fi

# Активируем виртуальное окружение
source venv/bin/activate

# Устанавливаем зависимости
echo "📦 Устанавливаем зависимости..."
pip install -r requirements.txt --quiet

# Создаем резервную копию БД если она существует
if [ -f "users.db" ]; then
    echo "💾 Создаем резервную копию базы данных..."
    cp users.db "users_backup_$(date +%Y%m%d_%H%M%S).db"
fi

echo
echo "🔧 Проверяем и исправляем базу данных..."
python3 fix_database.py

echo
echo "🎛️ Устанавливаем команды бота..."
python3 setup_commands.py

echo
echo "✅ Запускаем бота с автоперезапуском..."
echo "💡 Для остановки нажмите Ctrl+C"
echo

# Запускаем бота
python3 run_bot.py

echo
echo "👋 Бот остановлен"