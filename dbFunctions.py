from dictFunctions import *
import json

#decide whether a username/password combo works or not
def login(username, password):
    sql = 'SELECT userId FROM usersTable WHERE username=? AND password=?'
    result = c.execute(sql, (username, password))

    result = c.fetchall()

    if(len(result) == 1):
        return True
    else:
        return False 

def getUserId(username):
    sql = "SELECT userId FROM usersTable WHERE username=?"
    result = c.execute(sql, (username,))
    result = c.fetchone()
    result = result['userId']
    return result #should be an integer

#update the user's cart
#=======================================================
#               int    list     str      int 
def addToCart(userId, item, quantity):
    #find out if we have any duplicates
    sql = "SELECT * FROM inventoryTable WHERE item=?"
    result = c.execute(sql, (item,))
    result = c.fetchall()
    if(result == 0):
        return false #failed to add the item
    else:
        #put the item into a dictionary list
        newItem = returnRowDicts(sql, item)
        newItem = newItem[0] #just grab the dictionary
        #see if the user already has a cart
        sql = "SELECT * FROM cartTable WHERE userId=?"
        result = c.execute(sql, (userId,))
        result = c.fetchall()
        if(result == 0):
            #the user has no cart.  Make them one
            sql = "INSERT INTO cartTable(userId, item, total) VALUES(?, null, 0)"
            result = c.execute(sql, (userId,))
            conn.commit() #gotta commit the changes
        #now everyone has a table.  Let's grab their variables
        sql = "SELECT * FROM cartTable WHERE userId=?"
        result = c.execute(sql, (userId,))
        result = c.fetchone()
        userTotal = result['total']
        userItems = result['items']
        #they don't have any items.  Can't append to null so fix it
        if(userItems == None):
            userItems = []
        else:
            userItems = fromJSON(userItems)
        #fix the total
        newItemPrice = newItem['price']
        newItemCost = newItemPrice*quantity
        userTotal += newItemCost
        newItem['quantity'] = quantity #decide the quantity
        #fix the item 
        userItems.append(newItem)
        userItems = toJSON(userItems) #gotta save it as a string
        #send all this junk to the database
        sql = "UPDATE cartTable SET items=?, total=? WHERE userId=?"
        result = c.execute(sql, (userItems, userTotal, userId))
        conn.commit()
        return True #yayyyyy we did it

        
addToCart(1, 'LOTR', 1)


