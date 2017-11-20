from objects.characterAbilities import *
class BaseClass ():
    """
        This class is meant to be held by any character and represents the
         character's class. A class holds abilities and base attributes.
        All specific classes are subclasses of this object.
    """
    classDesc = """A Base Class. Doesn't have any abilities.
...Except for being super()"""
    classDescFontSize = (0.075, 0.075)
    classDescWrap = 19
    classAbilities = []

class Barbarian (BaseClass):
    classDesc = \
    """A wild warrior who wields a cruel fork, the Barbarian is a good choice for players wishing to charge head-first into the enemy.
Also, the Barbarian's table manners are the worst."""
    classDescFontSize = (0.05, 0.05)
    classDescWrap = 27
    classAbilities = [Move]
