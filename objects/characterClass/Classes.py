from objects.characterAbilities import *
from .ClassID import ClassID
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
    classID = ClassID.BASECLASS
    classIcon = "objects/characterClass/icons/WizardIcon.png"

class Barbarian (BaseClass):
    classDesc = \
    """A wild warrior who wields a cruel fork, the Barbarian is a good choice for players wishing to charge head-first into the enemy.
Also, the Barbarian's table manners are the worst."""
    classDescFontSize = (0.05, 0.05)
    classDescWrap = 27
    classAbilities = [Move, BasicAttack]
    classID = ClassID.BARBARIAN
    classIcon = "objects/characterClass/icons/BarbarianIcon.png"

class Thief (BaseClass):
    classDesc = \
    """Uh oh, someone has been in the cookie jar again!
The thief uses stealth to gain an edge on opponents."""
    classDescFontSize = (0.05, 0.05)
    classDescWrap = 27
    classAbilities = [Move, BasicAttack]
    classID = ClassID.THIEF
    classIcon = "objects/characterClass/icons/ThiefIcon.png"

class Wizard (BaseClass):
    classDesc = \
    """The Wizard is the master of all magic. Wizards can cook up all kinds of spells, but specialize in area effects."""
    classDescFontSize = (0.05, 0.05)
    classDescWrap = 27
    classAbilities = [Move, BasicAttack]
    classID = ClassID.WIZARD
    classIcon = "objects/characterClass/icons/WizardIcon.png"
