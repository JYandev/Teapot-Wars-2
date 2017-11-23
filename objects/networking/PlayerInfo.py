import json
from objects.defaultConfig.Consts import *
class PlayerInfo ():
    """
        Holds player information to be sent across the network and used in UI.
    """
    def __init__ (self, cID=None, fromJson=""):
        self.cID = cID
        self.cName = None
        self.cClass = None
        self.cColor = None
        self.health = 0
        self.maxHealth = PLAYER_MAX_HEALTH
        if fromJson != "":
            self.__dict__ = json.loads(fromJson)

    def toJson (self):
        return json.dumps(self.__dict__)
