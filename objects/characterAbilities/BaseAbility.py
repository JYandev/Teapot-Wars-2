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
    def getEnergyCost ():
        return baseEnergyCost

class Targeter ():
    """
        Represents a target of an ability. This static class uses class
         attributes to create an enum type variable.
    """
    Self = 1
    Position = 2
    Area = 3

class Effect ():
    """
        Represents an effect of an ability. Effects have a "doEffect" function
         that vary by sub-class.
    """

    @staticmethod
    def doEffect (caster, **kwargs):
        pass
