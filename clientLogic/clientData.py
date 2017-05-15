"""
Holds the client's data structures for easy access by both client and AI code
"""

from datetime import datetime

incoming = list()                       # The incoming message queue
outgoing = list()                       # The outgoing command queue
gameState = None                        # The current game state
                                        # (See the gameState section of the readme for docs on this)
lastUpdate = datetime.now()             # When the most recent gameState update arrived