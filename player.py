"""
[Author]: John Bostater

[Socket Group #]: 61

[Start Date]: 9/25/24

[Description]:
    {Client}

    This Python script contains code for the Player to interact with the server and Join ongoing games


[Group 61 Port Number Range]: 
    31500   to   31999    


[Usage]:
    (Prompted later: Server IPv4 and Port Number)
    >    python3 player.py <Client IPv4 Address> <Client Port Number>

    (Prompted later...)
    >    python3 player.py
"""


#Relevant Libaries
#-----------------
import threading
import socket

#NEW!!
import sys
#-----------------


#Global Variables
#----------------------------
#Tuple containing Player's entered IPv4 Address and Port Number
#[Example]: playerAddress = ("128.110.223.3", 31501)
playerAddress = (0,0)


#Server's Socket, IPv4 & Port Number
#serverAddress = ("128.110.223.4", 31500)
serverAddress = (0,0)
#----------------------------



#Client Functions
#-------------------------------------------------------------------------------------

#Send a Message to the Server
def sendServerMessage(message):
    #Send message to Server
    playerSocket.sendto(message.encode('utf-8'), serverAddress)


#Receive a Message/Response from the Server
def receiveMessage():
    #DEBUG
    print("Place holder")


#Close the Connection between the Client and the Server
def closeConnection():
    #Close the socket connection
    playerSocket.close()
#-------------------------------------------------------------------------------------



#Functions
#-------------------------------------------------------------------------------------
def displayPlayerGuide():
    print("********************************************************************************")
    print("*                                   Golf                                       *")
    print("********************************************************************************")
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
    print("********************************************************************************")
    print("{Command Space}")


def enterPlayerSock():
    #If the user has not already defined their ipv4 address and port # in the argv[]
    #This function will be called upon to collect that information...
    return 0

    #Enter the Client's Unique Port Number {Give the Specified range}



#-------------------------------------------------------------------------------------



#Main/Driver Space
#-------------------------------------------------------------------------------

#If the user has not entered the relevant information, then don't do anything
if len(sys.argv) == 5:
    #Collect Input and then place into tuple 'playerAddress'
    #playerIPv4 = sys.argv[1]
    #playerPort = int(sys.argv[2])
    playerAddress = (sys.argv[1], int(sys.argv[2]))
    #DEBUG
    print('New Executed!')

    #Server's Address Information
    trackerIPv4 = sys.argv[3]
    trackerPort = int(sys.argv[4])
    serverAddress = (trackerIPv4, trackerPort)

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


#Keep communication running between the Client and server
while True:
    #User can start a game from here via the correct command, "start game", this will make the player running THIS SCRIPT the Dealer
    sendServerMessage(str(input("\nCommand To Server: ")))

    #Receive response from Server
    serverResponse, serverAddress = playerSocket.recvfrom(1024)

    #Print the server's response
    print(f"Server Response: {serverResponse.decode('utf-8')}")
#-------------------------------------------------------------------------------