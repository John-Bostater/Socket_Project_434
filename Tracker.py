"""
[Author]: John Bostater

[Socket Group #]: 61

[Start Date]: 9/25/24

[Description]:
    {Server}

    Server-Python Script, maintains state information of players and ongoing games.
    This file is able to respond to players via a text-based user interface.

    When executing the Tracker Script a paramater for the Port Number must be defined
      [Command]:
        > python3 Tracker.py 123456     //123456 is the port number in this case, add ip paramater?


    This Server contains a fixed IP address and Port Number that the Player's/Player objects
    will use for sending and receiving information about the game

    
[Valid Port Number Range]: 
    31500   to   31999
"""


#Relevant Libaries
#------------------
import socket
import random
import os
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


#Games in Progress
runningGames = []
#Pass Tuples into this array of form: game_1 = (player_0, player_1)


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
def registerPlayer(playerInfo):
    #Delimeter for gathering relevant command info
    delimeter = playerInfo.find(' ')

    #Register a new player for the query
    
    #Place the newly made player 'tuple' into the tuple array for players waiting to queue?


    #IPv4
    ipAddress = playerInfo[0:delimeter]    
    
    #Update the given string and the delimeter
    playerInfo = playerInfo[(delimeter+1):]
    delimeter = playerInfo.find(' ')

    print('The next: ' + playerInfo[0:delimeter])
    
    #t-port


    #p-port


    #Complete the player tuple and add it to the registered players array
    

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




#Program Functions
#-------------------------------------------------------------------------------------
def displayMainMenu():
    print("********************************************************************************")
    print("*                                   Golf                                       *")
    print("********************************************************************************")
    print("{Server functions and their corresponding commands}\n")
    
    #Register the player
    print("  [Register Player]:    register <Player Name> <IPv4> <t-port> <p-port>\n")   
    #Returns number of players registered
    print("  [Query Registered Players]:    query players\n")
    print("  [Start Game]:  start game <Card Dealer Player's Name> <n> <# holes>\n")     
    #Return the # of ongoing games, with game-identifier and the current dealer's name of that game
    print("  [Query Games]: query games\n") 
    #End the specified game
    print("  [End Games]:   end <game-identifier> <Card Dealer Player's Name>\n")
    print("  [DeRegister Player]:   de register <player>\n")
    print("[Note]: Replace the parameters delimited by the chevrons with the relevant data")
    print("********************************************************************************")
#-------------------------------------------------------------------------------------



#Main/Driver Space
#-------------------------------------------------------------------------------

#DEBUG!!

p0_Cd = []

#PLAYER TUPLE EXAMPLE!!
player_0 = (p0_Cd, "Hello!", True)

p0_Cd.append('Hello')
#Display 
print(player_0[0][0])


#Display the menu with the relevant commands for the user
displayMainMenu()


#While-loop that will run forever to take in user requests
while True:
    #Collect the user's commands for running functions of the Client
    userInput = str(input("$: "))


    #Register Player
    if userInput.find("register") != -1:
        #Pass the: IPv4, t-port, and p-port
        registerPlayer(userInput[9:])


    #Query Players
    if userInput.find("query players") != -1:
        print('yes kay!')


    #Start Game
    if userInput.find("start game") != -1:
        print('yes kay!')


    #Query Games
    if userInput.find("query games") != -1:
        print('yes kay!')


    #End Games
    if userInput.find("end") != -1 and len(userInput) > 3:
        print('Ayooo')


    #DeRegister Player
    if userInput.find("de register") != -1 and len(userInput) > 12:
        print('Ayooo')
#-------------------------------------------------------------------------------

