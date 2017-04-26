import asyncio
import websockets
import socket

from . import clientData
from .logging import logPrint
from .clock import clientClock
import config

# The pyTanks player client backend and asyncio code

__running = True        # The asyncio event loop will end when this is set to False

# Sends queued messages to the server
async def __sendTask(websocket):
    while True:
        if len(clientData.outgoing) != 0:
            message = clientData.outgoing.pop(0)
            await websocket.send(message)

            logPrint("Sent message to server: " + message, 4)
        else:
            await asyncio.sleep(0.05)

# Handles incoming messages
async def __receiveTask(websocket):
    while True:
        message = await websocket.recv()
        clientData.incoming.append(message)

        logPrint("Received message from server: " + message, 4)

# Connects to the server and starts the tasks
async def __clientMain():
    async with websockets.connect("ws://" + config.client.ipAndPort + config.client.apiPath) as websocket:
        logPrint("Connected to server", 1)

        # Start up the tasks
        asyncio.get_event_loop().create_task(__sendTask(websocket))
        asyncio.get_event_loop().create_task(__receiveTask(websocket))
        asyncio.get_event_loop().create_task(clientClock())

        # Stay around until the running flag is set to False
        while __running:
            await asyncio.sleep(0.1)

# Spin up async io with the clientMain task
def runClient():
    # Used to close the connection and stop the async tasks on an exception
    def handleException(loop, context):
        global __running
        __running = False

        if "exception" in context:
            if isinstance(context["exception"], websockets.exceptions.ConnectionClosed):
                logPrint("Connection closed - shutting down", 1)
            else:
                raise context["exception"]

    try:
        asyncio.get_event_loop().set_exception_handler(handleException)
        asyncio.get_event_loop().run_until_complete(__clientMain())
    except ConnectionResetError:
        return
    except (ConnectionRefusedError, OSError):
        logPrint("Could not connect to server - shutting down", 1)
    except KeyboardInterrupt:
        # Exit cleanly on ctrl-C
        return
    except socket.gaierror:
        logPrint("Invalid ip and/or port", 1)