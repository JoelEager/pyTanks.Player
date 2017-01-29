import client
import math

# This script is the actual ai "player"

timeSinceLastCommand = 0

# Called once every frame by the client
#   elapsedTime:    The time elapsed in seconds since the last frame
def aiLoop(elapsedTime):
    global timeSinceLastCommand
    timeSinceLastCommand += elapsedTime

    if timeSinceLastCommand >= 5:
        timeSinceLastCommand = 0
        client.sendCommand(str(-math.pi / 2))