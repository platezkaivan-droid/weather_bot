#!/usr/bin/env python3
"""
Скрипт для тестирования health endpoints
"""

import asyncio
import aiohttp
import sys

async def test_endpoint(url, endpoint):
    """Тестирует один endpoint"""
    full_url = f"{url}{endpoint}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(full_url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                status = response.status
                text = await response.text()
                
                if status == 200:
                    print(f"✅ {endpoint} - OK ({status})")
                    print(f"   Response: {text[:100]}...")
                else:
                    print(f"❌ {endpoint} - FAILED ({status})")
                    print(f"   Response: {text[:100]}...")
                    
                return status == 200
                
    except Exception as e:
        print(f"💥 {endpoint} - ERROR: {e}")
        return False

async def main():
    """Главная функция тестирования"""
    if len(sys.argv) != 2:
        print("Использование: python test_health.py <URL>")
        print("Пример: python test_health.py https://your-app.onrender.com")
        sys.exit(1)
    
    base_url = sys.argv[1].rstrip('/')
    
    endpoints = [
        "/",
        "/health", 
        "/healthz",
        "/ready",
        "/alive"
    ]
    
    print(f"🧪 Тестирование health endpoints для {base_url}")
    print("=" * 50)
    
    results = []
    for endpoint in endpoints:
        result = await test_endpoint(base_url, endpoint)
        results.append(result)
        await asyncio.sleep(0.5)  # Небольшая пауза между запросами
    
    print("\n📊 Результаты:")
    print("=" * 50)
    
    success_count = sum(results)
    total_count = len(results)
    
    for i, endpoint in enumerate(endpoints):
        status = "✅ OK" if results[i] else "❌ FAILED"
        print(f"{endpoint:<10} - {status}")
    
    print(f"\n🎯 Успешно: {success_count}/{total_count}")
    
    if success_count == total_count:
        print("🎉 Все endpoints работают!")
        sys.exit(0)
    else:
        print("⚠️ Некоторые endpoints не работают")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())