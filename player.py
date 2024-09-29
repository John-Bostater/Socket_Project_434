"""
[Author]: John Bostater

[Socket Group #]: 61

[Start Date]: 9/25/24

[Description]:
    {Client}

    This Python script contains code for the Player to interact with the server and Join ongoing games


[Valid Port Number Range]: 
    31500   to   31999    


[Run Program]:
"""


#Relevant Libaries
#-----------------
import threading
import socket
#-----------------


#Global Variables
#----------------------------
#[Instantiated to default values]

player_socket = 0


#NEW!!,Server's IPv4 and Port Number


serverSocket = ("128.110.223.4", 31500)
#----------------------------



#Client Functions
#-------------------------------------------------------------------------------------

#Send a Message to the Server
def sendServerMessage(message):
    #Send message to Server
    player_socket.sendto(message.encode('utf-8'), serverSocket)


#Receive a Message/Response from the Server
def receiveMessage():
    #DEBUG
    print("Place holder")


#Close the Connection between the Client and the Server
def closeConnection():
    #Close the socket connection
    player_socket.close()
#-------------------------------------------------------------------------------------




#Global Variables
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------



#Functions
#-------------------------------------------------------------------------------------
def displayPlayerGuide():
    print("********************************************************************************")
    print("*                                   Golf                                       *")
    print("********************************************************************************")
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
    
    print("\n{Client functions and their corresponding commands}\n")    
    #Start the game, this command will make the current Player become the dealer
    print("  [Start Game]:                 start game")   
    print("********************************************************************************")
    print("{Command Space}\n")
#-------------------------------------------------------------------------------------



#Main/Driver Space
#-------------------------------------------------------------------------------



#While loop for the player to send messages to the Server!!


#Create a Socket for the Client to communicate over
player_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


#Bind the Player/Client to the Server's Socket



#User can start a game from here via the correct command, "start game", this will make the player running THIS SCRIPT the Dealer
sendServerMessage(str(input("Command To Server: ")))
#-------------------------------------------------------------------------------