from ..gameObject.GameObject import GameObject
from panda3d.core import LPoint3f, PandaNode

MODEL_FILE_PATH = "objects/tile/Tile.egg"
MODEL_SCALE = LPoint3f(0.5, 0.5, 0.5)
DEFAULT_TEXTURE_PATH = "objects/tile/Tile-Diffuse-Unselected.png"
SELECTED_TEXTURE_PATH = "objects/tile/Tile-Diffuse-Selected.png"

class Tile (GameObject):
    def __init__ (self, position, name="tile"):
        # Initialize our model and set up our object:
        GameObject.__init__(self, MODEL_FILE_PATH, position,
                            name)

        self.model.setScale(MODEL_SCALE)
        # Make sure our mouse raycasting can interact with this object:
        self.np.setPythonTag("selectable", self)

        # Load textures we need (Automatically ignores pre-loaded):
        self._defaultTex = base.loader.loadTexture(DEFAULT_TEXTURE_PATH)
        self._selectTex = base.loader.loadTexture(SELECTED_TEXTURE_PATH)
        # Set default texture:
        self.model.setTexture(self._defaultTex)

    def setSelected (self, select=True):
        """
            Changes this tile's texture to be selected or deselected.
        """
        if select:
            self.model.setTexture(self._selectTex)
        else:
            # Revert to default:
            self.model.setTexture(self._defaultTex)
