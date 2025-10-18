#!/usr/bin/env python3
"""
Скрипт для полного обновления Weather Bot
"""

import asyncio
import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Выполняет команду и показывает результат"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=Path(__file__).parent)
        if result.returncode == 0:
            print(f"✅ {description} - успешно")
            if result.stdout:
                print(f"📄 Вывод: {result.stdout.strip()}")
        else:
            print(f"❌ {description} - ошибка")
            if result.stderr:
                print(f"🚨 Ошибка: {result.stderr.strip()}")
        return result.returncode == 0
    except Exception as e:
        print(f"💥 Критическая ошибка при {description}: {e}")
        return False

async def main():
    print("🚀 Weather Bot v2.1 - Полное обновление")
    print("=" * 50)
    
    # 1. Обновление команд меню
    success1 = run_command("python setup_commands.py", "Обновление команд меню")
    
    # 2. Добавление изменений в git
    success2 = run_command("git add .", "Добавление файлов в git")
    
    # 3. Создание коммита
    commit_message = "🚀 Weather Bot v2.1: Добавлена информация о времени запуска и команда /status"
    success3 = run_command(f'git commit -m "{commit_message}"', "Создание коммита")
    
    # 4. Отправка на GitHub
    success4 = run_command("git push origin main", "Отправка на GitHub")
    
    print("\n" + "=" * 50)
    print("📊 Результаты обновления:")
    print(f"🔧 Команды меню: {'✅' if success1 else '❌'}")
    print(f"📦 Git add: {'✅' if success2 else '❌'}")
    print(f"💬 Git commit: {'✅' if success3 else '❌'}")
    print(f"🌐 Git push: {'✅' if success4 else '❌'}")
    
    if all([success1, success2, success3, success4]):
        print("\n🎉 Все обновления выполнены успешно!")
        print("🤖 Бот на Render обновится автоматически через несколько минут")
        print("🌍 Web App уже работает: https://platezkaivan-droid.github.io/weather-bot-webapp/")
    else:
        print("\n⚠️ Некоторые операции завершились с ошибками")
        print("💡 Проверьте логи выше для диагностики")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Обновление прервано пользователем")
    except Exception as e:
        print(f"\n💀 Критическая ошибка: {e}")