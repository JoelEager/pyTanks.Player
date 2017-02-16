# Configuration settings for both the game and the client

class gameSettings:
    class mapSize:
        # (0, 0) is the upper left corner with +x going to the right and +y going down
        x = 500                         # In pixels
        y = 500                         # In pixels

    class tankProps:
        speed = 25                      # In pixels per second
        height = 10                     # In pixels
        width = 10                      # In pixels

    shellSpeed = 100                    # In pixels per second

class clientSettings:
    ip = "127.0.0.1"                # The server's IP address
    port = "5678"                   # Server's port
    apiPath = "/pyTanksAPI/player"  # The player client API path to connect to the server on
    framesPerSecond = 60            # The target frame rate for the aiLoop function

    # Level of debugging logging for the websocket client
    logLevel = 1  # 0 for normal, 1 for FPS, 2 for all client status and io logs

    # String names for the commands the player can send
    class commands:
        fire = "Command_Fire"
        turn = "Command_Turn"
        stop = "Command_Stop"
        go = "Command_Go"