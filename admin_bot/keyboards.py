from aiogram.types import (
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

main_menu_keyboard = InlineKeyboardMarkup()
main_menu_keyboard.row(
    InlineKeyboardButton("Изменить города", callback_data="change~City")
)
main_menu_keyboard.row(
    InlineKeyboardButton("Изменить районы", callback_data="change~District")
)
main_menu_keyboard.row(
    InlineKeyboardButton(
        "Изменить платежные системы", callback_data="change~PaymentSystem"
    )
)


def select_action_keyboard(text):
    result = InlineKeyboardMarkup()
    result.row(InlineKeyboardButton(f"Добавить {text}", callback_data="add"))
    result.row(InlineKeyboardButton(f"Удалить {text}", callback_data="remove"))
    result.row(InlineKeyboardButton("Назад", callback_data="back~1"))
    return result


def object_keyboard(objects_change):
    result = InlineKeyboardMarkup()
    for object in objects_change:
        result.row(
            InlineKeyboardButton(object.name, callback_data=f"objects_id~{object.id}")
        )
    result.row(InlineKeyboardButton("Назад", callback_data="back~3"))
    return result
