from direct.actor.Actor import Actor
from .CameraSystem import CameraSystem
from objects.characters.Teapot import Teapot
from .InputSystem import InputSystem
from objects.gameUI.BarUI import BarUI
from objects.gameUI.RespawnScreen import RespawnScreen
from objects.gameUI.AbilityBar import AbilityBar
from objects.defaultConfig.Consts import *
from direct.task import Task
import time

class PlayerController ():
    """
        The Player class lets the user play the game.
        Handles client side player systems such as input, camera, and gameplay.
    """
    def __init__ (self, gameManager, cID, initialPos, charClass):
        self._gameManager = gameManager # Reference to gameManager for callbacks
        # Initialize this clients gameObject:
        self._character = Teapot(self, gameManager, cID, coords=initialPos)
        # Assign class and stats:
        self._charClass = charClass
        self._character.setMaxEnergy(PLAYER_MAX_ENERGY)
        # Initialize Camera Input:
        self.cameraSystem = CameraSystem(target=self._character.getNodePath())
        # Initialize the player's Input and UI:
        self.inputSystem = InputSystem(self, gameManager.getTileMap())
        self._energyBar = BarUI(self._character.getNodePath(),
                                ENERGY_BAR_OFFSET, 1,
                                ENERGY_BAR_FG_COLOR, ENERGY_BAR_BG_COLOR)
        self._abilityBar = AbilityBar(self)
        self._respawnScreen = None
        # Register object in the tileMap
        self._gameManager.getTileMap().spawnObject(self._character, initialPos)

        self._lastActionEndTime = 0 # Used for energy recharge delay
        self._energyRecharger = taskMgr.add(self._rechargeEnergyTask,
                                            "Player Energy Recharger")

    def activateAbility (self, abilityIndex):
        """ Called by the AbilityBar on click. Tell the inputSystem to update"""
        self.inputSystem.activateAbility(abilityIndex)

    def onAbilityActivated (self, abilityIndex):
        """ Highlight the activate ability in the AbilityBar """
        self._abilityBar.onAbilityActivated(abilityIndex)

    def onAbilityUsed (self):
        """ Deselects the abilities in the AbilityBar """
        self._abilityBar.deactivateAbilities()

    def updateEnergyBar (self):
        """
            Visually updates the energyBar value.
        """
        percentage = self._character.getEnergy() / PLAYER_MAX_ENERGY
        self._energyBar.setValue(percentage)

    def _rechargeEnergyTask (self, task):
        """
            Recharges the player's energy if they haven't acted for a certain
             delay.
        """
        # If we are currently in an action, simply update the _lastActionEndTime
        if self._character.getCurrentActionSequence():
            self._lastActionEndTime = time.time()
            return task.cont
        # If we are already full, skip this function:
        if self._character.getEnergy() > self._character.getMaxEnergy():
            self._character.setEnergy(self._character.getMaxEnergy())
            self.updateEnergyBar()
            return task.cont
        if time.time() >= self._lastActionEndTime\
                            + PLAYER_ENERGY_RECOVERY_DELAY:
            deltaTime = globalClock.getDt()
            self._character.setEnergy(self._character.getEnergy() + \
                                      PLAYER_ENERGY_RECOVERY_RATE * deltaTime)
            self.updateEnergyBar()
        return task.cont

    def isHostPlayer (self):
        """ Returns whether we are a host player. """
        return self._gameManager.isHost()

    def getClass (self):
        return self._charClass

    def getClassAbilities (self):
        return self._charClass.classAbilities

    def getCharacter (self):
        return self._character

    def onDeath (self):
        """
            Notify the player that they cannot act until a respawn timer is set.
            Start that respawn timer
        """
        # Prevent players from acting:
        self.inputSystem.clearAbility()
        self.inputSystem.setControllable(False)
        taskMgr.remove(self._energyRecharger)
        self._energyRecharger = None
        self._energyBar.removeNode()
        self._energyBar = None
        self._respawnScreen = RespawnScreen(self)

    def respawnRequest (self):
        """
            Sends a respawn request to the server.
        """
        self._gameManager.respawnLocalPlayer(self.getCharacter())

    def onRespawned (self):
        """
            Clientside function called when the controlled creature respawns.
            Reinitializes UI and controls.
        """
        # Remove blocking respawn screen
        self._respawnScreen.close()
        self._respawnScreen = None
        # Enable energy regen and GUIs:
        self._energyBar = BarUI(self._character.getNodePath(),
                                ENERGY_BAR_OFFSET, 1,
                                ENERGY_BAR_FG_COLOR, ENERGY_BAR_BG_COLOR)
        self._energyRecharger = taskMgr.add(self._rechargeEnergyTask,
                                            "Player Energy Recharger")
        # Allow the player to control again:
        self.inputSystem.setControllable(True)

    def syncAction (self, cID, actionID, **kwargs):
        """ Tells gameManager to sync action to the server """
        self._gameManager.onLocalPlayerAction(cID, actionID, **kwargs)

    def onActionStarted (self):
        """ Keeps track of time for energy regen purposes """
        self._lastActionEndTime = time.time()

    def onActionCanceled (self):
        """ Keeps track of time for energy regen purposes """
        self._lastActionEndTime = time.time()
        #TODO: Warn the user that the action canceled prematurely

    def onActionEnded (self):
        """ Keeps track of the action ending """
        self._lastActionEndTime = time.time()
