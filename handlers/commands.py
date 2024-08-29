from aiogram import types, Dispatcher
from config import bot


async def start_handler(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Приветствую в онлайн магазине!')


async def info_handler(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Бот создан специально для моего финального теста!\n"
                                "Ну и это типо магаз, удачи!")


def register_commands(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands="start")
    dp.register_message_handler(info_handler, commands="info")
