#!/usr/bin/env python3
"""
Скрипт для быстрого деплоя на Render
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_git():
    """Проверяет наличие git"""
    try:
        subprocess.run(['git', '--version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def check_files():
    """Проверяет наличие необходимых файлов"""
    required_files = [
        'main.py',
        'bot.py', 
        'config.py',
        'database.py',
        'keyboards.py',
        'requirements.txt',
        'render.yaml',
        '.env.example',
        '.gitignore'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    return missing_files

def check_env_vars():
    """Проверяет переменные окружения"""
    required_vars = ['BOT_TOKEN', 'WEATHER_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    return missing_vars

def main():
    """Главная функция"""
    print("🚀 Подготовка к деплою Weather Bot на Render")
    print("=" * 50)
    
    # Проверяем git
    if not check_git():
        print("❌ Git не найден! Установите Git для продолжения.")
        sys.exit(1)
    print("✅ Git найден")
    
    # Проверяем файлы
    missing_files = check_files()
    if missing_files:
        print(f"❌ Отсутствуют файлы: {', '.join(missing_files)}")
        sys.exit(1)
    print("✅ Все необходимые файлы найдены")
    
    # Проверяем переменные окружения (для локального тестирования)
    missing_vars = check_env_vars()
    if missing_vars:
        print(f"⚠️ Не установлены переменные окружения: {', '.join(missing_vars)}")
        print("💡 Это нормально для деплоя - установите их в Render Dashboard")
    else:
        print("✅ Переменные окружения найдены")
    
    print("\n📋 Чек-лист для деплоя:")
    print("=" * 30)
    print("1. ✅ Создайте репозиторий на GitHub")
    print("2. ✅ Загрузите файлы в репозиторий:")
    print("   git add .")
    print("   git commit -m 'Initial commit: Weather Bot'")
    print("   git push origin main")
    print("3. 🌐 Создайте Web Service на render.com")
    print("4. 🔗 Подключите GitHub репозиторий")
    print("5. ⚙️ Установите переменные окружения в Render:")
    print("   - BOT_TOKEN=your_bot_token")
    print("   - WEATHER_API_KEY=your_weather_api_key")
    print("   - USE_WEBHOOK=true")
    print("   - WEBHOOK_URL=https://your-app-name.onrender.com")
    print("6. 🚀 Нажмите 'Create Web Service'")
    
    print("\n🧪 Для тестирования после деплоя:")
    print("python test_health.py https://your-app-name.onrender.com")
    
    print("\n🎉 Готово к деплою!")

if __name__ == "__main__":
    main()