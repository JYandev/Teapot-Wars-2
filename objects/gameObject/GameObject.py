from panda3d.core import NodePath
from direct.actor.Actor import Actor
from ..tileMap.TileMapUtilities import coordToRealPosition
from objects.defaultConfig.Consts import *

class GameObject (object):
    """
        Represents all objects in game.
    """

    def __init__ (self, **kwargs):
        self._np = NodePath(kwargs['nodeName']) # Initializes our nodePath()
        self._gridPos = kwargs['coords']
        self._model = None # Will only be populated if static
        self._actor = None # Will only be populated if not static
        if 'animDict' in kwargs: # Non static
            # Load a dynamic actor and attach it to our Node Path:
            print(len([kwargs['modelPath'], self._gridPos,
                            kwargs['modelScale'], kwargs['animDict']]))
            self._initActor(kwargs['modelPath'], self._gridPos,
                            kwargs['modelScale'], kwargs['animDict'])
        else: # Static
            # Load and attach a static model:
            self._loadModel(kwargs['modelPath'], self._gridPos,
                            kwargs['modelScale'])

    def _loadModel(self, modelPath, coords, modelScale):
        """
            Given a loader and renderer instance, will load and enable
             rendering of this object.
            Sets the initial position of this model to coords.
        """
        # Load model
        self._model = base.loader.loadModel(modelPath)
        # First, reparent to our nodePath, then reparent nodePath to render:
        # This ensures that when this object is selected, we can access our
        #  class:
        self._model.reparentTo(self._np)
        self._np.reparentTo(base.render)
        self._np.setPos(coordToRealPosition(coords))
        # Scale our model properly:
        self.model.setScale(modelScale)

    def _initActor(self, modelPath, coords, modelScale, animDict):
        """
            Loads an actor and enable rendering.
            Sets the initial position.
        """
        # Load actor and animations:
        self._actor = Actor(modelPath, animDict)
        # First, reparent to our nodePath, then reparent nodePath to render:
        # This ensures that when this object is selected, we can access our
        #  class:
        self._actor.reparentTo(self._np)
        self._np.reparentTo(base.render)
        self._np.setPos(coordToRealPosition(coords))
        # Scale our model properly:
        self._actor.setPos(self._np, 0, 0 , 0)
        self._actor.setScale(modelScale)

    def facePointIgnoreXY (self, point):
        """ Makes this object face a given point """
        self.getNodePath().lookAt(coordToRealPosition(point))
        # Override x and y rotation:
        self.getNodePath().setP(0)
        self.getNodePath().setR(0)

    def getModel (self):
        return self._model

    def getActor (self):
        return self._actor

    def getNodePath (self):
        return self._np

    def getGridPosition (self):
        return self._gridPos

    def updateGridPosition (self, newPos):
        self._gridPos = newPos
