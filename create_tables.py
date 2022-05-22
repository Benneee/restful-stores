# This file will be in charge of creating tables in our DB taking the place of the test.py file
# as that will be deleted

import sqlite3


connection = sqlite3.connect('app.db')
cursor = connection.cursor()

# Using INTEGER instead of int so that the id auto-increments
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_items_table = "CREATE TABLE IF NOT EXISTS items (name text, price real)"
cursor.execute(create_items_table)

connection.commit()
connection.close()