from ...gameObject.GameObject import GameObject
from panda3d.core import LPoint3f

MODEL_FILE_PATH = "objects/characters/teapot/Teapot.egg"
MODEL_SCALE = LPoint3f(0.15, 0.15, 0.15)

class Teapot (GameObject):
    def __init__ (self, position, name):
        # Initialize our model and set up our object:
        GameObject.__init__(self, MODEL_FILE_PATH, position,
                            name)
                            
        # Scale our model properly:
        self.model.setScale(MODEL_SCALE)
