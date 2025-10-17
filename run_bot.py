#!/usr/bin/env python3
"""
Скрипт для запуска бота с автоперезапуском и мониторингом
"""

import asyncio
import logging
import signal
import sys
import time
from pathlib import Path

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot_runner.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class BotRunner:
    def __init__(self):
        self.running = True
        self.restart_count = 0
        self.max_restarts = 10
        self.restart_delay = 30  # секунд
        
    def signal_handler(self, signum, frame):
        """Обработчик сигналов для graceful shutdown"""
        logger.info(f"🛑 Получен сигнал {signum}, останавливаем бота...")
        self.running = False
        
    async def run_bot(self):
        """Запуск основного бота"""
        try:
            # Импортируем и запускаем основной бот
            from bot import main
            await main()
        except Exception as e:
            logger.error(f"❌ Ошибка в основном боте: {e}")
            raise
            
    async def monitor_and_restart(self):
        """Мониторинг и автоперезапуск бота"""
        logger.info("🚀 Запуск системы мониторинга бота...")
        
        # Устанавливаем обработчики сигналов
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        while self.running and self.restart_count < self.max_restarts:
            try:
                logger.info(f"🔄 Запуск бота (попытка {self.restart_count + 1})")
                await self.run_bot()
                
            except KeyboardInterrupt:
                logger.info("👋 Получен сигнал прерывания")
                break
                
            except Exception as e:
                self.restart_count += 1
                logger.error(f"💥 Бот упал (попытка {self.restart_count}/{self.max_restarts}): {e}")
                
                if self.restart_count < self.max_restarts and self.running:
                    logger.info(f"⏳ Перезапуск через {self.restart_delay} секунд...")
                    await asyncio.sleep(self.restart_delay)
                    
                    # Увеличиваем задержку для следующего перезапуска
                    self.restart_delay = min(self.restart_delay * 1.5, 300)  # максимум 5 минут
                else:
                    logger.error("💀 Превышено максимальное количество перезапусков")
                    break
        
        logger.info("🏁 Система мониторинга завершена")

def main():
    """Главная функция"""
    try:
        runner = BotRunner()
        asyncio.run(runner.monitor_and_restart())
    except Exception as e:
        logger.error(f"💀 Критическая ошибка системы мониторинга: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()