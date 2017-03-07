import sys

import config
import wsClient
import tankAI

# Main/startup script of the pyTanks player client
#   This script checks any command line args provided, applies them to config.py, and then starts wsClient.py with
#   references to the setup and loop functions in tankAI.py.
#
#   Requirements:
#       Python 3.5 or newer
#       websockets package (pip install websockets)
#
#   (See the below string for usage information.)

usage = """
Usage:
    python start.py

    The pyTanks player uses the settings found in config.py to control how the client works. Those values can be
    changed directly or be overridden by appending one or more of these command line args:
        log=n - Overrides the default logging level. (Replace n with 0 for minimal logging, 1 for FPS logging only,
                                                        or 2 for all client status and io logs.)
        ip:port - Overrides the ip and port used to connect to the server."""

if __name__ == "__main__":
    for arg in sys.argv:
        if arg == sys.argv[0]:
            continue
        elif arg.startswith("log="):
            try:
                config.clientSettings.logLevel = int(arg[-1:])
            except ValueError:
                print("Invalid log level")
                print(usage.strip())
                sys.exit()
        elif ":" in arg:
            config.clientSettings.ipAndPort = arg
        else:
            print(usage.strip())
            sys.exit()

    wsClient.runClient(tankAI.setup, tankAI.loop)