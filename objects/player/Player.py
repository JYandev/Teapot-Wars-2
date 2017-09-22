from direct.actor.Actor import Actor
from ..camera.Camera import Camera
class Player ():
    """
        The Player class lets the user play the game.
        Handles client side player systems such as input, camera, and gameplay.
    """
    def __init__ (self, mainCamera):
        # Initialize Camera Input:
        self.cameraSystem = Camera(mainCamera)
