from direct.actor.Actor import Actor
from .CameraSystem import CameraSystem
from ..characters.teapot.Teapot import Teapot
from .InputSystem import InputSystem

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
        gameManager.getTileMap().spawnObject(self._character, initialPos)
        self._charClass = charClass
        self.getClass().classAbilities[0].effect.doEffect(target=self,
                                                    position=gameManager.getTileMap().getRandomFloor(),
                                                    tileMap=gameManager.getTileMap())

    def getGridPosition (self):
        return self._gridPos

    def getClass (self):
        return self._charClass

    def getCharacter (self):
        return self._character
