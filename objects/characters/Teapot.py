from ..gameObject.Creature import Creature
from panda3d.core import LPoint3f
from objects.characters.CharacterType import CharacterType

MODEL_FILE_PATH = "objects/characters/models/Teapot.egg"
MODEL_SCALE = LPoint3f(0.15, 0.15, 0.15)
ANIM_DICT = {
        "walkcycle":"objects/characters/animations/Teapot-walkcycle.egg",
        "heavyAttack":"objects/characters/animations/Teapot-heavyAttack.egg",
        "death":"objects/characters/animations/Teapot-death.egg"}
    # TODO include respawn animation?

class Teapot (Creature):
    def __init__ (self, parentCtrlr, gameManager, cID, **kwargs):
        # Initialize our model and set up our object:
        Creature.__init__(self, parentCtrlr, gameManager, cID,
                          modelPath=MODEL_FILE_PATH, modelScale=MODEL_SCALE,
                          animDict=ANIM_DICT, **kwargs)

    def getCharacterTypeEnum (self):
        return CharacterType.Teapot
