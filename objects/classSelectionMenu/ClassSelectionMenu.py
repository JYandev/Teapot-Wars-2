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
        self._namePicker = NamePicker()
