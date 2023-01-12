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
    await message.answer(locale_configurator.get_locale_text(user.locale, "start_text"), reply_markup=markup_start)
    session.close()


@dp.message_handler(text="💳Обмен")
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
        f['currency_start'] = None
        f['currency_end'] = None
        f['currency_start_id'] = None
        f['currency_end_id'] = None
    session = Session()
    all_currency = session.query(Currency).all()
    await callback_query.message.edit_text(
        locale_configurator.get_locale_text(locale, "currency_choose"),
        reply_markup=exchange_chooser(all_currency, [[0 for i in range(len(all_currency))],[0 for i in range(len(all_currency))]]),
    )
    session.close()


@dp.callback_query_handler(
    lambda c: c.data.split("~")[0] == "choose", state="*"
)
async def send_currency_choose(
    callback_query: types.CallbackQuery, state, back_status=False
):
    session = Session()
    all_currency = session.query(Currency).all()
    currency_id, choose_id_y, choose_id_x = callback_query.data.split("~")[1:]
    choose_currency = session.query(Currency).filter_by(id =currency_id).first()
    choose_list = [0 for i in range(len(all_currency))],[0 for i in range(len(all_currency))]

    async with state.proxy() as f:
        locale = f["locale"]
        if not (back_status):
            f["payment_system_id"] = callback_query.data.split("~")[1]
        if choose_id_y == "0":

            f['currency_start'] = choose_currency.name
            f['currency_start_id'] = int(choose_id_x)
        else:
            f['currency_end'] = choose_currency.name
            f['currency_end_id'] = int(choose_id_x)
        if f['currency_start_id'] is not None:
            choose_list[0][f['currency_start_id']] = True
        if f['currency_end_id'] is not None:
            choose_list[1][f['currency_end_id']] = True
    print(choose_list,choose_id_y,choose_id_x)
    await callback_query.message.edit_text(
        locale_configurator.get_locale_text(locale, "currency_choose"),
        reply_markup=exchange_chooser(all_currency, choose_list),
    )
    session.close()

@dp.callback_query_handler(lambda c: c.data.split("~")[0] == "accept_currency", state="*")
async def send_await_sum(callback_query: types.CallbackQuery, state, back_status=False):
    async with state.proxy() as f:
        if f['currency_end'] is None or f['currency_start'] is None:
            await callback_query.answer("Пожалуйста, выберите валюты которые вы хотите обменять",show_alert=True)
            return 0
        locale = f["locale"]
        if not (back_status):
            f["currency_id"] = f"{f['currency_start']}-{f['currency_start']}"
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
        currency_pare = f["currency_id"]
        sum = f["sum"]
    session = Session()
    new_order = Order(
        User_id=message.from_user.id,
        city_id=city_id,
        district_id=district_id,
        payment_system_id=payment_system_id,
        sum=sum,
        longitude=longitude,
        latitude=latitude,
    )
    session.add(new_order)
    session.commit()
    await message.answer(
        locale_configurator.get_locale_text(locale, "successfully_created"),
        reply_markup=markup_start
    )
    await bot.send_message(
        channel_id,
        order_text.format(
            session.query(City).filter_by(id=city_id).first().name,
            session.query(District).filter_by(id=city_id).first().name,
            session.query(PaymentSystem).filter_by(id=city_id).first().name,
            currency_pare,
            sum
        ),
        reply_markup=order_keyboard(message.chat.id, new_order.id, 0)
    )
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

@dp.message_handler()
async def send_city_choose(message: types.Message, state):
    print(message)