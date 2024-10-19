"""
[Author]: John Bostater

[Socket Group #]: 61

[Start Date]: 9/25/24

[Description]:
    {Client}

    This Python script contains code for the Player to interact with the server and Join ongoing games

    Once a game has been started by a player, a message will be sent to all Players of the game that will
    clear the menu via a system command and start listening on the:      [p-port]    
    This is so that the player can interact with the game.

    The player/client script is able to both listen for messages from players and the server as well as send the via threading.
    Once the player has decided to end their session with the script, they can initiate a clean exit from the server via the command: "exit"

    
[Group 61 Port Number Range]: 
    31500   to   31999    


[Usage]:
    python3 player.py
    
    OR

    python3 player.py <Client IPv4 Address> <Client Port Number> <Server IPv4 Address> <Server Port Number>

    OR

    python3 player.py     
"""


#Relevant Libaries
#--------------------------------------------
import socket
import sys
import threading
import os
  #Used for clearing terminal and quick usage
#--------------------------------------------


#Global Variables
#--------------------------------------------------------------
#Tuple containing Player's entered IPv4 Address and Port Number
#[Example]: playerAddress = ("128.110.223.3", 31501)
playerAddress = (0,0)


#Server's Socket, IPv4 & Port Number
#serverAddress = ("128.110.223.4", 31500)
serverAddress = (0,0)

#Response converted to a string
stringResponse = ""

#Flag the allows the threads to run as well as stop them
threadsRunning = False

#Used for one-time print (so far...)
gameStarted = False



#NEW!!!
#Hold's the message containing information of the current game the player is in
#gameInfoMessage = ""

#NEW!!
#Hold's the player's personal card deck
cardDeck = []     #Make a function that will scrape a player's deck of cards from their deck...

#NEW!!!
#Identifier number for the game the player is currently in
gameIdentifier = -1

#Flag that will activate if the player is the dealer
isDealer = False
#--------------------------------------------------------------



#Print Functions
#-------------------------------------------------------------------------------------------------------
#Main/First Menu the player see's, this is for interacting with pre-game functions as seen below...
def displayPlayerGuide():
    print("****************************************************************************************")
    print("*                                       Golf                                           *")
    print("****************************************************************************************")
    #Client's Address
    print("{Client Address}:", playerAddress, '\n')

    #Commands to server for setting up games and viewing other information...
    print("{Server Commands}\n")
    #Register the player
    print("  [Register Player]:                 register <Player Name> <IPv4> <t-port> <p-port>\n")   
    #Returns number of players registered
    print("  [Query Registered Players]:        query players\n")
    print("  [Start Game]:                      start game <dealer's name> <n> <# holes>\n")     
    #Return the # of ongoing games, with game-identifier and the current dealer's name of that game
    print("  [Query Games]:                     query games\n") 
    #End the specified game
    print("  [End Games]:                       end <game-identifier> <dealer's name>\n")
    print("  [DeRegister Player]:               de register <player>\n")
    print("[Note]: Replace the parameters delimited by the chevrons with the relevant data")    
    #Start the game, this command will make the current Player become the dealer
    print("****************************************************************************************")
    print("{Command Space}")
    print("\nCommand to the Server: ", end="")


#Game Menu, Once a new game has started they player will see the following menu below
def displayGame(gameInfo):
    print("****************************************************************************************")
    print("*                                   Live Game                                          *")
    print("****************************************************************************************")
    #Section for displaying game information:  
    print("{Game Commands}\n")
    print("  [Deal Cards]:      deal\n")
    print("  []:      deal")
    print("****************************************************************************************")
    #Section for displaying game information:  
    print("{Game Information}\n")
    print(gameInfo)
    print("****************************************************************************************")
    #User-Input Space
    #print("\n[Gameplay Command]: ", end="")
    #Print all of the players in the game


#NEW!!
#Display the players



#NEW!!  (unecessary??)
#Display the Messages between Players
def playerInbox():
    #Placeholder
    print('placeholder')
#-------------------------------------------------------------------------------------------------------



#Client/Player Functions
#-------------------------------------------------------------------------------------
#Send a Message to the Server
def sendServerMessage(message):
    #Send Gameplay Message to the Server, if theplayer is in an active game
    if gameStarted:
        #Gameplay message variable
        gamePlayMessage = ""

        #If the player is also the dealer, include the game-identifier in the message
        if isDealer:
            #Add the game-identifier
            gamePlayMessage += ("[Game-Id]: " + str(gameIdentifier) + "\n\n")

        #Complete the message
        gamePlayMessage += "[Gameplay Command]: " + message

        #Send the gameplay message to the server
        playerSocket.sendto(gamePlayMessage.encode('utf-8'), serverAddress)
    else:
        #Send Regular Message to Server
        playerSocket.sendto(message.encode('utf-8'), serverAddress)



#User's input
def userInp():
    #Listen for the user's input until the exitFlag has been activated
    while threadsRunning:
        #Send commands to the Server/tracker.py
        sendServerMessage(str(input()))


#Handle Server Responses as a Client/Player
def servResp():
    #Set up the gameStarted flag as a global variable so our re-def does not break
    global gameStarted

    #Listen for the server's response until the exitFlag has been activated
    while threadsRunning:
        #Receive response from Server
        serverResponse, serverAddress = playerSocket.recvfrom(1024)

        #stringResponse
        stringResponse = serverResponse.decode('utf-8')
        

        #Game Started, user has been joined into a game
        if stringResponse.find("[Game Started]: ") != -1:
            #Clear the terminal, display game info UI, and allow the player to interact with the game

            #Linux & Unix terminal clear
            if str(os.name) != 'nt':
                os.system("clear")
            #Windows terminal clear
            else:
                os.system("cls")


            #Print a One-time success message to the Player, as their game has started
            if not gameStarted:
                #Success message
                print("\nServer Response:", serverResponse.decode('utf-8')[:serverResponse.decode('utf-8').find("\n")])

                #Update the flag (we can now listen for gameplay control messages)
                gameStarted = True

                #Player is Dealer Check...
                if stringResponse.find("[Game Started]: dealer") != -1:
                    #Update the player's personal 'isDealer' flag
                    global isDealer     #Make the flag global too!
                    isDealer = True

                    #Gather the game identifier
                    global gameIdentifier
                    gameIdentifier = stringResponse[stringResponse.find("[Game-Id]: "):stringResponse.find("\n\n[Card Dealer]:")]


            #Print the Game Information in a Menu-like format
            displayGame(stringResponse[stringResponse.find("[Game Started]: "):])
            print('\n[Gameplay Command]: ', end="")





#LEFT OFF:      [10/18/24]

        #[Gameplay Commands] branch
        if gameStarted:
            #Update to the players card-deck (dealt 6 cards, steal card from other player, new card deck, etc...)
            #Message: [Card-Deck Update]: //Information

            #Within this branch, we are listening for GamePlay Commands


    #Send a message to the server to deal cards to all of the players in the game
    #Confirm the dealer on 'tracker.py' end via:    ipv4 and t-port
                #player[4] == 'dealer'
                #       AND
                #player[1]


            #Add Cards to card deck     [Dealt cards    or      'Steal']
            if stringResponse.find("[Dealt Cards]: ") != -1:
                #Collect the cards from the string response and add them to the player's cardDeck list
                #Parse through the response and collect all of the '[Dealt Card]: ' encountered

                #Gather the starting index (cards will follow and be separated with ",")
                delimiter = stringResponse.find("[Dealt Cards]: ")+15


                #Use a delimiter so we can break apart the string!! via: find('[Dealt Card]: ')
                while True:
                    
                    #If the delimiter returns -1 end the gather loop
                    if delimiter == -1:
                        #Break the while-loop
                        break

                    #Else, collect the card from the string and add the card to the deck
                    cardDeck.append(stringResponse[delimiter:stringResponse.find(",")])

                    #Update the delimiter
                    delimiter = stringResponse.find(",")

                    #Update the stringResponse (trim the collected cards)

            
#DEBUG!!!
                print("Player's card deck: ", cardDeck)

  


        #[Non-Gameplay Commands]
        if not gameStarted:
            #Print the server's response
            print(f"\nServer Response: {serverResponse.decode('utf-8')}" + "\n\nCommand to the Server: ", end="")    
#-------------------------------------------------------------------------------------



#Main/Driver Space
#-------------------------------------------------------------------------------

#If the user has not entered the relevant information, then don't do anything
if len(sys.argv) == 5:
    #Player's Address Info
    playerAddress = (sys.argv[1], int(sys.argv[2]))
    
    #Server's Address Information
    serverAddress = (sys.argv[3], int(sys.argv[4]))

else:
    #Manually collect the Player's IPv4 and Port
    #Collect IPv4
    tmpIPv4 = input("Your IPv4: ")
    
    #Collect Port
    tmpPort = input("Your Port #: ")

    #Enter the Client's IPv4 Address (found via: ifconfig eth0, eth1, etc.)
    playerAddress = (tmpIPv4, int(tmpPort))

    #Collect IPv4
    tmp0IPv4 = input("Server IPv4: ")
    tmp0Port = input("Server Port: ")

    #Enter the Server's IPv4 Address 
    serverAddress = (tmp0IPv4, tmp0Port)

    #DEBBUG
    print('Result:', playerAddress, serverAddress)


#Create a Socket for the Client to communicate over
playerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


#Bind the Player socket to the Player's unique IPv4 and Port #
playerSocket.bind(playerAddress)


#Print the Command Menu/Main Menu
displayPlayerGuide()


#Later on....
#May need a new thread for player to player responses??


#Threads
userInputThread = threading.Thread(target=userInp)
serverResponse = threading.Thread(target=servResp)

#Update the flag so the threads can run indefinitely until prompted to stop
threadsRunning = True

#Start the threads
userInputThread.start()
serverResponse.start()
#-------------------------------------------------------------------------------