from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

cancel = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Отмена')
)


submit_buttons = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Да'),
    KeyboardButton('Нет')
)
