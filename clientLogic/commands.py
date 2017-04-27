"""
Provides functions for generating commands for the player's tank and appending them to the outgoing queue
"""

import json

import config
from . import clientData

def __appendCommand(name, arg=None):
    """
    Creates a JSON string for a given command and appends it to the outgoing queue
    """
    command = dict()
    command["action"] = name
    if arg is not None:
        command["arg"] = arg

    clientData.outgoing.append(json.dumps(command, separators=(',', ':')))

def fire(heading):
    """
    Issues the fire command
        Will only send the command if clientData.gameState.myTank.canShoot is True
        The server will also silently ignore commands to shot too quickly
    :param heading: Direction to shoot in radians from the +x axis (independent of tank's heading)
    """
    if clientData.gameState.myTank.canShoot:
        clientData.gameState.myTank.canShoot = False
        __appendCommand(config.client.commands.fire, arg=heading)

def turn(heading):
    """
    Issues the command to turn the tank
    :param heading: New direction for the tank in radians from the +x axis
    """
    __appendCommand(config.client.commands.turn, arg=heading)
    clientData.gameState.myTank.heading = heading

def stop():
    """
    Issues the command to stop the tank
    """
    __appendCommand(config.client.commands.stop)
    clientData.gameState.myTank.moving = False

def go():
    """
    Issues the command to make the tank drive in the direction of its heading
        It will continue to move until the stop command is issued
    """
    __appendCommand(config.client.commands.go)
    clientData.gameState.myTank.moving = True