"""
[Author]: John Bostater

[Start Date]: 9/25/24

[Description]:
    {Networking Project}

    This Python script contains code for Sockets to communicate with eachother through different hosts.
    These hosts can then play the card game 'Golf' as followed in the tutorial. 
"""

#Relevant Libaries
#-----------------
import socket
import random
#-----------------


#Global Variables
#-----------------

#-----------------



#Server and Client Code Space
#----------------------------


#----------------------------



#Player Class Object
#----------------------------
class CardPlayer:
    #Constructor/Data Initialization
    #------------------------------------------------------
    def __init__(self):
        #Array that will hold the players uniquely dealed cards
        self.playerDeck = []
        self.userNumber = 0
    #------------------------------------------------------


    #Methods
    #------------------------------------------------------
    def showDeck(self):
        #Print every card in the Player's deck
        for card in self.playerDeck:
            print(card)
    #------------------------------------------------------

  

#----------------------------


#Game Functions
#----------------------------

#Add Player
def addPlayer(newPlayer):
    #This function will add all of the players to an array of CardPlayer Objects

    return '0'

def removePlayer():
    #This function

    return '0'


#Deal Cards
def dealCards(playerArray):

    #For each player object in the array


    #Add's 6 cards to each players deck
    shuffleNum = 0

    #Based on the random number pull the corresponding card out
    match shuffleNum:
        case 0: 
            print('okay')
            return "hello"
        
    
#Match the 

#----------------------------


#User Functions


#Server Functions


#Driver Space

#Print a menu for the user to navigate and use!