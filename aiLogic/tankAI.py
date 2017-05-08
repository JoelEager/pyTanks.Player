"""
The player's AI code
    The two functions here are called by clock.py to run the AI code
"""

import random
import math

from clientLogic.logging import logPrint
from clientLogic import clientData, commands

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
    gs = clientData.gameState

    # Collided so try to get moving again
    if not gs.myTank.moving:
        commands.turn((math.pi / 4) * random.randint(0, 7))
        commands.go()
        logPrint("Turned and starting moving", 2)

    # Shooting logic
    if gs.myTank.canShoot and random.randint(0, 4) == 0:
        # Select a target
        random.shuffle(gs.tanks)
        for target in gs.tanks:
            if target.alive:
                # Do the math
                deltaX = abs(gs.myTank.x - target.x)
                if deltaX == 0: return
                deltaY = gs.myTank.y - target.y
                angle = math.atan(deltaY / deltaX)

                if target.x < gs.myTank.x:
                    angle = math.pi - angle

                commands.fire(angle)
                logPrint("Fired", 2)

                break
