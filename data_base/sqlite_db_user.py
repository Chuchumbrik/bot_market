from data_base import sqlite_start


async def check_exists_product_catalog_user():
    count_products_catalog = \
        sqlite_start\
        .cur.execute('SELECT Count(*) FROM `product_catalog` WHERE is_hidden == 0')\
        .fetchall()[0][0]
    if count_products_catalog > 0:
        return True
    else:
        return False


async def get_product_catalog_user():
    return sqlite_start\
        .cur.execute('SELECT * FROM `product_catalog` WHERE is_hidden == 0')\
        .fetchall()
