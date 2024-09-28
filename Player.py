"""
[Author]: John Bostater

[Start Date]: 9/25/24

[Description]:
    {Networking Project}

    This Python script contains code relevant for the Player Objects of the Card Game: 'Golf'
"""


#Relevant Libaries
#-----------------
import random
#-----------------



#Global Variables
#---------------------------------------------------------------------------------
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
#---------------------------------------------------------------------------------



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


    #Print all of the cards in the player's deck
    def showDeck(self):
        #Print every card in the Player's deck
        for card in self.playerDeck:
            print(card)


    #DEBUG PRINT
    def debug0(self):
        return "Wacky waving inflatable arm flailing tubeman!!"
#------------------------------------------------------


#Functions
#-------------------------------------------------------------------------------------
#Reset Card Deck (Add the card's back)
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