#!/usr/bin/env python3
"""
Скрипт для принудительной установки команд бота в Telegram
"""

import asyncio
import logging
from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault, MenuButtonCommands
import config

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def setup_bot_commands():
    """Устанавливает команды бота"""
    bot = Bot(token=config.BOT_TOKEN)
    
    commands = [
        BotCommand(command="start", description="🚀 Запустить бота"),
        BotCommand(command="weather", description="🌤️ Текущая погода"),
        BotCommand(command="forecast", description="📅 Прогноз на 5 дней"),
        BotCommand(command="map", description="🗺️ Карта осадков"),
        BotCommand(command="setcity", description="🏙️ Установить город"),
        BotCommand(command="stats", description="📊 Статистика"),
        BotCommand(command="about", description="ℹ️ О боте"),
        BotCommand(command="help", description="❓ Помощь"),
    ]
    
    try:
        # Получаем информацию о боте
        bot_info = await bot.get_me()
        logger.info(f"🤖 Подключен к боту: @{bot_info.username}")
        
        # Удаляем старые команды
        logger.info("🗑️ Удаляю старые команды...")
        await bot.delete_my_commands(BotCommandScopeDefault())
        
        # Ждем немного
        await asyncio.sleep(2)
        
        # Устанавливаем новые команды
        logger.info("📝 Устанавливаю новые команды...")
        await bot.set_my_commands(commands, BotCommandScopeDefault())
        
        # Устанавливаем кнопку меню
        logger.info("🎛️ Устанавливаю кнопку меню...")
        await bot.set_chat_menu_button(menu_button=MenuButtonCommands())
        
        # Проверяем результат
        current_commands = await bot.get_my_commands(BotCommandScopeDefault())
        logger.info(f"✅ Успешно установлено команд: {len(current_commands)}")
        
        print("\n📋 Установленные команды:")
        for i, cmd in enumerate(current_commands, 1):
            print(f"  {i}. /{cmd.command} - {cmd.description}")
        
        print(f"\n🎉 Команды успешно установлены для бота @{bot_info.username}!")
        print("💡 Теперь пользователи увидят панель команд в Telegram")
        
    except Exception as e:
        logger.error(f"❌ Ошибка при установке команд: {e}")
        print(f"\n💥 Ошибка: {e}")
        print("🔧 Проверьте токен бота в config.py")
        
    finally:
        await bot.session.close()

if __name__ == "__main__":
    print("🚀 Установка команд для Weather Bot...")
    print("=" * 50)
    
    try:
        asyncio.run(setup_bot_commands())
    except KeyboardInterrupt:
        print("\n👋 Прервано пользователем")
    except Exception as e:
        print(f"\n💀 Критическая ошибка: {e}")