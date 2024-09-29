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



#NEW!!,Server's IPv4 and Port Number


serverSocket = ("128.110.223.4", 31500)
#----------------------------



#Client Functions
#-------------------------------------------------------------------------------------
#Bind the Player/Client to the Server's Socket
player_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



#Send a Message to the server
def sendServerMessage(message):
    #Send message to server
    player_socket.sendto(message.encode('utf-8'), serverSocket)



def closeConnection():
    #Close the socket connection
    player_socket.close()
#-------------------------------------------------------------------------------------




#Global Variables
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------



#Functions
#-------------------------------------------------------------------------------------


#-------------------------------------------------------------------------------------



#Main/Driver Space
#-------------------------------------------------------------------------------

#DEBUG!!
sendServerMessage("No way it works again?!?!?")
closeConnection()
#-------------------------------------------------------------------------------