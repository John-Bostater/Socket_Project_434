"""
[Author]: John Bostater

[Start Date]: 9/25/24

[Description]:
    {Networking Project}

    This Python script contains code that will track the game as well as server-client processes
"""


#Relevant Libaries
#-----------------
import socket
import random
#-----------------



#Global Variables
#--------------------------------------------------------------------------------

#This is the main Card deck that the Dealer will deal use
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
#--------------------------------------------------------------------------------



#Server-Client Functions
#---------------------------

#---------------------------



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

    #Deal each player 6 cards
    for players in playerArray:
        #Add's 6 cards to each players deck
        
        #Randomly generate a number that will correspond to a card in the deck       
        shuffleNum = random.randint(0, 51)

        #Based on the random number pull the corresponding card out
        match shuffleNum:
            case 0: 
                print('okay')
                return "hello"


 
#Determine if card_1 beats card_2
def compareCards(card_1, card_2):
    #Add code here...
    
    return 0
#----------------------------



#Driver Space
#----------------------------

#DEBUG
for player in cardDeck:
    print(player + " ")
#----------------------------