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
    def __init__ (self):
        self.np = NodePath("TileMap")
        self.tileMap = dict()
        self._tileModel = base.loader.loadModel(MODEL_FILE_PATH)
        self._tileTexture = base.loader.loadTexture(TEXTURE_PATH)
        self._tileModel.setTexture(self._tileTexture)
        self._generateMap() # Create our map and fill np with real geometry.
        self._tileModel.clearModelNodes() # Mandatory processing of the model
        self.np.flattenStrong() # Used to optimize rendering.
        self.np.reparentTo(render) # Start rendering this map

    def _generateMap (self):
        # Create 2d list dungeon with pybsp:
        newDungeon = pybsp.generateDungeon2DList((100, 100), (20, 20))
        # Use the output to fill our tileMap dict.
        for row in range(len(newDungeon)):
            for col in range(len(newDungeon[row])):
                self.tileMap[Point2D(row, col)] = [newDungeon[row][col], []]
                if newDungeon[row][col] == 1: # Create tile models along the way
                    placeholder = self.np.attachNewNode("Tile(%s,%s)"\
                        %(row, col))
                    placeholder.setPos(row*TILE_SIZE, col*TILE_SIZE, 1)
                    self._tileModel.instanceTo(placeholder)

    def isFloor (self, coords):
        """
            Returns whether the given Point2D is a valid tile in the tileMap
        """
        if coords in self.tileMap.keys():
            if self.tileMap[coords][0] == 1:
                return True
        return False

    def getRandomFloor (self):
        """
            Picks a random floor from the dict.
            Assumes the dungeon has been initialized.
        """
        validKeys = []
        for key in self.tileMap.keys():
            if self.tileMap[key][0] == 1:
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
