from direct.actor.Actor import Actor
from ..camera.Camera import Camera
from ..characters.teapot.Teapot import Teapot

class Player ():
    """
        The Player class lets the user play the game.
        Handles client side player systems such as input, camera, and gameplay.
    """
    def __init__ (self, mainCamera, loader, renderer, initialPos):

        # Initialize this clients gameObject:
        self.character = Teapot(loader, renderer, initialPos)

        # Initialize Camera Input:
        self.cameraSystem = Camera(mainCamera, target=self.character.model)
