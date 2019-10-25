from database import *
from dictFunctions import *
from dbFunctions import *

#this is where we'll hold some gui functions to make our life easier
def viewInventoryScreen(userId):
    showInventory()
    userInput = input("Type 'add' to add an item to your cart. Type 'viewCart' to view your cart.\nType 'logout' to logout. ")
    check = checkUserInput(userInput, userId)
    while(check == True):
        showInventory()
        userInput = input("Type 'add' to add an item to your cart. Type 'viewCart' to view your cart.\nType 'logout' to logout. ")
        check = checkUserInput(userInput, userId)
    return False



def checkUserInput(userInput, userId):
    print("")
    print("")
    #this will be our add keyword
    if(userInput == "add"):
        try:
            item, quantity = input("Enter the item ID you would like and how many: ").split()
        except:
            print("We're sorry, that didn't work!  Remember, enter the item's ID and then quantity desired.")
            input("Please hit enter to continue.")
            return True
        try:
            #print("type item: ", type(item), "type quan: ", type(quantity))
            item = int(item)
            quantity = int(quantity)
            addToCart(userId, item, quantity)
            print("added", quantity,"of item of ID", item)
            input("hit enter to continue. ")
            return True
        except:
            print("Something went wrong.  Make sure the quantity is a whole number.")
            return True
    
    #check if the user wants to leave
    if(userInput == 'logout'):
        return False
    #this is also gonna hold all of the cart functions
    elif(userInput == "viewCart"):
        #check if the user even has a cart
        try:
            sqlHasCart = "SELECT * FROM cartTable WHERE userId=?"
            result = c.execute(sqlHasCart, (userId,))
            result = c.fetchone()
        except:
            print("Looks like you don't have a cart.  Add an item to create a cart.")
            input("hit enter to continue ")
            return True
        if(result == None):
            print("Looks like your cart is empty.  Add an item to view your cart.")
            input("hit enter to continue ")
            return True
        #the user does have a cart. Show them the cart and offer some functions
        else:
            checkCart = True
            while(checkCart == True):
                showCart(userId)
                try:
                    userInputCart = input("type 'return' to go back to the inventory page.  Type 'options' to view options. ")
                except:
                    print("I'm sorry, that command was not accepted. Please try again.")
                    input("Hit enter to continue")
                    return True
                while(userInputCart != 'return' and userInputCart != 'options'):
                    print("")
                    print("Sorry, that wasn't 'return' or 'options'\n")
                    userInputCart = input("type 'return' to go back to the inventory page.  Type 'options' to view options. ")
                if(userInputCart == 'return'):
                    return True
                elif(userInputCart == 'options'):
                    check = checkUserInputCart(userId)

    else:
        print("We didn't understand that command.  Please try again. (hit enter to continue)")
        input("")
        return True

def checkUserInputCart(userId):
    print("")
    print("")
    showCart(userId)
    print("You can increase the quantity of items by using 'add'.")
    print("You can remove items by using 'remove'.")
    print("You can checkout by using 'checkout'.")
    print("You can return to the inventory screen by using 'return'.")
    command = input("")

    #this will be our add keyword
    if(command == "add"):
        try:
            item, quantity = input("Enter the item ID you would like and how many (case sensitive): ").split()
        except:
            print("We're sorry, that didn't work!  Remember to type the item's ID and then quantity.")
            input("Please hit enter to continue.")
            return True
        try:
            addToCart(userId, item, int(quantity))
            input("hit enter to continue. ")
            return True
        except:
            print("Something went wrong.  Make sure the quantity is a whole number.")
            return True #something went wrong, but that doesn't mean the user wants to leave
    
    elif(command == "remove"):
        try:
            item, quantity = input("Enter the item ID of the item you would like and how many (case sensitive): ").split()
        except:
            print("We're sorry, that didn't work!  Remember to type the item's ID and then quantity.")
            input("Please hit enter to continue.")
            return True
        try:
            item = int(item)
            quantity = int(quantity)
            deleteFromCart(userId, item, int(quantity))
            input("hit enter to continue. ")
            return True
        except:
            print("Something went wrong.  Make sure the quantity is a whole number.")
            return True #something went wrong, but that doesn't mean the user wants to leave
    elif(command == 'checkout'):
        checkout(userId)
        return False
    elif(command == 'return'):
        return False