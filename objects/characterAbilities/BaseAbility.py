class BaseAbility ():
    """
        Every ability has two main parts:
            * A Targeter (self, area, position, etc)
            * An Effect (Movement, Damage, Both, etc.)
        The way an ability should be used is to first check getEnergyCost to see
         if caster has enough energy. If so, then we call
         Ability.effect.doEffect, passing in any necessary arguments.
    """
    targeterType = None
    baseEnergyCost = 0
    effect = None

    @staticmethod
    def getEnergyCost (**kwargs):
        return baseEnergyCost

class Targeter ():
    """
        Represents a target of an ability. This static class uses class
         attributes to create an enum type variable.
    """
    Self = 1
    Position = 2
    Area = 3
    Path = 4
    SelfPath = 5
    SelfReachPosition = 6 # Pick a position within a certain range around self

class Effect ():
    """
        Represents an effect of an ability. Effects have a "doEffect" function
         that vary by sub-class.
    """

    @staticmethod
    def doEffect (caster, **kwargs):
        pass

def checkDrainEnergy (caster, energyDrainFunction):
    """
        Checks if the energy drain on the caster can be completed, otherwise,
         cancels the currentAction.
    """
    if not caster.drainEnergy(energyDrainFunction()):
        caster.cancelAction()

def syncAction (caster, actionID, **actionKwargs):
    """
        Syncs the given action across the network.
    """
    caster.syncAction(actionID, **actionKwargs)

def endAction (caster):
    """
        Place this at the end of an action sequence to signal to the caster that
         the action has ended.
    """
    caster.endCurrentAction()
