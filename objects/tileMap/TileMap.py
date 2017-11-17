from external.PyBSP_Dungeon_Generator import pybsp
from panda3d.core import Point2D, LVector3f
from panda3d.core import NodePath
import random

# --- Tile Const ---
TILE_SIZE = 1
TILE_HEIGHT = 1
MODEL_FILE_PATH = "objects/tileMap/tile/Tile.egg"
TEXTURE_PATH = "objects/tileMap/tile/Tile-Diffuse.png"
# --- ---

class TileMap ():
    def __init__ (self, tileMap = None):
        self.np = NodePath("TileMap")
        self._tileModel = base.loader.loadModel(MODEL_FILE_PATH)
        self._tileTexture = base.loader.loadTexture(TEXTURE_PATH)
        self._tileModel.setTexture(self._tileTexture)
        self._tileMap = dict()
        self._tileMap2D = None
        self._generateMap(tileMap) # Create our map and fill np with real geometry.
        self._tileModel.clearModelNodes() # Mandatory processing of the model
        self.np.flattenStrong() # Used to optimize rendering.
        self.np.reparentTo(render) # Start rendering this map

    def _generateMap (self, tileMap = None):
        """
            Generates a new map (or a given one) for rendering.
            Optionally takes in a flat string representation (Use in networking)
        """
        if tileMap == None:
            # Create 2d list dungeon with pybsp:
            newDungeon = pybsp.generateDungeon2DList((100, 100), (20, 20))
            self._tileMap2D = newDungeon
        else:
            tileMap = convertDungeonFromString(tileMap, 100)
            self._tileMap2D = tileMap
            newDungeon = tileMap
        # Use the output to fill our tileMap dict.
        for row in range(len(newDungeon)):
            for col in range(len(newDungeon[row])):
                self._tileMap[Point2D(row, col)] = [newDungeon[row][col], []]
                if newDungeon[row][col] == 1: # Create tile models along the way
                    placeholder = self.np.attachNewNode("Tile(%s,%s)"\
                        %(row, col))
                    placeholder.setPos(row*TILE_SIZE, col*TILE_SIZE, 1)
                    self._tileModel.instanceTo(placeholder)

    def isFloor (self, coords):
        """
            Returns whether the given Point2D is a valid tile in the tileMap
        """
        if coords in self._tileMap.keys():
            if self._tileMap[coords][0] == 1:
                return True
        return False

    def getTileMap (self):
        return self._tileMap

    def getTileMapStr (self):
        """
            Used to send map layout across the network. Essentially flattens the
             2D list into a string of 0s and 1s.
        """
        newString = "".join(str(tile) for row in self._tileMap2D for tile in row)
        return newString

    def getRandomFloor (self):
        """
            Picks a random floor from the dict.
            Assumes the dungeon has been initialized.
        """
        validKeys = []
        for key in self._tileMap.keys():
            if self._tileMap[key][0] == 1:
                validKeys.append(key)
        return validKeys[random.randint(0, len(validKeys))]

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

def convertDungeonFromString (tileMap, size):
    """
        Converts from a dungeon string to a 2D list.
        Used in network optimization.
    """
    new2DList = []
    for row in range(size):
        subList = []
        for col in range(size):
            subList.append(int(tileMap[row*size+col]))
        new2DList.append(subList)
    return new2DList
