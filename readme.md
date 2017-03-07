# pyTanks
 \- A battleground for Python AIs to fight it out.

pyTanks is a project in three modules:
- Player - A Python AI that connects to the server and plays the game of tanks.
- [Viewer](https://github.com/JoelEager/pyTanks.Viewer) - A JavaScript/HTML UI for humans to view the ongoing battle.
- [Server](https://github.com/JoelEager/pyTanks.Server) - A Python server that hosts a top-down, simplistic game of tanks. This takes care of maintaining the game state, handling commands from the players, and sending game state updates to both viewers and players.

Requirements:
- Python 3.5 or newer
- websockets package (pip install websockets)

#### Note: pyTanks is currently in an "alpha" state. Feel free to play around with it and offer feedback but don't expect the code to be feature-complete or fully documented.

## Player
Mostly functional but the AI is very simplistic.

#### Usage:
```python start.py```

The pyTanks player uses the settings found in config.py to control how the client works. Those values can be changed directly or be overridden by appending one or more of these command line args:
- log=n - Overrides the default logging level. (Replace n with 0 for minimal logging, 1 for FPS logging only, or 2 for all client status and io logs.)
- ip:port - Overrides the ip and port used to connect to the server.

---
(For the other modules see the repos linked at the top of this readme.)