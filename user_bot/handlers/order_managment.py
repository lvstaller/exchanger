import shelve
from datetime import datetime


from aiogram import Bot, types
from aiogram.types.message import ContentTypes
from telegraph import Telegraph
from aiogram.types import ParseMode
from aiogram.types.input_media import (
    InputMediaPhoto,
    InputMediaVideo,
    InputMediaAnimation,
    InputFile,
    MediaGroup,
)

from ..mics import dp, bot, locale_configurator
from ..keyboards import *
from ..texts import *

from databases.databases import User, City, District, PaymentSystem, Currency, Order
from databases.database_mics import Session
from ..states import Form
from ..config import channel_id


@dp.callback_query_handler(
    lambda c: c.data.split("~")[0] == "get_in_work", state="*"
)
async def order_in_work(callback_query: types.CallbackQuery, state):
    order_id = callback_query.data.split('~')[1]
    session = Session()
    order = session.query(Order).filter_by(id = int(order_id)).update({
        "master_id": callback_query.message.chat.id,
        "status_id": 1
    })
    session.commit()
    await callback_query.message.edit_text(
        callback_query.message.text + f"\n<b>Взят в работу @{callback_query.message.chat.username}</b>",
        reply_markup=order_keyboard(order.user_id,order_id,1)
    )
    session.close()

@dp.callback_query_handler(
    lambda c: c.data.split("~")[0] == "close_order", state="*"
)
async def order_in_work(callback_query: types.CallbackQuery, state):
    order_id = callback_query.data.split('~')[1]
    session = Session()
    order = session.query(Order).filter_by(id = int(order_id)).update({
        "status_id": 2
    })
    session.commit()
    await callback_query.message.edit_text(
        callback_query.message.text + f"\n<b>Закрыт!/b>",
    )
    session.close()