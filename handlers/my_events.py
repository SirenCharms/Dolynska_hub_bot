from aiogram import Router, F, types
from utils.json_manager import load_events  # Використовуємо твою функцію
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from utils.json_manager import get_event_display_data
from config import PLACEHOLDER
import json

router = Router()

@router.message(F.text=="👤 Мої події")
async def show_my_events(message: types.Message):
    user_id = message.from_user.id
    all_events = load_events()

    my_events = [e for e in all_events if e.get('user_id') == user_id]

    if not my_events:
        await message.answer("Ви ще не створили жодної події. ✍️")
        return
    for event in my_events:
        photo, caption, _ = get_event_display_data(event)
        summary = (
            f"👤 <b>Ваші події</b>\n\n"
            f"{caption}"
        )

        # Створюємо Inline-кнопку саме для цієї події
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text="❌ Видалити",
                    callback_data=f"delete_{event['event_id']}"
                )]
            ]
        )
        # Відображаємо результат
        await message.answer_photo(
            photo = photo,
            caption=summary,
            reply_markup=keyboard,
            parse_mode="HTML"
        )

@router.callback_query(F.data.startswith("delete_"))
async def delete_event_handler(callback: types.CallbackQuery):
    event_id = int(callback.data.split("_")[1])

    all_events = load_events()

    updated_events = [e for e in all_events if e.get('event_id') != event_id]

    with open("data/events.json", "w", encoding="utf-8") as f:
        json.dump(updated_events, f, indent=4, ensure_ascii=False)

    await callback.answer("Подію видалено! ✅")

    await callback.message.delete()