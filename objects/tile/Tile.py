from ..gameObject.GameObject import GameObject

MODEL_FILE_PATH = "objects/tile/Tile.egg"

class Tile (GameObject):
    def __init__ (self, loader, renderer, position):
        # Initialize our model and set up our object:
        GameObject.__init__(self, loader, renderer, MODEL_FILE_PATH, position)
