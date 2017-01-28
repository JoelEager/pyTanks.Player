import asyncio
import websockets
import datetime
import config
import aiPlayer

outgoing = list()   # The outgoing message queue

# Sends a command to the server
def sendCommand(command):
    outgoing.append(command)

# Connects to the server and configures the asyncio tasks used to run the client
async def runClient():
    incoming = list()

    # --- Internal client API functions: ---

    # Handles printing of debug info
    def logPrint(message, minLevel):
        if config.clientSettings.logLevel >= minLevel:
            print(message)

    # Gets the delta between now and a given datetime in seconds
    def timeDelta(aTime):
        diff = datetime.datetime.now() - aTime
        return diff.seconds + (diff.microseconds / 1000000)

    # Sends queued messages to the server
    async def sendTask():
        while True:
            if len(outgoing) != 0:
                message = outgoing.pop(0)
                await websocket.send(message)

                logPrint("Sent message to server: " + message, 2)
            else:
                await asyncio.sleep(0.05)

    # Runs aiPlayer.aiLoop() every frame and aims to hold the given frame rate
    #   Also handles extrapolation and updating of game state data
    async def frameLoop():
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

            # TODO - Update game state

            # Run the callback
            aiPlayer.aiLoop(frameDelta)

            # Sleep until the next frame
            await asyncio.sleep(delay)  # (If this doesn't sleep then the other tasks can never be completed.)

    # --- Client startup code: ---

    async with websockets.connect("ws://127.0.0.1:5678/playerAPI") as websocket:
        print("Connected to server")

        # Start the sendTask and frameLoop
        asyncio.get_event_loop().create_task(sendTask())
        asyncio.get_event_loop().create_task(frameLoop())

        # Handles incoming messages
        while True:
            message = await websocket.recv()
            incoming.append(message)

            logPrint("Received message from server: " + message, 2)

if __name__ == "__main__":
    # Execute only if run as a script
    try:
        asyncio.get_event_loop().run_until_complete(runClient())
    except ConnectionResetError:
        print("Lost connection to server - shutting down")
    except ConnectionRefusedError:
        print("Could not connect to server - shutting down")