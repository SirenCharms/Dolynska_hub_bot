from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_menu():
    # Створюємо список кнопок
    # Кожен вкладений список [ ] — це окремий рядок кнопок
    kb = [
        [KeyboardButton(text="📅 Найближчі події"), KeyboardButton(text="🗓️ Події на тиждень")],
        [KeyboardButton(text="✍️ Додати подію"), KeyboardButton(text="👤 Мої події")],
        [KeyboardButton(text="ℹ️ Про проєкт")]
    ]

    # Збираємо клавіатуру
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True, # Робить кнопки маленькими та акуратними
        input_field_placeholder="Обери розділ меню" # Текст у полі вводу
    )
    return keyboard

def get_confirm_keyboard():
    kb = [
        [KeyboardButton(text="✅ Підтвердити")],
        [KeyboardButton(text="❌ Скасувати")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Все вірно?")

def get_return_keyboard():
    kb = [
        [KeyboardButton(text="⬅️ Відмінити")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def get_skip_keyboard():
    kb = [
        [KeyboardButton(text="Пропустити ⏭️")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
