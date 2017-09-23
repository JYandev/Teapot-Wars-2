from direct.actor.Actor import Actor
from ..camera.Camera import Camera
from ..characters.teapot.Teapot import Teapot
from .InputSystem import InputSystem

class Player ():
    """
        The Player class lets the user play the game.
        Handles client side player systems such as input, camera, and gameplay.
    """
    def __init__ (self, initialPos):

        # Initialize this clients gameObject:
        self.character = Teapot(initialPos, "player")

        # Initialize Camera Input:
        self.cameraSystem = Camera(target=self.character.model)

        # Initialize the player's Input and UI:
        self.inputSystem = InputSystem()
