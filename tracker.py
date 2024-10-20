"""
[Author]: John Bostater

[Socket Group #]: 61

[Start Date]: 9/25/24

[Description]:
    {Server}

    Server Python Script 
    Maintains state information of players and ongoing games.
    This file is interactable via a text-based User-Interface.

    This Server contains a fixed IP address and Port Number that the Player's/Player objects
    will use for sending and receiving information about the game.


    - [Registered Player Tuple]:
    
        ["Name", IPv4, t-port, p-port, dealerFlag, inGameFlag]

        {player[0]}                                {player[5]}

        
        <dealerFlag> =  "dealer" | "player"

        <inGameFlag> =  "free" | "in-play"


        
    - [Active Game Dictionary]:

        {Game-Id: <id#>}:   [<mainDeck[]>, <discardDeck[]>, <playerScores[]>, <hole #>, <total holes>]

        

[Group 61 Port Number Range]: 
    31500   to   31999


[Usage]:    //Port # is statically defined in script

    python3 tracker.py
    
            OR

    python3 tracker.py <Server IPv4 Address>       
        
            OR

    python3 tracker.py automatic-set    
        //This will get the user's IPv4 from eth0 so the user does not have to manually write it out

"""


#Relevant Libaries
#------------------
import socket
import random
import sys
#------------------



#Global Variables
#--------------------------------------------------------------------------------------------------------------#Server Address & Port (Tuple)
serverAddress = (0,0)

#Static value
serverPort = 31500

#Card deck that will be used as a reference for the card deck created for a game
referenceDeck = [
    #Clubs
    "AC", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C", "JC", "QC", "KC",

    #Spades
    "AS", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "JS", "QS", "KS",

    #Hearts
    "AH", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "JH", "QH", "KH",

    #Diamonds
    "AD", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D", "JD", "QD", "KD"
]

#Registered Players
registeredPlayers = []


#Dictionary (HashMap) of all Games in Progress,  Game-Id, Dealer, Players, Number of Holes
gamesList = {}


#Running game information
activeGames = {}


#Every In-Game player's card deck
playerDecks = {}    # 'Name-GameId': <playerDeck[]> 
#                         Key       :     Data


#Card Deck used in the player's game, displays the flipped cards
playerGameDecks = {}


#Client address of the latest message/command
currentClientAddress = 0
#--------------------------------------------------------------------------------------------------------------



#Messaging functions
#-----------------------------------------------------------------------------------------
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

    #Player's name
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
def dealCards(gameIdentifier):
    #Deal 6 cards to the dealer first
    for i in range(6):
        #Gather card from the Deck used by the game
        hold = activeGames[f"Game-Id: {gameIdentifier}"][0].pop()


        #Pop a card from the game's unique and shuffled deck    
        playerDecks[f"{gamesList[f'Game-Id: {gameIdentifier}'][1]}-{gameIdentifier}"].append(hold)


    #Deal 6 cards to every other player's deck
    for i in range((len(gamesList[f"Game-Id: {gameIdentifier}"][2])) * 6):
        #Gather card from the Deck used by the game
        hold = activeGames[f"Game-Id: {gameIdentifier}"][0].pop()

        #Pop the card from the game's unique deck, interchange player every 1 card dealt
        playerDecks[f"{gamesList[f'Game-Id: {gameIdentifier}'][2][i % (len(gamesList[f'Game-Id: {gameIdentifier}'][2]))][0]}-{gameIdentifier}"].append(hold)


    #Pop one card from the stack and place it into the discard pile
    activeGames[f"Game-Id: {gameIdentifier}"][1].append(activeGames[f"Game-Id: {gameIdentifier}"][0].pop())

    #String containing the game information which will be sent to every player and displayed on the players end
    gameInfoStr = activeGameInfo(gameIdentifier)


    #Send the Dealer their Card Deck
    sendRegisteredPlayerMessage(gamesList[f"Game-Id: {gameIdentifier}"][1], message=(gameInfoStr + "\n\n[Dealt Cards]: " + str(playerDecks[f"{gamesList[f'Game-Id: {gameIdentifier}'][1]}-{gameIdentifier}"])))

    #flip two cards (i.e. create a new gameDeck for the player which will start like: 'AS 7D ***'  ... for example)
    playerGameDecks[f"{gamesList[f'Game-Id: {gameIdentifier}'][1]}-{gameIdentifier}"] = [str(playerDecks[f"{gamesList[f'Game-Id: {gameIdentifier}'][1]}-{gameIdentifier}"][0]), str(playerDecks[f"{gamesList[f'Game-Id: {gameIdentifier}'][1]}-{gameIdentifier}"][1]), "***", "***", "***", "***"]

    #Send the other players their Card Deck
    for player in gamesList[f"Game-Id: {gameIdentifier}"][2]:
        sendRegisteredPlayerMessage(player[0], message=(gameInfoStr + "\n\n[Dealt Cards]: " + str(playerDecks[f"{player[0]}-{gameIdentifier}"])))

  
#DEBUG!!
    print("Active Games\n", activeGames)



#Shuffle the deck
def shuffleDeck(gameIdentifier):
    #Deck that will be "shuffled"/created for the game  @game-identifier
    shuffledDeck = []

    #get the reference deck ready for use
    global referenceDeck

    #Shuffle/Create the new 52 card deck as a shuffling/rng of the reference deck
    for i in range(52):
        #Randomly generate a number that will correspond to a card in the deck       
        shuffleNum = random.randint(0, len(referenceDeck)-1)

        #Add the cards to the players deck
        shuffledDeck.append(referenceDeck[shuffleNum])

        #Remove the pulled card from the reference deck
        del referenceDeck[shuffleNum]


    #Reset the reference deck!
    referenceDeck = resetDeck()

    #Add the new deck to the Active Game pile too
    activeGames[f"Game-Id: {gameIdentifier}"][0] = shuffledDeck

    
    #Send a Success message to the dealer
    sendRegisteredPlayerMessage(gamesList[f"Game-Id: {gameIdentifier}"][1], "SUCCESS")



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


#Return the Active game info of 'game Identifier' as a string (used in deal cards) and (draw/after player's turn) 
def activeGameInfo(gameIdent):
    #Game Info String
    gameInf = ("[Hole #]: " + str(activeGames[f"Game-Id: {gameIdent}"][3]) + "\t[Out of]: " + str(activeGames[f"Game-Id: {gameIdent}"][4]))
    gameInf += "\n\n[Discard Pile]: " + str(activeGames[f"Game-Id: {gameIdent}"][1]) + "\n\n[Scores]: " 

    #Add every player's deck and score
    #for player in activeGames[f"Game-Id: {gameIdent}"]

    return gameInf
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


    #Register Player
    if clientRequest.find("register") != -1 and len(clientRequest) >= 28:
        #Pass the: IPv4, t-port, and p-port
        registerPlayer(clientRequest[9:])


    #Query Players
    elif clientRequest.find("query players") != -1:
        #Message of the Player Query
        queryMessage = '\n[Number of Registered Players]: ' + str(len(registeredPlayers))

        #Number of register players > 0
        if len(registeredPlayers) > 0:
            #Parse all the Registered Players/Tuples so their info can be printed
            for player in registeredPlayers:
                #Add the players information to the queryMessage
                queryMessage += f"\n\t{player}"
        else:
            #Show empty list
            queryMessage += '\n\t[]'

        #Send the query of players to the requesting client/current client
        sendClientMessage(currentClientAddress, queryMessage)



    #Start Game
    elif clientRequest.find("start game") != -1:
        #Collect the parameters of the 'start game' command
        
        #Updated player tuple (placeholder)
        updatedPlayer = 0

        #Name of the dealer
        cutString = clientRequest[11:]      #Contains: <dealerName> <n> <#holes>
        dealerName = str(cutString[:cutString.find(' ')])

        #n (Number of players)
        cutString = cutString[(cutString.find(' ')+1):]
        numberOfPlayers = cutString[:cutString.find(' ')]
        #Convert the number of players into a decimal type for later...
        numberOfPlayers = int(numberOfPlayers)

        #Number of Holes
        numberOfHoles = int(cutString[(cutString.find(' ')+1):])

        #Messages containing game information that will be compiled and sent to the player and dealer
        global messageToPlayer
        global messageToDealer
        messageToDealer = ""
        messageToPlayer = ""


        #Number of Players falls within the appropriate range:  2 <= x <= 4
        #Number og Holes falls within the appropriate range: 1 <= y <= 9
        if playerIsRegistered(dealerName) and numberOfPlayers >= 2 and numberOfPlayers <= 4 and numberOfHoles >= 1 and numberOfHoles <= 9 and not (numberOfPlayers > len(registeredPlayers)): 
            #Index variable
            dealerIndex = 0

            #Change the dealer player's flags:   
            #       player[4] --> {dealerFlag}     player[5] --> {inGameFlag} 
            for player in registeredPlayers:
      
                #Dealer Found
                #We have found the coinciding dealer's tuple which we will modify
                if player[0] == dealerName:
                    #Update the Dealer's flags and replace the tuple with the new one
                    updatedPlayer = (player[0], player[1], player[2], player[3], "dealer", "in-play")

                    #Build the message to be sent to the Dealer
                    messageToDealer = "SUCESSS\n\n[Game Started]: dealer\n\n[Game-Id]: " + str(len(gamesList)) + "\n\n[Card Dealer]: " + dealerName + "\n\n[Players in Game]:\n"

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

                    #Message to be sent to the Player(s)
                    messageToPlayer = "SUCCESS\n[Game Started]: player\n[Game-Id]: " + str(len(gamesList))  + "\n\n[Dealer]: " + dealerName + "\n\n[Players in Game]:\n"

                 
                #Sufficient number of players added
                if addedPlayers == numberOfPlayers-1:
                    #Create the new game tuple
                    #Add the player list to the new game tuple
                    gamesList[f"Game-Id: {len(gamesList)}"] = (len(gamesList), dealerName, otherPlayers)


                    #Parse the 'otherPlayers' list and compile a message to send to the dealer and other players
                    for player in otherPlayers:
                        #Add the player's information to both messages
                        messageToPlayer += f"\t{player}\n"
                        messageToDealer += f"\t{player}\n"

                    #Add the number of holes to each message, then add [End of Message] to help stop parsing
                    messageToDealer += "\n[Number of Holes]: " + str(numberOfHoles)
                    messageToPlayer += "\n[Number of Holes]: " + str(numberOfHoles)


                    #Send the "Game Started" message to all players (non-dealer)
                    for player in otherPlayers:
                        #Other Players Message
                        sendRegisteredPlayerMessage(player[0], messageToPlayer)
                        
                        #Instantiate a new Card-Deck for the Player:    
                        playerDecks[f"{player[0]}-{len(gamesList)-1}"] = []
                        #     format   {player-gameId}:  <cardDeckList[]>


                    #Dealer "Game Started" Message
                    sendRegisteredPlayerMessage(dealerName, messageToDealer)
                    #Instantiate a new Card-Deck for the Dealer:    
                    playerDecks[f"{dealerName}-{len(gamesList)-1}"] = []


                    #Instantiate a new game in activeGames,     Tracking stats
                    activeGames[f"Game-Id: {len(gamesList)-1}"] = [[], [], {}, 1, numberOfHoles]


                    #Add each player's score @ activeGames[2]
                    #Dealer
                    activeGames[f"Game-Id: {len(gamesList)-1}"]

                    #Other players..
                    for player in gamesList[f'Game-Id: {len(gamesList)-1}'][2]:
                        #Instantiate the players score for the active game
                        activeGames[f"Game-Id: {len(gamesList)-1}"][2][f'{player[0]}-{len(gamesList)-1}'] = 0


                    #Break the while loop!
                    break
        else:
            #Player input is incorrect, send FAILURE message
            sendClientMessage(currentClientAddress, "FAILURE")


    #Query Games
    elif clientRequest.find("query games") != -1:
        #Message of the Player Query
        queryMessage = "\n\n[Number of Ongoing Games]: " + str(len(gamesList)) + "\n"

        #Parse all the Registered Players/Tuples so their info can be printed
        for i in range(len(gamesList)):
            queryMessage += f"\n[Game-Id]: {i}\n"

            #Print all of the tuple elements
            queryMessage += f"\n[Dealer]: {gamesList[f'Game-Id: {i}'][1]}\n\n[Other Players]:\n"            

            #Parse all of the other players and add their names to the message
            for j in range(len(gamesList[f"Game-Id: {i}"][2])):
                queryMessage += f"\t{gamesList[f'Game-Id: {i}'][2][j]}\n"


        #Send the query of players to the requesting client/current client
        sendClientMessage(currentClientAddress, queryMessage)


#LEFT OFF:

    #End Games
    elif clientRequest.find("end") != -1 and len(clientRequest) > 3:
        #Gathered info string variable
        gatheredInfo = clientRequest[clientRequest.find("end"):]
  
        #Gather info via a string, user split to gather indexed information between " ", dealer name @[2]
        gatheredInfo = gatheredInfo.split()
  
        #Send success message to the Dealer
        sendRegisteredPlayerMessage(gatheredInfo[2], message="[Game Ended]\nSUCCESSS")
        
        #Send success message to every player of the game
        for player in gamesList[f"Game-Id: {gatheredInfo[1]}"][2]:
            #Update the player's tuple
            for regPlayer in registeredPlayers:
                #Found the tuple we want to replace/update
                if regPlayer[0] == player[0]:
                    #Replace the tuple
                    regPlayer = (regPlayer[0], regPlayer[1], regPlayer[2], regPlayer[3], regPlayer[4], 'free')


            #Send success message
            sendRegisteredPlayerMessage(player[0], message="[Game Ended]\nSUCCESSS")

        #Delete the game vai its id
        del gamesList[f"Game-Id: {gatheredInfo[1]}"]
        del activeGames[f"Game-Id: {gatheredInfo[1]}"]


    #DeRegister Player
    elif clientRequest.find("de register") != -1 and len(clientRequest) > 12:
        #Message for the Client (either: SUCCESS or FAILURE)
        deRegMsg = 'FAILURE'

        #Get the player's name from the string
        deRegName = str(clientRequest[12:])

        #Check if the user is in an ongoing game, if they are, return FAILURE
        #Parse over a copy so we can delete the player from the regular array
        for player in registeredPlayers:
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


    #Allocate this area of the script for gameplay commands //just to be better organized
    elif clientRequest.find("[Gameplay Command]: ") != -1:
    #NOTE (Delete later...)
        #We use [Player Type]: <Dealer> | <Player>  This matters because messages from either should include [Game-Id] to make things easier down the road...

        #Shuffle Cards  [Dealer Only]
        if clientRequest.find("shuffle deck") != -1 and clientRequest.find("[Player-Type]: Dealer") != -1:
            #Get the client's address from the incoming message
            for player in registeredPlayers:
                #If the player is the dealer and in an active game, allow the shuffling of cards!!
                if player[1] == currentClientAddress[0] and player[2] == str(currentClientAddress[1]) and player[4] == "dealer" and player[5] == "in-play":
                    #Shuffle the card deck, use the Game-Id
                    shuffleDeck(clientRequest[clientRequest.find("[Game-Id]:")+11:clientRequest.find("\n\n[Gameplay Command]")])

                    #break the for-loop
                    break


        #Deal Cards  [Dealer Only]
        #Use the created card deck to pop off cards from the top (pop card and deal to player)
        elif clientRequest.find("deal cards") != -1 and clientRequest.find("[Player-Type]: Dealer") != -1:
            #Get the incoming current client's address
            for player in registeredPlayers:
                if player[1] == currentClientAddress[0] and player[2] == str(currentClientAddress[1]) and player[4] == "dealer" and player[5] == "in-play":
                    #Dealer has initiated the "dealCards" function!!, call upon the function to do so
                    dealCards(clientRequest[clientRequest.find("[Game-Id]:")+11:clientRequest.find("\n\n[Gameplay Command]")])
                    
                    #Break the for loop (every player has been given their deck and messaged!)
                    break


        #Draw a card from the chosen deck
        elif clientRequest.find("draw") != -1:
            #Pop from the specified deck and send it to the current Client address...
            #card = cleint

        #PLACEHOLDER!
            print('Placeholder')

        
        #Invalid Command
        else:
            #Send a message to the Client, informing them of their invalid command
            sendClientMessage(currentClientAddress, "Invalid Command")


    #Invalid Command
    else:
        #Send a message to the Client, informing them of their invalid command
        sendClientMessage(currentClientAddress, "Invalid Command")
#-------------------------------------------------------------------------------