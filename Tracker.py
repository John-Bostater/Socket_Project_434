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
import random

#NEW!!
import sys #Used for getting command line args
#------------------



#Global Variables
#-----------------------------------
#Main Card deck that the Dealer-Player will deal cards from
cardDeck = [
    #Clubs
    "AC", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C", "JC", "QC", "KC",

    #Spades
    "AS", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "JS", "QS", "KS",

    #Hearts
    "AH", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "JH", "QH", "KH",

    #Diamonds
    "AD", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D", "JD", "QD", "KD"
]

#Current Players in the game {Array}
playerArray = []
#-----------------------------------



#Server-Client Functions
#---------------------------

#Send Message to Client

#Receive Message


#---------------------------



#Game Functions
#-------------------------------------------------------------------------------------
#Add Player
def addPlayer(newPlayer):
    #This function will add a new player to the game

    return '0'


#Remove Player
def removePlayer(selectedPlayer):
    #This function will remove the player from the game

    return '0'


#Deal Cards [Dealer Only]
def dealCards(self, playerArray):
    #If the Player is the dealer, proceed
    if self.dealer:
        #Deal each player 6 cards
        for players in playerArray:

            #Add's 6 cards to each players deck
            for i in range(6):
                #Randomly generate a number that will correspond to a card in the deck       
                shuffleNum = random.randint(0, len(cardDeck))

                #Add the cards to the players deck
                players.addCard(cardDeck[shuffleNum])

                #Remove the pulled card from the deck
                del cardDeck[shuffleNum]
    else:
        print('You are not a dealer')


#Reset Card Deck (Adds the missing cards back)
def resetDeck():
    #Add the cards back to the deck/reset the deck
    cardDeck = [
        #Clubs
        "AC", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C", "JC", "QC", "KC",

        #Spades
        "AS", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "JS", "QS", "KS",

        #Hearts
        "AH", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "JH", "QH", "KH",

        #Diamonds
        "AD", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D", "JD", "QD", "KD"
    ]
#-------------------------------------------------------------------------------------



#Player Class Object
#---------------------------------------------------------------
class CardPlayer:
    #Constructor/Data Initialization
    #------------------------------------------------------
    def __init__(self):
        #Array that will hold the player's uniquely dealt cards
        self.playerDeck = []
        
        #Players id Number, {1-3}
        self.userNumber = 0

        #Dealer Flag
        self.dealer = False
    #------------------------------------------------------


    #Methods
    #------------------------------------------------------
    #Print all of the cards in the player's deck
    def showDeck(self):
        #Print every card in the Player's deck
        for card in self.playerDeck:
            print(card)


    #DEBUG PRINT
    def debug0(self):
        return "Wacky waving inflatable arm flailing tubeman!!"
#---------------------------------------------------------------



#Program Functions
#-------------------------------------
def displayMainMenu():
    print("************************")
    print("*         Golf         *")
    print("************************")
    print("1. New Game")
    print("2. Games in Progress")
    print("************************")
#-------------------------------------



#Main/Driver Space
#-------------------------------------------------------------------------------
print("Arguments: ", sys.argv[1])


#[Requirements]:
    #Establish a Static IP Address Port and Port range for listening 

    #Make a Game


    #Join a Game






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