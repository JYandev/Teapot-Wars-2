class GameObject ():

    def __init__ (self, loader, renderer, modelPath, position):
        self.model = None
        self._loadModel(loader, renderer, modelPath, position)

    def _loadModel(self, loader, renderer, modelPath, position):
        """
            Given a loader and renderer instance, will load and enable
             rendering of this object.
            Sets the initial position of this model to position.
        """
        self.model = loader.loadModel(modelPath)
        self.model.reparentTo(renderer)
        self.model.setPos(*position)
