"""
Startup script for the pyTanks player client
    
Requirements:
    Python 3.5 or newer
    websockets 3.3 (pip install websockets==3.3)

Usage:
    python start.py
    
    The pyTanks player uses the settings found in config.py to control how the client works. Those values can be
    changed directly or be overridden by appending one or more of these command line args:
        log=n - Overrides the default logging level. (See the usage section of the readme.)
        ip:port - Overrides the ip and port used to connect to the server.
"""

import sys
import config

def main():
    """
    Check the environment, apply any command line args to config.py, and start wsClient.py
    """
    # Check Python version
    if sys.version_info[0] < 3 or sys.version_info[1] < 5:
        print("Python 3.5 or newer is required to run the pyTanks player client")
        return

    # Check for websockets
    from importlib import util
    if util.find_spec("websockets") is None:
        print("The websockets module is required to run the pyTanks player client")
        return

    # Import the code that requires the above things
    from clientLogic.wsClient import runClient

    # Parse and apply the args
    for arg in sys.argv:
        if arg == sys.argv[0]:
            continue
        elif arg.startswith("log="):
            try:
                config.client.logLevel = int(arg[-1:])
            except ValueError:
                print("Invalid log level")
                return
        elif ":" in arg:
            config.client.ipAndPort = arg
        else:
            print(__doc__[__doc__.index("Usage:"):].strip())
            return

    # Start the client
    runClient()

if __name__ == "__main__":
    main()