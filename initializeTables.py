from initializeDB import *

c.execute("INSERT INTO inventoryTable (price, item, description, quantity) VALUES ('12.35', 'Billy Bobs Guide to Programming', 'learn to program from the best', '10');")

conn.commit()

c.execute("INSERT INTO inventoryTable(price, item, description, quantity) VALUES(15.75, 'A Biography: Bullys Story', 'learn about our favorite bulldog', 8)")

conn.commit()

c.execute("INSERT INTO inventoryTable(price, item, description, quantity) VALUES(24.10, 'Learn to Program with Pictures!', 'learn to program from pictures!', 2)")

conn.commit()

c.execute("INSERT INTO inventoryTable(price, item, description, quantity) VALUES(7.00, 'Lil Johns WHAT! A love story', 'better love story than Twilight', 5)")

conn.commit()

c.execute("INSERT INTO inventoryTable(price, item, description, quantity) VALUES(12.35, 'Encyclopedia: Assorted Encyclopedias', 'the only encyclopedia you will ever need', 12)")

conn.commit()

c.execute("INSERT INTO inventoryTable(price, item, description, quantity) VALUES(6.30, 'Day of the Dying Alive', 'a new take on horror', 4)")

conn.commit()

c.execute("INSERT INTO usersTable(username, password, firstName, lastName, shippingAddress) VALUES('username123', 'password123', 'Username', 'Userton', 'User Lane Road, Starkville, MS 39759')")

conn.commit()