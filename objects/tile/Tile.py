from ..gameObject.GameObject import GameObject
from panda3d.core import LPoint3f, PandaNode

MODEL_FILE_PATH = "objects/tile/Tile.egg"
MODEL_SCALE = LPoint3f(0.5, 0.5, 0.5)

class Tile (GameObject):
    def __init__ (self, position, name="tile"):
        # Initialize our model and set up our object:
        GameObject.__init__(self, MODEL_FILE_PATH, position,
                            name)

        self.model.setScale(MODEL_SCALE)

        # Make sure our mouse raycasting can interact with this object:
        self.np.setPythonTag("selectable", self)

    def setSelected (self, select=True):
        """
            Changes this tile's texture to be selected or deselected.
        """
        if select:
            #TODO: Set selected texture
            pass
        else:
            pass
            #TODO: Revert selected texture
        print ("Selected:", select)
