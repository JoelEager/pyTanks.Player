import random
import math
import wsClient
import config

# Main script of the pyTanks "player" client
#   This script starts py with a callback to its aiLoop() function
#   The aiLoop() function is where the actual ai code lives

timeSinceLastCommand = 0
timeToNextAction = 0
didTurn = False

# Called once every frame by py
#   elapsedTime:    The time elapsed in seconds since the last frame
def aiLoop(elapsedTime):
    global timeSinceLastCommand, didTurn, timeToNextAction
    timeSinceLastCommand += elapsedTime

    # Placeholder for actual AI logic
    if timeSinceLastCommand >= timeToNextAction:
        timeSinceLastCommand = 0
        timeToNextAction = random.randrange(1, 60) / 20
        
        action = random.randint(0, 6)
        if action == 0 and wsClient.gameState.myTank.moving:
            wsClient.issueCommand.stop()
            print("Stopped")
        elif action >= 2 and not wsClient.gameState.myTank.moving:
            wsClient.issueCommand.go()
            print("Moving")
        elif action >= 2 and not didTurn:
            wsClient.issueCommand.turn(wsClient.gameState.myTank.heading + (math.pi / 2))
            print("Turned")

    if wsClient.issueCommand.canShoot() and random.randint(0, 4) == 0:
        wsClient.issueCommand.fire((math.pi / 4) * random.randint(0, 7))
        print("Fired")

    # Half-hearted attempt to avoid running off the edge of the map
    if wsClient.gameState.myTank.moving:
        if (wsClient.gameState.myTank.x > config.gameSettings.mapSize.x - 25 or wsClient.gameState.myTank.x < 25 or
            wsClient.gameState.myTank.y > config.gameSettings.mapSize.y - 25 or wsClient.gameState.myTank.y < 25):
            if not didTurn:
                wsClient.issueCommand.turn(wsClient.gameState.myTank.heading + math.pi)
                didTurn = True
                print("Trying not to fall off the map")
        elif not (wsClient.gameState.myTank.x > config.gameSettings.mapSize.x - 50 or wsClient.gameState.myTank.x < 50 or
            wsClient.gameState.myTank.y > config.gameSettings.mapSize.y - 50 or wsClient.gameState.myTank.y < 50) and didTurn:
            didTurn = False

# Start the client with a reference to the aiLoop callback function
wsClient.runClient(aiLoop)