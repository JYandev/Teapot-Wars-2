from panda3d.core import NodePath
from ...gameObject.GameObject import GameObject
from ...tileMap.TileMap import coordToRealPosition

MODEL_PATH = "objects/localPlayer/selector/TileSelector.egg"
TEXTURE_PATH = "objects/localPlayer/selector/Selector-Diffuse.png"

class Selector ():
    def __init__ (self, nodeName, colorTint):
        self.np = NodePath(nodeName)
        self._initModel(colorTint) # Initialize our model and set up object.
        self.np.reparentTo(render) # Render our model

    def _initModel (self, colorTint):
        self._model = base.loader.loadModel(MODEL_PATH)
        self._texture = base.loader.loadTexture(TEXTURE_PATH)
        self._model.setTexture(self._texture)
        self._model.setColorScale(*colorTint)
        self._model.reparentTo(self.np)

    def showAt (self, coords):
        """
            Displays this selector at the given coordinates.
        """
        self.np.setPos(coordToRealPosition(coords))
        self.np.show()

    def hide (self):
        """
            Stops rendering this selector.
        """
        self.np.hide()
