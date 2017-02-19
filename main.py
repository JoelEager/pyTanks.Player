import random
import math
import wsClient
import config

# Main script of the pyTanks "player" client
#   This script starts py with a callback to its aiLoop() function
#   The aiLoop() function is where the actual ai code lives

timeSinceLastCommand = 0
didTurn = False

# Called once every frame by py
#   elapsedTime:    The time elapsed in seconds since the last frame
def aiLoop(elapsedTime):
    global timeSinceLastCommand
    global didTurn
    timeSinceLastCommand += elapsedTime

    # Placeholder for actual AI logic
    if timeSinceLastCommand >= 3:
        timeSinceLastCommand = 0
        
        action = random.randint(0, 2)
        if action == 0 and wsClient.gameState.myTank.moving and not didTurn:
            wsClient.issueCommand.turn(wsClient.gameState.myTank.heading + (math.pi / 2))
            print("Turned")
        elif action == 1:
            wsClient.issueCommand.fire((math.pi / 2) * random.randint(0, 3))
            print("Fired")
        else:
            if wsClient.gameState.myTank.moving:
                wsClient.issueCommand.stop()
                print("Stopped")
            else:
                wsClient.issueCommand.go()
                print("Moving")

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