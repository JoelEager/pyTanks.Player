import math
import json
from datetime import datetime
import asyncio

import config
from aiLogic import tankAI
from . import clientData
from .logging import logPrint

# TODO: File docs

# Moves a game object the given distance along its current heading
#   The object must have the x, y, and heading properties
def moveObj(obj, distance):
    obj.x += math.cos(obj.heading) * distance
    obj.y += math.sin(obj.heading) * distance

# Helper function for decoding json that turns a dict into a matching object
def dictToObj(dictIn):
    class objFromDict:
        def __init__(self):
            for key, value in dictIn.items():
                setattr(self, key, value)

    return objFromDict()

# Runs loopCallback() every frame, setupCallback() on the first frame, and aims to hold the given frame rate
#   Also handles extrapolation and updating of game state data
async def clientClock():
    # For frame rate targeting
    lastFrameTime = datetime.now()
    baseDelay = 1 / config.client.framesPerSecond
    delay = baseDelay
    deltas = list()

    # For calculating the FPS for logging
    lastFSPLog = datetime.now()
    frameCount = 0

    while True:
        # Calculate the time passed in seconds and adds it to the list of deltas
        frameDelta = (datetime.now() - lastFrameTime).total_seconds()
        lastFrameTime = datetime.now()
        deltas.append(frameDelta)
        if len(deltas) > 15:
            deltas.pop(0)

        # Adjust delay to try to keep the actual frame rate within 5% of the target
        avgDelta = sum(deltas) / float(len(deltas))
        if avgDelta * config.client.framesPerSecond < 0.95:  # Too fast
            delay += baseDelay * 0.01
        elif avgDelta * config.client.framesPerSecond > 1.05:  # Too slow
            delay -= baseDelay * 0.01

        if delay < 1 / 250:
            delay = 1 / 250

        # Log FPS if server logging is enabled
        if config.client.logLevel >= 1:
            frameCount += 1

            if (datetime.now() - lastFSPLog).total_seconds() >= 5:
                print("FPS: " + str(frameCount / 5))
                frameCount = 0
                lastFSPLog = datetime.now()

        # Update gameState and run AI the functions
        gameStateWasNone = clientData.gameState is None
        wasAlive = None
        if not gameStateWasNone:
            wasAlive = clientData.gameState.myTank.alive

        if len(clientData.incoming) != 0:
            # Message received from server, try to decode it
            message = clientData.incoming.pop(0)
            try:
                clientData.gameState = json.loads(message, object_hook=dictToObj)
            except json.decoder.JSONDecodeError:
                # Message isn't JSON so print it
                # (This is usually used to handle error messages)
                logPrint("Message from server: " + message, 1)
        elif clientData.gameState is not None:
            # Extrapolate the gameState
            totalDistance = config.game.tank.speed * frameDelta
            moveObj(clientData.gameState.myTank, totalDistance)
            for tank in clientData.gameState.tanks:
                if tank.moving:
                    moveObj(tank, totalDistance)

            totalDistance = config.game.shell.speed * frameDelta
            for shell in clientData.gameState.shells:
                moveObj(shell, totalDistance)

        if clientData.gameState is not None:
            if gameStateWasNone:
                logPrint("Received command of the " + clientData.gameState.myTank.name, 1)

            if clientData.gameState.ongoingGame:
                if clientData.gameState.myTank.alive:
                    if not wasAlive:
                        logPrint("Tank spawned", 2)
                        tankAI.onSpawn()

                    tankAI.onTick(frameDelta)

            if not clientData.gameState.myTank.alive and wasAlive:
                logPrint("Tank killed", 2)

        # Sleep until the next frame
        await asyncio.sleep(delay)  # (If this doesn't sleep then the other tasks can never be completed.)