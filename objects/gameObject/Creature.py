from ..gameObject.GameObject import GameObject
from panda3d.core import LPoint3f
from objects.defaultConfig.Consts import *

class Creature (GameObject):
    """
        All living, optionally controllable creatures in the game.
    """
    def __init__ (self, parentCtrlr, cID, **kwargs):
        # Initialize our model and set up our object:
        GameObject.__init__(self, nodeName=str(cID), **kwargs)

        self._parentController = parentCtrlr
        self._cID = cID

        # Apply default creature stats:
        self._maxEnergy = CREATURE_MAX_ENERGY
        self._energy = self._maxEnergy

        self._currentActionSequence = None

    def startAction (self, actionSequence):
        """ Assigns and starts the current action sequence """
        #TODO Figure out what to do when action is already running! Put in queue!?!? Tell player he/she cannot do that?!?!?
        self._currentActionSequence = actionSequence
        self._currentActionSequence.start()

    def cancelAction (self):
        """
            Aborts the current Action. Tells the parentController that something
             happened.
        """
        if self._currentActionSequence:
            self._currentActionSequence.pause()
            self._currentActionSequence = None
            self._parentController.onActionCanceled() #TODO: IF IT EXISTS

    def endCurrentAction (self):
        """
            Similar to cancel, but doesn't warn the user because no stuns/energy
             limits were occured.
        """
        if self._currentActionSequence:
            self._currentActionSequence = None
        self._parentController.onActionEnded()

    def syncAction (self, actionID, **kwargs):
        """ Tells the parentController to sync the action with the server """
        self._parentController.syncAction(self.getCID(), actionID, **kwargs)

    def getParentController(self):
        return self._parentController

    def getCurrentActionSequence(self):
        return self._currentActionSequence

    def getEnergy (self):
        return self._energy

    def getMaxEnergy(self):
        return self._maxEnergy

    def setEnergy (self, amount):
        self._energy = amount

    def setMaxEnergy (self, amount):
        self._maxEnergy = amount

    def drainEnergy (self, energyCost):
        """
            Drains energy and returns true if there was enough energy for the
             action.
            If there is not enough energy to perform the action, returns false
             and activates a UI warning.
        """
        if self._energy - energyCost < 0:
            # TODO: Perform energy warning!
            return False
        else:
            self._energy -= energyCost
            # If we have a parent controller, tell it to update UI
            if self._parentController:
                self._parentController.updateEnergyBar()
            return True

    def getCID (self):
        return self._cID

    def __eq__ (self, other):
        if not isinstance(other, Creature):
            return False
        return self._cID == other.getCID()
