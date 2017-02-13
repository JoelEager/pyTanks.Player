import asyncio
import websockets
import datetime
import json
import math
import config

# The websocket client and asyncio functions
#   Handles communication with the server and runs the ai's aiLoop function

gameState = None    # The current game state (received from the server and extrapolated by the client)
outgoing = list()   # The outgoing message queue

# Sends a command to the server
def sendCommand(command):
    outgoing.append(command)

# Connects to the server and configures the asyncio tasks used to run the client
def runClient(loopCallback):
    incoming = list()

    # --- Internal websocket client functions: ---

    # Handles printing of debug info
    def logPrint(message, minLevel):
        if config.clientSettings.logLevel >= minLevel:
            print(message)

    # Gets the delta between now and a given datetime in seconds
    def timeDelta(aTime):
        diff = datetime.datetime.now() - aTime
        return diff.seconds + (diff.microseconds / 1000000)

    # Helper function for decoding json that turns a dict into a matching object
    def dictToObj(dictIn):
        class objOfDict:
            def __init__(self):
                for key, value in dictIn.items():
                    setattr(self, key, value)

        return objOfDict()

    # Moves a game object the given distance along its current heading
    #   The object must have the x, y, and heading properties
    def moveObj(obj, distance):
        obj.x += math.cos(obj.heading) * distance
        obj.y += math.sin(obj.heading) * distance

    # Sends queued messages to the server
    async def sendTask(websocket):
        while True:
            if len(outgoing) != 0:
                message = outgoing.pop(0)
                await websocket.send(message)

                logPrint("Sent message to server: " + message, 2)
            else:
                await asyncio.sleep(0.05)

    # Runs loopCallback() every frame and aims to hold the given frame rate
    #   Also handles extrapolation and updating of game state data
    async def frameLoop():
        global gameState

        # For frame rate targeting
        lastFrameTime = datetime.datetime.now()
        baseDelay = 1 / config.clientSettings.framesPerSecond
        delay = baseDelay
        deltas = list()

        # For calculating the FPS for logging
        lastFSPLog = datetime.datetime.now()
        frameCount = 0

        while True:
            # Calculate the time passed in seconds and adds it to the list of deltas
            frameDelta = timeDelta(lastFrameTime)
            lastFrameTime = datetime.datetime.now()
            deltas.append(frameDelta)
            if len(deltas) > 15:
                deltas.pop(0)

            # Adjust delay to try to keep the actual frame rate within 5% of the target
            avgDelta = sum(deltas) / float(len(deltas))
            if avgDelta * config.clientSettings.framesPerSecond < 0.95:  # Too fast
                delay += baseDelay * 0.01
            elif avgDelta * config.clientSettings.framesPerSecond > 1.05:  # Too slow
                delay -= baseDelay * 0.01

            if delay < 1 / 250:
                delay = 1 / 250

            # Log FPS if server logging is enabled
            if config.clientSettings.logLevel >= 1:
                frameCount += 1

                if timeDelta(lastFSPLog) >= 5:
                    print("FPS: " + str(frameCount / 5))
                    frameCount = 0
                    lastFSPLog = datetime.datetime.now()

            # Update gameState
            if len(incoming) != 0:
                # Message received from server, try to decode it
                message = incoming.pop()
                try:
                    newGameState = json.loads(message, object_hook=dictToObj)
                except json.decoder.JSONDecodeError:
                    # Message isn't JSON so it's probably an error from the server
                    print("Received error message from server: " + message)

                # Print the name of the player's tank if this is the first time a gameState has been received
                if gameState is None:
                    print("This AI has been given command of the " + newGameState.myTank.name)

                gameState = newGameState
            elif gameState is not None:
                # Extrapolate the gameState
                totalDistance = config.gameSettings.tankProps.speed * frameDelta
                moveObj(gameState.myTank, totalDistance)
                for tank in gameState.tanks:
                    if tank.moving:
                        moveObj(gameState.tanks, totalDistance)

            # Run the callback
            if gameState is not None:
                loopCallback(frameDelta)

            # Sleep until the next frame
            await asyncio.sleep(delay)  # (If this doesn't sleep then the other tasks can never be completed.)

    # Connects to the server, starts the other tasks, and handles incoming messages
    async def mainTask():
        async with websockets.connect("ws://" + config.clientSettings.ip + ":" + config.clientSettings.port +
                                      config.clientSettings.apiPath) as websocket:
            print("Connected to server")

            # Start the sendTask and frameLoop
            asyncio.get_event_loop().create_task(sendTask(websocket))
            asyncio.get_event_loop().create_task(frameLoop())

            # Handles incoming messages
            while True:
                message = await websocket.recv()
                incoming.append(message)

                logPrint("Received message from server: " + message, 2)

    # --- Websocket client startup code: ---
    try:
        asyncio.get_event_loop().run_until_complete(mainTask())
    except ConnectionResetError:
        print("Lost connection to server - shutting down")
    except ConnectionRefusedError:
        print("Could not connect to server - shutting down")
    except websockets.exceptions.ConnectionClosed:
        if len(incoming) != 0:
            print("Received error message from server: " + incoming.pop())

        print("Server closed connection - shutting down")
    except KeyboardInterrupt:
        # Exit cleanly on ctrl-C
        return