from direct.actor.Actor import Actor
from .CameraSystem import CameraSystem
from objects.characters.Teapot import Teapot
from .InputSystem import InputSystem
from objects.gameUI.BarUI import BarUI
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
        base.disableMouse() # Disables default Panda3D camera control
        # Initialize this clients gameObject:
        self._character = Teapot(self, cID, coords=initialPos)
        # Initialize Camera Input:
        self.cameraSystem = CameraSystem(target=self._character.getNodePath())
        # Initialize the player's Input and UI:
        self.inputSystem = InputSystem(self, gameManager.getTileMap())
        self._energyBar = BarUI(self._character.getNodePath(),
                                ENERGY_BAR_OFFSET, 1,
                                ENERGY_BAR_FG_COLOR, ENERGY_BAR_BG_COLOR)
        # Register object in the tileMap
        self._gameManager.getTileMap().spawnObject(self._character, initialPos)
        # Assign class and stats:
        self._charClass = charClass
        self._character.setMaxEnergy(PLAYER_MAX_ENERGY)

        self._currentActionSequence = None
        self._lastActionEndTime = 0 # Used for energy recharge delay
        self._energyRecharger = taskMgr.add(self._rechargeEnergyTask,
                                            "Player Energy Recharger")

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
        if self._currentActionSequence:
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

    def getClass (self):
        return self._charClass

    def getClassAbilities (self):
        return self._charClass.classAbilities

    def getCharacter (self):
        return self._character

    def startAction (self, actionSequence):
        """ Assigns and starts the current action sequence """
        #TODO Figure out what to do when action is already running!
        self._currentActionSequence = actionSequence
        self._currentActionSequence.start()
        self._lastActionEndTime = time.time()

    def cancelCurrentAction (self):
        """ Cancels the _currentActionSequence """
        if self._currentActionSequence:
            self._currentActionSequence.pause()
            self._currentActionSequence = None
            self._lastActionEndTime = time.time()
            #TODO: Warn the user that the action canceled prematurely

    def endCurrentAction (self):
        """
            Similar to cancel, but doesn't warn the user because no stuns/energy
             limits were occured.
        """
        if self._currentActionSequence:
            self._currentActionSequence = None
            self._lastActionEndTime = time.time()
