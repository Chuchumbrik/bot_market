from data_base import sqlite_start


async def add_product_catalog(state):
    async with state.proxy() as data:
        sqlite_start.cur.execute(
            'INSERT INTO product_catalog '
            '(image, name, description, price, is_hidden, count_before, count_after) '
            'VALUES(?, ?, ?, ?, ?, ?, ?)',\
            (data['photo'], data['name'], data['description'], data['price'], data['isHidden'], data['count'],
             data['count'],))
        sqlite_start.base.commit()
