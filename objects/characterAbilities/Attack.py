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
        if 'casterObj' in kwargs and 'targetPos' in kwargs\
            and 'damage' in kwargs and 'tileMap' in kwargs\
            and 'attackClass' in kwargs:
            singleTargetAttack(kwargs['casterObj'], kwargs['targetPos'],
                               kwargs['damage'], kwargs['tileMap'],
                               kwargs['attackClass'])

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
        return BasicAttack.baseEnergyCost

def inflictDamage (targets, damage):
    """
        Inflicts damage on each of the target objects.
    """
    for target in targets:
        target.takeDamage(damage)

def singleTargetAttack (caster, targetPos, damage, tileMap, attackClass):
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
                               targetCID=target.getCID(), damage=damage))
    #TODO Attack animation
    attackSequence.append(Func(endAction, caster)) # Apply end signal to action.
    caster.startAction(attackSequence)

def singleTargetAttackSync (targetObject, **kwargs):
    """
        Played clientside on a creature that makes an attack.
        If this is run on the host machine, damage is dealt and health is synced
        Returns the sequence described above.
    """

    # Create and Play animation sequence on targetObject:
    newSequence = Sequence()
    #TODO Create and Play animation sequence on targetObject
    newSequence.append(Func(endAction, targetObject))

    attackTarg = kwargs['target']
    print("ATTACK SYNCING. Attacker:", targetObject.getCID(), " Defender: ",
          attackTarg.getCID())
    if kwargs['isServer'] == True: # Deal damage and sync!
        print("AM SERVER. DEAL THE DAMAGE")
        inflictDamage([attackTarg], kwargs['damage'])
        # TODO: SYNC
    return newSequence
