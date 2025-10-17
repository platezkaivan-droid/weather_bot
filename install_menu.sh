#!/bin/bash

echo "🎛️ Установка панели команд для Weather Bot"
echo "================================================"
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

echo
echo "🚀 Устанавливаем команды..."
python3 setup_commands.py

echo
echo "✅ Готово! Теперь запустите бота командой:"
echo "   ./start_bot.sh"
echo