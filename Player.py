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
