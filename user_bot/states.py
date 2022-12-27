from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.dispatcher.filters.state import State, StatesGroup


class Form(StatesGroup):
    AwaitID = State()
    AwaitSum = State()
    AwaitGeolocation = State()
