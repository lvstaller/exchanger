import sys

sys.path.insert(1, "C:/Users/Lvstaller/Desktop/Bot/exchanger/")

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

from ..mics import dp, bot
from ..keyboards import *
from ..texts import *
from databases.databases import Admin, City, District, PaymentSystem, Currency
from databases.database_mics import Session
from ..states import Form


@dp.message_handler(commands=["start"], state="*")
async def send_welcome(message: types.Message, state):
    session = Session()
    admin = session.query(Admin).filter_by(id=message.from_user.id).first()
    if not (admin is None):
        await message.answer(start_text, reply_markup=main_menu_keyboard)
    session.close()
    await state.reset_state()


@dp.callback_query_handler(lambda c: c.data.split("~")[0] == "change", state="*")
async def send_change(callback_query: types.CallbackQuery, state, back_status=False):
    session = Session()
    admin = session.query(Admin).filter_by(id=callback_query.from_user.id).first()
    if not (admin is None):
        if back_status:
            async with state.proxy() as f:
                object_change = f["object_change"]
        else:
            async with state.proxy() as f:
                f["object_change"] = callback_query.data.split("~")[1]
            object_change = callback_query.data.split("~")[1]
        await callback_query.message.edit_text(
            select_action,
            reply_markup=select_action_keyboard(object_change_text[object_change]),
        )
    session.close()


@dp.callback_query_handler(lambda c: c.data == "add", state="*")
async def object_add(callback_query: types.CallbackQuery, state):
    session = Session()
    admin = session.query(Admin).filter_by(id=callback_query.from_user.id).first()
    if not (admin is None):
        async with state.proxy() as f:
            object_change = f["object_change"]
            f["type_operation"] = "add"
        object_change_not_enabled = (
            session.query(eval(object_change)).filter_by(is_enabled=False).all()
        )
        await callback_query.message.edit_text(
            object_add_text[object_change],
            reply_markup=object_keyboard(object_change_not_enabled),
        )
    session.close()
    await Form.AwaitNewObjec.set()


@dp.message_handler(state=Form.AwaitNewObjec)
async def add_new_objec(message: types.Message, state):
    session = Session()
    admin = session.query(Admin).filter_by(id=message.from_user.id).first()
    if not (admin is None):
        async with state.proxy() as f:
            object_change = f["object_change"]
        object = session.query(eval(object_change)).filter_by(name=message.text).first()
        if object is None:
            new_objec = eval(object_change)(name=message.text, is_enabled=True)
            session.add(new_objec)
            session.commit()
            await state.reset_state()
            await message.answer("Успешно")
            await message.answer("Главное меню", reply_markup=main_menu_keyboard)
        else:
            await message.answer(objec_name_repetition_text[object_change])
    session.close()


@dp.callback_query_handler(lambda c: c.data == "remove", state="*")
async def object_remove(callback_query: types.CallbackQuery, state):
    session = Session()
    admin = session.query(Admin).filter_by(id=callback_query.from_user.id).first()
    if not (admin is None):
        async with state.proxy() as f:
            object_change = f["object_change"]
            f["type_operation"] = "remove"
        object_change_enabled = (
            session.query(eval(object_change)).filter_by(is_enabled=True).all()
        )
        await callback_query.message.edit_text(
            object_remove_text[object_change],
            reply_markup=object_keyboard(object_change_enabled),
        )
    session.close()


@dp.callback_query_handler(lambda c: c.data.split("~")[0] == "objects_id", state="*")
async def object_add(callback_query: types.CallbackQuery, state):
    session = Session()
    admin = session.query(Admin).filter_by(id=callback_query.from_user.id).first()
    if not (admin is None):
        async with state.proxy() as f:
            object_change = f["object_change"]
            type_operation = f["type_operation"]
        change_object_is_enabled = (
            session.query(eval(object_change))
            .filter_by(id=callback_query.data.split("~")[1])
            .first()
        )
        if type_operation == "remove":
            change_object_is_enabled.is_enabled = False
            object_change_enabled = (
                session.query(eval(object_change)).filter_by(is_enabled=True).all()
            )
        else:
            change_object_is_enabled.is_enabled = True
            object_change_enabled = (
                session.query(eval(object_change)).filter_by(is_enabled=False).all()
            )
        session.add(change_object_is_enabled)
        session.commit()

        await callback_query.message.edit_reply_markup(
            reply_markup=object_keyboard(object_change_enabled)
        )
    session.close()


@dp.callback_query_handler(lambda c: c.data.split("~")[0] == "back", state="*")
async def object_add(callback_query: types.CallbackQuery, state):
    session = Session()
    admin = session.query(Admin).filter_by(id=callback_query.from_user.id).first()
    if not (admin is None):
        if callback_query.data.split("~")[1] == "1":
            await callback_query.message.edit_text(
                "Главное меню", reply_markup=main_menu_keyboard
            )
        elif callback_query.data.split("~")[1] == "3":
            await send_change(callback_query, state, True)
    session.close()
