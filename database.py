import sqlite3
import json

conn = sqlite3.connect('bookstoreDB.db')
conn.row_factory = sqlite3.Row
c = conn.cursor() 


c.execute('''CREATE TABLE IF NOT EXISTS usersTable( userId INTEGER PRIMARY KEY, username text, password text, firstName text, lastName text, shippingAddress text)''')

conn.commit()

c.execute('''CREATE TABLE IF NOT EXISTS inventoryTable(inventoryId INTEGER PRIMARY KEY, price REAL, item text, description text, quantity INTEGER)''')

conn.commit()

c.execute('''CREATE TABLE IF NOT EXISTS cartTable(cartId INTEGER PRIMARY KEY, userId INTEGER, items text, total REAL, FOREIGN KEY(userId) REFERENCES usersTable(userId))''')

conn.commit()

c.execute('''CREATE TABLE IF NOT EXISTS ordersTable(orderId INTEGER PRIMARY KEY, userId INTEGER, items text, total REAL, date text, FOREIGN KEY(userId) REFERENCES usersTable(UserId))''')

conn.commit()

