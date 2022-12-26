from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from config import channel_link

markup_start = ReplyKeyboardMarkup(resize_keyboard=True)
markup_start.row("Обмен")
markup_start.row("FAQ")