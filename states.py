from aiogram.fsm.state import State, StatesGroup

# Клас, для створення події за принципом анкетування (дата, місце, час...)
class AddEvent(StatesGroup):
    title = State() # wait for event name
    date = State() # wait for date
    time = State() # wait for time
    description = State() # wait for description
    poster = State() # wait for poster
    confirm = State() # wait for user confirm
    # cancel = State()