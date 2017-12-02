import random
from direct.task import Task
from objects.characters.Teapot import Teapot
from objects.defaultConfig.Consts import *
import time, random
from objects.characterAbilities.Move import Move
from objects.tileMap.TileMapUtilities import getDistance, tileWithinRange
from objects.pathfinding.BFS import getAreaTiles
from objects.characterAbilities.Attack import BasicAttack

class EnemyController ():
    """
        Enemy controllers do exactly what there name implies - they act as the
         AI controller for the NPCs.
        Each enemy controller makes decisions on an interval which is randomly
         chosen after a decision is made. Decisions are limited, of course, by
         the character's energy level.
        These controllers should only be running on the Host player's game.
         the actions of these creatures should only be synced to the remote
         clients.
    """
    def __init__(self, gameManager, cID, initialPos):
        self._gameManager = gameManager # Reference to gameManager for callbacks
        self._character = Teapot(self, gameManager, cID, coords=initialPos)
        # Register object in the tileMap
        self._tileMap = gameManager.getTileMap()
        self._tileMap.spawnObject(self._character, initialPos)

        # Assign stats:
        self._character.setMaxEnergy(ENEMY_MAX_ENERGY)

        self._lastActionEndTime = 0 # Used for energy recharge delay
        self._energyRecharger = taskMgr.add(self._rechargeEnergyTask,
                                            "Player Energy Recharger")
        initialTickDelay = self.getRandomTickDelay()
        self._aiTickTask = taskMgr.doMethodLater(initialTickDelay, self._aiTick,
                                                 "Enemy AI tick: " + cID)

        # AI State variables:
        self._knownTargets = set() # The set of found targets.
        self._currentTarget = None

    def _aiTick (self, task):
        """
            The core function of the AI decision making. This is called every so
             often on a random 'tick'.
        """
        # Scan around and locate new targets:
        self._performSearchUpdate()
        # Filter out targets that are too far away:
        self._performOutOfRangeFilter()
        if self._character._currentActionSequence != None:
            task.delayTime = self.getRandomTickDelay()
            return task.again
        print(self._knownTargets, self._currentTarget)
        if self._currentTarget != None:
            myPos = self._character.getGridPosition()
            targetPos = self._currentTarget.getGridPosition()
            if getDistance(myPos, targetPos) > 1:
                # Move to the target if they are too far.
                self._considerMove(True)
            else:
                # Attack the target:
                self._considerAttack()
        else:
            # Pick a target based on distance:
            newTarget = self._getClosestKnownTarget()
            if newTarget != None:
                self._currentTarget = newTarget
            else:
                self._considerMove(False)

        task.delayTime = self.getRandomTickDelay()
        return task.again

    def _considerMove (self, chase):
        """
            Considers a move action and decides based on energy and other
             factors
        """
        if Move.getEnergyCost() <= self._character.getEnergy():
            if chase:
                self._chaseDecision()
            else:
                self._roamDecision()

    def _considerAttack (self):
        """
            Considers an attack action and decides based on energy and other
             factors.
        """
        if BasicAttack.getEnergyCost() <= self._character.getEnergy():
            self._attackDecision()

    def _attackDecision (self):
        """
            Performs an attack on the currentTarget
        """
        char = self.getCharacter()
        params = {'targetPos' : self._currentTarget.getGridPosition(),
                  'casterObj' : char,
                  'tileMap' : self._tileMap,
                  'damage' : char.getDamage(),
                  'attackClass' : BasicAttack,
                  'isServer' : True} # isServer always true on EnemyController
        BasicAttack.effect.doEffect(**params)

    def _roamDecision (self):
        """
            The AI has decided to roam randomly
        """
        roamTiles = getAreaTiles(self._character.getGridPosition(),
                                 self._tileMap, ENEMY_AI_ROAM_MAX_RANGE)
        if len(roamTiles) == 0: return
        chosenRoam = roamTiles[random.randint(0, len(roamTiles) - 1)]
        # Move to the chosen position:
        params = {'targetPos' : chosenRoam,
                  'casterObj' : self.getCharacter(),
                  'tileMap' : self._tileMap}
        Move.effect.doEffect(**params)

    def _chaseDecision (self):
        """
            The AI has decided to chase the current player.
        """
        # Choose a random adjacent position next to the player:
        chosenPositions = self._tileMap.findAdjacentOpenSpaces(
                        self._currentTarget.getGridPosition())
        if len(chosenPositions) == 0: return
        chosenPosition = chosenPositions[random.randint(0,
                                         len(chosenPositions) - 1)]
        # Move to the chosen position:
        params = {'targetPos' : chosenPosition,
                  'casterObj' : self.getCharacter(),
                  'tileMap' : self._tileMap}
        Move.effect.doEffect(**params)

    def getRandomTickDelay (self):
        """
            Gets the next random tick between constant bounds.
        """
        nextTickTime = random.uniform(ENEMY_AI_TICK_DELAY_RANGE[0],
                                      ENEMY_AI_TICK_DELAY_RANGE[1])
        return nextTickTime

    def _performSearchUpdate(self):
        """
            Updates our found players based on a radius-based search.
        """
        foundCharacters = self._tileMap.getCharactersAroundPoint(
                            self.getCharacter().getGridPosition(),
                            ENEMY_AI_SIGHT_RANGE)
        print("foundCharacters: ", foundCharacters)
        foundPlayers = self._findPlayersFromList(foundCharacters)
        # Add any players within range to the set of known players:
        for player in foundPlayers:
            self._knownTargets.add(player)

    def _performOutOfRangeFilter (self):
        """
            Filters out any found players that have gone out of range.
        """
        myPos = self._character.getGridPosition()
        newKnownTargets = self._knownTargets.copy()
        for target in self._knownTargets:
            targetPos = target.getGridPosition()
            if not tileWithinRange(myPos, ENEMY_AI_SIGHT_LOSS_RANGE, targetPos):
                newKnownTargets.remove(target)
                # Also check to see if we lost our current target:
                if target == self._currentTarget:
                    self._currentTarget = None
        self._knownTargets = newKnownTargets

    def _findPlayersFromList (self, characterList):
        """
            Returns the players in characterList
        """
        pcList = list()
        for character in characterList:
            if not isinstance(character.getParentController(), EnemyController):
                pcList.append(character)
        return pcList

    def _getClosestKnownTarget (self):
        """
            Attempts to find the closest known player. Returns none if there are
             no players.
        """
        closestTarget = None
        closestRange = None
        myPos = self._character.getGridPosition()
        for target in self._knownTargets:
            targetPos = target.getGridPosition()
            targetDist = getDistance(myPos, targetPos)
            if closestRange == None or targetDist < closestRange:
                closestTarget = target
                closestRange = targetDist
        return closestTarget

    def _rechargeEnergyTask (self, task):
        """
            Recharges the enemy's energy if they haven't acted for a certain
             delay.
        """
        # If we are currently in an action, simply update the _lastActionEndTime
        if self._character.getCurrentActionSequence():
            self._lastActionEndTime = time.time()
            return task.cont
        # If we are already full, skip this function:
        if self._character.getEnergy() > self._character.getMaxEnergy():
            self._character.setEnergy(self._character.getMaxEnergy())
            return task.cont
        if time.time() >= self._lastActionEndTime\
                            + ENEMY_ENERGY_RECOVERY_DELAY:
            deltaTime = globalClock.getDt()
            self._character.setEnergy(self._character.getEnergy() + \
                                      ENEMY_ENERGY_RECOVERY_RATE * deltaTime)
        return task.cont

    def getCharacter (self):
        return self._character

    def updateEnergyBar (self):
        """
            Function that must be overridden to receive messages but otherwise
             should do nothing since enemy energy bars are not displayed.
        """
        pass

    def syncAction (self, cID, actionID, **kwargs):
        """ Tells gameManager to sync action to the server """
        print("SYNCING ACTION", cID, actionID, kwargs)
        self._gameManager.onLocalPlayerAction(cID, actionID, **kwargs)

    def onActionStarted (self):
        """ Keeps track of time for energy regen purposes """
        self._lastActionEndTime = time.time()

    def onActionCanceled (self):
        """ Keeps track of time for energy regen purposes """
        self._lastActionEndTime = time.time()

    def onActionEnded (self):
        """ Keeps track of the action ending """
        self._lastActionEndTime = time.time()
