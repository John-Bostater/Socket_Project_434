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


[Program Testing]:
    Program was tested/ran via 'CloudLab' experiment with two Nodes, both nodes are under the same subnet
        [Romeo]: 123.213.123.4  {Server}
        [Juliet]: 123.213.123.3  {Client}

    Place the python script 'tracker.py' in Romeo and run it

    Place the python script 'player.py' in Juliet and run it
    calling upon the function 'sendMessage()' in player.py will send a message to the Server that can be displayed by the server 

    {Read incoming messages as Server}
        #Receive message
        message, clientAddress = serverSocket.recvfrom(1024)
        
        #Print message
        print(f"Received Message from Client: {message.decode('utf-8')}")

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
registeredPlayer = []


#Client address of the latest message/command
currentClientAddress = 0
#-----------------------------------



#Server-Client Functions
#---------------------------
#Create UDP Socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


#Bind the server to the first available port, 31500
serverAddress = ("128.110.223.4", 31500)


#DEBUG!!
print(f"Starting server on {serverAddress}")


#Bind the Server's Socket
serverSocket.bind(serverAddress)


#Send Message to Client
def sendClientMessage(clientAddress, message):
    #Send a customized message back to the Client via their address tuple: (IPv4, Port#)
    serverSocket.sendto(message.encode('utf-8'), clientAddress)

    #DEBUG
    print('Debug print')

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
    

    #Break function here if the playerName already exists within the registered players
    for player in registeredPlayer:
        #Do NOT continue if the player's name is a duplicate
        if player[0] == playerName:
            sendClientMessage(currentClientAddress, "FAILURE")
            return 'FAILURE'


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
    #Communication between Player and Server
    #The server will use this port to talk back to the Client??

    #Update the given string and the delimeter
    playerInfo = playerInfo[(delimeter+1):]
    delimeter = playerInfo.find(' ')


    #p-port
    p_port = playerInfo
    #Communication between Player and Player

    #Dealer Flag 
    dealerFlag = False


#DEBUG!!
#    print("Data Pulled: ", playerName, clientAddress, p_port)


    #Complete the player tuple and add it to the registered players array
    newPlayer = (playerName, ipAddress, t_port, p_port, dealerFlag)


    #Add the player-tuple to the queued player array
    registeredPlayer.append(newPlayer)


#NEW
    #Send a message back to the client, "SUCCESS"
    sendClientMessage(currentClientAddress, "SUCCESS")


#DEBUG!!
#    print('Player Array:', registeredPlayer)

    return 'SUCCESS'


#Remove Player
def removePlayer(selectedPlayer):
    #This function will remove the player from the game

    return '0'


#Deal Cards [Dealer Only]
def dealCards():
    #If the Player is the dealer, proceed
    #if self.dealer:
    
    #Deal each player 6 cards
    for players in registeredPlayer:

        #Add's 6 cards to each players deck
        for i in range(6):
            #Randomly generate a number that will correspond to a card in the deck       
            shuffleNum = random.randint(0, len(cardDeck))

            #Add the cards to the players deck
            players[1] = (cardDeck[shuffleNum])

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
    print("*                              Golf   [Server-Side]                            *")
    print("********************************************************************************")
    print("{Client Commands/Messages}\n")
    
    #print("{Command Space}\n")
#-------------------------------------------------------------------------------------



#Main/Driver Space
#-------------------------------------------------------------------------------

#DEBUG!!

#p0_Cd = []

#PLAYER TUPLE EXAMPLE!!
#player_0 = (p0_Cd, "Hello!", True)

#p0_Cd.append('Hello')
#Display 
#print(player_0[0][0])


#Display the menu with the relevant commands for the Server
displayMainMenu()


#While-loop that will run forever to take in commands for server manipulation
while True:
    #Receive a Message/Request from the Client
    message, currentClientAddress = serverSocket.recvfrom(1024)
    #print(f"Received Message from Client: {message.decode('utf-8')} from {currentClientAddress}")


    #Client Request variable 
    clientRequest = str(message.decode('utf-8'))

    #Print the incoming Client-Command
    print(f'Client Command:\t\t{clientRequest} from {currentClientAddress}')


#OLD!!!
    #Collect the user's commands for running functions of the Client
    #userInput = str(input("$: "))


    #Register Player
    if clientRequest.find("register") != -1 and len(clientRequest) >= 28:
        #Pass the: IPv4, t-port, and p-port
        registerPlayer(clientRequest[9:])

        #DEBUG!!
        print('Player Array After Register:',registeredPlayer)


    #Query Players
    elif clientRequest.find("query players") != -1:
        #Query the players currently registered with the tracker

        #return number of registered players


        print('yes kay!')


    #Start Game
    elif clientRequest.find("start game") != -1:
        print('yes kay!')


    #Query Games
    elif clientRequest.find("query games") != -1:
        print('yes kay!')


    #End Games
    elif clientRequest.find("end") != -1 and len(clientRequest) > 3:
        print('Ayooo')


    #DeRegister Player
    elif clientRequest.find("de register") != -1 and len(clientRequest) > 12:
        print('Ayooo')

    #Invalid Command
    else:
        #Send a message to the Client, informing them of their invalid command
        sendClientMessage(currentClientAddress, "Invalid Command")
#-------------------------------------------------------------------------------