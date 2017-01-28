# This script contains the configuration settings for both the game and the client

class mapSize:
    # (0, 0) is the upper left corner with +x going to the right and +y going down
    x = 500                         # In pixels
    y = 500                         # In pixels

class tankProps:
    speed = 25                       # In pixels per second

class clientSettings:
    ip = "127.0.0.1"                # The server's IP address
    port = 5678                     # Server's port
    framesPerSecond = 60            # The target frame rate for the frameCallback function

    # Level of debugging logging for the client
    logLevel = 2  # 0 for normal, 1 for FPS, 2 for all client status and io logs