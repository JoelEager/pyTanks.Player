import json

import config
from . import clientData

# Provides functions for generating commands for the AI's tank and appending them to the outgoing queue

# Creates a JSON string for a given command and appends it to the outgoing queue
def __appendCommand(name, arg=None):
    command = dict()
    command["action"] = name
    if arg is not None:
        command["arg"] = arg

    clientData.outgoing.append(json.dumps(command, separators=(',', ':')))

# Issues the fire command
#   heading - Direction to shoot in radians from the +x axis (independent of tank's heading)
#   Note: Will only send the command if clientData.gameState.myTank.canShoot is True. Commands to shot too quickly will
#       be silently ignored.
def fire(heading):
    if clientData.gameState.myTank.canShoot:
        clientData.gameState.myTank.canShoot = False
        __appendCommand(config.client.commands.fire, arg=heading)

# Issues the command to turn the tank
#   heading - New direction for the tank in radians from the +x axis
def turn(heading):
    __appendCommand(config.client.commands.turn, arg=heading)
    clientData.gameState.myTank.heading = heading

# Issues the command to stop the tank
def stop():
    __appendCommand(config.client.commands.stop)
    clientData.gameState.myTank.moving = False

# Issues the command to make the tank drive forward
#   (It will continue to move at max speed until the stop command is issued)
def go():
    __appendCommand(config.client.commands.go)
    clientData.gameState.myTank.moving = True