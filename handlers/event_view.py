from datetime import datetime
from aiogram import Router, F, types
from aiogram.types import FSInputFile
from utils.json_manager import load_events
from config import PLACEHOLDER
from utils.json_manager import get_event_display_data

router = Router()

@router.message(F.text == "📅 Найближчі події")
async def nearest_event(message: types.Message):
    all_events = load_events()
    if not all_events:
        await message.answer("Афіша поки порожня. Станьте першим, хто додасть подію!")
        return
    
    today = datetime.now()
    future_events = []

    # Лишаємо тільки майбутні події
    for event in all_events:
        # Перетворюємо рядок "31.12.2025" у справжню дату
        event_date = datetime.strptime(event['date'], "%d.%m.%Y")
    
        if event_date >= today.replace(hour=0, minute=0, second=0, microsecond=0):
            # Додаємо в список саму подію ТА її об'єкт дати (щоб легше сортувати)
            future_events.append((event_date, event))
    
    if not future_events:
        await message.answer("На жаль, всі події вже минули. Чекаємо на нові анонси!")
    
    # Сортуємо за датою (від найближчої)
    future_events.sort(key=lambda x: (x[0], x[1]['time']))
    
    if not future_events:
        return
    
    # Беремо дату найпершої події
    nearest_date = future_events[0][0].date()
    
    # Виводимо всі події, які припадають на цю саму дату
    for date_obj, event in future_events:
        # print(f"Порівнюю: {date_obj.date()} з {nearest_date}")
        if date_obj.date() == nearest_date:
            photo, caption, _ = get_event_display_data(event)
            summary = (
                f"🌟 <b>НАЙБЛИЖЧА ПОДІЯ</b> 🌟\n\n"
                f"{caption}"
            )
            await message.answer_photo(photo=photo, caption=summary, parse_mode="HTML")
        else:
            # Оскільки список відсортований, як тільки пішли інші дати — можна зупинятись
            break
