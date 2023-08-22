import sqlite3 as sq

cur = None
base = None


def sql_start():
    global base, cur
    base = sq.connect('accountant.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    base.execute('CREATE TABLE IF NOT EXISTS product_catalog(\
		id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,\
		image TEXT,\
		name TEXT,\
		description TEXT,\
		price REAL NOT NULL,\
		is_hidden INTEGER NOT NULL,\
		count_before INTEGER NOT NULL,\
		count_after INTEGER NOT NULL\
	)')
    base.commit()
