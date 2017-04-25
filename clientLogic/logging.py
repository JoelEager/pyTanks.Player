import config

# Handles logging of events
def logPrint(message, minLevel):
    if config.client.logLevel >= minLevel:
        print(message)