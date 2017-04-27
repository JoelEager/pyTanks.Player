# pyTanks
 \- A battleground for Python AIs to fight it out.

pyTanks is a project in three modules:
- [Server](https://github.com/JoelEager/pyTanks.Server) - A Python server that hosts a top-down, simplistic game of tanks. This takes care of maintaining the game state, handling commands from the players, and sending game state updates to both viewers and players.
- **Player** - A Python AI that connects to the server and plays the game of tanks.
- [Viewer](https://github.com/JoelEager/pyTanks.Viewer) - A JavaScript/HTML UI for humans to view the ongoing battle.

### Requirements
- Python 3.5 or newer
- [websockets 3.3](https://github.com/aaugustin/websockets) (pip install websockets==3.3)

**Note: pyTanks is currently in an "alpha" state. Feel free to play around with it and offer feedback but don't expect the code to be feature-complete or bug free.**

# Player
Mostly functional but the AI is very simplistic.

### Usage
```python start.py```

The pyTanks player uses the settings found in `config.py` to control how the client works. Those values can be changed directly or be overridden by appending one or more of these command line args:
- log=n - Overrides the default logging level.
- ip:port - Overrides the ip and port used to connect to the server.

Where the log level is one of:
- 0 for no logging
- 1 for connect/disconnect and errors
- 2 for game events and AI logic
- 3 for FPS
- 4 for client IO
- 5 for verbose websocket logs

(All log events of a log level equal to or less than the set log level will be printed.)

## Documentation on the API and AI development

The AI's code lives in `aiLogic/tankAI.py`. (That whole folder is meant for AI-specific code.) In that file you'll find the 2 callbacks that will form the core of the AI. Currently they just hold the code for a simplistic, example AI.

A few things to keep in mind:
- Your tank will die with one hit.
- Your tank will automatically stop (as in `gameState.myTank.moving = False`) when it hits another tank or a wall.
- The list of enemy tanks is not guaranteed to stay in the same order.
- All headings (both in commands.py and gameState) are in radians from the +x axis.
- Play nice.

### Sending commands
To send a command call one of the functions in `clientLogic.commands`. The documentation on each function explains its args and what the command does.

Here's a quick overview:
- `fire(heading)` - Shoots in the direction of heading. Automatically capped to the tank's rate of fire by both the actual function and the server-side logic.
- `turn(heading)` - Turns the tank to the new heading.
- `stop()` - Tells the tank to stop moving.
- `go()` - Tells the tank to start moving.

Behind the scenes each of these functions will feed your arguments and the correct string from `config.py` into a function that appends the JSON representation of the command onto the outgoing queue. That will then be sent off to the server and be applied to the game. The command functions also apply the action to the local gameState variable so it always matches the most recent AI commands.

### The gameState variable
(Found in `clientLogic.clientData.gameState`)

The contents of the gameState variable come from the state updates that the server sends. The code in clock.py and commands.py extrapolate on it every frame to ensure that it's up to date with movement and AI commands. Since the object is constructed on the fly from JSON you can refer to the below code to see what you can expect it to look like at runtime. The value will be assigned before any AI code is called so you can count on it matching this.

The JSON is turned into a valid Python object so values can be referenced using normal Python syntax. For example:
```python
from clientLogic import clientData

isMoving = clientData.gameState.myTank.moving           # A boolean value for if the tank is moving
theirHeading = clientData.gameState.tanks[1].heading    # A float value for the 2nd enemy tank's current heading
```

And here's the structure of the object (in JSON):
```
gameState = {
   "ongoingGame":true,
   "myTank":{
      "x":344.56081386562886,
      "y":349.4948861343713,
      "heading":5.497787143782138,
      "moving":false,
      "alive":true,
      "name":"Crusader Mk III",
      "canShoot":false
   },
   "tanks":[
      {
         "x":57.308355339059325,
         "y":94.69735533905933,
         "heading":3.9269908169872414,
         "moving":false,
         "alive":false
      },
      ... (and so on)
   ],
   "shells":[
      {
         "shooterId":23,
         "x":492.58348412358544,
         "y":290.7623424927426,
         "heading":0.4799365983861276
      },
      ... (and so on)
   ],
   "walls":[
      {
         "height":70,
         "width":25,
         "y":147.0,
         "x":136.5
      },
      ... (and so on)
   ]
}
```

### config.py
`config.py` holds all the configuration values relevant to the game or client. Some of these can be modified to match your preference while most need to match the server's settings. (See the file for which are which.) However, the important bit is that these values can be referenced by the AI to make decisions. For example, if you want to know the speed of a tank just use this code:
```python
import config

tankSpeed = config.game.tank.speed
```

### Logging
To hook into the existing logging system for your AI logs just call it like this:
```python
from clientLogic.logging import logPrint

logPrint("Did a thing", 2)
```

The 2 is for log level 2 which includes AI actions. However, nothing is stopping you from changing that if you want more flexibility in your logging.

---
(For the other modules see the repos linked at the top of this readme.)