#!/bin/bash

echo "🔧 Исправление базы данных Weather Bot"
echo "=========================================="
echo

# Проверяем наличие Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден! Установите Python 3.8+"
    exit 1
fi

# Переходим в папку с ботом
cd "$(dirname "$0")"

echo "🚀 Исправляем базу данных..."
python3 fix_database.py

echo
echo "✅ Готово! Теперь можно запускать бота."
echo