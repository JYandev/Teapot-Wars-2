from .Teapot import Teapot
from .CharacterType import CharacterType

CHARACTER_TYPES_TO_CLASS = {CharacterType.Teapot:Teapot}

def getCharacterTypeAsClass(charType):
    """ Returns the class associated with the given integer """
    return CHARACTER_TYPES_TO_CLASS[charType]
