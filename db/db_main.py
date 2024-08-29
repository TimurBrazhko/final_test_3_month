import sqlite3 as sq
from db import quaries

db = sq.connect('db/db.sqlite3')
cursor = db.cursor()


async def sql_create_product():
    if db:
        print('LOL')
    cursor.execute(quaries.CREATE_TABLE_PRODUCTS)
    db.commit()


async def sql_insert_products(name, category, size, price, id_product, photo):
    cursor.execute(quaries.INSERT_PRODUCTS,(
        name,
        category,
        size,
        price,
        id_product,
        photo
    ))
    db.commit()
