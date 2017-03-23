import random
import math

import config

# The AI code of the pyTanks player client
#   The two functions here are called by wsClient to run the AI code.

timeSinceLastCommand = 0
timeToNextAction = 0

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
    global timeSinceLastCommand, timeToNextAction
    timeSinceLastCommand += elapsedTime

    # Placeholder for actual AI logic
    if timeSinceLastCommand >= timeToNextAction:
        timeSinceLastCommand = 0
        timeToNextAction = random.randrange(1, 60) / 20

        if not gameState.myTank.moving:
            issueCommand.turn((math.pi / 4) * random.randint(0, 7))
            issueCommand.go()
            print("Turned and starting moving")
        else:
            action = random.randint(0, 1)
            if action == 1:
                issueCommand.turn((math.pi / 4) * random.randint(0, 7))
                print("Turned")

    if issueCommand.canShoot() and random.randint(0, 4) == 0:
        issueCommand.fire((math.pi / 4) * random.randint(0, 7))
        print("Fired")