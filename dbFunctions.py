from dictFunctions import *
import json
import os
from initializeDB import *

#decide whether a username/password combo works or not
def login(username, password):
    sql = 'SELECT userId FROM usersTable WHERE username=? AND password=?'
    result = c.execute(sql, (username, password))
    try:
        result = c.fetchone()
    except:
        return 0
    if(result != None):
        return result['userId']
    else:
        return 0

def getUserId(username):
    sql = "SELECT userId FROM usersTable WHERE username=?"
    result = c.execute(sql, (username,))
    result = c.fetchone()
    result = result['userId']
    return result #should be an integer

#update the user's cart
#=======================================================
#               int    list     str      int 
def addToCart(userId, inventoryId, quantity):
    #find out if we have any duplicates
    sql = "SELECT * FROM inventoryTable WHERE inventoryId=?"
    result = c.execute(sql, (inventoryId,))
    result = c.fetchall()
    if(result == 0):
        print("FAILED TO ADD ITEM")
        return false #failed to add the item
    else:
        #put the item into a dictionary list
        newItem = returnRowDicts(sql, inventoryId)
        newItem = newItem[0] #just grab the dictionary
        #see if the user already has a cart
        sql = "SELECT * FROM cartTable WHERE userId=?"
        result = c.execute(sql, (userId,))
        result = c.fetchall()
        if not result:
            #the user has no cart.  Make them one
            print("USER ID: ", userId)
            sql = "INSERT INTO cartTable(userId, items, total) VALUES(?, null, 0)"
            c.execute(sql, (userId,))
            conn.commit() #gotta commit the changes
        
        #now everyone has a table.  Let's grab their variables
        sql = "SELECT * FROM cartTable WHERE userId=?"
        result = c.execute(sql, (userId,))
        result = c.fetchall()
        userTotal = []
        userItems = []
        if(result):
            for row in result:
                userTotal.append(row['total'])
                userItems.append(row['items'])
                #print(userItems)
                #print("usertotal", userTotal[row])
                #print("useritems", userItems[row])
        #they don't have any items.  Can't append to null so fix it
        if (userItems[0] == None):
            #print("IN IF")
            #print("GOT HERE")
            userItems = []
            userTotal = 0.0
        else:
            #print("IN ELSE")
            #print("useritems: ", result['items'])
            userItems = fromJSON(userItems[0])
            userTotal = userTotal[0]
        #fix the total
        #print(userItems[0]['item'])
        newItemPrice = newItem['price']
        newItemCost = newItemPrice*quantity
        userTotal += newItemCost
        newItem['quantity'] = quantity #decide the quantity
        #if the item exists already
        itemNotFound = 1 #assume the item isn't in there
        for x in range(len(userItems)):
            if(inventoryId == userItems[x]['inventoryId']):
                #print("GOT HERE")
                userItems[x]['quantity'] += quantity
                itemNotFound = 0 #we found the item
        if(itemNotFound == 1):
            #print("DIDNT FIND THE ITEM")
            #append the new item
            userItems.append(newItem)
        userItems = toJSON(userItems) #gotta save it as a string
        #update everything due to new item
        sql = "UPDATE cartTable SET items=?, total=? WHERE userId=?"
        result = c.execute(sql, (userItems, userTotal, userId))
        conn.commit()
        #print("GOT HERE")
        return True #yayyyyy we did it

#deletefromcart function
#=================================================================

def deleteFromCart(userId, inventoryId, quantity):
    #grab the user's cart
    sql = "SELECT * FROM cartTable WHERE userId=?"
    result = c.execute(sql, (userId,))
    result = c.fetchone()
    #see if the item is in the cart at all
    userItems = result['items']
    userTotal = result['total']
    index = -1
    userItems = fromJSON(userItems)
    for x in range(len(userItems)):
        if(inventoryId == userItems[x]['inventoryId']):
            #print("Found index")
            index = x #grab the index where the item is
    if(index == -1):   
        print('failed')
        print("inventoryId: ", userItems[x]['inventoryId'])
        return False  #looks like the item wasn't there

    userItemsQuantity = userItems[index]['quantity']
    userItemsPrice = userItems[index]['price']
    userItemsCost = 0 #we're gonna figure this later
    #print(userItemsQuantity)
    #check how many the user wants to take out of cart
    if(quantity >= userItemsQuantity):
        userItems.pop(index) #remove that section entirely
        #we're taking the whole thing out, so take the total of this item out of the cart total
        userItemsCost = userItemsQuantity*userItemsPrice #this way someone doesn't delete items and get back money somehow
    else:
        userItemsQuantity -= quantity
        userItemsCost = userItemsPrice*quantity #this value wasn't above how many was in the cart.  So we're good
            #let's update the database now 
        userItems[index]['quantity'] = userItemsQuantity #can't have this outside the else or we might try and change a quantity that deson't exist
    userTotal -= userItemsCost
    if(len(userItems) != 0):
        userItems = toJSON(userItems)
    else:
        userItems = None
    sql = "UPDATE cartTable SET items=?, total=? WHERE userId=?"
    result = c.execute(sql, (userItems, userTotal, userId))
    conn.commit()
    return True #YEEHAW we did it

#Gotta check the actual total because people can add more to the cart
#than is in inventory.  So let's get a real total and update inventory at the same time
def updateFinalTotalandInventory(userId):
    sql = "SELECT * FROM cartTable WHERE userId=?"
    result = c.execute(sql, (userId,))
    result = c.fetchone()
    userItems = result['items']
    userItems = fromJSON(userItems) #remember to always switch from json
    items = []
    itemQuantities = []
    #let's get all the names of the items and their quantity
    for x in range(len(userItems)):
        items.append(userItems[x]['inventoryId'])
        itemQuantities.append(userItems[x]['quantity'])
    #we got the user's items, let's get the items and their quantity from the
    #inventory table
    sqlInventory = "SELECT * FROM inventoryTable"
    results = c.execute(sqlInventory)
    results = c.fetchall() #we gotta use a fetchall here.  So a bit more logic involved
    #first, let's get a dictionary of the all the items.
    #then we'll get a list of all the quantities
    inventoryItems = []
    inventoryQuantities = []
    correctInventoryQuantities = [] #this is just the quantities of the IDs that are held in items[]
    for row in results:
        inventoryItems.append(row['inventoryId'])
        inventoryQuantities.append(row['quantity'])
    #alright, now we gotta do comparisons
    totalChanged = False #we'll check if the total changed later
    for i in range(len(userItems)): #for how many items are in the cart
        for x in range(len(inventoryItems)): #check them against how many items there are in inventory
            if(items[i] == inventoryItems[x]):
                correctInventoryQuantities.append(inventoryQuantities[x])
                if(itemQuantities[i] > inventoryQuantities[x]):
                    totalChanged = True #if we got here, the total changed 
                    itemQuantities[i] = inventoryQuantities[x] #simply change the value in the cart.  The user will never know until the order is placed
    #we've got the inventory updated, let's update the cart
    #this takes a bit more since all of our stuff is in dictionaries. so
    finalTotal = 0
    print("")
    print("")
    print("Checkout: \n====================================") #using this to prettify our purchase print()
    for x in range(len(userItems)):
        userItems[x]['quantity'] = itemQuantities[x]
        #now we got that solved.  Let's fix the total
        finalTotal += userItems[x]['price']*userItems[x]['quantity']
        #let's print out what the user bought
        print(userItems[x]['quantity'], userItems[x]['item'], "at", userItems[x]['price'], "per unit")
    #booyah.  Let's update the cart and call it a day.
    print("------------------------------------")
    print("For a grand total of: $", ( "%5.2f"% finalTotal))
    print("")
    print("")
    if(totalChanged == True):
        print("Your cart had a few items over the stock quantity.")
    print("Your total is going to be $", (( "%5.2f"% finalTotal)))
    check = input("Would you like to continue checking out[y/n]?")
    if(check == 'n'):
        return False
    else:
        #now update the totals and the inventory
        sqlInventoryUpdate = "UPDATE inventoryTable SET quantity=? WHERE inventoryId=?"
        #we're gonna do multiple updates, so
        for x in range(len(items)):
            #print("ITEMS[x]: ", items[x], "inventoryQ[x]: ", correctInventoryQuantities[x], "invId: ", inventoryItems[x], "ITEMQ: ", itemQuantities[x])
            c.execute(sqlInventoryUpdate, ((correctInventoryQuantities[x]-itemQuantities[x]), items[x] ))
            conn.commit()
        userItems = toJSON(userItems) #put it back in json format
        sqlUpdateCart = "UPDATE cartTable SET items=?, total=? WHERE userId=?"
        c.execute(sqlUpdateCart, (userItems, finalTotal, userId,))
        conn.commit()
        return True


    
    

##Woohoo, almost done. 
#here's the checkout function that walks the user through checkout
#==================================================================
def checkout(userId):
    print("")
    print("")
    print("Welcome to checkout!  We hope you found everything you wanted!")
    sqlCheckCart = "SELECT total FROM cartTable WHERE userId=?"
    checkTotal = c.execute(sqlCheckCart, (userId,))
    checkTotal = c.fetchone()
    if(checkTotal['total'] == 0):
        print("Your cart is empty. Cannot checkout")
        print("")
        print("press enter to continue")
        input("")
        return
    #check to see if the user has a shipping address
    sql = "SELECT * FROM usersTable WHERE userId=?"
    result = c.execute(sql, (userId,))
    result = c.fetchone()
    check = 'n'
    #the user has a shipping address
    if(result['shippingAddress'] != None):
        print("The package will be sent to", result['shippingAddress'])
        check = input("Is this correct[y/n]?")
    #either the user wanted to change their shipping address or didn't have one
    if(result['shippingAddress'] == None or check == 'n'):
        #it's a multi spaced input sooooooo
        shippingAddress = list(map(str,input("Please enter your shipping address and hit enter.. ").split()))
        shipAddString = ""
        #make a string out of the list
        for x in range(len(shippingAddress)):
            shipAddString = shipAddString + " " + shippingAddress[x]
        #update the shipping address in the database
        sqlShipping = "UPDATE usersTable SET shippingAddress=? WHERE userId=?"
        result = c.execute(sqlShipping, (shipAddString, userId,))
        conn.commit()
        print("The package will be sent to", shipAddString)
    #grab the user's cart information
    sql = "SELECT * FROM cartTable WHERE userId=?"
    result = c.execute(sql, (userId,))
    result = c.fetchone()
    print("")
    print("")
    print("")
    #get the user's credit card
    while(True):
        creditcard = input("Please type your 10 digit credit-card number: ")
        try:
            if(len(creditcard) == 10):
                creditcard = int(creditcard)
                break
        except:
            print("please type a 10 digit credit-card number ")
            continue
    print("")
    print("")
    #check the user's final total
    check = updateFinalTotalandInventory(userId)
    if(check == False):
        print("your order has been canceled.")
        print("")
        print("")
        return
    else:
        sqlChange = "SELECT * FROM cartTable WHERE userId=?"
        change = c.execute(sql, (userId,))
        change = c.fetchone()
        #gotta be extra sure with a final yes or no
        #we're gonna update the final total and such in the cart for the correct amount
            #grab the user's cart again because the fields have changed since then
        sql = "SELECT * FROM cartTable WHERE userId=?"
        result = c.execute(sql, (userId,))
        result = c.fetchone()
        #store the order in the ordersTable
        sql = "INSERT INTO ordersTable(userId, items, total, date, creditcard) VALUES(?, ?, ?, CURRENT_TIMESTAMP, ?)"
        result = c.execute(sql, (userId, result['items'], result['total'], creditcard ))
        conn.commit()
        sql = "UPDATE cartTable SET items=NULL, total=0 WHERE userId=?" #this is just emptying out the cart for later uses.
        result = c.execute(sql, (userId,))
        conn.commit()
        print("")
        print("Congratulations on your purchase! You can view this order on the orders screen.  Have a nice day!")
        input("press enter to continue back to the inventory screen.")


        


#show inventory
def showInventory():
    sql = "SELECT * FROM inventoryTable"
    result = c.execute(sql)
    result = c.fetchall()
    #print the legend
    print("")
    print("")
    print("")
    print("ALIBABA BOOK STORE")
    print("=============================================================================================================================================================")
    print ("%-5s%-40s%-60s%-5s%27s%10s\n" % ("ID", "Item Name", "Description", "In Stock","|", "Price"))
    for row in result:
        print ("%-5s%-40s%-60s%-5s%30s%10s\n" % (row['inventoryId'], row['item'], row['description'], row['quantity'],"$", ( "%8.2f"% row['price'])))
    
#Looks like a lot of logic, but it's just some print statements
def showCart(userId):
    #let's get the user's username for good looks
    sqlGetUsername = "SELECT username FROM usersTable WHERE userId=?"
    username = c.execute(sqlGetUsername, (userId,))
    username = c.fetchone()
    username = username['username']
    #now let's get the cart
    sql = "SELECT * FROM cartTable WHERE userId=?"
    result = c.execute(sql, (userId,))
    result = c.fetchone()
    if not result['items']:
        print("Looks like your cart is empty!")
        print("")
        print("Press return to leave.")
        return
    #gotta do some logic so we don't print out a bunch of json files
    userItems = result['items']
    userTotal = result['total']
    userItems = fromJSON(userItems)
    IdList = []
    itemsList = []
    quantityList = []
    priceList = []
    descriptionList = []
    for x in range(len(userItems)):
        IdList.append(userItems[x]['inventoryId'])
        itemsList.append(userItems[x]['item'])
        quantityList.append(userItems[x]['quantity'])
        priceList.append(userItems[x]['price'])
        descriptionList.append(userItems[x]['description'])
    #spacing like the inventory page
    print(username + "'s Cart")
    print("==================================================================================================================================================================")
    print ("%-5s%-60s%-40s%-5s%24s%10s\n" % ("ID", "Item Name", "Description", "Quantity","|", "Price"))
    for x in range(len(userItems)):
        print ("%-5s%-60s%-40s%-5s%27s%10s\n" % (str(IdList[x]), str(itemsList[x]), str(descriptionList[x]), str(quantityList[x]),"$", str(( "%8.2f"% priceList[x]))))
    print("Total in Cart: $", ( "%8.2f"% userTotal))
    print("")

def showOrders(userId):
    print("")
    print("")
    sql = "SELECT * FROM ordersTable WHERE userId=?"
    results = c.execute(sql, (userId,))
    results = c.fetchall()
    #if we have any results
    if(results):
        print ("%-5s%-60s%24s%20s\n" % ("ID", "Total", "Date", "Credit Card"))
        for row in results:
            print ("%-5s%-60s%24s%20s\n" % (row['orderId'],("%8.2f"% row['total']), row['date'], row['creditcard']))
    #if we don't
    else:
        print("looks like you don't have any orders.")

def showUniqOrder(userId, orderId):
    print("")
    print("")
    sql = "SELECT * FROM ordersTable WHERE orderId=?"
    result = c.execute(sql, (orderId,))
    result = c.fetchone()
    if not result:
        print("No order of that ID")
        return
    userItems = result['items']
    userTotal = result['total']
    userItems = fromJSON(userItems) #change from json into list
    IdList = []
    itemsList = []
    quantityList = []
    priceList = []
    descriptionList = []
    for x in range(len(userItems)):
        IdList.append(userItems[x]['inventoryId'])
        itemsList.append(userItems[x]['item'])
        quantityList.append(userItems[x]['quantity'])
        priceList.append(userItems[x]['price'])
        descriptionList.append(userItems[x]['description'])
    print ("%-5s%-60s%-40s%-5s%24s%10s\n" % ("ID", "Item Name", "Description", "Quantity","|", "Price"))
    for x in range(len(userItems)):
        print ("%-5s%-60s%-40s%-5s%27s%10s\n" % (str(IdList[x]), str(itemsList[x]), str(descriptionList[x]), str(quantityList[x]),"$", str(( "%8.2f"% priceList[x]))))
    print("Final Total: $", ( "%8.2f"% userTotal))
    print("")
    print("")


