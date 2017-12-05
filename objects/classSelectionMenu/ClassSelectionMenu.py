from objects.classSelectionMenu.ClassPicker import ClassPicker
from objects.classSelectionMenu.NamePicker import NamePicker
from objects.networking.PlayerInfo import PlayerInfo
from objects.defaultConfig.Consts import *

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
        self._classPicker = ClassPicker(self)
        self._namePicker = NamePicker(self)

    def createCharacter (self):
        """
            Creates a new localPlayer and spawns it with the given name and
             chosen class.
            If there is no name or class, this will not spawn a player.
        """
        self.syncInfo(cName=self._namePicker.getName(),
                      cClass=self._classPicker.getSelected())
        if self._playerInfo.cClass == None:
            #TODO Warn the user that they must pick a class!
            return
        if self._playerInfo.cName == None\
            or self._playerInfo.cName == NPKR_ENTRY_INITIAL_TEXT:
            #TODO Warn the user that they must pick a name!
            return

        # Create Player
        self._gameManager.createPlayer(self._playerInfo)

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
