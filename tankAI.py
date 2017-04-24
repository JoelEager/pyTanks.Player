import random
import math

import config

# The AI code of the pyTanks player client
#   The two functions here are called by wsClient to run the AI code.

timeSinceLastCommand = 0.0
timeToNextAction = 0.0

# Called when the AI's tank spawns
#   gameState:      An up to date version of the game's state - TODO: Documentation on the contents of this object
#   issueCommand:   Reference to a class that allows the issuing of commands
def onSpawn(gameState, issueCommand):
    pass

# Called once every frame while the tank is alive
#   gameState:      An up to date version of the game's state - TODO: Documentation on the contents of this object
#   issueCommand:   Reference to a class that allows the issuing of commands
#   elapsedTime:    The time elapsed in seconds since the last frame
def onTick(gameState, issueCommand, elapsedTime):
    global timeSinceLastCommand, timeToNextAction
    timeSinceLastCommand += elapsedTime

    # Placeholder for actual AI logic
    if timeSinceLastCommand >= timeToNextAction:
        timeSinceLastCommand = 0.0
        timeToNextAction = random.randrange(1, 60) / 20

        if not gameState.myTank.moving:
            issueCommand.turn((math.pi / 4) * random.randint(0, 7))
            issueCommand.go()
            print("Turned and starting moving")

    if gameState.myTank.canShoot and random.randint(0, 4) == 0:
        # Select a target
        while True:
            target = random.randint(0, len(gameState.tanks) - 1)

            if gameState.tanks[target].alive:
                break

        # Do the math
        deltaX = abs(gameState.myTank.x - gameState.tanks[target].x)
        deltaY = gameState.myTank.y - gameState.tanks[target].y
        angle = math.atan(deltaY / deltaX)

        if gameState.tanks[target].x < gameState.myTank.x:
            angle = math.pi - angle

        issueCommand.fire(angle)
        print("Fired")