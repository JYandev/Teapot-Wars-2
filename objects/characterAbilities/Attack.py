from objects.characterAbilities.BaseAbility import *
from direct.interval.IntervalGlobal import Sequence, Parallel
from direct.interval.FunctionInterval import Func
from .ActionID import ActionID

BASIC_ATTACK_ENERGY_COST = 40

class SingleTargetDamageEffect (Effect):
    """
        Damages a target by lowering its health attribute.
        Requires a target object and an amount of damage to inflict.
    """

    @staticmethod
    def doEffect(**kwargs):
        if 'casterObj' in kwargs and 'targetObj' in kwargs\
            and 'damage' in kwargs and 'tileMap' in kwargs:
            singleTargetAttack(kwargs['casterObj'], kwargs['targetPos'],
                               kwargs['damage'], kwargs['tileMap'])

class BasicAttack (BaseAbility):
    """
        Attacks a single nearby target with the creature's base range.
    """
    targeterType = Targeter.SelfReachPosition
    baseEnergyCost = BASIC_ATTACK_ENERGY_COST
    effect = SingleTargetDamageEffect
    actionID = ActionID.BASIC_ATTACK

    @staticmethod
    def getEnergyCost (**kwargs):
        return baseEnergyCost

def inflictDamage (targets, damage):
    """
        Inflicts damage on each of the target objects.
    """
    for target in targets:
        target.takeDamage(damage)

def singleTargetAttack (caster, targetPos, damage, tileMap):
    """
        Makes caster attack target, inflicting damage.
        Drains energy on activation.
    """
    target = tileMap.getCreatureAtPos(targetPos)
    # Safety check:
    if target == None:
        return
    attackSequence = Sequence() # Create a new Sequence
    # Check for energy availability:
    attackSequence.append(Func(checkDrainEnergy, caster,
                               attackClass.getEnergyCost))
    # Deal damage server-side and sync:
    attackSequence.append(Func(syncAction, caster, BasicAttack.actionID,
                               target=target, damage=damage))
    #TODO Attack animation
    attackSequence.append(Func(endAction, caster)) # Apply end signal to action.
    caster.startAction(attackSequence)
