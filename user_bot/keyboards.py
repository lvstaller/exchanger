from aiogram.types import (
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from .config import channel_link
from .mics import locale_configurator


markup_start = ReplyKeyboardMarkup(resize_keyboard=True)
markup_start.row("💳Обмен")
markup_start.row("🆘FAQ","📩Личный кабинет")


def city_choose_keyboard(all_city, locale):
    result = InlineKeyboardMarkup()
    for city in all_city:
        if city.is_enabled:
            result.row(
                InlineKeyboardButton(city.name, callback_data=f"city_id~{city.id}")
            )
    return result


def district_choose_keyboard(all_district, locale):
    result = InlineKeyboardMarkup()
    for district in all_district:
        if district.is_enabled:
            result.row(
                InlineKeyboardButton(
                    district.name, callback_data=f"district_id~{district.id}"
                )
            )
    result.row(
        InlineKeyboardButton(
            locale_configurator.get_locale_text(locale, "step_back_order"),
            callback_data=f"step_back_order~{2}",
        )
    )
    return result


def payment_system_choose_keyboard(all_payment_system, locale):
    result = InlineKeyboardMarkup()
    for payment in all_payment_system:
        result.row(
            InlineKeyboardButton(
                payment.name, callback_data=f"payment_system_id~{payment.id}"
            )
        )
    result.row(
        InlineKeyboardButton(
            locale_configurator.get_locale_text(locale, "step_back_order"),
            callback_data=f"step_back_order~{3}",
        )
    )
    return result


def currency_choose_keyboard(all_currency, locale):
    result = InlineKeyboardMarkup()
    for currency in all_currency:
        result.row(
            InlineKeyboardButton(
                currency.name, callback_data=f"currency_id~{currency.id}"
            )
        )
    result.row(
        InlineKeyboardButton(
            locale_configurator.get_locale_text(locale, "step_back_order"),
            callback_data=f"step_back_order~{4}",
        )
    )
    return result


def await_sum_keyboard(locale):
    result = InlineKeyboardMarkup()
    result.row(
        InlineKeyboardButton(
            locale_configurator.get_locale_text(locale, "step_back_order"),
            callback_data=f"step_back_order~{5}",
        )
    )
    return result


def await_geolocation_keyboard(locale):
    result = ReplyKeyboardMarkup(resize_keyboard=True)
    result.row(
        KeyboardButton(
            locale_configurator.get_locale_text(locale, "send_your_location"),
            request_location=True,
        )
    )
    result.row(
        KeyboardButton(
            locale_configurator.get_locale_text(locale, "anonymously"),
        )
    )
    return result

def exchange_chooser(currency_list,choose_list):
    result = InlineKeyboardMarkup()
    for ind,i in enumerate(currency_list):
        result.row(InlineKeyboardButton(f"{i.name} {'✅' if choose_list[0][ind] else ''}",callback_data=f"choose~{i.id}~0~{ind}"),InlineKeyboardButton(f"{i.name} {'✅' if choose_list[1][ind] else ''}",callback_data=f"choose~{i.id}~1~{ind}"))
    result.row(InlineKeyboardButton(f"Подтвердить выбор",callback_data="accept_currency"))
    return result

def order_keyboard(user_id, order_id, status):
    result = InlineKeyboardMarkup()
    result.row(InlineKeyboardButton("Ссылка на пользователя",url=f"tg://user?id={user_id}"))
    if status == 0:
        result.row(InlineKeyboardButton("Взять в работу",callback_data=f"get_in_work~{order_id}"))
    elif status == 1:
        result.row(InlineKeyboardButton("Закрыть обмен",callback_data=f"close_order~{order_id}"))
    return result