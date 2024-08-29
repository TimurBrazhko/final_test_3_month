from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import buttons
from config import staff, bot


class Fsm_order(StatesGroup):
    id_product = State()
    size = State()
    quantity = State()
    customer_phone = State()
    check_order = State()


async def fsm_start(message: types.Message):
    await Fsm_order.id_product.set()
    await message.answer(text='Введите артикул товара: ',
                         reply_markup=buttons.cancel)


async def load_id_product(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id_product'] = message.text

    await Fsm_order.next()
    await message.answer(text="Укажите размер:")


async def load_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text

    await Fsm_order.next()
    await message.answer(text="Укажите кол-во товара:")


async def load_quantity(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['quantity'] = message.text

    await Fsm_order.next()
    await message.answer(text="Укажите ваш контактный номер:")


async def load_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['customers_phone'] = message.text

    await Fsm_order.next()
    await message.answer('Отправляем?', reply_markup=buttons.submit_buttons)


async def check_order(message: types.Message, state: FSMContext):
    if message.text == 'Да':
        kb = types.ReplyKeyboardRemove()
        async with state.proxy() as data:
            for i in staff:
                await bot.send_message(chat_id=i, text=f"Артикул - {data['id_product']}\n"
                                                    f"Размер - {data['size']}\n"
                                                    f"Кол-во - {data['quantity']}\n"
                                                    f"Номер - {data['customers_phone']}"
                                    )

        await message.answer(text='Отправлено!', reply_markup=kb)

        await state.finish()

    else:
        await message.answer(text='Отменено')


async def cancel_fsm(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer(text='Отменено!')


def register_fsm_client(dp: Dispatcher):
    dp.register_message_handler(cancel_fsm, Text(equals='Отмена',
                                                 ignore_case=True),
                                state="*")
    dp.register_message_handler(fsm_start, commands=['order'])
    dp.register_message_handler(load_id_product, state=Fsm_order.id_product)
    dp.register_message_handler(load_size, state=Fsm_order.size)
    dp.register_message_handler(load_quantity, state=Fsm_order.quantity)
    dp.register_message_handler(load_phone, state=Fsm_order.customer_phone)
    dp.register_message_handler(check_order, state=Fsm_order.check_order)
