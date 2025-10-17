import asyncio
import logging
import aiohttp
import sys
import traceback
from datetime import datetime, timezone, timedelta
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.exceptions import TelegramNetworkError, TelegramRetryAfter, TelegramBadRequest
from aiogram.types import BotCommand, BotCommandScopeDefault, MenuButtonCommands, CallbackQuery

# Импортируем модули
import config
import database as db
import keyboards as kb

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# инициализация бота и диспетчера
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()

# создание базы данных и таблицы при старте
db.init_db()

# установка города
class SetCity(StatesGroup):
    waiting_for_city_name = State()

# Обработчики команд с обработкой ошибок
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    try:
        user_id = message.from_user.id
        username = message.from_user.username or "Пользователь"
        logger.info(f"Пользователь {username} (ID: {user_id}) запустил бота")
        
        await message.answer(
            "🌤️ Привет! Я бот для прогноза погоды.\n\n"
            "🔹 Просто отправь мне название города, и я пришлю актуальную погоду\n"
            "🔹 Используй кнопки ниже для быстрого доступа к функциям\n"
            "🔹 Или воспользуйся командами из меню\n\n"
            "� Прeимер: отправь \"Москва\" или \"Moscow\"",
            reply_markup=kb.get_inline_menu_keyboard()
        )
    except Exception as e:
        logger.error(f"Ошибка в команде start: {e}")
        await safe_send_message(message, "❌ Произошла ошибка. Попробуйте позже.")

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    try:
        await message.answer(
            "📋 Доступные команды:\n\n"
            "🔹 /start - запустить бота\n"
            "🔹 /weather - погода в вашем городе\n"
            "🔹 /setcity - установить город по умолчанию\n"
            "🔹 /stats - статистика бота\n"
            "� /hкelp - показать эту справку\n\n"
            "💡 Также можно просто написать название любого города!"
        )
    except Exception as e:
        logger.error(f"Ошибка в команде help: {e}")
        await safe_send_message(message, "❌ Произошла ошибка. Попробуйте позже.")

@dp.message(Command("stats"))
async def cmd_stats(message: types.Message):
    try:
        stats = db.get_user_stats()
        user_city = db.get_user_city(message.from_user.id)
        
        await message.answer(
            f"📊 Статистика бота:\n\n"
            f"👥 Всего пользователей: {stats['total_users']}\n"
            f"🏙️ Уникальных городов: {stats['unique_cities']}\n"
            f"🌍 Ваш город: {user_city or 'Не установлен'}\n"
            f"🤖 Версия: 2.0\n"
            f"⚡ Статус: Активен\n\n"
            f"💡 Используйте /setcity для установки города по умолчанию"
        )
    except Exception as e:
        logger.error(f"Ошибка в команде stats: {e}")
        await safe_send_message(message, "❌ Произошла ошибка. Попробуйте позже.")

@dp.message(Command("about"))
async def cmd_about(message: types.Message):
    try:
        await message.answer(
            "🤖 О боте:\n\n"
            "🌤️ Weather Bot v2.0\n"
            "Надежный бот для получения прогноза погоды\n\n"
            "✨ Возможности:\n"
            "• Актуальная погода для любого города\n"
            "• Сохранение города по умолчанию\n"
            "• Подробная информация о погоде\n"
            "• Статистика использования\n\n"
            "👨‍💻 Разработчик: @Skrizzzy4\n"
            "🔗 GitHub: github.com/platezkaivan-droid\n\n"
            "💡 Просто отправьте название города!"
        )
    except Exception as e:
        logger.error(f"Ошибка в команде about: {e}")
        await safe_send_message(message, "❌ Произошла ошибка. Попробуйте позже.")

@dp.message(Command("setcity"))
async def cmd_setcity(message: types.Message, state: FSMContext):
    try:
        await message.answer("🏙️ Пожалуйста, введите название вашего города:")
        await state.set_state(SetCity.waiting_for_city_name)
    except Exception as e:
        logger.error(f"Ошибка в команде setcity: {e}")
        await safe_send_message(message, "❌ Произошла ошибка. Попробуйте позже.")

@dp.message(SetCity.waiting_for_city_name)
async def city_chosen(message: types.Message, state: FSMContext):
    try:
        city_name = message.text.strip()
        if not city_name:
            await message.answer("❌ Название города не может быть пустым. Попробуйте еще раз:")
            return
            
        # Проверяем, существует ли город, запросив погоду
        weather_info = await get_weather(city_name)
        if "не найден" in weather_info.lower() or "ошибка" in weather_info.lower():
            await message.answer(f"{weather_info}\n\nПопробуйте ввести название города еще раз:")
            return
            
        try:
            db.set_user_city(
                message.from_user.id, 
                city_name,
                message.from_user.username,
                message.from_user.first_name
            )
        except Exception as db_error:
            logger.error(f"Ошибка при сохранении города в БД: {db_error}")
            # Попробуем базовый вариант
            try:
                db.set_user_city(message.from_user.id, city_name)
            except Exception as db_error2:
                logger.error(f"Критическая ошибка БД: {db_error2}")
                await message.answer(f"⚠️ Город найден, но не удалось сохранить настройки.\n\n{weather_info}")
                await state.clear()
                return
        await message.answer(f"✅ Отлично! Ваш город по умолчанию: {city_name.capitalize()}\n\n{weather_info}")
        await state.clear()
        
        logger.info(f"Пользователь {message.from_user.id} установил город: {city_name}")
        
    except Exception as e:
        logger.error(f"Ошибка при установке города: {e}")
        await safe_send_message(message, "❌ Произошла ошибка. Попробуйте позже.")
        await state.clear()

# получение погоды с обработкой ошибок
async def get_weather(city: str):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={config.WEATHER_API_KEY}&units=metric&lang=ru"
        
        timeout = aiohttp.ClientTimeout(total=10)  # таймаут 10 секунд
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    description = data['weather'][0]['description']
                    temp = data['main']['temp']
                    feels_like = data['main']['feels_like']
                    wind_speed = data['wind']['speed']
                    humidity = data['main']['humidity']
                    pressure = data['main']['pressure']
                    
                    # Получаем информацию о часовом поясе города
                    timezone_offset = data.get('timezone', 0)  # смещение в секундах от UTC
                    logger.info(f"Часовой пояс для {city}: {timezone_offset} секунд от UTC")
                    
                    # Вычисляем местное время города
                    utc_now = datetime.now(timezone.utc)
                    local_time = utc_now + timedelta(seconds=timezone_offset)
                    local_time_str = local_time.strftime('%H:%M:%S')
                    local_date_str = local_time.strftime('%d.%m.%Y')
                    
                    # Получаем время восхода и заката (если доступно)
                    sunrise_str = "—"
                    sunset_str = "—"
                    
                    try:
                        if 'sys' in data and 'sunrise' in data['sys'] and 'sunset' in data['sys']:
                            sunrise_utc = datetime.fromtimestamp(data['sys']['sunrise'], tz=timezone.utc)
                            sunset_utc = datetime.fromtimestamp(data['sys']['sunset'], tz=timezone.utc)
                            
                            sunrise_local = sunrise_utc + timedelta(seconds=timezone_offset)
                            sunset_local = sunset_utc + timedelta(seconds=timezone_offset)
                            
                            sunrise_str = sunrise_local.strftime('%H:%M')
                            sunset_str = sunset_local.strftime('%H:%M')
                    except (KeyError, ValueError, OSError) as e:
                        logger.warning(f"Ошибка при получении времени восхода/заката: {e}")
                        # Используем значения по умолчанию
                    
                    # Определяем эмодзи для погоды
                    weather_emoji = get_weather_emoji(data['weather'][0]['main'])
                    
                    return (
                        f"{weather_emoji} Погода в городе {city.capitalize()}:\n\n"
                        f"🌡️ Температура: {temp}°C\n"
                        f"🤔 Ощущается как: {feels_like}°C\n"
                        f"🌬️ Скорость ветра: {wind_speed} м/с\n"
                        f"💧 Влажность: {humidity}%\n"
                        f"📊 Давление: {pressure} гПа\n"
                        f"📝 Описание: {description.capitalize()}\n\n"
                        f"📅 Дата: {local_date_str}\n"
                        f"🕐 Местное время: {local_time_str}\n"
                        f"🌅 Восход: {sunrise_str}\n"
                        f"🌇 Закат: {sunset_str}\n"
                        f"🌍 Часовой пояс: UTC{timezone_offset//3600:+d}"
                    )
                elif response.status == 404:
                    return "❌ Город не найден. Проверьте правильность написания названия города."
                elif response.status == 401:
                    logger.error("Неверный API ключ OpenWeatherMap")
                    return "⚠️ Ошибка сервиса. Попробуйте позже."
                else:
                    logger.error(f"API вернул статус {response.status}")
                    return "⚠️ Сервис временно недоступен. Попробуйте позже."
                    
    except asyncio.TimeoutError:
        logger.error(f"Таймаут при запросе погоды для города {city}")
        return "⏰ Превышено время ожидания. Попробуйте позже."
    except aiohttp.ClientError as e:
        logger.error(f"Ошибка сети при запросе погоды: {e}")
        return "🌐 Проблемы с сетью. Попробуйте позже."
    except Exception as e:
        logger.error(f"Неожиданная ошибка при получении погоды: {e}")
        return "❌ Произошла ошибка. Попробуйте позже."

def get_weather_emoji(weather_main: str) -> str:
    """Возвращает эмодзи в зависимости от типа погоды"""
    weather_emojis = {
        'Clear': '☀️',
        'Clouds': '☁️',
        'Rain': '🌧️',
        'Drizzle': '🌦️',
        'Thunderstorm': '⛈️',
        'Snow': '❄️',
        'Mist': '🌫️',
        'Fog': '🌫️',
        'Haze': '🌫️'
    }
    return weather_emojis.get(weather_main, '🌤️')

# Настройка команд бота
async def set_bot_commands():
    """Устанавливает список команд для меню бота"""
    commands = [
        BotCommand(command="start", description="🚀 Запустить бота"),
        BotCommand(command="weather", description="🌤️ Погода в моем городе"),
        BotCommand(command="setcity", description="🏙️ Установить город по умолчанию"),
        BotCommand(command="stats", description="📊 Статистика бота"),
        BotCommand(command="about", description="ℹ️ О боте"),
        BotCommand(command="help", description="❓ Помощь и список команд"),
    ]
    
    try:
        # Сначала удаляем старые команды
        await bot.delete_my_commands(BotCommandScopeDefault())
        logger.info("🗑️ Старые команды удалены")
        
        # Ждем немного
        await asyncio.sleep(1)
        
        # Устанавливаем новые команды для всех пользователей
        await bot.set_my_commands(commands, BotCommandScopeDefault())
        logger.info("📝 Новые команды установлены")
        
        # Устанавливаем кнопку меню команд
        await bot.set_chat_menu_button(menu_button=MenuButtonCommands())
        logger.info("🎛️ Кнопка меню установлена")
        
        # Проверяем установленные команды
        current_commands = await bot.get_my_commands(BotCommandScopeDefault())
        logger.info(f"✅ Установлено команд: {len(current_commands)}")
        for cmd in current_commands:
            logger.info(f"   /{cmd.command} - {cmd.description}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Ошибка при установке команд: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False

@dp.message(Command("weather"))
async def cmd_weather(message: types.Message):
    try:
        city = db.get_user_city(message.from_user.id)
        if city:
            await message.answer("🔄 Получаю актуальную погоду...")
            weather_info = await get_weather(city)
            await message.answer(weather_info)
        else:
            await message.answer(
                "🏙️ У вас не установлен город по умолчанию.\n\n"
                "Используйте /setcity чтобы установить город, "
                "или просто отправьте название любого города!"
            )
    except Exception as e:
        logger.error(f"Ошибка в команде weather: {e}")
        await safe_send_message(message, "❌ Произошла ошибка. Попробуйте позже.")

@dp.message(F.text)
async def text_weather_handler(message: types.Message):
    try:
        city_name = message.text.strip()
        if not city_name:
            await message.answer("❌ Пожалуйста, введите название города.")
            return
            
        # Игнорируем слишком длинные сообщения (вероятно, не названия городов)
        if len(city_name) > 50:
            await message.answer("❌ Название города слишком длинное. Попробуйте еще раз.")
            return
            
        await message.answer("🔄 Получаю погоду...")
        weather_info = await get_weather(city_name)
        await message.answer(weather_info)
        
        logger.info(f"Пользователь {message.from_user.id} запросил погоду для города: {city_name}")
        
    except Exception as e:
        logger.error(f"Ошибка при обработке текста: {e}")
        await safe_send_message(message, "❌ Произошла ошибка. Попробуйте позже.")

# Безопасная отправка сообщений
async def safe_send_message(message: types.Message, text: str):
    try:
        await message.answer(text)
    except TelegramRetryAfter as e:
        logger.warning(f"Rate limit, ждем {e.retry_after} секунд")
        await asyncio.sleep(e.retry_after)
        await message.answer(text)
    except TelegramBadRequest as e:
        logger.error(f"Неверный запрос: {e}")
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения: {e}")

# Обработчики инлайн кнопок
@dp.callback_query(F.data == "weather")
async def callback_weather(callback: CallbackQuery):
    try:
        await callback.answer()
        city = db.get_user_city(callback.from_user.id)
        if city:
            await callback.message.answer("🔄 Получаю актуальную погоду...")
            weather_info = await get_weather(city)
            await callback.message.answer(weather_info)
        else:
            await callback.message.answer(
                "🏙️ У вас не установлен город по умолчанию.\n\n"
                "Используйте кнопку ниже чтобы установить город:",
                reply_markup=kb.get_inline_menu_keyboard()
            )
    except Exception as e:
        logger.error(f"Ошибка в callback weather: {e}")

@dp.callback_query(F.data == "setcity")
async def callback_setcity(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer()
        await callback.message.answer("🏙️ Пожалуйста, введите название вашего города:")
        await state.set_state(SetCity.waiting_for_city_name)
    except Exception as e:
        logger.error(f"Ошибка в callback setcity: {e}")

@dp.callback_query(F.data == "stats")
async def callback_stats(callback: CallbackQuery):
    try:
        await callback.answer()
        stats = db.get_user_stats()
        user_city = db.get_user_city(callback.from_user.id)
        
        await callback.message.answer(
            f"📊 Статистика бота:\n\n"
            f"👥 Всего пользователей: {stats['total_users']}\n"
            f"🏙️ Уникальных городов: {stats['unique_cities']}\n"
            f"🌍 Ваш город: {user_city or 'Не установлен'}\n"
            f"🤖 Версия: 2.0\n"
            f"⚡ Статус: Активен\n\n"
            f"💡 Используйте кнопки для управления ботом:",
            reply_markup=kb.get_inline_menu_keyboard()
        )
    except Exception as e:
        logger.error(f"Ошибка в callback stats: {e}")

@dp.callback_query(F.data == "about")
async def callback_about(callback: CallbackQuery):
    try:
        await callback.answer()
        await callback.message.answer(
            "🤖 О боте:\n\n"
            "🌤️ Weather Bot v2.0\n"
            "Надежный бот для получения прогноза погоды\n\n"
            "✨ Возможности:\n"
            "• Актуальная погода для любого города\n"
            "• Сохранение города по умолчанию\n"
            "• Подробная информация о погоде\n"
            "• Статистика использования\n\n"
            "👨‍💻 Разработчик: @Skrizzzy4\n"
            "🔗 GitHub: github.com/platezkaivan-droid\n\n"
            "💡 Попробуйте популярные города:",
            reply_markup=kb.get_weather_examples_keyboard()
        )
    except Exception as e:
        logger.error(f"Ошибка в callback about: {e}")

@dp.callback_query(F.data == "help")
async def callback_help(callback: CallbackQuery):
    try:
        await callback.answer()
        await callback.message.answer(
            "📋 Доступные команды:\n\n"
            "🚀 /start - запустить бота\n"
            "🌤️ /weather - погода в вашем городе\n"
            "🏙️ /setcity - установить город по умолчанию\n"
            "📊 /stats - статистика бота\n"
            "ℹ️ /about - информация о боте\n"
            "❓ /help - показать эту справку\n\n"
            "💡 Также можно просто написать название любого города!\n\n"
            "🎯 Примеры:",
            reply_markup=kb.get_weather_examples_keyboard()
        )
    except Exception as e:
        logger.error(f"Ошибка в callback help: {e}")

@dp.callback_query(F.data.startswith("city_"))
async def callback_city_weather(callback: CallbackQuery):
    try:
        await callback.answer()
        city_name = callback.data.replace("city_", "")
        await callback.message.answer(f"🔄 Получаю погоду для города {city_name}...")
        weather_info = await get_weather(city_name)
        await callback.message.answer(
            weather_info + "\n\n💡 Хотите установить этот город по умолчанию?",
            reply_markup=kb.get_inline_menu_keyboard()
        )
        
        logger.info(f"Пользователь {callback.from_user.id} запросил погоду через кнопку: {city_name}")
        
    except Exception as e:
        logger.error(f"Ошибка в callback city weather: {e}")

# Команда для обновления меню (только для разработчика)
@dp.message(Command("updatemenu"))
async def cmd_update_menu(message: types.Message):
    try:
        # Проверяем, что это разработчик (замените на ваш ID)
        if message.from_user.username != "Skrizzzy4":  # Замените на ваш username
            await message.answer("❌ У вас нет прав для выполнения этой команды.")
            return
            
        await message.answer("🔄 Обновляю меню команд...")
        success = await set_bot_commands()
        
        if success:
            await message.answer("✅ Меню команд успешно обновлено!")
        else:
            await message.answer("❌ Ошибка при обновлении меню команд.")
            
    except Exception as e:
        logger.error(f"Ошибка в команде updatemenu: {e}")
        await safe_send_message(message, "❌ Произошла ошибка. Попробуйте позже.")

# Обработчик ошибок
@dp.error()
async def error_handler(event, data):
    logger.error(f"Критическая ошибка: {event.exception}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    return True

# Функция запуска с автоперезапуском
async def main():
    max_retries = 5
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            logger.info("🚀 Запуск бота...")
            
            # Инициализация базы данных
            db.init_db()
            logger.info("✅ База данных инициализирована")
            
            # Проверка подключения к боту
            bot_info = await bot.get_me()
            logger.info(f"✅ Бот подключен: @{bot_info.username}")
            
            # Устанавливаем команды и меню
            await set_bot_commands()
            
            # Запуск polling
            await dp.start_polling(bot, skip_updates=True)
            
        except TelegramNetworkError as e:
            retry_count += 1
            wait_time = min(60 * retry_count, 300)  # максимум 5 минут
            logger.error(f"❌ Сетевая ошибка Telegram (попытка {retry_count}/{max_retries}): {e}")
            logger.info(f"⏳ Повторная попытка через {wait_time} секунд...")
            await asyncio.sleep(wait_time)
            
        except Exception as e:
            retry_count += 1
            wait_time = min(30 * retry_count, 180)  # максимум 3 минуты
            logger.error(f"❌ Критическая ошибка (попытка {retry_count}/{max_retries}): {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            
            if retry_count < max_retries:
                logger.info(f"⏳ Перезапуск через {wait_time} секунд...")
                await asyncio.sleep(wait_time)
            else:
                logger.error("💀 Превышено максимальное количество попыток перезапуска")
                break
    
    logger.error("🛑 Бот остановлен")

# Graceful shutdown
async def shutdown():
    logger.info("🛑 Получен сигнал остановки...")
    await bot.session.close()
    logger.info("✅ Бот корректно остановлен")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Получен сигнал прерывания (Ctrl+C)")
        asyncio.run(shutdown())
    except Exception as e:
        logger.error(f"💀 Фатальная ошибка: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")