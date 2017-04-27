"""
Holds the client's data structures for easy access by both client and AI code
"""

incoming = list()                       # The incoming message queue
outgoing = list()                       # The outgoing command queue
gameState = None                        # The current game state
                                        # (See the gameState section of the readme for docs on this)