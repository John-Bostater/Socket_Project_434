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


#New!!
#Flag the allows the threads to run as well as stop them
threadsRunning = False


#NEW!!!
#Used for one-time print (so far...)
gameStarted = False


#NEW!!!


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
    #Register the player
    print("  [Register Player]:                 register <Player Name> <IPv4> <t-port> <p-port>\n")   
    #Returns number of players registered
    print("  [Query Registered Players]:        query players\n")
    print("  [Start Game]:                      start game <Card Dealer Player's Name> <n> <# holes>\n")     
    #Return the # of ongoing games, with game-identifier and the current dealer's name of that game
    print("  [Query Games]:                     query games\n") 
    #End the specified game
    print("  [End Games]:                       end <game-identifier> <Card Dealer Player's Name>\n")
    print("  [DeRegister Player]:               de register <player>\n")
    print("[Note]: Replace the parameters delimited by the chevrons with the relevant data")    
    #Start the game, this command will make the current Player become the dealer
    print("****************************************************************************************")
    print("{Command Space}")
    print("\nCommand to the Server: ", end="")


#Game Menu, Once a new game has started they player will see the following menu below
def displayGame(gameId):
    print("****************************************************************************************")
    print("*                                   Live Game                                          *")
    print("****************************************************************************************")
    print("{Game Identifier}:", gameId)
    print("\n{Players in Game}:")
    print("\n{Number of Holes}:")
    #Parse all of the players in the game (find game via the game Id) and print their names!!

    print("****************************************************************************************")
    #User-Input Space
    print("\n[Gameplay Command]: ", end="")
    #Print all of the players in the game


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
    #Send message to Server
    playerSocket.sendto(message.encode('utf-8'), serverAddress)


#User's input
def userInp():
    #Listen for the user's input until the exitFlag has been activated
    while threadsRunning:
        #Send commands to the Server/tracker.py
        sendServerMessage(str(input()))


#Print and handle server responses
def servResp():
    #Set up the gameStarted flag as a global variable so our re-def does not break
    global gameStarted

    #Listen for the server's response until the exitFlag has been activated
    while threadsRunning:
        #Receive response from Server
        serverResponse, serverAddress = playerSocket.recvfrom(1024)

        #stringResponse
        stringResponse = str(serverResponse.decode('utf-8'))
        

        #Game Started, user has been joined into a game
        if stringResponse.find("Game Started: ") != -1:
            #Clear the terminal, display game info UI, and allow the player to interact with the game

            #Linux & Unix terminal clear
            if str(os.name) != 'nt':
                os.system("clear")
            #Windows terminal clear
            else:
                os.system("cls")

            #Collect the Game-Id of the user's game
            gameIdentifier = stringResponse[(stringResponse.find("[Game Id]:")+11):stringResponse.find("\n[Players in Game]:")]

        #Collect the 
#Collect other information below: (Players in Game {use /t for parsed lines?})


            #Print a One-time success message to the Player, as their game has started
            if not gameStarted:
                #Success message
                print("\nServer Response:", serverResponse.decode('utf-8')[:serverResponse.decode('utf-8').find("\n")])

                #Update the flag
                #global gameStarted
                gameStarted = True


            #Print the Game Information
            displayGame(gameIdentifier)


            #Start a thread for the active game that will listen on p-port?


#DEBUG!!!
            #Print the game started message (contains game info!)
            print('!!!!!GAME STARTED MESSAGE\n\n' + stringResponse)


        else:
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