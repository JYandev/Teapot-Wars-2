"""
    Static Global Utilities related to the TileMap (used to seperate imports).
"""

TILE_SIZE = 1
TILE_HEIGHT = 1 # TODO Find some better way of storing this and the duplicate in TileMap.py

from panda3d.core import Point2D, LVector3f
def coordToRealPosition (coords):
    """
        Converts coordinate position (Point2D) to real space (LVector3f)
        This gets the center of the tile.
    """
    newTileStart = coords
    newTileEnd = Point2D(newTileStart.getX() + TILE_SIZE,
                         newTileStart.getY() + TILE_SIZE)
    tileCenter = (newTileStart + newTileEnd) / 2
    return LVector3f(tileCenter.getX(), tileCenter.getY(), TILE_HEIGHT)

def tileWithinRange (origin, reach, target):
    """
        Returns true if the target is within range in all directions from origin
    """
    # Since we count diagonals as 1, we simply calculate the x and y components
    #  seperately:
    xDist = abs(origin.getX() - target.getX())
    yDist = abs(origin.getY() - target.getY())
    # As long as each component is below or equal to the range, we are good:
    if xDist <= reach and yDist <= reach:
        return True
    return False
