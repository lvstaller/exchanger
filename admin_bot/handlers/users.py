import shelve
from datetime import datetime

from aiogram import Bot, types
from aiogram.types.message import ContentTypes
from telegraph import Telegraph
from aiogram.types import ParseMode
from aiogram.types.input_media import InputMediaPhoto,InputMediaVideo,InputMediaAnimation ,InputFile, MediaGroup

from mics import dp, bot, Session
from keyboards import *
from texts import *
from databases import User, Reservation
from states import Form
from config import channel_id,subs_channel,notification_id

@dp.message_handler(commands = ['start'])
async def send_welcome(message: types.Message):
    session = Session()
    try:
        result = session.query(User).filter_by(id=message.chat.id).first()
        print(result)
        session.close()
    except:
        newItem = User(id=message.chat.id, name=message.chat.username)
        session.add(newItem)
        session.commit()
        session.close()
    await message.answer_photo(InputFile(r'photo\1.jpg'),start_text.format(name = message.chat.full_name),reply_markup = markup_start)

@dp.callback_query_handler(lambda c: c.data == 'Pocket Option')
async def answer_call(callback_query: types.CallbackQuery):
    status = await bot.get_chat_member(channel_id,callback_query.message.chat.id)
    if status['status'] != 'left':
        await callback_query.message.edit_media(InputMediaPhoto(InputFile(r'photo\2.png'),caption=pocket_option_text),reply_markup = reg_Pocket_keyboard)
    else:
        await callback_query.answer(text=sub_not_text,show_alert=True)


@dp.callback_query_handler(lambda c: c.data == 'Quotex')
async def answer_call(callback_query: types.CallbackQuery):
    status = await bot.get_chat_member(channel_id,callback_query.message.chat.id)
    if status['status'] != 'left':
        await callback_query.message.edit_media(InputMediaPhoto(InputFile(r'photo\3.png'),caption=quotex_text),reply_markup = reg_Quotex_keyboard)
    else:
        await callback_query.answer(text=sub_not_text,show_alert=True)

@dp.callback_query_handler(lambda c: c.data.split('~')[0] == 'check_id')
async def answer_call(callback_query: types.CallbackQuery,state):
    status = await bot.get_chat_member(channel_id,callback_query.message.chat.id)
    if status['status'] != 'left':
        await callback_query.message.delete()
#        await callback_query.message.edit_media(InputMediaPhoto(InputFile(r'photo\2.png'),caption=quotex_text),reply_markup = reg_Quotex_keyboard)
        await callback_query.message.answer('Отправьте ваш ID чтобы мы могли проверить вашу подписку. Если все хорошо, через какое-то время вы получите ссылку на канал для подписки')
        async with state.proxy() as f:
            f['market'] = callback_query.data.split('~')[1]
        await Form.AwaitID.set()
    else:
        await callback_query.answer(text=sub_not_text,show_alert=True)

@dp.message_handler(state = Form.AwaitID)
async def send_welcome(message: types.Message,state):
    await message.answer('Готово, ваши данные отправлены на проверку',reply_markup = back_keyboard)
    async with state.proxy() as f:
        await bot.send_message(notification_id,message.text+f'\n\n{f["market"]}',reply_markup = notification_keyboard(message.chat.id))
    await state.reset_state()
@dp.callback_query_handler(lambda c: c.data.split('~')[0] == 'accept_notific')
async def answer_call(callback_query: types.CallbackQuery):
    link = await bot.export_chat_invite_link(subs_channel)
    await bot.send_message(int(callback_query.data.split('~')[1]),f'Готово, ваша ссылка на подписку:\n{link}',reply_markup = back_keyboard)
    await callback_query.message.edit_text('Отвечено')

@dp.callback_query_handler(lambda c: c.data.split('~')[0] == 'cancel_notific')
async def answer_call(callback_query: types.CallbackQuery):
    await bot.send_message(int(callback_query.data.split('~')[1]),f'Во время проверки произошла ошибка',reply_markup = back_keyboard)
    await callback_query.message.edit_text('Отвечено')

@dp.callback_query_handler(lambda c: c.data == 'other')
async def answer_call(callback_query: types.CallbackQuery):
    status = await bot.get_chat_member(channel_id,callback_query.message.chat.id)
    if status['status'] != 'left':
        await callback_query.message.edit_media(InputMediaPhoto(InputFile(r'photo\4.jpg'),caption=other_brockers_text),reply_markup = other_brockers_keyboard)
    else:
        await callback_query.answer(text=sub_not_text,show_alert=True)

@dp.callback_query_handler(lambda c: c.data == 'back',state='*')
async def answer_call(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await callback_query.message.answer_photo(InputFile(r'photo\1.jpg'),caption=start_text.format(name = callback_query.message.chat.full_name),reply_markup = markup_start)

@dp.callback_query_handler(lambda c: c.data == 'payment')
async def answer_call(callback_query: types.CallbackQuery):
    # status = await bot.get_chat_member(channel_id,callback_query.message.chat.id)
    # if status['status'] != 'left':
    #     await callback_query.message.edit_media(InputMediaPhoto(InputFile(r'photo\4.jpg'),caption=other_brockers_text),reply_markup = other_brockers_keyboard)
    # else:
    await callback_query.answer(text=payment_text)