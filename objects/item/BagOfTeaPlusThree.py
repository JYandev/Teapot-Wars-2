from .Item import Item
from .ItemType import ItemType
from panda3d.core import LPoint3f

MODEL_FILE_PATH = "objects/item/models/Teabag.egg"
MODEL_SCALE = LPoint3f(0.1, 0.1, 0.1)

class BagOfTeaPlusThree (Item):
    """
        The BagOfTeaPlusThree is the most powerful item in the game. Holding
         this means the player wins. Yay.
    """
    def __init__ (self, gameManager, cID, **kwargs):
        Item.__init__(self, gameManager, cID,
                      modelPath=MODEL_FILE_PATH, modelScale=MODEL_SCALE,
                      **kwargs)

    def activateItem (self, pickupChar):
        """ All item activations are done client side and then synced """
        Item.activateItem(self, pickupChar)
        self._gameManager.localPlayerWinStateAchieved()

    def getItemTypeEnum (self):
        return ItemType.BagOfTeaPlusThree
