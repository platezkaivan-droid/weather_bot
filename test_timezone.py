#!/usr/bin/env python3
"""
Тест для проверки правильности отображения времени в разных городах
"""

import asyncio
import sys
from datetime import datetime, timezone, timedelta

# Добавляем путь для импорта модулей бота
sys.path.append('.')

async def test_timezone_calculation():
    """Тестирует расчет времени для разных часовых поясов"""
    
    # Тестовые данные для разных городов
    test_cities = [
        {"name": "Москва", "timezone": 10800},      # UTC+3
        {"name": "Лондон", "timezone": 0},          # UTC+0
        {"name": "Нью-Йорк", "timezone": -18000},   # UTC-5
        {"name": "Токио", "timezone": 32400},       # UTC+9
    ]
    
    print("🕐 Тест расчета времени для разных городов")
    print("=" * 50)
    
    utc_now = datetime.now(timezone.utc)
    print(f"UTC время: {utc_now.strftime('%H:%M:%S %d.%m.%Y')}")
    print()
    
    for city in test_cities:
        timezone_offset = city["timezone"]
        local_time = utc_now + timedelta(seconds=timezone_offset)
        
        hours_offset = timezone_offset // 3600
        offset_str = f"UTC{hours_offset:+d}" if hours_offset != 0 else "UTC"
        
        print(f"🏙️ {city['name']:<10} ({offset_str}): {local_time.strftime('%H:%M:%S %d.%m.%Y')}")
    
    print("\n✅ Тест завершен")

if __name__ == "__main__":
    asyncio.run(test_timezone_calculation())