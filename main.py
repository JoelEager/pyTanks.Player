import wsClient
import math

# Main script of the pyTanks "player" client
#   This script starts wsClient.py with a callback to its aiLoop() function
#   The aiLoop() function is where the actual ai code lives

timeSinceLastCommand = 0

# Called once every frame by wsClient.py
#   elapsedTime:    The time elapsed in seconds since the last frame
def aiLoop(elapsedTime):
    global timeSinceLastCommand
    timeSinceLastCommand += elapsedTime

    if timeSinceLastCommand >= 5:
        timeSinceLastCommand = 0
        wsClient.issueCommand.turn(wsClient.gameState.myTank.heading + (math.pi / 2))

# Start the client with a reference to the aiLoop callback function
wsClient.runClient(aiLoop)