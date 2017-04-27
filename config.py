# Configuration settings for both the game and the client
#   Fields marked with [*] can be freely changed since they don't need to match the server you're connecting to.

class game:
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

class client:
    # Both logLevel and ipAndPort can be overridden by command line args so the value here is only the default
    ipAndPort = "localhost:9042"        # [*] The server's IP address and port
    logLevel = 3                        # [*] The amount of client-side logging (See the usage section of the readme)

    framesPerSecond = 60                # [*] The target frame rate for the clientClock and tankAI's onTick()

    apiVersion = "alpha-0"              # Used to make sure the client and server versions match

    # The player API path to connect to the server on
    apiPath = "/pyTanksAPI/" + apiVersion + "/player"

    # String names for the commands the player can send
    class commands:
        fire = "Command_Fire"
        turn = "Command_Turn"
        stop = "Command_Stop"
        go = "Command_Go"