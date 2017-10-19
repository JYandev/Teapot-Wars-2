from panda3d.core import NodePath
from ..tileMap.TileMap import coordToRealPosition
class GameObject (object):

    def __init__ (self, modelPath, coords, nodeName):
        self.np = NodePath(nodeName) # Initializes our nodePath()
        self.model = None
        self._loadModel(modelPath, coords)

    def _loadModel(self, modelPath, coords):
        """
            Given a loader and renderer instance, will load and enable
             rendering of this object.
            Sets the initial position of this model to coords.
        """
        # Load model
        self.model = base.loader.loadModel(modelPath)
        # First, reparent to our nodePath, then reparent nodePath to render:
        # This ensures that when this object is selected, we can access our
        #  class:
        self.model.reparentTo(self.np)
        self.np.reparentTo(base.render)
        self.np.setPos(coordToRealPosition(coords))
