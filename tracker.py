"""
[Author]: John Bostater

[Socket Group #]: 61

[Start Date]: 9/25/24

[Description]:
    {Server}

    Server Python Script, maintains state information of players and ongoing games.
    This file is able to respond to players via a text-based user interface.

    This Server contains a fixed IP address and Port Number that the Player's/Player objects
    will use for sending and receiving information about the game.

    
[Group 61 Port Number Range]: 
    31500   to   31999


[Usage]:
    python3 tracker.py
    
    OR

    python3 tracker.py <Server IPv4 Address> <Server Port Number>


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
import sys
#------------------



#Global Variables
#-----------------------------------
#Server Address & Port (Tuple)
serverAddress = (0,0)

#Static value
serverPort = 31500

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


#Registered Players
registeredPlayers = []


#Client address of the latest message/command
currentClientAddress = 0
#-----------------------------------



#Server-Client Functions
#---------------------------

#Take a single argv statement! 
# python3 tracker.py <IPv4Address>

#Send Message to Client (Player)
def sendClientMessage(clientAddress, message):
    #Send a customized message back to the Client via their address tuple: (IPv4, Port#)
    serverSocket.sendto(message.encode('utf-8'), clientAddress)
#---------------------------



#Game Functions
#-------------------------------------------------------------------------------------
#Add Player
def registerPlayer(playerInfo):
    #Delimeter for gathering relevant command info
    delimeter = playerInfo.find(' ')

    #Place the newly made player 'tuple' into the tuple list for players waiting to queue?
    #Register a new player for the query    

    #Name
    playerName = playerInfo[0:delimeter]    
    

    #Break function here if the playerName already exists within the registered players
    for player in registeredPlayers:
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
    #The server will use this port to talk back to the Client/Player

    #Update the given string and the delimeter
    playerInfo = playerInfo[(delimeter+1):]
    delimeter = playerInfo.find(' ')


    #p-port
    p_port = playerInfo
    #Port for Communication between Player and Player

    #Dealer Flag 
    dealerFlag = False


    #Complete the player tuple and add it to the registered players list
    newPlayer = (playerName, ipAddress, t_port, p_port, dealerFlag)


    #Add the player-tuple to the queued player list
    registeredPlayers.append(newPlayer)


    #Send a message back to the client, "SUCCESS"
    sendClientMessage(currentClientAddress, "SUCCESS")


    return 'SUCCESS'


#Remove Player
def de_RegisterPlayer(selectedPlayer):
    #This function will remove the player from the game

    return '0'


#Deal Cards [Dealer Only]
def dealCards():
    #If the Player is the dealer, proceed
    #if self.dealer:
    
    #Deal each player 6 cards
    for players in registeredPlayers:

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
#Collect the Server IPv4 Address and Port Number, which will be [31500] for my group

#Check if the user has added IPv4 in their command line argument
if len(sys.argv) == 2:
    #Update the Server's address to contain 
    serverAddress = (sys.argv[1], serverPort)
else:
    #Make the user input the servers IPv4 manually
    serverAddress = (str(input("Enter the Tracker/Server's IPv4 Address: ")), serverPort)

#Bind the server to the first available port, 31500

#Create UDP Socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Bind the Server's Socket
serverSocket.bind(serverAddress)


#Display the menu with the relevant Commands for the player to interact with the Server/Tracker
displayMainMenu()


#While-loop that will run forever to take in commands for server manipulation
while True:
    #Receive a Message/Request from the Client
    message, currentClientAddress = serverSocket.recvfrom(1024)
    #print(f"Received Message from Client: {message.decode('utf-8')} from {currentClientAddress}")


    #Client Request variable 
    clientRequest = str(message.decode('utf-8'))

    #Print the incoming Client-Command
    print(f'[Client Command]:\t{clientRequest}   from    {currentClientAddress}')


#STATUS: COMPLETE
    #Register Player
    if clientRequest.find("register") != -1 and len(clientRequest) >= 28:
        #Pass the: IPv4, t-port, and p-port
        registerPlayer(clientRequest[9:])

        #DEBUG!!
        print('Player list After Register:',registeredPlayers)


#STATUS: COMPLETE
    #Query Players
    elif clientRequest.find("query players") != -1:
        #Message of the Player Query
        queryMessage = '\n[Number of Registered Players]: ' + str(len(registeredPlayers))

        #Number of register players > 0
        if len(registeredPlayers) > 0:
            #Parse all the Registered Players/Tuples so their info can be printed
            for player in registeredPlayers:
                queryMessage += f"\n  [\"{player[0]}\", {player[1]}, {player[2]}, {player[3]}, {player[4]}]"
        else:
            #Show empty list
            queryMessage += '\n  []'

        #Send the query of players to the requesting client/current client
        sendClientMessage(currentClientAddress, queryMessage)


    #Start Game
    elif clientRequest.find("start game") != -1:
        print('yes kay!')


#STATUS: INCOMPLETE
    #Query Games
    elif clientRequest.find("query games") != -1:
        #Message of the Player Query
        queryMessage = '\n[Number of Ongoing Games]: ' + str(len(runningGames))

        #Parse all the Registered Players/Tuples so their info can be printed
        for game in runningGames:
            queryMessage += f"\n  [\"{player[0]}\", {player[1]}, {player[2]}, {player[3]}, {player[4]}]"

        #Send the query of players to the requesting client/current client
        sendClientMessage(currentClientAddress, queryMessage)


    #End Games
    elif clientRequest.find("end") != -1 and len(clientRequest) > 3:
        print('Ayooo')


#STATUS: INCOMPLETE
    #DeRegister Player
    elif clientRequest.find("de register") != -1 and len(clientRequest) > 12:
        print('Ayooo')


    #Invalid Command
    else:
        #Send a message to the Client, informing them of their invalid command
        sendClientMessage(currentClientAddress, "Invalid Command")
#-------------------------------------------------------------------------------