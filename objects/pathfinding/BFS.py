from panda3d.core import Point2D
"""
    This file is dedicated to any pathfinding functionality.
"""

PATHFINDING_LEGAL_DIRECTIONS = [(-1, 0), (-1, 1), (0, 1), (1, 1),
                                (1, 0), (1, -1), (0, -1), (-1, -1)]

def findTilesFromTo (fromPos, toPos, tileMap):
    """
        Returns a list of grid coordinates to get from fromPos to toPos.
        All calculations are done and returned in grid space (row, col).
        "fromPos" and "toPos" are Point2D inputs.
        Returns None if failed.
    """

    # Do two efficiency checks:
    if not tileMap.isFloor(toPos): return None
    if fromPos == toPos: return None

    visitedNodes = list()
    queue = [[fromPos]] # list of paths to check
    while len(queue) > 0:
        # Check each starting node to ensure we haven't already visited:
        currentPath = queue.pop(0)
        node = currentPath[-1] # Last node in the current Path
        if not node in visitedNodes:
            visitedNodes.append(node)
            # Get list of legal tiles in any legal direction in tileMap
            nextNodes = getLegalTilesInDirections(node, tileMap)
            # We will visit each of these nodes in the next step:
            for nextNode in nextNodes:
                newPath = currentPath[:] # Copy currentPath
                newPath.append(nextNode)
                queue.append(newPath)
                if nextNode == toPos: # If we found our destination!
                    return newPath
    return None

def getLegalTilesInDirections (originCoords, tileMap):
    """
        Returns a list of legal tiles to check based on a current position
         and a tileMap. Takes Point2D inputs.
    """
    newTiles = list()
    for direction in PATHFINDING_LEGAL_DIRECTIONS:
        newTile = Point2D(originCoords.getX()+direction[0],
                          originCoords.getY()+direction[1])
        if not tileMap.isTileOccupied(newTile):
            newTiles.append(newTile)
    return newTiles
