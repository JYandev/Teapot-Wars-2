from objects.characterAbilities.BaseAbility import *
from direct.interval.IntervalGlobal import Sequence, Parallel
from direct.interval.LerpInterval import LerpPosInterval
from direct.interval.FunctionInterval import Func, Wait
from objects.pathfinding.BFS import findTilesFromTo
from objects.tileMap.TileMapUtilities import coordToRealPosition
from .ActionID import ActionID
from panda3d.core import Point2D

MOVEMENT_ENERGY_COST = 10

class MoveEffect (Effect):
    """
        Moves a target to a position. Requires a position and an object to move.
        Optionally drains caster's energy bar based on the
         distance traveled.
    """

    @staticmethod
    def doEffect(**kwargs):
        if 'casterObj' in kwargs and 'targetPos' in kwargs\
                                  and 'tileMap' in kwargs:
            moveTargetToPosition(kwargs['casterObj'], kwargs['targetPos'],
                                 kwargs['tileMap'])

class Move (BaseAbility):
    """
        Moves a target to a position using pathfinding.
    """
    targeterType = Targeter.SelfPath
    baseEnergyCost = MOVEMENT_ENERGY_COST
    effect = MoveEffect
    actionID = ActionID.MOVE
    actionIcon = "objects/characterAbilities/icons/MoveIcon.png"

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
    # Safety Check:
    if steps == None:
        print ("NO PATH FOUND") #TODO: Implement case when no path is found! Perhaps cancel caster targeter!
        return
    # Our algorithm always includes the start position, which we don't want in
    #  this case:
    steps.pop(0)
    # For every step, create a movement interpolation interval and then update:
    initialPos = caster.getGridPosition()
    count = 0
    for step in steps:
        lastPos = initialPos if count == 0 else steps[count-1]
        newPos = coordToRealPosition(step)
        moveSequence.append(Func(checkDrainEnergy, caster, Move.getEnergyCost))
        moveSequence.append(Wait(0.1))
        moveSequence.append(Func(syncAction, caster, Move.actionID,
                                 coords=(step[0], step[1])))
        moveSequence.append(Func(updateObjectLocation, caster,
                                 lastPos, step, tileMap))
        moveSequence.append(Func(playMoveAnim, caster, step))
        moveSequence.append(LerpPosInterval(caster.getNodePath(), 1.0, newPos)) #TODO make 1.0 a speed constant
        moveSequence.append(Func(pickupAnyItems, caster, tileMap))
        moveSequence.append(Func(stopMoveAnim, caster))
        count += 1
    moveSequence.append(Func(endAction, caster)) # Apply end signal to action.
    # Finally, play the movement sequence:
    caster.startAction(moveSequence)

def playMoveAnim (caster, point):
    """ Play move anim and face correct direction """
    caster.facePointIgnoreXY(point)
    caster.loopAnim('walkcycle')

def stopMoveAnim (caster):
    caster.stopAnim()

def moveSync (targetObject, **kwargs):
    """
        Given a target Object and coords, simply syncs this movement by playing
         an interval. Called by a network message.
        Returns the moveSync interval action
    """
    lastPos = targetObject.getGridPosition()
    coords = Point2D(kwargs['coords'][0], kwargs['coords'][1])
    newSequence = Sequence()
    newSequence.append(Func(updateObjectLocation, targetObject, lastPos, coords,
                            kwargs['tileMap']))
    newSequence.append(Func(playMoveAnim, targetObject, coords))
    newSequence.append(LerpPosInterval(targetObject.getNodePath(), 1.0,
                                       coordToRealPosition(coords)))
    newSequence.append(Func(stopMoveAnim, targetObject))
    # Apply end signal to action:
    newSequence.append(Func(endAction, targetObject))
    return newSequence

def pickupAnyItems (targetObject, tileMap):
    """
        Should be called right after a local client move is complete.
        Activates any pickups in the targetObject's current space.
    """
    items = tileMap.getItemsAtPosition(targetObject.getGridPosition())
    for item in items:
        item.activateItem(targetObject)

def updateObjectLocation (targetObj, oldPosition, position, tileMap):
    """
        Puts the targetObj at position in tileMap.
        Removes the reference at the oldPosition.
    """
    tileMap.updateObjectLocation(targetObj, oldPosition, position)
    targetObj.updateGridPosition(position)
