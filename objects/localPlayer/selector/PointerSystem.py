from direct.showbase.ShowBase import Plane, Vec3, Point3, Point2D
from .Selector import Selector
from objects.characterAbilities.BaseAbility import Targeter
from objects.pathfinding.BFS import findTilesFromTo

#SELECTOR_TINT = [0.5, 0.5, 1, 1]
HIGHLIGHTER_TINT = [1, 0.5, 0.5, 1]
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
        self._highlightMode = None # Targeter reference
        self._highlightModeParams = None # Targeter params dict
        self._highlightedTiles = list() # List of tile highlighted by pointer.

        # Perform mouse raycasting every frame:
        taskMgr.add(self._updateHovered, "mouseScanning")

    def _updateHovered (self, task):
        """
            Updates the position of the Highlighter selector based on mouse
             position.
            Only updates if the value should change. Should not call every frame
             unless the user can shake his/her mouse really fast between tiles.
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
                    self._highlightTiles()
                elif self._hoveredCoord != None and\
                                         not self._tileMap.isFloor(highlCoords):
                    self._hoveredCoord = None
                    self._highlightTiles()
        return task.cont

    def setHighightMode (self, mode, params=None):
        """
            Sets the current method of highlighting nodes given a mode.
            Params allow for customizations specific to each mode, such as range
             or AOE size.
        """
        self._highlightMode = mode
        self._highlightModeParams = params

    def resetHighlightMode (self):
        """
            Resets highlight mode to None and removes all highlighted tiles.
        """
        self._highlightMode = None
        self._highlightModeParams = dict()
        # Remove all previous highlights:
        while len(self._highlightedTiles) > 0:
            selector = self._highlightedTiles.pop(0)
            selector.destroy()

    def _highlightTiles (self):
        """
            Highlights the tiles given by list of tile positions as highlighted
             by the player's pointer.
            Highlights in different ways depending on the highlightMode
        """
        # Remove all previous highlights:
        while len(self._highlightedTiles) > 0:
            selector = self._highlightedTiles.pop(0)
            selector.destroy()
        # Depending on the highlight mode, fill a list of highlighted positions:
        coordsList = list() # List of Point2D()

        if self._highlightMode == Targeter.SelfPath and\
                                  self._hoveredCoord != None:
            # coordsList is the path to the tile from the current position.
            fromPos = self._highlightModeParams['origin']
            if self._hoveredCoord != fromPos:
                coordsList = findTilesFromTo(fromPos, self._hoveredCoord,
                                             self._tileMap)
        if coordsList != None:
            count = 0
            for coord in coordsList:
                newHighlight = Selector("HighL %d" % count, HIGHLIGHTER_TINT)
                newHighlight.showAt(coord)
                self._highlightedTiles.append(newHighlight)
                count += 1

    def getHovered (self):
        return self._hoveredCoord
