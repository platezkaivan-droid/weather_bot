#!/usr/bin/env python3
"""
Основной файл для запуска бота на Render Web Service
Поддерживает как webhook (для продакшена), так и polling (для разработки)
"""

import asyncio
import logging
import sys
import traceback
from aiohttp import web
from aiohttp.web_request import Request
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram.types import Update

# Импортируем модули бота
import config
import database as db
from bot import dp, bot, set_bot_commands

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

async def webhook_handler(request: Request, bot: Bot) -> web.Response:
    """Обработчик webhook запросов"""
    try:
        update = Update.model_validate(await request.json(), context={"bot": bot})
        await dp.feed_update(bot, update)
        return web.Response(status=200)
    except Exception as e:
        logger.error(f"Ошибка в webhook handler: {e}")
        return web.Response(status=500)

async def health_check(request: Request) -> web.Response:
    """Health check endpoint для Render"""
    return web.json_response({
        "status": "ok", 
        "bot": "weather_bot",
        "version": "2.0",
        "timestamp": asyncio.get_event_loop().time()
    })

async def healthz_check(request: Request) -> web.Response:
    """Healthz endpoint для Kubernetes/Render"""
    return web.json_response({"status": "healthy"})

async def root_handler(request: Request) -> web.Response:
    """Корневой обработчик"""
    return web.json_response({
        "name": "Weather Bot",
        "version": "2.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "healthz": "/healthz", 
            "ready": "/ready",
            "webhook": config.WEBHOOK_PATH
        }
    })

async def setup_webhook():
    """Настройка webhook для продакшена"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            webhook_url = f"{config.WEBHOOK_URL}{config.WEBHOOK_PATH}"
            logger.info(f"🔄 Попытка {attempt + 1}/{max_retries} установки webhook: {webhook_url}")
            
            # Удаляем старый webhook
            await bot.delete_webhook(drop_pending_updates=True)
            logger.info("🗑️ Старый webhook удален")
            
            # Ждем немного
            await asyncio.sleep(1)
            
            # Устанавливаем новый webhook
            await bot.set_webhook(
                url=webhook_url,
                allowed_updates=dp.resolve_used_update_types(),
                drop_pending_updates=True,
                secret_token=None  # Можно добавить секретный токен для безопасности
            )
            logger.info(f"✅ Webhook установлен: {webhook_url}")
            
            # Проверяем webhook
            await asyncio.sleep(2)
            webhook_info = await bot.get_webhook_info()
            logger.info(f"📡 Webhook info:")
            logger.info(f"   URL: {webhook_info.url}")
            logger.info(f"   Pending updates: {webhook_info.pending_update_count}")
            logger.info(f"   Last error: {webhook_info.last_error_message or 'None'}")
            
            if webhook_info.url == webhook_url:
                logger.info("✅ Webhook успешно установлен и проверен")
                return True
            else:
                logger.warning(f"⚠️ Webhook URL не совпадает: ожидался {webhook_url}, получен {webhook_info.url}")
                
        except Exception as e:
            logger.error(f"❌ Ошибка установки webhook (попытка {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 2
                logger.info(f"⏳ Ждем {wait_time} секунд перед следующей попыткой...")
                await asyncio.sleep(wait_time)
            else:
                logger.error("💀 Все попытки установки webhook исчерпаны")
                return False
    
    return False

@web.middleware
async def logging_middleware(request: Request, handler):
    """Middleware для логирования запросов"""
    start_time = asyncio.get_event_loop().time()
    
    try:
        response = await handler(request)
        process_time = asyncio.get_event_loop().time() - start_time
        
        logger.info(f"📡 {request.method} {request.path} - {response.status} - {process_time:.3f}s")
        return response
        
    except Exception as e:
        process_time = asyncio.get_event_loop().time() - start_time
        logger.error(f"❌ {request.method} {request.path} - ERROR: {e} - {process_time:.3f}s")
        raise

async def create_app() -> web.Application:
    """Создание веб-приложения для webhook режима"""
    # Создаем приложение с middleware
    app = web.Application(middlewares=[logging_middleware])
    
    # Health check endpoints
    app.router.add_get("/", root_handler)
    app.router.add_get("/health", health_check)
    app.router.add_get("/healthz", healthz_check)
    app.router.add_get("/ready", health_check)
    app.router.add_get("/alive", health_check)
    
    # Webhook endpoint
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    webhook_requests_handler.register(app, path=config.WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    
    return app

async def run_webhook():
    """Запуск в режиме webhook (для Render)"""
    try:
        # Инициализация
        db.init_db()
        await set_bot_commands()
        
        # Настройка webhook
        if not await setup_webhook():
            raise Exception("Не удалось настроить webhook")
        
        # Создание веб-приложения
        app = await create_app()
        
        # Запуск сервера
        runner = web.AppRunner(app)
        await runner.setup()
        
        site = web.TCPSite(runner, "0.0.0.0", config.PORT)
        await site.start()
        
        logger.info(f"🚀 Webhook сервер запущен на порту {config.PORT}")
        logger.info(f"🌐 Health endpoints:")
        logger.info(f"   - http://0.0.0.0:{config.PORT}/health")
        logger.info(f"   - http://0.0.0.0:{config.PORT}/healthz")
        logger.info(f"   - http://0.0.0.0:{config.PORT}/ready")
        logger.info(f"🔗 Webhook: {config.WEBHOOK_URL}{config.WEBHOOK_PATH}")
        
        # Держим сервер запущенным
        try:
            while True:
                await asyncio.sleep(60)  # Проверяем каждую минуту
                
                # Периодическая проверка webhook
                if hasattr(config, 'WEBHOOK_URL') and config.WEBHOOK_URL:
                    try:
                        webhook_info = await bot.get_webhook_info()
                        if webhook_info.last_error_message:
                            logger.warning(f"⚠️ Webhook error: {webhook_info.last_error_message}")
                    except Exception as e:
                        logger.error(f"❌ Ошибка проверки webhook: {e}")
                        
        except asyncio.CancelledError:
            logger.info("🛑 Получен сигнал остановки сервера")
            await runner.cleanup()
            raise
            
    except Exception as e:
        logger.error(f"💥 Ошибка в webhook режиме: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise

async def run_polling():
    """Запуск в режиме polling (для разработки)"""
    try:
        # Инициализация
        db.init_db()
        await set_bot_commands()
        
        # Удаляем webhook если есть
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("🗑️ Webhook удален, используем polling")
        
        # Запуск polling
        logger.info("🔄 Запуск в режиме polling...")
        await dp.start_polling(bot, skip_updates=True)
        
    except Exception as e:
        logger.error(f"💥 Ошибка в polling режиме: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise

async def main():
    """Главная функция"""
    try:
        # Логируем информацию о среде
        logger.info("🚀 Запуск Weather Bot...")
        logger.info(f"🐍 Python версия: {sys.version}")
        logger.info(f"🌐 Порт: {config.PORT}")
        logger.info(f"🔗 Webhook URL: {config.WEBHOOK_URL or 'Не установлен'}")
        logger.info(f"📡 Режим webhook: {config.USE_WEBHOOK}")
        
        # Проверяем конфигурацию
        if not config.BOT_TOKEN:
            raise ValueError("❌ BOT_TOKEN не установлен! Добавьте переменную окружения.")
        
        if not config.WEATHER_API_KEY:
            raise ValueError("❌ WEATHER_API_KEY не установлен! Добавьте переменную окружения.")
        
        # Проверяем подключение к боту
        logger.info("🔍 Проверяем подключение к Telegram...")
        bot_info = await bot.get_me()
        logger.info(f"✅ Бот подключен: @{bot_info.username} (ID: {bot_info.id})")
        
        # Выбираем режим работы
        if config.USE_WEBHOOK:
            if not config.WEBHOOK_URL:
                logger.warning("⚠️ USE_WEBHOOK=true, но WEBHOOK_URL не установлен. Переключаемся на polling.")
                await run_polling()
            else:
                logger.info("🌐 Запуск в режиме WEBHOOK (продакшен)")
                await run_webhook()
        else:
            logger.info("🔄 Запуск в режиме POLLING (разработка)")
            await run_polling()
            
    except Exception as e:
        logger.error(f"💀 Критическая ошибка: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        # Пытаемся очистить webhook при ошибке
        try:
            await bot.delete_webhook()
            logger.info("🧹 Webhook очищен при завершении")
        except:
            pass
            
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Получен сигнал прерывания (Ctrl+C)")
    except Exception as e:
        logger.error(f"💀 Фатальная ошибка: {e}")
        sys.exit(1)