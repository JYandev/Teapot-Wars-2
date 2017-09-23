from ..gameObject.GameObject import GameObject
from panda3d.core import LPoint3f

MODEL_FILE_PATH = "objects/tile/Tile.egg"
MODEL_SCALE = LPoint3f(0.5, 0.5, 0.5)

class Tile (GameObject):
    def __init__ (self, loader, renderer, position):
        # Initialize our model and set up our object:
        GameObject.__init__(self, loader, renderer, MODEL_FILE_PATH, position)
        self.model.setScale(MODEL_SCALE)
