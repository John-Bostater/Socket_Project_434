"""
[Author]: John Bostater

[Start Date]: 9/25/24

[Description]:
    {Networking Project}

    Server-Python Script, maintains state information of players and ongoing games.
    This file is able to respond to players via a text-based user interface.

    When executing the Tracker Script a paramater for the Port Number must be defined
      [Command]:
        > python3 Tracker.py 123456     //123456 is the port number in this case, add ip paramater?


    This Server contains a fixed IP address and Port Number that the Player's/Player objects
    will use for sending and receiving information about the game
"""


#Relevant Libaries
#------------------
import socket
from Player import*

#DEBUG!!
import random
#------------------



#Global Variables
#-----------------------------------
#Current Players in the game {Array}
playerArray = []
#-----------------------------------



#Server-Client Functions
#---------------------------

#---------------------------



#Game Functions
#----------------------------s
#Add Player
def addPlayer(newPlayer):
    #This function will add a new player to the game

    return '0'


#Remove Player
def removePlayer(selectedPlayer):
    #This function will remove the player from the game

    return '0' 
#----------------------------



#Program Functions
#-------------------------------------
def displayMainMenu():
    print("************************")
    print("*         Golf         *")
    print("************************")
    print("1. New Game")
    print("2. Join A Game")
    print("3. Games in Progress")
    print("************************")
#-------------------------------------



#Main/Driver Space
#-------------------------------------------------------------------------------
#[Requirements]:
    #Make a Game

    #Join a Game



#DEBUG Zone
print(len(cardDeck))
del cardDeck[0]
del cardDeck[25]

resetDeck()
print(len(cardDeck))


#Display the menu
displayMainMenu()


#While-loop that will run forever to take in user requests
while True:
    #Collect the user's choice for the Main Menu
    userInput = int(input("Selection: "))
    
    #Use a match-case for the user to select the functions of the User Interface
    match userInput:
        #DEBUG BELOW!!!
        case 1:
            print("No Way!!")
        
        #DEBUG BELOW!!!
        case 2: 
            print("Exiting Loop!")
            break
        
        case 3:
            print("Case #3")

    #Break the Program loop when the user choses to exit the program
    
#print("Loop Successfully broken!!, END OF PROGRAM!!")

#-------------------------------------------------------------------------------