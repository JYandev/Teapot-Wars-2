"""
    This file is dedicated to any pathfinding functionality.
"""

PATHFINDING_LEGAL_DIRECTIONS = [(-1, 0), (1, 0), (0, 1), (0, -1)]

def findTilesFromTo (fromPos, toPos, tileMap):
    """
        Returns a list of grid coordinates to get from fromPos to toPos.
        All calculations are done and returned in grid space (row, col).
    """
    visitedNodes = list()
    queue = [fromPos]
    while len(queue) > 0:
        # Check each starting node to ensure we haven't already visited:
        node = queue.pop(0)
        if not node in visitedNodes:
            visitedNodes.add(node)
            #TODO: get list of legal tiles in any legal direction in tileMap
            #TODO: queue.extend([ABOVE LIST])
    return visitedNodes # This will return the smallest path.
