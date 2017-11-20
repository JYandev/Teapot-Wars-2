from direct.showbase import DirectObject
from .selector.PointerSystem import PointerSystem
import string
from objects.characterAbilities.BaseAbility import Targeter

class InputSystem (DirectObject.DirectObject):
    """
        Handles all input except for camera controls.
    """
    def __init__ (self, playerController, tileMap):
        self._plyrCtrl = playerController
        self._pointerSystem = PointerSystem(tileMap)
        self._currentAbility = None # The current activated ability
        self.accept("mouse1", self._onMouseButtonDown)
        for key in range(0, 10):
            self.accept(str(key), self._handleAbilityKey, [str(key)])

    def _handleAbilityKey (self, key):
        """ Handles ability selection input from the player. """
        key = key[0]
        print(key)
        # If user presses any numerical keys, activate the selector for the
        #  ability:
        if key.isdigit():
            activatedHotkey = 9 if key == '0' else int(key)-1
            if 0 < activatedHotkey < len(
                                      self._plyrCtrl.getClass().classAbilities):
                self._currentAbility = self._plyrCtrl.getClass()\
                                           .classAbilities[activatedHotkey]
                self._activateTargeter()

    def _activateTargeter ():
        """
            Highlights tiles and tells the pointer system to indicate area or
             single-target based on the current ability's targeter.
        """
        if self._currentAbility:
            targeter = self._currentAbility.targeterType
            print ("Activating targeter for ability, %s" % str(self._currentAbility))
            # Show how much energy it will take updateEnergyRequirement()
            if targeter == Targeter.Path:
                self._pointerSystem.highlightPath(
                                              self._playrCtrl.getGridPosition())




    def _onMouseButtonDown(self):
        """
            Handler for mouse presses.
        """
        print("Activating ability: %s" % str(self._currentAbility))
        pass
