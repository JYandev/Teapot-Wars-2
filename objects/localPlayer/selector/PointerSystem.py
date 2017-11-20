from direct.showbase.ShowBase import Plane, Vec3, Point3, Point2D
from .Selector import Selector

#SELECTOR_TINT = [0.5, 0.5, 1, 1]
#HIGHLIGHTER_TINT = [1, 0.5, 0.5, 1]
#TODO Put the above in Consts

class PointerSystem ():
    """
        Handles user pointer (mouse) input. Contains information and
         functionality related to selecting and highlighting tiles.
    """
    def __init__ (self, tileMap):
        self._tileMap = tileMap
        self._groundPlane = Plane(Point3(0, 0, 1), Point3(0, 0, 1))
        self._hoveredCoord = None # The coordinates we are hovering over.
        self.highlightMode = 0 # off
        self._pointedHighLTiles = list() # List of tile highlighted by pointer.
        self._availHighLTiles = list() # List of tiles highlighted as available.
        #Selector("Selector", SELECTOR_TINT)

        taskMgr.add(self._updateHovered, "mouseScanning")

    def _updateHovered (self, task):
        """
            Updates the position of the Highlighter selector based on mouse
             position.
        """
        if base.mouseWatcherNode.hasMouse(): # If mouse is in the window:
            # Draw a line from the point on screen through the camera to the
            #  imaginary plane and check for intersections:
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
                # Ensure the calculated position is a valid tile:
                if self._hoveredCoord != highlCoords and\
                        self._tileMap.isFloor(highlCoords):
                    self._hoveredCoord = highlCoords
                elif not self._tileMap.isFloor(highlCoords):
                    self._hoveredCoord = None
        return task.cont

    def setHighightMode (self):
        pass

    def highlightAvailableTiles (self, coordsList):
        """
            Highlights the tiles given by list of tile positions as available.
        """
        pass

    def highlightPointedTiles (self, coordsList):
        """
            Highlights the tiles given by list of tile positions as highlighted
             by the player's pointer.
        """
        #Selector("Selector", SELECTOR_TINT)
        pass
