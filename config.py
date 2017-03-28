# Configuration settings for both the game and the client
#   Fields marked with [*] can be freely changed since they don't need to match the server you're connecting to.
#   Both clientSettings.logLevel and clientSettings.ipAndPort can be overridden by command line args so the value here
#   is only the default.

class gameSettings:
    class map:
        # (0, 0) is the upper left corner with +x going to the right and +y going down
        width = 500                     # In pixels
        height = 500                    # In pixels

    class tank:
        speed = 25                      # In pixels per second
        height = 10                     # In pixels
        width = 10                      # In pixels
        reloadTime = 2                  # Minimum time to reload the tank's cannon (in seconds)

    class shell:
        speed = 100                     # In pixels per second
        height = 1                      # In pixels
        width = 1                       # In pixels

class clientSettings:
    ipAndPort = "localhost:9042"        # [*] The server's IP address and port
    logLevel = 1                        # [*] Level of debugging logging for the websocket client
    # (0 for minimal, 1 for FPS, 2 for all client status and io logs)
    framesPerSecond = 60                # [*] The target frame rate for the aiLoop function

    apiPath = "/pyTanksAPI/player"      # The player client API path to connect to the server on

    # String names for the commands the player can send
    class commands:
        fire = "Command_Fire"
        turn = "Command_Turn"
        stop = "Command_Stop"
        go = "Command_Go"