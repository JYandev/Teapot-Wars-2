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
        if 'targetNode' in kwargs and 'targetPos' in kwargs\
                                  and 'tileMap' in kwargs:
            moveTargetToPosition(kwargs['targetNode'], kwargs['targetPos'],
                                 kwargs['tileMap'])

class Move (BaseAbility):
    """
        Moves a target to a position.
    """
    targeterType = Targeter.SelfPath
    baseEnergyCost = MOVEMENT_ENERGY_COST
    effect = MoveEffect

    @staticmethod
    def getEnergyCost (**kwargs):
        # Energy cost of movement is dependent on the amount of spaces moved:
        if 'path' in kwargs:
            return len(kwargs['targetPath'] - 1) * MOVE.baseEnergyCost
        else:
            return Move.baseEnergyCost

def moveTargetToPosition (caster, position, tileMap):
    """
        Moves caster to position.
        Uses Breadth First Search to get a path to the position.
        Create and play a sequence of intervals to travel from node to node
         until reaching the final tile.
        Drains energy on each move:
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
    initialPos = caster.getGridPosition()
    count = 0
    for step in steps:
        lastPos = initialPos if count == 0 else steps[count-1]
        newPos = coordToRealPosition(step)
        moveSequence.append(Func(checkDrainEnergy, caster, Move.getEnergyCost))
        moveSequence.append(LerpPosInterval(caster.getCharacter(), 1.0, newPos)) #TODO make 1.0 a speed constant
        moveSequence.append(Func(updateObjectLocation, caster,
                                 lastPos, step, tileMap))
        count += 1
    moveSequence.append(Func(endAction, caster)) # Apply end signal to action.
    # Finally, play the movement sequence:
    caster.startAction(moveSequence)

def updateObjectLocation (node, oldPosition, position, tileMap):
    """
        Puts the node at position in tileMap.
        Removes the reference at the oldPosition.
    """
    tileMap.updateObjectLocation(node, oldPosition, position)
    node.updateGridPosition(position)
