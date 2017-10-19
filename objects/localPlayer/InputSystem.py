from direct.showbase import DirectObject
from direct.showbase.ShowBase import Plane, Vec3, Point3, CardMaker, Point2D
from direct.task import Task
from .selector.Selector import Selector

SELECTOR_TINT = [0.5, 0.5, 1, 1]
HIGHLIGHTER_TINT = [1, 0.5, 0.5, 1]

class InputSystem (DirectObject.DirectObject):
    """
        Handles all input except for camera controls.
    """
    def __init__ (self, tileMap):
        self._groundPlane = Plane(Point3(0, 0, 1), Point3(0, 0, 1))
        self._selectedTileCoord = None
        self._hoveredTileCoord = None
        taskMgr.add(self._getMouseCoord, "mouseScanning")
        self._tileMap = tileMap
        self._selector = Selector("Selector", SELECTOR_TINT)
        self._highlighter = Selector("Highlighter", HIGHLIGHTER_TINT)

    def _getMouseCoord (self, task):
        if base.mouseWatcherNode.hasMouse():
            mPos = base.mouseWatcherNode.getMouse()
            pos3D = Point3() # Output stored here.
            nearPoint = Point3()
            farPoint = Point3()
            base.camLens.extrude(mPos, nearPoint, farPoint) # Create a line
            # Check for intersection:
            if self._groundPlane.intersectsLine(pos3D,
                    render.getRelativePoint(base.cam, nearPoint),
                    render.getRelativePoint(base.cam, farPoint)):
                self._hoveredTileCoord = Point2D(int(pos3D.x), int(pos3D.y))
                self._highlightHovered()
        return task.cont

    def _setTileMap (self, tileMap):
        self._tileMap = tileMap

    def _highlightHovered (self):
        """
            Highlights the tile at self._hoveredTileCoord, if there is one.
        """
        if self._tileMap.isFloor(self._hoveredTileCoord):
            self._highlighter.showAt(self._hoveredTileCoord)
        else:
            self._highlighter.hide()
