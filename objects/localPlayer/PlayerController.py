from direct.actor.Actor import Actor
from .CameraSystem import CameraSystem
from ..characters.teapot.Teapot import Teapot
from .InputSystem import InputSystem

class PlayerController ():
    """
        The Player class lets the user play the game.
        Handles client side player systems such as input, camera, and gameplay.
    """
    def __init__ (self, initialPos, gameManager):
        self._gameManager = gameManager # Reference to gameManager for callbacks

        base.disableMouse() # Disables default Panda3D camera control
        # Initialize this clients gameObject:
        self.character = Teapot(initialPos, "player")

        # Initialize Camera Input:
        self.cameraSystem = CameraSystem(target=self.character.np)

        # Initialize the player's Input and UI:
        self.inputSystem = InputSystem(gameManager.getTileMap())
