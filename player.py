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


#Holds the 6 card's dealt to the player, update as we go along...
cardDeck = []     #Make a function that will scrape a player's deck of cards from their deck...


#NEW!!
#Interactable version of 'cardDeck', displayable to player and other players
gameDeck = ["***","***","***","***","***","***"]



#NEW!!!
#Identifier number for the game the player is currently in
gameIdentifier = -1

#Flag that will activate if the player is the dealer
isDealer = False
#--------------------------------------------------------------



#Print and Terminal Functions
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
    print("\n[General Command]: ", end="")


#Game Menu, Once a new game has started they player will see the following menu below
def displayGameInformation(gameInfo):
    print("****************************************************************************************")
    print("*                                   Live Game                                          *")
    print("****************************************************************************************")
    #Section for displaying game information:  
    print("{Game Information}\n")
    #Prints the remaining game information
    print(gameInfo)
#NEW!!!
    #Command for the 'help' print that will display the gameplay command menu...
    print("\n[Display Game Commands via: 'help']")
    print("****************************************************************************************")
    #User-Input Space
    #print("\n[Gameplay Command]: ", end="")
    #Print all of the players in the game


#NEW!!
#Display the [Gameplay Commands] that can be sent to the server (& other players)
def displayGameCommands():
    #Clear the terminal of previous commands, display the help menu (this will clear things up)

    #Linux & Unix terminal clear
    if str(os.name) != 'nt':
        os.system("clear")
    #Windows terminal clear
    else:
        os.system("cls")

    #Print the new set of Commands
    print("****************************************************************************************")
    print("*                                    Help Menu                                         *")
    print("****************************************************************************************")
    print("{Gameplay Commands}\n")
    print("[Shuffle Deck {Dealer Only}]:        shuffle deck\n")
    print("[Deal Cards {Dealer Only}]:          deal cards\n")

    #NEW!!
    print("[Flip Card]:                         flip <card index>\n") #Card index: 0-5  {left -> right}
    print("[Draw Card]:                         draw card\n")
    print("[Message Inbox]:                     inbox")   #Send a Message to other player
    #print("")

    print("[Steal Card]:                        steal card from <playerName>")
    print("****************************************************************************************")
    print("\n[Gameplay Command]: ", end="")


#NEW!!
#Display the Cards of the player and the other players
def displayGame(gameView=None):
    print("\n****************************************************************************************")
    print("*                                    Game Data                                         *")
    print("****************************************************************************************")
    #Prints the game's live stats:  Score, Hole #, Other Player's card decks
    if not gameView is None:
        print(gameView + '\n\n')

    #Print the Player's personal deck (Specified format)
    print("[Your Card Deck]:")
    print(f"\t\t\t\t\t{gameDeck[0]} {gameDeck[1]} {gameDeck[2]}")
    print(f"\t\t\t\t\t{gameDeck[3]} {gameDeck[4]} {gameDeck[5]}")
    print("****************************************************************************************")
    print("\n[Gameplay Command]: ", end="")


#PLACEHOLDER
#    print('Placeholder')



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
        #Gameplay message variable (Local)
        gamePlayMessage = ""

        #[Dealer Message]
        if isDealer and gameStarted:
            #Add the Game-Id
            gamePlayMessage += "[Player-Type]: Dealer\n\n[Game-Id]: " + str(gameIdentifier) + "\n\n[Gameplay Command]: " + message
        #[Player Message]
        else:
            #Contains Game-Id for easier commmand acknowledgement 
            gamePlayMessage += "[Player-Type]: Player\n\n[Game-Id]: " + str(gameIdentifier) + "\n\n[Gameplay Command]: " + message

        #Send the gameplay message to the server
        playerSocket.sendto(gamePlayMessage.encode('utf-8'), serverAddress)
    else:
        #Send Regular Message to Server
        playerSocket.sendto(message.encode('utf-8'), serverAddress)



#User's input
def userInp():
    #Listen for the user's input until the exitFlag has been activated
    while threadsRunning:
        #Collect user's command(s) as a variable so we can check for 'help'
        userInputStr = str(input())

        #If the user has entered the 'help' command, clear the termninal and display the gameplay command menu
        if userInputStr.find('help') != -1:
            #Print the [Gameplay Commands] menu
            displayGameCommands()
        #Else, Send Command to Server 
        else:
            #Send commands to the Server/tracker.py
            sendServerMessage(userInputStr)



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
        if stringResponse.find("[Game Started]: ") != -1 and not gameStarted:
            #Clear the terminal, display game info UI, and allow the player to interact with the game

            #Linux & Unix terminal clear
            if str(os.name) != 'nt':
                os.system("clear")
            #Windows terminal clear
            else:
                os.system("cls")


            #Success message, necessary for grading
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
                gameIdentifier = stringResponse[stringResponse.find("[Game-Id]: ")+11:stringResponse.find("\n\n[Card Dealer]:")]


            #Print the Game Information in a Menu-like format
            displayGameInformation(stringResponse[stringResponse.find("[Game-Id]: "):])
            print('\n[Gameplay Command]: ', end="")



#LEFT OFF:      [10/18/24]

        #[Gameplay Command Branch]
        elif gameStarted:


#STATUS: Unfinished
            #Add Cards to personal deck
            if stringResponse.find("[Dealt Cards]: ") != -1:
                #Use 'eval' to convert the String message to a list (can be done bc of formatting)
                global cardDeck
                global gameDeck

                #If the length of the current card deck is > 6, pop as many cards as we need for 

                cardDeck += eval(stringResponse[stringResponse.find("[Dealt Cards]: ")+15:])

                #Print Response (Doesn't show cards)
                print(f"\nServer Response: Cards have been added to Personal Deck\n\n[Gameplay Command]: ", end="")

                #If the length of the incoming/dealt cards list is == 6, 
                if len(eval(stringResponse[stringResponse.find("[Dealt Cards]: ")+15:])) == 6:
                    #Create/update the player's 'gameDeck' (this is the deck that the player will be able to see)
                    gameDeck[0] = cardDeck[0]
                    gameDeck[1] = cardDeck[1]

                    #Display the game
                    displayGame()
                    
#DEBUG!!!
                    print("Player's card deck: ", cardDeck, "\nGAME DECK!!", gameDeck)


            #End Game
            elif stringResponse.find("[Game Ended]") != -1:
                #Reset all card decks and flags
                cardDeck = []
                gameDeck = []
                gameStarted = False


            #Else, Server response
            else:
                #Print Response
                print(f"\nServer Response: {stringResponse}\n\n[Gameplay Command]: ", end="")
  
        #[Non-Gameplay Commands]
        else:
            #Print the server's response
            print(f"\nServer Response: {stringResponse}\n\n[General Command]: ", end="")    
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