from data_base import sqlite_start


async def add_product_in_catalog(state):
    async with state.proxy() as data:
        sqlite_start.cur.execute('INSERT INTO product_catalog (image, name, description, price) VALUES(?, ?, ?, ?)', \
                                 (data['photo'], data['name'], data['description'], data['price'],))
        sqlite_start.base.commit()


async def get_product_catalog():
    return sqlite_start.cur.execute('SELECT * FROM `product_catalog`').fetchall()


async def check_exists_product_catalog():
    count_products_catalog = sqlite_start.cur.execute('SELECT Count(*) FROM `product_catalog`').fetchall()[0]
    if count_products_catalog[0] > 0:
        return True
    else:
        return False


async def get_product_by_name(name):
    return sqlite_start.cur.execute('SELECT * FROM `product_catalog` WHERE `name` == ?', (name,)).fetchall()[0]


async def get_product_by_id(id):
    return sqlite_start.cur.execute('SELECT * FROM `product_catalog` WHERE `id` == ?', (id,)).fetchall()[0]


async def delete_product_by_id(id):
    print(f'delete id -{id}')
    sqlite_start.cur.execute('DELETE FROM `product_catalog` WHERE `id` == ?', (id,))
    sqlite_start.base.commit()


async def get_product_name_by_id(id):
    catalog_product = \
    sqlite_start.cur.execute('SELECT `name` FROM `product_catalog` WHERE `id` == ?', (id,)).fetchall()[0]
    return catalog_product[0]


async def get_product_id_by_name(id):
    catalog_product = \
    sqlite_start.cur.execute('SELECT `id` FROM `product_catalog` WHERE `name` == ?', (id,)).fetchall()[0]
    return catalog_product


async def check_exists_product_by_id(id):
    count_product = \
    sqlite_start.cur.execute('SELECT Count(*) FROM `product_catalog` WHERE `id` == ?', (id,)).fetchall()[0]
    if count_product[0] > 0:
        return True
    else:
        return False


async def edit_product_photo(id, photo):
    sqlite_start.cur.execute('UPDATE `product_catalog` SET `image` = ? WHERE `id` = ?', (photo, id,))
    sqlite_start.base.commit()


async def edit_product_name(id, name):
    sqlite_start.cur.execute('UPDATE `product_catalog` SET `name` = ? WHERE `id` = ?', (name, id,))
    sqlite_start.base.commit()


async def edit_product_description(id, description):
    sqlite_start.cur.execute('UPDATE `product_catalog` SET `description` = ? WHERE `id` = ?', (description, id,))
    sqlite_start.base.commit()


async def edit_product_price(id, price):
    sqlite_start.cur.execute('UPDATE `product_catalog` SET `price` = ? WHERE `id` = ?', (price, id,))
    sqlite_start.base.commit()


async def check_exists_user(user_name):
    users = sqlite_start.cur.execute('SELECT Count(*) FROM `users` WHERE `user_name` == ?', (user_name,)).fetchall()[0]
    if users[0] > 0:
        return True
    else:
        return False


async def add_user(user_name):
    sqlite_start.cur.execute('INSERT INTO users (user_name) VALUES (?)', (user_name,))
    sqlite_start.base.commit()


async def get_access_level(user_name):
    access_level = sqlite_start.cur.execute('SELECT `access_level` FROM `users` WHERE `user_name` == ?', (user_name,)).fetchall()[0]
    print(access_level)
    return access_level[0]


async def add_admin(user_name):
    sqlite_start.cur.execute('UPDATE `users` SET `access_level` = "admin" WHERE `user_name` = ?', (user_name,))
    sqlite_start.base.commit()


async def delete_admin(user_name):
    sqlite_start.cur.execute('UPDATE `users` SET `access_level` = "user" WHERE `user_name` = ?', (user_name,))
    sqlite_start.base.commit()
