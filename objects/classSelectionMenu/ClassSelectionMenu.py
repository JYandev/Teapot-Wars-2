from objects.classSelectionMenu.ClassPicker import ClassPicker
from objects.classSelectionMenu.NamePicker import NamePicker
from objects.networking.PlayerInfo import PlayerInfo

class ClassSelectionMenu ():
    """
        The class selection menu is where the User picks a name, favorite color,
         and class for their custom character.
        Other player names and data is also displayed, but in a different class!
    """

    def __init__ (self, gameManager, cID):
        self._gameManager = gameManager
        self._playerInfo = PlayerInfo(cID)
        # self._colorPicker
        self._classPicker = None
        self._namePicker = None
        self._draw()

    def _draw (self):
        """ Draws the sub-elements. """
        self._classPicker = ClassPicker()
        self._namePicker = NamePicker(self)

    def createCharacter (self, newName):
        """
            Creates a new localPlayer and spawns it with the given name and
             chosen class.
            If there is no name or class, this will not spawn a player.
        """
        #TODO Redo this to use the synced values (self._playerInfo)
        newClass = self._classPicker.getSelected()
        if newName == None or newClass == None:
            return

        # Create Player
        self._gameManager.createPlayer(newName, newClass)

    def syncInfo (self, cName=None, cClass=None, cColor=None):
        """ Syncs info with the server/client manager """
        if cName != None:
            self._playerInfo.cName = cName
        if cClass != None:
            self._playerInfo.cClass = cClass
        if cColor != None:
            self._playerInfo.cColor = cColor

        self._gameManager.updateLocalInfoAndSync(self._playerInfo)

    def close (self):
        """ Close UI """
        self._classPicker.close()
        self._namePicker.close()
        del self #Destroy this instance
