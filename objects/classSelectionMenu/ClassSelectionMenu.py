from objects.classSelectionMenu.ClassPicker import ClassPicker
from objects.classSelectionMenu.NamePicker import NamePicker

class ClassSelectionMenu ():
    """
        The class selection menu is where the User picks a name, favorite color,
         and class for their custom character.
        Other player names and data is also displayed, but in a different class!
    """

    def __init__ (self, gameManager):
        self._gameManager = gameManager
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
        newClass = self._classPicker.getSelected()
        if newName == None or newClass == None:
            return

        # Create Player

        # Close UI:
        self._classPicker.close()
        self._namePicker.close()
        del self #Destroy this instance
