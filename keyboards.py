"""
Клавиатуры для телеграм бота
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

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
                InlineKeyboardButton(text="🗺️ Карта осадков", callback_data="map"),
                InlineKeyboardButton(text="🏙️ Установить город", callback_data="setcity")
            ],
            [
                InlineKeyboardButton(text="📊 Статистика", callback_data="stats"),
                InlineKeyboardButton(text="ℹ️ О боте", callback_data="about")
            ],
            [
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