from direct.actor.Actor import Actor
from .CameraSystem import CameraSystem
from ..characters.teapot.Teapot import Teapot
from .InputSystem import InputSystem
from objects.gameUI.BarUI import BarUI
from objects.defaultConfig.Consts import *

class PlayerController ():
    """
        The Player class lets the user play the game.
        Handles client side player systems such as input, camera, and gameplay.
    """
    def __init__ (self, initialPos, gameManager, charClass):
        self._gameManager = gameManager # Reference to gameManager for callbacks
        base.disableMouse() # Disables default Panda3D camera control
        # Initialize this clients gameObject:
        self._character = Teapot(initialPos, "player").np
        # Initialize Camera Input:
        self.cameraSystem = CameraSystem(target=self._character)
        # Initialize the player's Input and UI:
        self.inputSystem = InputSystem(self, gameManager.getTileMap())
        #self.maxEnergy
        #self.currentEnergy
        self._gridPos = initialPos
        gameManager.getTileMap().spawnObject(self, initialPos)
        self._charClass = charClass
        self._energyBar = BarUI(self._character, ENERGY_BAR_OFFSET, 1,
                                ENERGY_BAR_FG_COLOR, ENERGY_BAR_BG_COLOR)

    def getGridPosition (self):
        return self._gridPos

    def getClass (self):
        return self._charClass

    def getClassAbilities (self):
        return self._charClass.classAbilities

    def getCharacter (self):
        return self._character

    def updateGridPosition (self, newPos):
        self._gridPos = newPos

    # Define equality and representation functions for searching.
    def __eq__ (self, other):
        if not isinstance(other, PlayerController): return False
        return True # This is the one and only player controller
