from ...gameObject.GameObject import GameObject

MODEL_FILE_PATH = "objects/characters/teapot/Teapot.egg"

class Teapot (GameObject):
    def __init__ (self, loader, renderer, position):
        # Initialize our model and set up our object:
        GameObject.__init__(self, loader, renderer, MODEL_FILE_PATH, position)
