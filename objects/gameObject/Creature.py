from ..gameObject.GameObject import GameObject
from panda3d.core import LPoint3f
from objects.defaultConfig.Consts import *
from objects.gameUI.DamageText import DamageText
from objects.gameUI.BarUI import BarUI

class Creature (GameObject):
    """
        All living, optionally controllable creatures in the game.
    """
    def __init__ (self, parentCtrlr, gameManager, cID, **kwargs):
        # Initialize our model and set up our object:
        GameObject.__init__(self, nodeName=str(cID), **kwargs)

        # Initialize creature specific:
        self._parentController = parentCtrlr
        self._gameManager = gameManager
        self._cID = cID

        # Apply default creature stats:
        self._maxEnergy = CREATURE_DEFAULT_MAX_ENERGY
        self._energy = self._maxEnergy
        self._reach = CREATURE_DEFAULT_REACH
        self._baseDamage = CREATURE_BASE_DAMAGE
        self._maxHealth = CREATURE_DEFAULT_MAX_HEALTH
        self._health = self._maxHealth

        self._healthBar = BarUI(self.getNodePath(), HEALTH_BAR_OFFSET, 1,
                                HEALTH_BAR_FG_COLOR, HEALTH_BAR_BG_COLOR)

        self._actionQueue = []
        self._currentActionSequence = None

    def takeDamage (self, damage):
        """
            Takes damage.
            If this creature's HP drops to below 0, plays a death sequence and
             syncs across the network.
        """
        print("OUCH ", damage)
        newHealth = self._health - damage
        self.onHPModified(newHealth) # This will update health
        if self._health <= 0:
            print("CREATURE DIED: ", self.getCID())
            #TODO: Death sequence

    def onHPModified (self, newValue):
        """
            Changes HP to be the newValue and creates damage/heal floating text.
            Called by the current network controller when the host attempts to
             sync damage/healing.
        """
        print("SYNCING HP, ", newValue)
        change = newValue - self._health
        self._health = newValue
        DamageText(self.getNodePath(), -change) # Spawn damage text
        percentage = self._health / self.getMaxHealth()
        self._healthBar.setValue(percentage)
        if self._gameManager: # Sync that we took damage
            self._gameManager.onCreatureHealthChanged(self)

    def getDamage (self):
        """
            Final base damage output is based on equipped weapons.
            Actual damage dealt depends on the ability and its multiplier(s)
        """
        return self._baseDamage #TODO Make this depend on equipped weapon/class

    def startAction (self, actionSequence):
        """ Assigns and starts the current action sequence """
        print(self._actionQueue)
        if self._currentActionSequence:
            self._actionQueue.append(actionSequence)
        else:
            self._currentActionSequence = actionSequence
            self._currentActionSequence.start()

    def cancelAction (self):
        """
            Aborts the current Action. Tells the parentController that something
             happened.
            Also continues to the next queued action (if possible)
        """
        if self._currentActionSequence:
            self._currentActionSequence.pause()
            self._currentActionSequence = None
            self._parentController.onActionCanceled() #TODO: IF IT EXISTS
        # Start next queued action
        if len(self._actionQueue) > 0:
            newAction = self._actionQueue.pop(0)
            self.startAction(newAction)

    def endCurrentAction (self):
        """
            Similar to cancel, but doesn't warn the user because no stuns/energy
             limits were occured.
            Also continues to the next queued action (if possible)
        """
        if self._currentActionSequence:
            self._currentActionSequence = None
        # If we have a parent Controller, let them know we've ended:
        if self._parentController:
            self._parentController.onActionEnded()
        # Start next queued action:
        if len(self._actionQueue) > 0:
            newAction = self._actionQueue.pop(0)
            self.startAction(newAction)

    def syncAction (self, actionID, **kwargs):
        """ Tells the parentController to sync the action with the server """
        self._parentController.syncAction(self.getCID(), actionID, **kwargs)

    def getParentController(self):
        return self._parentController

    def getCurrentActionSequence(self):
        return self._currentActionSequence

    def getHealth (self):
        return self._health

    def getMaxHealth (self):
        return self._maxHealth

    def getEnergy (self):
        return self._energy

    def getReach (self):
        return self._reach

    def getMaxEnergy(self):
        return self._maxEnergy

    def setEnergy (self, amount):
        self._energy = amount

    def setMaxEnergy (self, amount):
        self._maxEnergy = amount

    def loopAnim (self, animName):
        """ Attempts to loop an anim if this object is an actor """
        print(self.getActor().getPos())
        actor = self.getActor()
        if actor != None:
            actor.loop(animName)

    def stopAnim (self):
        actor = self.getActor()
        if actor != None:
            actor.stop()

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

    def __hash__ (self):
        return hash(self._cID)

    def __eq__ (self, other):
        if not isinstance(other, Creature):
            return False
        return self._cID == other.getCID()
