"""
Starts up the asyncio tasks and handles the websocket io logic
"""

import asyncio
import websockets
import socket

from . import clientData, clock
from .logging import logPrint
import config

async def __sendTask(websocket):
    """
    Send messages to the server as they are appended to the outgoing queue
    """
    while True:
        if len(clientData.outgoing) != 0:
            message = clientData.outgoing.pop(0)
            await websocket.send(message)

            logPrint("Sent message to server: " + message, 4)
        else:
            await asyncio.sleep(0.05)

async def __receiveTask(websocket):
    """
    Append incoming messages from the server to the incoming queue for handling by clock.py
    """
    while True:
        message = await websocket.recv()
        clientData.incoming.append(message)

        logPrint("Received message from server: " + message, 4)

async def __clientMain():
    """
    Connect to the server and start the asyncio tasks
    """
    async with websockets.connect("ws://" + config.client.ipAndPort + config.client.apiPath, timeout=3) as websocket:
        logPrint("Connected to server", 1)

        # Start up the tasks
        asyncio.get_event_loop().create_task(__sendTask(websocket))
        asyncio.get_event_loop().create_task(__receiveTask(websocket))
        await clock.clientClock()

def runClient():
    """
    Spin up the async io client with the clientMain task
    """
    def handleException(loop, context):
        """
        Closes the websocket and stops the async tasks on an exception
            Called by asyncio on an exception
        """
        clock.running = False

        if len(clientData.incoming) != 0:
            message = clientData.incoming.pop(0)
            if message[0] == "[":
                # It's probably an error message from the server so print it
                logPrint("Message from server: " + message, 1)

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
    except (socket.gaierror, ValueError):
        logPrint("Invalid ip and/or port", 1)