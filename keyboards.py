"""
Клавиатуры для телеграм бота
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

def get_main_menu_keyboard():
    """Основное меню с кнопками"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🌤️ Моя погода"),
                KeyboardButton(text="🏙️ Установить город")
            ],
            [
                KeyboardButton(text="📊 Статистика"),
                KeyboardButton(text="❓ Помощь")
            ]
        ],
        resize_keyboard=True,
        persistent=True
    )
    return keyboard

def get_inline_menu_keyboard():
    """Инлайн клавиатура с командами"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🌤️ Текущая погода", callback_data="weather"),
                InlineKeyboardButton(text="📅 Прогноз на 5 дней", callback_data="forecast")
            ],
            [
                InlineKeyboardButton(text="🗺️ Карта погоды", callback_data="map"),
                InlineKeyboardButton(text="🌍 Интерактивная карта", web_app=WebAppInfo(url="https://platezkaivan-droid.github.io/weather-bot-webapp/weather_map.html"))
            ],
            [
                InlineKeyboardButton(text="🏙️ Установить город", callback_data="setcity"),
                InlineKeyboardButton(text="📊 Статистика", callback_data="stats")
            ],
            [
                InlineKeyboardButton(text="ℹ️ О боте", callback_data="about"),
                InlineKeyboardButton(text="❓ Помощь", callback_data="help")
            ]
        ]
    )
    return keyboard

def get_weather_examples_keyboard():
    """Клавиатура с примерами городов"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🏛️ Москва", callback_data="city_Москва"),
                InlineKeyboardButton(text="🌉 Санкт-Петербург", callback_data="city_Санкт-Петербург")
            ],
            [
                InlineKeyboardButton(text="🗽 New York", callback_data="city_New York"),
                InlineKeyboardButton(text="🏰 London", callback_data="city_London")
            ],
            [
                InlineKeyboardButton(text="🗼 Paris", callback_data="city_Paris"),
                InlineKeyboardButton(text="🏔️ Tokyo", callback_data="city_Tokyo")
            ]
        ]
    )
    return keyboard

def get_settings_keyboard():
    """Клавиатура настроек"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🏙️ Изменить город", callback_data="setcity"),
                InlineKeyboardButton(text="🗑️ Удалить город", callback_data="deletecity")
            ],
            [
                InlineKeyboardButton(text="📊 Моя статистика", callback_data="mystats"),
                InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")
            ]
        ]
    )
    return keyboard

def get_weather_map_keyboard(web_app_url="https://platezkaivan-droid.github.io/weather-bot-webapp/weather_map.html"):
    """Клавиатура с Web App для карты погоды"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🌍 Открыть интерактивную карту", 
                    web_app=WebAppInfo(url=web_app_url)
                )
            ],
            [
                InlineKeyboardButton(text="🗺️ Обычная карта", callback_data="map"),
                InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")
            ]
        ]
    )
    return keyboard

def get_location_request_keyboard():
    """Клавиатура для запроса местоположения"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📍 Отправить местоположение", request_location=True)
            ],
            [
                KeyboardButton(text="❌ Отмена")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard

def get_weather_map_links_keyboard(lat, lon):
    """Клавиатура со ссылками на карты погоды по координатам"""
    base_url = "https://openweathermap.org/weathermap"
    zoom = 10
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🌧️ Карта осадков", 
                    url=f"{base_url}?basemap=map&cities=true&layer=precipitation&lat={lat}&lon={lon}&zoom={zoom}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="☁️ Карта облачности", 
                    url=f"{base_url}?basemap=map&cities=true&layer=clouds&lat={lat}&lon={lon}&zoom={zoom}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🌡️ Карта температуры", 
                    url=f"{base_url}?basemap=map&cities=true&layer=temp&lat={lat}&lon={lon}&zoom={zoom}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="💨 Карта ветра", 
                    url=f"{base_url}?basemap=map&cities=true&layer=wind&lat={lat}&lon={lon}&zoom={zoom}"
                )
            ],
            [
                InlineKeyboardButton(text="🔙 Главное меню", callback_data="back_to_menu")
            ]
        ]
    )
    return keyboard