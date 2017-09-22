from direct.showbase import DirectObject
from direct.task import Task

class Camera (DirectObject.DirectObject):
    """
        Accepts input and controls the camera based on an orbit around a target.
    """
    def __init__ (self, cam):

        self.target = None

        # Accept right mouse orbit input:
        self.accept("mouse3", self._onRightMouseButtonDown)
        self.accept("mouse3-up", self._onRightMouseButtonUp)
        self._lastMousePosX = 0
        self._lastMousePosY = 0
        self._currentOrbitTask = None

    def _onRightMouseButtonDown (self):
        """
            When the right mouse button is pressed, start orbiting the cam.
        """
        if self._currentOrbitTask == None:
            self._currentOrbitTask = taskMgr.add(self._camOrbitTask,
                                                 "Cam Orbit")

    def _onRightMouseButtonUp (self):
        """
            When the right mouse button is released, stop calculating orbit.
        """
        if self._currentOrbitTask != None:
            taskMgr.remove(self._currentOrbitTask)
            self._currentOrbitTask = None

    def _camOrbitTask (self, task):
        """
            Called every frame while the right mouse button is down.
            Updates the camera position by mouse drag around a the current
             target (if any).
        """
        if base.mouseWatcherNode.hasMouse() and self.target != None:
            # Get change in mouse position since last frame:
            currentX = base.mouseWatcherNode.getMouseX()
            currentY = base.mouseWatcherNode.getMouseY()
            deltaX = currentX-self.lastMousePosX
            deltaY = currentY-self.lastMousePosY
            #TODO: Rotate camera with this direction around target. Set lookat

            # Set our lastMousePositions to be the current frame's
            self._lastMousePosX = currentX
            self._lastMousePosY = currentY
        # Repeat task until we are manually destroyed
        return task.cont
