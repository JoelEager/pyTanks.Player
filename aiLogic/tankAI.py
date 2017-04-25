import random
import math

from clientLogic.logging import logPrint
from clientLogic import clientData, commands

# The AI code of the player
#   The two functions here are called by clock.py to run the AI code

timeSinceLastCommand = 0.0
timeToNextAction = 0.0

# Called when the AI's tank spawns
def onSpawn():
    pass

# Called once every frame while the tank is alive
#   elapsedTime:    The time elapsed in seconds since the last frame
def onTick(elapsedTime):
    global timeSinceLastCommand, timeToNextAction
    timeSinceLastCommand += elapsedTime

    # Placeholder for actual AI logic
    if timeSinceLastCommand >= timeToNextAction:
        timeSinceLastCommand = 0.0
        timeToNextAction = random.randrange(1, 60) / 20

        if not clientData.gameState.myTank.moving:
            commands.turn((math.pi / 4) * random.randint(0, 7))
            commands.go()
            logPrint("Turned and starting moving", 2)

    if clientData.gameState.myTank.canShoot and random.randint(0, 4) == 0:
        # Select a target
        while True:
            target = random.randint(0, len(clientData.gameState.tanks) - 1)

            if clientData.gameState.tanks[target].alive:
                break

        # Do the math
        deltaX = abs(clientData.gameState.myTank.x - clientData.gameState.tanks[target].x)
        deltaY = clientData.gameState.myTank.y - clientData.gameState.tanks[target].y
        angle = math.atan(deltaY / deltaX)

        if clientData.gameState.tanks[target].x < clientData.gameState.myTank.x:
            angle = math.pi - angle

        commands.fire(angle)
        logPrint("Fired", 2)