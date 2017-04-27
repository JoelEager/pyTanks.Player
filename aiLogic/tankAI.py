"""
The player's AI code
    The two functions here are called by clock.py to run the AI code
"""

import random
import math

from clientLogic.logging import logPrint
from clientLogic import clientData, commands

timeSinceLastCommand = 0.0
timeToNextAction = 0.0

def onSpawn():
    """
    Called when the tank spawns in a new game
    """
    pass

def onTick(elapsedTime):
    """
    Called once every frame while the tank is alive
    :param elapsedTime: The time elapsed, in seconds, since the last frame
    """
    global timeSinceLastCommand, timeToNextAction
    gs = clientData.gameState
    timeSinceLastCommand += elapsedTime

    # Placeholder for actual AI logic
    if timeSinceLastCommand >= timeToNextAction:
        timeSinceLastCommand = 0.0
        timeToNextAction = random.randrange(1, 60) / 20

        if not gs.myTank.moving:
            commands.turn((math.pi / 4) * random.randint(0, 7))
            commands.go()
            logPrint("Turned and starting moving", 2)

    if gs.myTank.canShoot and random.randint(0, 4) == 0:
        # Select a target
        while True:
            target = random.randint(0, len(gs.tanks) - 1)

            if gs.tanks[target].alive:
                break

        # Do the math
        deltaX = abs(gs.myTank.x - gs.tanks[target].x)
        deltaY = gs.myTank.y - gs.tanks[target].y
        angle = math.atan(deltaY / deltaX)

        if gs.tanks[target].x < gs.myTank.x:
            angle = math.pi - angle

        commands.fire(angle)
        logPrint("Fired", 2)