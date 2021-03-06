from external.PyBSP_Dungeon_Generator import pybsp
from objects.gameObject.Creature import Creature
from panda3d.core import Point2D, LVector3f
from panda3d.core import NodePath
import random
from objects.pathfinding.BFS import getAreaTiles

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
                # Values hold whether the tile is a floor or not,
                #  what creatures or blocking objects it holds
                #  and what items occupy the space.
                self._tileMap[Point2D(row, col)] = [newDungeon[row][col],[],[]]
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

    def isTileOccupied (self, coords):
        """
            Returns whether the tile at Point2D coords is occupied or exists.
            If the tile is free and exists, this returns False.
        """
        # Check if tile is a floor:
        if self.isFloor(coords):
            # Check if the tile is free of characters/obstructions:
            tile = self._tileMap[coords]
            if len(tile[1]) == 0:
                return False # Tile exists and free!
        return True # Tile doesn't exist at this spot or is occupied.

    def getTileMap (self):
        return self._tileMap

    def getCreatureAtPos (self, coords):
        """
            Returns the first creature object found at coords, if there are any.
            If there are no creatures at the specified coords, returns None.
        """
        if self.isFloor(coords) and self.isTileOccupied(coords):
            creaturesList = self._tileMap[coords][1]
            for obj in creaturesList:
                if isinstance(obj, Creature):
                    return obj
        # Automatically returns None

    def updateObjectLocation (self, node, oldLocation, newLocation):
        """
            Finds the node at old location and moves it to newLocation.
        """
        if node in self._tileMap[oldLocation][1]:
            self._tileMap[oldLocation][1].remove(node)
        self._tileMap[newLocation][1].append(node)

    def spawnObject (self, node, newLocation):
        self._tileMap[newLocation][1].append(node)

    def spawnItem (self, item, newLocation):
        self._tileMap[newLocation][2].append(item)

    def pickupItem (self, item):
        self._tileMap[item.getGridPosition()][2].remove(item)

    def getItemsAtPosition (self, position):
        """ Returns the list of items at a given position """
        return self._tileMap[position][2]

    def despawnCreature(self, creature):
        """ Removes the creature from this tileMap """
        self._tileMap[creature.getGridPosition()][1].remove(creature)

    def getCharactersAroundPoint (self, point, reach):
        """
            Returns any creatures around point within range.
        """
        creatureList = list()
        tilesToSearch = getAreaTiles(point, self, reach)
        for tile in tilesToSearch:
            creature = self.getCreatureAtPos(tile)
            if creature:
                creatureList.append(creature)
        return creatureList

    def findAdjacentOpenSpaces (self, point):
        """
            Returns points around point that are empty floors.
        """
        openSpaces = list()
        tilesToSearch = getAreaTiles(point, self, 1)
        for tile in tilesToSearch:
            creature = self.getCreatureAtPos(tile)
            if not creature:
                openSpaces.append(tile)
        return openSpaces

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
        return validKeys[random.randint(0, len(validKeys)-1)] # Random inclusive

    def getRandomEmptyFloor (self):
        """
            Picks a random empty floor from the dict.
            Assumes the dungeon has been initialized.
        """
        validKeys = []
        for key in self._tileMap.keys():
            if self._tileMap[key][0] == 1 and len(self._tileMap[key][1]) == 0:
                validKeys.append(key)
        return validKeys[random.randint(0, len(validKeys)-1)] # Random inclusive

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
