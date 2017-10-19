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
        self._selectedTileCoords = None
        self._hoveredTileCoords = None
        taskMgr.add(self._updateHighlighter, "mouseScanning")
        self._tileMap = tileMap
        self._selector = Selector("Selector", SELECTOR_TINT)
        self._highlighter = Selector("Highlighter", HIGHLIGHTER_TINT)

        self.accept("mouse1", self._onMouseButtonDown)

    def _onMouseButtonDown(self):
        """
            Handler for mouse presses.
        """
        if (self._hoveredTileCoords):
            # Select the tile we are hovering over:
            self.selectTileAt(self._hoveredTileCoords)
        else:
            # Deselect tile:
            self.selectTileAt(None)

    def selectTileAt(self, coords):
        """
            Updates the _selector to highlight the given coordinates if coords
             are not none.
            If coords are None, then we hide the _selector.
        """
        self._selectedTileCoords = coords
        if self._selectedTileCoords:
            self._selector.showAt(self._selectedTileCoords)
            self._setHoveredAt(None) # Remove the last highlighter
        else:
            self._selector.hide()

    def _updateHighlighter (self, task):
        """
            Updates the position of the Highlighter selector based on mouse
             position.
        """
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
                highlCoords = Point2D(int(pos3D.x), int(pos3D.y))
                if highlCoords != self._selectedTileCoords and\
                    self._tileMap.isFloor(highlCoords):
                    self._setHoveredAt(highlCoords)
                else:
                    self._setHoveredAt(None)

        return task.cont

    def _setTileMap (self, tileMap):
        self._tileMap = tileMap

    def _setHoveredAt (self, hoveredTileCoords):
        """
            Sets and highlights the tile at hoveredTileCoords, if coords are
             given.
            Assumes due to earlier processes that we are either given valid
             floor coords or None.
            If None is given as the coords, we set this instance's coords to
             None and hide the highlighter.
        """
        self._hoveredTileCoords = hoveredTileCoords
        if self._hoveredTileCoords:
            self._highlighter.showAt(self._hoveredTileCoords)
        else:
            self._highlighter.hide()
