from panda3d.core import NodePath
from ..tileMap.TileMap import coordToRealPosition
from objects.defaultConfig.Consts import *

class GameObject (object):
    """
        Represents all objects in game.
    """

    def __init__ (self, **kwargs):
        self._np = NodePath(kwargs['nodeName']) # Initializes our nodePath()
        self.model = None
        self._gridPos = kwargs['coords']
        self._loadModel(kwargs['modelPath'], self._gridPos,
                        kwargs['modelScale'])

    def _loadModel(self, modelPath, coords, modelScale):
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
        self.model.reparentTo(self._np)
        self._np.reparentTo(base.render)
        self._np.setPos(coordToRealPosition(coords))
        # Scale our model properly:
        self.model.setScale(modelScale)

    def getNodePath (self):
        return self._np

    def getGridPosition (self):
        return self._gridPos

    def updateGridPosition (self, newPos):
        self._gridPos = newPos
