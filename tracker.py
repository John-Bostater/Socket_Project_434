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


    - [Registered Player Tuple]:
    
        ["Name", IPv4, t-port, p-port, dealerFlag, inGameFlag]

        {player[0]}                                {player[5]}

       
       ~ dealerFlag =  "dealer" | "player"

       ~ inGameFlag =  "free" | "in-play"


        

[Group 61 Port Number Range]: 
    31500   to   31999


[Usage]:
    python3 tracker.py
    
    OR

    python3 tracker.py <Server IPv4 Address>
        
        //Port number is statically defined in py script

    OR

    python3 tracker.py automatic-set
        
        //This will get the user's IPv4 from eth0 so the user does not have to manually write it out


[Gameplay/Experiment]:
    //Text here...


[TO DO]:
    {10/11/24}

    - USE MULTITHREADING FOR STARTING NEW GAMES, BECAUSE WE WILL HAVE MULTIPLE GAMES RUNNING AT ONCE, OMG!!!

"""


#Relevant Libaries
#------------------
import socket
import random
import sys

#NEW!!
import threading    #Use for running multiple games at once??
#------------------



#Global Variables
#-----------------------------------
#Server Address & Port (Tuple)
serverAddress = (0,0)

#Static value
serverPort = 31500

#Card deck that the Dealer-Player will deal cards from
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
activeGames = []


#Registered Players
registeredPlayers = []


#Client address of the latest message/command
currentClientAddress = 0
#-----------------------------------



#Messaging functions
#-----------------------------------------------------------------------------------------

#Take a single argv statement! 
# python3 tracker.py <IPv4Address>

#[Server --> Player]
#{Communication Port}: t-port

#Send Message to Client (Player) based on their address tuple: (IPv4, Port#)
def sendClientMessage(clientAddress, message):
    #Send a customized message back to the Client via their address tuple: (IPv4, Port#)
    serverSocket.sendto(message.encode('utf-8'), clientAddress)


#[Server --> Player]
#{Communication Port}: t-port
#
#Send Message to Registered Player via their name
def sendRegisteredPlayerMessage(registeredPlayerName, message):
    
    #Parse the registeredPlayers list and send a message to the player via their name
    for player in registeredPlayers:
        #We have found the player we want to send the message to
        if player[0] == registeredPlayerName:        
            #Tuple that contains the player's IPv4 and t-port
            registeredAddress = (player[1], int(player[2]))

            #Send the client a message using our other function
            sendClientMessage(registeredAddress, message)
#-----------------------------------------------------------------------------------------



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

    
    #Complete the player tuple and add it to the registered players list
    newPlayer = (playerName, ipAddress, t_port, p_port, "player", "free")
        #isDealer = False, inActiveGame = False


    #Add the player-tuple to the queued player list
    registeredPlayers.append(newPlayer)

    #Send a message back to the client, "SUCCESS"
    sendClientMessage(currentClientAddress, "SUCCESS")



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
    return [
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
#Main menu of the Server/Tracker (Sets up the scene for displaying incoming messages)
def displayMainMenu():
    print("********************************************************************************")
    print("*                              Golf   [Server-Side]                            *")
    print("********************************************************************************")
    print("{Client Commands/Messages}\n")


#returns T/F as to whether a registered player with 'playerName' exists
def playerIsRegistered(playerName):
    #Parse the registeredPlayers list and return a True if found
    for player in registeredPlayers:
        #If the registered player's name matches that of the playerName parameter
        if player[0] == playerName:
            #playerName IS registered
            return True
    
    #Else, return's false (playerName is NOT registered)
    return False


#returns T/F as to whether the player of 'playerName' is in an active game or not
def playerInActiveGame(playerName):
    #Parse the activeGames tuples and look for a matching name
    for player in activeGames:
        #If the player of "playerName" is in an active game, return True
        if player[0] == playerName:
            #playerName IS registered
            return True
    
    #Else, return's false (playerName is NOT in an active game)
    return False


#Return the number of players NOT in an active game
def numPlayersInActiveGame():
    #Variable to hold the total number of registered players in an active game
    numberOfActivePlayers = 0

    #Parse the 'registeredPlayers' array and check whether the player is in a game
    for player in registeredPlayers:
        #If player is in game, increment counter
        if player[4] == "in-play":
            #Increment the counter of players in an active game
            numberOfActivePlayers += 1

    #Return the number of players actively in a game
    return numberOfActivePlayers
#-------------------------------------------------------------------------------------


#DEBUG FUNCTIONS
#-------------------------------------------------------------------------------------
def showRegPlayers():
    for player in registeredPlayers:
        print(f"{player[0]}, {player[1]}, {player[2]}, {player[3]}, {player[4]}, {player[5]}")
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

    #Client Request variable
    clientRequest = str(message.decode('utf-8'))

    #Print the incoming Client-Command
    print(f'[Client Command]:\t{clientRequest}   from    {currentClientAddress}')


#STATUS: Finished? (double check!)
    #Register Player
    if clientRequest.find("register") != -1 and len(clientRequest) >= 28:
        #Pass the: IPv4, t-port, and p-port
        registerPlayer(clientRequest[9:])

#DEBUG!!
        print('Player list After Register:',registeredPlayers)


#STATUS: Double Check, I think finished??
    #Query Players
    elif clientRequest.find("query players") != -1:
        #Message of the Player Query
        queryMessage = '\n[Number of Registered Players]: ' + str(len(registeredPlayers))

        #Number of register players > 0
        if len(registeredPlayers) > 0:
            #Parse all the Registered Players/Tuples so their info can be printed
            for player in registeredPlayers:
                queryMessage += f"\n  [\"{player[0]}\", {player[1]}, {player[2]}, {player[3]}, {player[4]}, {player[5]}]"
        else:
            #Show empty list
            queryMessage += '\n  []'

        #Send the query of players to the requesting client/current client
        sendClientMessage(currentClientAddress, queryMessage)



#LEFT OFF: [10/14/24]  
    # Make the message sent to the player regarding "gameInfo" look similar to


#STATUS: Unfinished
    #Start Game
    elif clientRequest.find("start game") != -1:
        #Collect the parameters of the 'start game' command
        
        #Updated player tuple (placeholder)
        updatedPlayer = 0


        #Name of the dealer
        cutString = clientRequest[11:]      #Contains: <dealerName> <n> <#holes>
        dealerName = cutString[:cutString.find(' ')]


        #n (Number of players)
        cutString = cutString[(cutString.find(' ')+1):]
        numberOfPlayers = cutString[:cutString.find(' ')]
        #Convert the number of players into a decimal type for later...
        numberOfPlayers = int(numberOfPlayers)


        #Number of Holes
        numberOfHoles = int(cutString[(cutString.find(' ')+1):])


        #Number of Players falls within the appropriate range:  2 <= x <= 4
        #Number og Holes falls within the appropriate range: 1 <= y <= 9
        if playerIsRegistered(dealerName) and not playerInActiveGame(dealerName) and numberOfPlayers >= 2 and numberOfPlayers <= 4 and numberOfHoles >= 1 and numberOfHoles <= 9 and not (numberOfPlayers > len(registeredPlayers)): 
            #Index variable
            dealerIndex = 0


            #Change the dealer player's flags:   
            #       player[4] --> {dealerFlag}     player[5] --> {inGameFlag} 
            for player in registeredPlayers:
      
                #We have found the coinciding dealer's tuple which we will modify
                if player[0] == dealerName:
                    #Update the Dealer's flags and replace the tuple with the new one
                    updatedPlayer = (player[0], player[1], player[2], player[3], "dealer", "in-play")

#ORIGINAL POSITION!!
                    #Send the "Game Started" message to the dealer/player so their player.py script can react accordingly
                    sendRegisteredPlayerMessage(dealerName, ("SUCCESS\nGame Started: dealer\n[Game Id]: " + str(len(activeGames))))

                    #Break the loop                    
                    break
                #Else...
                else:
                    #Increment the index (there is probably a way to do this with less syntax....)
                    dealerIndex += 1


            #Update the dealer's tuple, isDealer[4] = "dealer", inActiveGame[4] = True
            registeredPlayers[dealerIndex] = updatedPlayer


            #Break while-loop once 'numberOfPlayers - 1' players is added
            addedPlayers = 0

            #List of all of the players In the game (including dealer)
            otherPlayers = []


            #Pick <n> more random players from the 'registeredPlayers' array that we will add to the (gameTuple)
            #Inform the randomly picked player that they have been added to a new game 
            #   via: sendRegisteredPlayerMessage
            while True:
                #Generate a random number of the player to be picked via their index # from registeredPlayers list
                randPlayerIndex = random.randint(0, len(registeredPlayers)-1)
                
    #DEBUG!!!
                print("Omg!", addedPlayers, registeredPlayers)

                #NEW!!
                #if len(registeredPlayers)-1 != 0:
                #else:
                    #NEW?!?!?
                 #   break

                #Add random player into the game
                #If the selected player is not already in a game add them to the list 'otherPlayers'
                if registeredPlayers[randPlayerIndex][5] != 'in-play':
                    #Increment the break counter
                    addedPlayers += 1

                    #Update the player's flag, inActiveGame = True  {registeredPlayers[4]}
                    updatedPlayer = (registeredPlayers[randPlayerIndex][0], registeredPlayers[randPlayerIndex][1], registeredPlayers[randPlayerIndex][2], registeredPlayers[randPlayerIndex][3], "player", "in-play")
                    #Update the players tuple
                    registeredPlayers[randPlayerIndex] = updatedPlayer

                    #Add the player to the list 'otherPlayers'
                    otherPlayers.append(registeredPlayers[randPlayerIndex])

                    #Message to be sent
                    gameMessage = "SUCCESS\nGame Started: player\n [Game Id]: " + str(len(activeGames))

                    #Send a special message to the player.. starting a game on the players end
                    sendRegisteredPlayerMessage(registeredPlayers[randPlayerIndex][0], gameMessage)


                #Sufficient number of players added
                elif addedPlayers == (numberOfPlayers - 1):
#NEW!! Position
                    #Send the "Game Started" message to the dealer/player so their player.py script can react accordingly
                   # sendRegisteredPlayerMessage(dealerName, "SUCESS\nGame Started: dealer\n[Game Id]: ")

                    
#NEW GAME TUPLE!!! Add this to the list of active games: activeGames
                    #Add the player list to the new game tuple
                    activeGames.append((len(activeGames), dealerName, otherPlayers))


                    #Break the while loop!
                    break
        else:
            #Player input is incorrect, send FAILURE message
            sendClientMessage(currentClientAddress, "FAILURE")


#STATUS: Finished
    #Query Games
    elif clientRequest.find("query games") != -1:
        #Message of the Player Query
        queryMessage = "\n\n[Number of Ongoing Games]: " + str(len(activeGames)) + "\n"

        #Parse all the Registered Players/Tuples so their info can be printed
        for game in activeGames:
            queryMessage += f"\n[Game Identifier]: {game[0]}\n"

            #For-loop that will add all of the players names to the query message
            #for i in range((len(game))-1):
            #Print all of the tuple elements
            queryMessage += f" \n [Dealer]: {game[1]}\n\n [Players]:\n"
            

            #Parse all of the other players and add their names to the message
            #{game[2][0]}
            for player in game[2]:
                queryMessage += f"\t{player}\n"


        #Send the query of players to the requesting client/current client
        sendClientMessage(currentClientAddress, queryMessage)


#STATUS: Unfinished
    #End Games
    elif clientRequest.find("end") != -1 and len(clientRequest) > 3:
        #Delimiter for breaking apart the clientRequest and getting information
        delimiter = clientRequest.find(" ")+1

        #Get the game identifier from the other half of the client request
        gameId = clientRequest[delimiter:]


        print("Game Id to End!!:", gameId)


#Check that the <player> name entered is actually the Dealer. if not, send: FAILURE


        #print('PlaceHolder')



#Thread testing space
#DEBUG!!
    elif clientRequest.find("debug") != -1 and len(clientRequest) > 3:
        print('PlaceHolder')


#STATUS: Finished??
    #DeRegister Player
    elif clientRequest.find("de register") != -1 and len(clientRequest) > 12:
        #Message for the Client (either: SUCCESS or FAILURE)
        deRegMsg = 'FAILURE'

        #Get the player's name from the string
        deRegName = str(clientRequest[12:])

        #Check if the user is in an ongoing game, if they are, return FAILURE
        #Parse over a copy so we can delete the player from the regular array
        for player in registeredPlayers[:]:
            #Player found, delete the tuple from the list
            if player[0] == deRegName:
                #Delete the player from the list
                registeredPlayers.remove(player)
                
                #Update the message
                deRegMsg = 'SUCCESS'

                #break the loop
                break

        #Inform the Client of either their SUCCESS or FAILURE
        sendClientMessage(currentClientAddress, deRegMsg)


    #Invalid Command
    else:
        #Send a message to the Client, informing them of their invalid command
        sendClientMessage(currentClientAddress, "Invalid Command")
#-------------------------------------------------------------------------------