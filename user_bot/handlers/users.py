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

from mics import dp, bot, locale_configurator
from keyboards import *
from texts import *

from databases.databases import User, City, District, PaymentSystem, Currency, Order
from databases.database_mics import Session
from states import Form
from config import channel_id


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message, state):
    session = Session()
    user = session.query(User).filter_by(id=message.from_user.id).first()
    if user is None:
        user = User(
            id=message.from_user.id,
            username=message.from_user.username,
        )
        session.add(user)
        session.commit()
    async with state.proxy() as f:
        f["locale"] = user.locale
    await message.answer(locale_configurator.get_locale_text(user.locale, "start_text"))
    session.close()


@dp.message_handler(text="Обмен")
async def send_city_choose(message: types.Message, state):
    session = Session()
    async with state.proxy() as f:
        try:
            locale = f["locale"]
        except:
            locale = (
                session.query(User).filter_by(id=message.from_user.id).first().locale
            )
            f["locale"] = locale
    all_city = session.query(City).all()
    await message.answer(
        locale_configurator.get_locale_text(locale, "city_choose"),
        reply_markup=city_choose_keyboard(all_city, locale),
    )
    session.close()


@dp.callback_query_handler(lambda c: c.data.split("~")[0] == "city_id", state="*")
async def send_district_choose(
    callback_query: types.CallbackQuery, state, back_status=False
):
    async with state.proxy() as f:
        locale = f["locale"]
        if not (back_status):
            f["city_id"] = callback_query.data.split("~")[1]
        city_id = f["city_id"]
    session = Session()
    all_district = session.query(District).filter_by(city_id=city_id)
    await callback_query.message.edit_text(
        locale_configurator.get_locale_text(locale, "district_choose"),
        reply_markup=district_choose_keyboard(all_district, locale),
    )
    session.close()


@dp.callback_query_handler(lambda c: c.data.split("~")[0] == "district_id", state="*")
async def send_payment_system_choose(
    callback_query: types.CallbackQuery, state, back_status=False
):
    async with state.proxy() as f:
        locale = f["locale"]
        if not (back_status):
            f["district_id"] = callback_query.data.split("~")[1]
    session = Session()
    all_payment_system = session.query(PaymentSystem).all()
    await callback_query.message.edit_text(
        locale_configurator.get_locale_text(locale, "payment_system_choose"),
        reply_markup=payment_system_choose_keyboard(all_payment_system, locale),
    )
    session.close()


@dp.callback_query_handler(
    lambda c: c.data.split("~")[0] == "payment_system_id", state="*"
)
async def send_currency_choose(
    callback_query: types.CallbackQuery, state, back_status=False
):
    async with state.proxy() as f:
        locale = f["locale"]
        if not (back_status):
            f["payment_system_id"] = callback_query.data.split("~")[1]
    session = Session()
    all_currency = session.query(Currency).all()
    await callback_query.message.edit_text(
        locale_configurator.get_locale_text(locale, "currency_choose"),
        reply_markup=currency_choose_keyboard(all_currency, locale),
    )
    session.close()


@dp.callback_query_handler(lambda c: c.data.split("~")[0] == "currency_id", state="*")
async def send_await_sum(callback_query: types.CallbackQuery, state, back_status=False):
    async with state.proxy() as f:
        locale = f["locale"]
        if not (back_status):
            f["currency_id"] = callback_query.data.split("~")[1]
    await callback_query.message.edit_text(
        locale_configurator.get_locale_text(locale, "await_sum"),
        reply_markup=await_sum_keyboard(locale),
    )
    await Form.AwaitSum.set()


@dp.message_handler(state=Form.AwaitSum)
async def send_await_geolocation(message: types.Message, state):
    async with state.proxy() as f:
        locale = f["locale"]
    try:
        sum = float(message.text)
    except:
        sum = None
    if sum != None and sum > 0:
        async with state.proxy() as f:
            f["sum"] = sum
        await message.answer(
            locale_configurator.get_locale_text(locale, "await_geolocation"),
            reply_markup=await_geolocation_keyboard(locale),
        )
        await Form.AwaitGeolocation.set()
    else:
        await message.answer(locale_configurator.get_locale_text(locale, "await_sum"))


@dp.message_handler(state=Form.AwaitGeolocation, content_types=ContentTypes.ANY)
async def order_creation_completed(message: types.Message, state):
    if message.location != None:
        longitude = message.location["longitude"]
        latitude = message.location["latitude"]
    else:
        longitude = None
        latitude = None
    async with state.proxy() as f:
        locale = f["locale"]
        city_id = f["city_id"]
        district_id = f["district_id"]
        payment_system_id = f["payment_system_id"]
        currency_id = f["currency_id"]
        sum = f["sum"]
    session = Session()
    new_order = Order(
        User_id=message.from_user.id,
        city_id=city_id,
        district_id=district_id,
        payment_system_id=payment_system_id,
        currency_id=currency_id,
        sum=sum,
        longitude=longitude,
        latitude=latitude,
    )
    session.add(new_order)
    session.commit()
    session.close()
    await message.answer(
        locale_configurator.get_locale_text(locale, "successfully_created")
    )
    await bot.send_message(channel_id, f"Новый заказ\nГород:{new_order.city.name}")
    session.close()
    await state.reset_state()


@dp.callback_query_handler(
    lambda c: c.data.split("~")[0] == "step_back_order", state="*"
)
async def step_back_placing_order(callback_query: types.CallbackQuery, state):
    step_number = int(callback_query.data.split("~")[1])
    if step_number == 2:
        await callback_query.message.delete()
        await send_city_choose(callback_query.message, state)
    elif step_number == 3:
        await send_district_choose(callback_query, state, True)
    elif step_number == 4:
        await send_payment_system_choose(callback_query, state, True)
    elif step_number == 5:
        await send_currency_choose(callback_query, state, True)
        await state.reset_state(with_data=False)


@dp.callback_query_handler(lambda c: c.data == "close", state="*")
async def get_close(callback_query: types.CallbackQuery, state):
    await callback_query.message.delete()
    await state.reset_state()
