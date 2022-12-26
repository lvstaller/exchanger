import shelve
from datetime import datetime

from aiogram import Bot, types
from aiogram.types.message import ContentTypes
from telegraph import Telegraph
from aiogram.types import ParseMode
from aiogram.types.input_media import InputMediaPhoto,InputMediaVideo,InputMediaAnimation ,InputFile, MediaGroup

from mics import dp, bot, locale_configurator
from keyboards import *
from texts import *
from databases.databases import User
from databases.database_mics import Session
from states import Form
from config import channel_id,subs_channel,notification_id

@dp.message_handler(commands = ['start'])
async def send_welcome(message: types.Message, state):
    session = Session()
    user = session.query(User).filter_by(id = message.from_user.id).first()
    if user is None:
        user = User(
            id = message.from_user.id,
            name = message.from_user.username,
        )
        session.add(user)
        session.commit()
    async with state.proxy() as f:
        f['locale'] = user.locale
    await message.answer(locale_configurator.get_locale_text(user.locale,"start_text"))

@dp.message_handler(text = "Обмен")
async def send_welcome(message: types.Message, state):
    