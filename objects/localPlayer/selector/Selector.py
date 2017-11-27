from panda3d.core import NodePath
from ...gameObject.GameObject import GameObject
from ...tileMap.TileMapUtilities import coordToRealPosition

MODEL_PATH = "objects/localPlayer/selector/TileSelector.egg"
TEXTURE_PATH = "objects/localPlayer/selector/Selector-Diffuse.png"

class Selector ():
    def __init__ (self, nodeName, colorTint, previewer=False):
        self.np = NodePath(nodeName)
        self._initModel(colorTint, previewer)
        self.np.reparentTo(render) # Render our model

    def _initModel (self, colorTint, previewer):
        self._model = base.loader.loadModel(MODEL_PATH)
        self._texture = base.loader.loadTexture(TEXTURE_PATH)
        self._model.setTexture(self._texture)
        self._model.setColorScale(*colorTint)
        self._model.reparentTo(self.np)
        # Set our offset if we are not a previewer selector:
        if previewer == False:
            self._model.setPos(self.np, 0, 0, 0.01)

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

    def destroy (self):
        """ Destroys this object and the node path associated with it """
        self.np.removeNode()
        del self
