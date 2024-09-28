"""
[Author]: John Bostater

[Start Date]: 9/25/24

[Description]:
    {Networking Project}

    Server-Python Script, maintains state information of players and ongoing games.
    This file is able to respond to players via a text-based user interface.

    When executing the Tracker Script a paramater for the Port Number must be defined
      [Command]:
        > python3 Tracker.py 123456     //123456 is the port number in this case, add ip paramater?


    This Server contains a fixed IP address and Port Number that the Player's/Player objects
    will use for sending and receiving information about the game
"""


#Relevant Libaries
#-----------------
import socket
from Player import*
#-----------------



#Global Variables
#----------------
#----------------



#Server-Client Functions
#---------------------------

#---------------------------



#Game Functions
#----------------------------

#Add Player
def addPlayer(newPlayer):
    #This function will add a new player to the game

    return '0'


#Remove Player
def removePlayer():
    #This function will remove the player from the game

    return '0' 
#----------------------------



#Main/Driver Space
#----------------------------

#Text Menu for the Player to Start A new Game, Join and Exisitng one, or delete it??
#[Requirements]:
    #Make a Game

    #Join A game



#Make a player object
player0 = CardPlayer()
#----------------------------