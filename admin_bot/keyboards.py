from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from config import channel_link

markup_start = InlineKeyboardMarkup()
markup_start.row(InlineKeyboardButton('Подпишись на новости',url = channel_link))
markup_start.row(InlineKeyboardButton('Pocket Option',callback_data = 'Pocket Option'),InlineKeyboardButton('Quotex',callback_data = 'Quotex'))
markup_start.row(InlineKeyboardButton('Другой Брокер',callback_data = 'other'))


def remove_reservation(ls):
    result = InlineKeyboardMarkup()
    for i in ls:
        result.row(InlineKeyboardButton(f'{str(i.start_date)[:10]} - {str(i.end_date)[:10]}',callback_data = f'remove~{i.id}'))
    return result

reg_Pocket_keyboard = InlineKeyboardMarkup()
reg_Pocket_keyboard.row(InlineKeyboardButton('Регистрация Pocket Option',url = 'https://m.pocketoption.com/ru/land/quick-sign-up/?utm_source=affiliate&a=7JJV7zfhF31zjy&ac=soft&code=1MORECHANCE'))
reg_Pocket_keyboard.row(InlineKeyboardButton('Проверить id',callback_data = 'check_id~Pocket Option'))
reg_Pocket_keyboard.row(InlineKeyboardButton('Вернуться назад',callback_data='back'))

reg_Quotex_keyboard = InlineKeyboardMarkup()
reg_Quotex_keyboard.row(InlineKeyboardButton('Регистрация Quotex',url = 'https://quotex.com/ru/?lid=14041'))
reg_Quotex_keyboard.row(InlineKeyboardButton('Проверить id',callback_data = 'check_id~Quotex'))
reg_Quotex_keyboard.row(InlineKeyboardButton('Вернуться назад',callback_data='back'))

other_brockers_keyboard = InlineKeyboardMarkup()
other_brockers_keyboard.row(InlineKeyboardButton('Iq Option',callback_data='payment'),InlineKeyboardButton('Binomo',callback_data='payment'))
other_brockers_keyboard.row(InlineKeyboardButton('Olymp Trade',callback_data='payment'),InlineKeyboardButton('Binarium',callback_data='payment'))
other_brockers_keyboard.row(InlineKeyboardButton('Intrade bar',callback_data='payment'),InlineKeyboardButton('binary.com',callback_data='payment'))
other_brockers_keyboard.row(InlineKeyboardButton('Finmax',callback_data='payment'),InlineKeyboardButton('Другой брокер',callback_data='payment'))
other_brockers_keyboard.row(InlineKeyboardButton('Вернуться назад',callback_data='back'))


back_keyboard = InlineKeyboardMarkup()
back_keyboard.row(InlineKeyboardButton('В главное меню',callback_data='back'))

def notification_keyboard(id):
    result = InlineKeyboardMarkup()
    result.row(InlineKeyboardButton('Подтвердить',callback_data=f'accept_notific~{id}'))
    result.row(InlineKeyboardButton('Отклонить',callback_data=f'cancel_notific~{id}'))
    return result