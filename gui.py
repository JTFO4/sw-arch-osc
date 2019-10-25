from database import *
from dictFunctions import *
from dbFunctions import *
from guiFunctions import *
#This is where we're gonna make our big GUI type deal
USER = 0

#GUI
#====================================================
def gui():
    isLoggedIn = 0
    #make some beginning print statements
    print("")
    print("")
    print("")
    print("Hello!  Welcome to Alibaba's new bookstore!")
    print("")
    username = input("You must login to use the system.  Please type your username and hit enter or type 'exit' to leave.. ")
    if(username == 'exit'):
        exit()
    password = input("Now please enter your password and hit enter.. ")
    #first, they gotta login.  Won't do anything until they do
    i = 0 #just a counter to make sure we don't throw up errors on the first go
    while(isLoggedIn == 0):

        if(i > 0):
            print("")
            print("We're Sorry, that was the wrong username and/or password.  Please try again or type 'exit' to leave.")
            username = input("Please type your username or exit and hit enter.. ")
            if(username == 'exit'):
                exit() #exit the program
            password = input("Please enter your password and hit enter.. ")
        isLoggedIn = login(username, password)
        i += 1

    #we're all logged in.  Start the inventory screen
    while(True):
        viewInventoryScreen(isLoggedIn)
        return #if they left the inventory system, then they wanted to leave



    
