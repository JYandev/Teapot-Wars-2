from BaseAbility import *
from direct.interval.IntervalGlobal import Sequence

class Move (BaseAbility):
    """
        Moves a target to a position.
    """
    targeterType = Targeter.Position
    baseEnergyCost = 0
    effect = MoveEffect

    @staticmethod
    def getEnergyCost ():
        return baseEnergyCost


class MoveEffect (Effect):
    """
        Moves a target to a position. Requires a position and an object to move.
        Optionally drains caster's energy bar based on the
         distance traveled.
    """

    @staticmethod
    def doEffect(**kwargs):
        if 'target' in kwargs and 'position' in kwargs:
            moveTargetToPosition(kwargs['target'], kwargs['position'])

def moveTargetToPosition (caster, position):
    """
        Moves caster to position.
        Uses Breadth First Search to get a path to the position.
        Create and play a sequence of intervals to travel from node to node
         until reaching the final tile.
    """
    pass
