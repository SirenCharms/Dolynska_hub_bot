import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from datetime import datetime
from aiogram import F # F - магічний фльтр тексту
from config import BOT_TOKEN  # Підтягуємо твій токен із сусіднього файлу
from utils.keyboard import get_main_menu
import json
from handlers.event_creation import router

def load_events():
    with open("data/events.json", "r", encoding='utf-8') as f:
        return json.load(f)




# Налаштування логування (щоб бачити помилки в консолі, якщо вони будуть)
logging.basicConfig(level=logging.ERROR)

# Ініціалізація бота та диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Підключаємо РОУТЕР!
dp.include_router(router)

# Обробник команди /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # message.from_user.first_name візьме ім'я користувача з Телеграму
    user_name = message.from_user.first_name
    await message.answer(f"Привіт, {user_name}!", reply_markup = get_main_menu())

# Оброник команди /help
@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("Я допоможу тобі дізнатися про події в Долинській! Використовуй кнопки для навігації.")

# Реагуємо на "події на тиждень"
@dp.message(F.text == "🗓️ Події на тиждень")
async def show_week_events(message: types.Message):
    all_events = load_events()
        
    week_response = "🗓️ <b>Події на тиждень:</b>\n\n"
    for e in all_events:
        week_response += f"🔹{e['date']}\n{e['title']}\n{e['description']}\n\n"
    await message.answer(week_response, parse_mode="HTML")
    

# Реагуємо на "події сьогодні"
@dp.message(F.text == "📅 Події сьогодні")
async def show_today_events (message: types.Message):
    # отримуємо сьогоднішню дату
    today = datetime.now().strftime("%d.%m.%Y")
    # відкриваємо файл events.json
    events = load_events()

    # Шукаємо події на сьогодні
    today_events = [e for e in events if e ["date"] == today]

    if today_events:
        response = "📅 <b>Події сьогодні у Долинській:</b>\n\n"
        for ev in today_events:
            response += f"🔹 {ev['title']}\n{ev['description']}\n\n"
        await message.answer(response, parse_mode="HTML")
    else:
        await message.answer("На сьогодні подій не знайдено. Відпочиваємо! 😉")
        # Показати найближчу подію

# Функція запуску бота
async def main():
    print("--- Бот запущений і готовий до роботи в Долинській! ---")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nБот зупинений.")