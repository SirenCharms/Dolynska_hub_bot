import json
from aiogram.types import FSInputFile
from config import PLACEHOLDER

def load_events():
    try:
        with open("data/events.json", "r", encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    
def get_event_display_data(event, keyboard=None):
    caption = (
        f"📌 Назва: {event['title']}\n"
        f"📅 Дата: {event['date']}\n"
        f"⌛ Час: {event['time']}\n"
        f"📝 Опис: {event['description']}\n"
    )

    poster = event.get('poster')
    if event.get('poster') and event['poster'] != "no_poster":
        photo_to_send = poster
    else:
        photo_to_send = FSInputFile(PLACEHOLDER)
    return photo_to_send, caption, keyboard 