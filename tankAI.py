import random
import math

import config

# The AI code of the pyTanks player client
#   The two functions here are called by wsClient to run the AI code.

timeSinceLastCommand = 0
timeToNextAction = 0
didTurn = False

# Called after the client has connected and been given a tank
#   gameState:      An up to date version of the game's state - TODO: Documentation on the contents of this object
#   issueCommand:   Reference to a class that allows the issuing of commands
def setup(gameState, issueCommand):
    pass

# Called once every frame
#   gameState:      An up to date version of the game's state - TODO: Documentation on the contents of this object
#   issueCommand:   Reference to a class that allows the issuing of commands
#   elapsedTime:    The time elapsed in seconds since the last frame
def loop(gameState, issueCommand, elapsedTime):
    global timeSinceLastCommand, didTurn, timeToNextAction
    timeSinceLastCommand += elapsedTime

    # Placeholder for actual AI logic
    if timeSinceLastCommand >= timeToNextAction:
        timeSinceLastCommand = 0
        timeToNextAction = random.randrange(1, 60) / 20
        
        action = random.randint(0, 6)
        if action == 0 and gameState.myTank.moving:
            issueCommand.stop()
            print("Stopped")
        elif action >= 2 and not gameState.myTank.moving:
            issueCommand.go()
            print("Moving")
        elif action >= 2 and not didTurn:
            issueCommand.turn(gameState.myTank.heading + (math.pi / 2))
            print("Turned")

    if issueCommand.canShoot() and random.randint(0, 4) == 0:
        issueCommand.fire((math.pi / 4) * random.randint(0, 7))
        print("Fired")

    # Half-hearted attempt to avoid running off the edge of the map
    if gameState.myTank.moving:
        if (gameState.myTank.x > config.gameSettings.mapSize.x - 25 or gameState.myTank.x < 25 or
            gameState.myTank.y > config.gameSettings.mapSize.y - 25 or gameState.myTank.y < 25):
            if not didTurn:
                issueCommand.turn(gameState.myTank.heading + math.pi)
                didTurn = True
                print("Trying not to fall off the map")
        elif not (gameState.myTank.x > config.gameSettings.mapSize.x - 50 or gameState.myTank.x < 50 or
                  gameState.myTank.y > config.gameSettings.mapSize.y - 50 or gameState.myTank.y < 50) and didTurn:
            didTurn = False