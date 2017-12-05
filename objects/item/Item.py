from objects.gameObject.GameObject import GameObject

class Item (GameObject):
    """
        Items can be dropped in a space and can occupy a space while another
         creature is in it.
        Any creature that moves into a space with an item in it holds and
         activates the item.
    """

    def __init__ (self, gameManager, cID, **kwargs):
        GameObject.__init__(self, nodeName=str(cID), **kwargs)
        self._gameManager = gameManager
        self._cID = cID

    def activateItem (self, pickupChar):
        """ All item activations are done client side and then synced """
        self._gameManager.getTileMap().pickupItem(self)
        # This method should be overridden in subclasses of items.

    def getItemTypeEnum (self):
        pass # This method should also be overridden in subclasses of items.

    def getCID (self):
        return self._cID
