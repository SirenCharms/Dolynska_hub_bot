from aiogram import F, Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from datetime import datetime
import json

# Імпорт станів та кнопок
from states import AddEvent
from utils.keyboard import get_confirm_keyboard, get_main_menu, get_return_keyboard

# Створюєм роутер
router = Router()

# Кнопка підтвердження вище для пріорітету фльтрів
@router.message(AddEvent.confirm, F.text == "✅ Підтвердити")
async def confirm_event(message: types.Message, state: FSMContext):
    # Отримуємо данні які записали в чернетку
    user_data = await state.get_data()
    # Читаємо старий файл
    try:
        with open("data/events.json", "r", encoding="utf-8") as f:
            events_list = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        events_list = []
    
    # Додаємо нову подію до списку
    events_list.append(user_data)

    # Записуємо оновлений список назад у файл
    with open("data/events.json", "w", encoding="utf-8") as f:
        # indent=4 робить JSON красивим і читабельним для людини
        # ensure_ascii=False дозволяє зберігати кирилицю як текст, а не коди
        json.dump(events_list, f, indent=4, ensure_ascii=False)
    
    # Фіналізуємо
    await message.answer("🚀 Подію успішно додано до афіші!", reply_markup=get_main_menu())
    await state.clear() # Очистка пам'яті

# Кнопка відміни вище для пріорітету фльтрів
@router.message(AddEvent.confirm, F.text == "❌ Скасувати")
async def cancel_event(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Скасовано", reply_markup=get_main_menu())

# Кнопка відмінити у всіх станах анкетування    
@router.message(StateFilter(AddEvent), F.text == "⬅️ Відмінити")
async def return_main_menu (message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Повертаємось до головного меню", reply_markup=get_main_menu())

# Обробник для кнопки "+ Додати подію" СТАРТ АНКЕТИ
@router.message(F.text == "✍️ Додати подію")
async def start_add_event(message: types.Message, state: FSMContext):
    await message.answer("Назва події?", reply_markup=get_return_keyboard())
    await state.set_state(AddEvent.title)

# Ловимо назву і питаємо далі
@router.message(AddEvent.title)
async def process_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text) # Записуємо назву в "тимчасову пам'ять"
    await message.answer("📅 Введіть дату події у форматі ДД.ММ.РРРР (наприклад 31.12.2025)")
    await state.set_state(AddEvent.date) # Переходимо до дати


# Тепер обробляємо дату події
@router.message(AddEvent.date)
async def process_date(message: types.Message, state: FSMContext):
    user_input = message.text.strip()

    try:
        # Намагаємось перетворити текст у об'єкт дати
        # %d.%m.%Y - це шаблон (ДД.ММ.РРРР)
        date_obj = datetime.strptime(user_input, "%d.%m.%Y")
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        if date_obj < today:
            await message.answer("Минуле не вернтуть\nНе виправить минуле...")
            return
        # Якщо помилки не виникло, зберігаємо дату назад у рядок
        formatted_date = date_obj.strftime("%d.%m.%Y")
        
        await state.update_data(date=formatted_date)
        await message.answer("⌛ Додайте час у фрматі ГГ:ХХ\nНаприклад 17:00.")
        await state.set_state(AddEvent.time)
    except ValueError:
        await message.answer(
            "❌ Невірний формат дати!\n"
            "Будь ласка, введіть дату у форматі **ДД.ММ.РРРР** (наприклад: 25.12.2026).\n"
            "Переконайтеся, що такий день дійсно існує."
        )

# Обробляємо час
@router.message(AddEvent.time)
async def process_time(message: types.Message, state: FSMContext):
    user_input = message.text.strip() # прибираємо випадкові пробіли
    try:
        time_obj = datetime.strptime(user_input, "%H:%M")
        formatted_time = time_obj.strftime("%H:%M")
                                           
        await state.update_data(time=formatted_time)
        await message.answer("Додайте опис.")
        await state.set_state(AddEvent.description)
    except ValueError:
        await message.answer(
            "❌ Невірний формат часу!\n"
            "Будь ласка, введіть час у форматі **ГГ:ХХ** (наприклад: 18:00 або 09:30).\n"
            "Використовуйте 24-годинний формат."
        )

@router.message(AddEvent.description)
async def process_descriprion(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("На цьому поки все!")

    # Витягуємо всі збережені данні з чернетки (FSMContext)
    user_data = await state.get_data()
    # await message.answer(get_confirm_keyboard)
    summary = (
        f"👁‍🗨 Чекаю на підтвердження!\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📌 Назва: {user_data['title']}\n"
        f"📅 Дата: {user_data['date']}\n"
        f"⌛ Час: {user_data['time']}\n"
        f"📝 Опис: {user_data['description']}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"Все вірно? Оберіть дію нижче: 👇"
    )

    await message.answer(summary, reply_markup=get_confirm_keyboard())
    await state.set_state(AddEvent.confirm)
    

