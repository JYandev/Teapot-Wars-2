from direct.showbase import DirectObject
from .selector.PointerSystem import PointerSystem
import string
from objects.characterAbilities.BaseAbility import Targeter
from objects.characterAbilities import *

class InputSystem (DirectObject.DirectObject):
    """
        Handles all input except for camera controls.
    """
    def __init__ (self, playerController, tileMap):
        self._plyrCtrl = playerController
        self._tileMap = tileMap
        self._pointerSystem = PointerSystem(tileMap)
        self._currentAbility = None # The current activated ability
        self.accept("mouse1", self._onMouseButtonDown)
        for key in range(0, 10):
            self.accept(str(key), self._handleAbilityKey, [str(key)])

    def _handleAbilityKey (self, key):
        """ Handles ability selection input from the player. """
        key = key[0]
        # If user presses any numerical keys, activate the selector for the
        #  ability:
        if key.isdigit():
            activatedHotkey = 9 if key == '0' else int(key)-1
            classAbilities = self._plyrCtrl.getClassAbilities()
            if 0 <= activatedHotkey < len(classAbilities):
                self._currentAbility = classAbilities[activatedHotkey]
                self._activateTargeter()

    def _activateTargeter (self):
        """
            Highlights tiles and tells the pointer system to indicate area or
             single-target based on the current ability's targeter.
        """
        if self._currentAbility:
            targeter = self._currentAbility.targeterType
            # Show how much energy it will take updateEnergyRequirement()
            if targeter == Targeter.SelfPath:
                params = {'origin':self._plyrCtrl.getCharacter()\
                                                 .getGridPosition()}
                self._pointerSystem.setHighightMode(targeter, params)

    def _onMouseButtonDown(self):
        """
            Handler for mouse presses.
        """
        if self._currentAbility:
            if self._currentAbility.targeterType == Targeter.SelfPath:
                params = {'targetPos' : self._pointerSystem.getHovered(),
                          'targetNode' : self._plyrCtrl.getCharacter(),
                          'tileMap' : self._tileMap}
                self._currentAbility.effect.doEffect(**params)
                # We've succesfully initiated action, reset the active ability:
                self._currentAbility = None
                self._pointerSystem.resetHighlightMode()
