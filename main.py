import logging
from config import dp, bot
from aiogram.utils import executor
from handlers import commands, FSM_Products, FSM_client

commands.register_commands(dp)
FSM_Products.register_fsm_products(dp)
FSM_client.register_fsm_client(dp)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
