from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import buttons
from db import db_main


class Fsm_products(StatesGroup):
    name_product = State()
    category = State()
    size = State()
    price = State()
    id_product = State()
    photo_product = State()
    submit = State()


async def fsm_start(message: types.Message):
    await Fsm_products.name_product.set()
    await message.answer(text='Введите название товара: ',
                         reply_markup=buttons.cancel)


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data_store:
        data_store['name_product'] = message.text

    await Fsm_products.next()
    await message.answer(text="Укажите категорию товара:")


async def load_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data_store:
        data_store['category'] = message.text

    await Fsm_products.next()
    await message.answer(text="Укажите размер товара:")


async def load_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data_store:
        data_store['size_product'] = message.text

    await Fsm_products.next()
    await message.answer(text="Укажите цену товара:")


async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data_store:
        data_store['price'] = message.text

    await Fsm_products.next()
    await message.answer(text="Укажите артикул товара:")


async def load_id_product(message: types.Message, state: FSMContext):
    async with state.proxy() as data_store:
        data_store['id_product'] = message.text

    await Fsm_products.next()
    await message.answer(text="Отправьте фотографию товара:")


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data_store:
        data_store['photo_product'] = message.photo[-1].file_id

    await message.answer_photo(photo=data_store['photo_product'],
                               caption=f"Название товара - {data_store['name_product']}\n"
                                       f"Категория - {data_store['category']}\n"
                                       f"Размер - {data_store['size_product']}\n"
                                       f"Цена - {data_store['price']}\n"
                                       f"Артикул - {data_store['id_product']}\n"
                                       f"Верны ли данные?",
                               reply_markup=buttons.submit_buttons)
    await Fsm_products.next()


async def submit(message: types.Message, state: FSMContext):
    if message.text == "Да":
        kb = types.ReplyKeyboardRemove()

        async with state.proxy() as data_store:
            await db_main.sql_create_product()
            await db_main.sql_insert_products(
                name=data_store['name_product'],
                category=data_store['category'],
                size=data_store['size_product'],
                price=data_store['price'],
                id_product=data_store['id_product'],
                photo=data_store['photo_product']
            )

        await message.answer(text='Ваши данные сохранены!', reply_markup=kb)
        await state.finish()

    else:
        await message.answer(text='Отменено!')
        await state.finish()


async def cancel_fsm(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer(text='Отменено!')


def register_fsm_products(dp: Dispatcher):
    dp.register_message_handler(cancel_fsm, Text(equals='Отмена',
                                                 ignore_case=True),
                                state="*")
    dp.register_message_handler(fsm_start, commands=['product'])
    dp.register_message_handler(load_name, state=Fsm_products.name_product)
    dp.register_message_handler(load_category, state=Fsm_products.category)
    dp.register_message_handler(load_size, state=Fsm_products.size)
    dp.register_message_handler(load_price, state=Fsm_products.price)
    dp.register_message_handler(load_id_product, state=Fsm_products.id_product)
    dp.register_message_handler(load_photo, state=Fsm_products.photo_product, content_types=['photo'])
    dp.register_message_handler(submit, state=Fsm_products.submit)
