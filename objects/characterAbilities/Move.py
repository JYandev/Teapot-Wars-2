from objects.characterAbilities.BaseAbility import *
from direct.interval.IntervalGlobal import Sequence, Parallel
from direct.interval.LerpInterval import LerpPosInterval
from direct.interval.FunctionInterval import Func
from objects.pathfinding.BFS import findTilesFromTo
from objects.tileMap.TileMap import coordToRealPosition

MOVEMENT_ENERGY_COST = 10

class MoveEffect (Effect):
    """
        Moves a target to a position. Requires a position and an object to move.
        Optionally drains caster's energy bar based on the
         distance traveled.
    """

    @staticmethod
    def doEffect(**kwargs):
        if 'target' in kwargs and 'position' in kwargs and 'tileMap' in kwargs:
            moveTargetToPosition(kwargs['target'], kwargs['position'],
                                 kwargs['tileMap'])

class Move (BaseAbility):
    """
        Moves a target to a position.
    """
    targeterType = Targeter.Path
    baseEnergyCost = 0
    effect = MoveEffect
    #effectParameters = ['target', 'position', 'tileMap']

    @staticmethod
    def getEnergyCost ():
        #if 'path' in kwargs:
        #    return len(kwargs['path'] - 1) * MOVEMENT_ENERGY_COST
        #else:
        return baseEnergyCost

def moveTargetToPosition (caster, position, tileMap):
    """
        Moves caster to position.
        Uses Breadth First Search to get a path to the position.
        Create and play a sequence of intervals to travel from node to node
         until reaching the final tile.
    """
    moveSequence = Sequence()
    # Get list of steps to destination:
    steps = findTilesFromTo(caster.getGridPosition(), position, tileMap)
    # Our algorithm always includes the start position, which we don't want in
    #  this case:
    steps.pop(0)
    print ("From %s\nTo %s\nSteps:\n%s" % (caster.getGridPosition(), position, steps))
    # For every step, create a movement interpolation interval and then update:
    if steps == None:
        print ("NO PATH FOUND") #TODO: Implement case when no path is found!
        return
    for step in steps:
        initialPos = caster.getGridPosition()
        newPos = coordToRealPosition(step)
        moveSequence.append(LerpPosInterval(caster.getCharacter(), 1.0, newPos))
        moveSequence.append(Func(updateObjectLocation, caster.getCharacter(),
                                 initialPos, step, tileMap))
    # Finally, play the movement sequence:
    moveSequence.start()

def updateObjectLocation (node, oldPosition, position, tileMap):
    """
        Puts the node at position in tileMap.
        Removes the reference at the oldPosition.
    """
    tileMap.updateObjectLocation(node, oldPosition, position)
