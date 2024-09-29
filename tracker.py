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


[Simulate/Run Program]:
    Program was ran via 
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


#Registered Players
playerArray = []
#-----------------------------------



#Server-Client Functions
#---------------------------
#Create UDP Socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


#Bind the server to the first available port, 31500
server_address = ("128.110.223.4", 31500)

#DEBUG!!
print(f"Starting server on {server_address}")


#Bind the socket
server_socket.bind(server_address)


#LISTEN FOR MESSAGES!!
print('Waiting for a message...')

while True:
    #Receive message
    message, client_address = server_socket.recvfrom(1024)
    print(f"Received Message from Client: {message.decode('utf-8')} from {client_address}")




#Send Message to Client


#Receive Message


#---------------------------



#Game Functions
#-------------------------------------------------------------------------------------
#Add Player
def registerPlayer(playerInfo):
    #Delimeter for gathering relevant command info
    delimeter = playerInfo.find(' ')

    #Place the newly made player 'tuple' into the tuple array for players waiting to queue?
    #Register a new player for the query    

    #Name
    playerName = playerInfo[0:delimeter]    
    

    #Break function here if there is 


    #Update the given string and the delimeter
    playerInfo = playerInfo[(delimeter+1):]
    delimeter = playerInfo.find(' ')


    #IPv4
    ipAddress = playerInfo[0:delimeter]    
    
    #Update the given string and the delimeter
    playerInfo = playerInfo[(delimeter+1):]
    delimeter = playerInfo.find(' ')

    
    #t-port
    t_port = playerInfo[0:delimeter]

    #Update the given string and the delimeter
    playerInfo = playerInfo[(delimeter+1):]
    delimeter = playerInfo.find(' ')


    #p-port
    p_port = playerInfo


    #Dealer Flag 
    dealerFlag = False


#DEBUG!!
#    print("Data Pulled: ", playerName, ipAddress, t_port, p_port)


    #Complete the player tuple and add it to the registered players array
    newPlayer = (playerName, ipAddress, t_port, p_port, dealerFlag)


    #Add the player-tuple to the queued player array
    playerArray.append(newPlayer)


#DEBUG!!
    print('Player Array:', playerArray)


    return 0


#Remove Player
def removePlayer(selectedPlayer):
    #This function will remove the player from the game

    return '0'


#Deal Cards [Dealer Only]
def dealCards():
    #If the Player is the dealer, proceed
    #if self.dealer:
    
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
    print("{Command Space}\n")
#-------------------------------------------------------------------------------------



#Main/Driver Space
#-------------------------------------------------------------------------------

#DEBUG!!

p0_Cd = []

#PLAYER TUPLE EXAMPLE!!
#player_0 = (p0_Cd, "Hello!", True)

#p0_Cd.append('Hello')
#Display 
#print(player_0[0][0])


#Display the menu with the relevant commands for the user
displayMainMenu()


#While-loop that will run forever to take in user requests
while True:
    #Collect the user's commands for running functions of the Client
    userInput = str(input("$: "))


    #Register Player
    if userInput.find("register") != -1 and len(userInput) >= 28:
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