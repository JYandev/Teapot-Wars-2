from direct.task import Task
from objects.defaultConfig.Consts import *
from objects.localPlayer.CameraSystem import calculateOrbit
from objects.tileMap.TileMap import coordToRealPosition
import random

class TileMapOrbiterCam ():
    """
        A camera that orbits around random points in the given TileMap, kind of
         like a spinning dungeon tour guide.
        Used in the background of the Class Selection screen.
    """

    def __init__ (self, tileMap):
        base.disableMouse() # Disable default Panda3D camera controls.
        self._tileMap = tileMap
        self._currentPoint = None
        self._camInstance = base.cam

        self._currentInterval = random.uniform(TILEMAP_ORBITER_MIN_INTERVAL,
                                               TILEMAP_ORBITER_MAX_INTERVAL)
        self._currentTheta = random.uniform(TILEMAP_ORBITER_MIN_VERTICAL_ANGLE,
                                            TILEMAP_ORBITER_MAX_VERTICAL_ANGLE)
        self._currentPhi = 0 # Our orbiting angle
        self._currentDistance = random.uniform(TILEMAP_ORBITER_MIN_DIST,
                                               TILEMAP_ORBITER_MAX_DIST)

        self._orbiterTask = taskMgr.add(self._randomOrbitTask,
                                        "Dungeon Tour Task")

    def _randomOrbitTask (self, task):
        """
            Randomly picks tiles to orbit around and switches at random
             intervals.
        """
        # Decrement our currentTimer
        deltaTime = globalClock.getDt()
        self._currentInterval -= deltaTime
        # Once we run out of time, we pick a new point.
        if self._currentInterval <= 0:
            self._currentPoint = None
            # Reset timer:
            self._currentInterval = random.uniform(TILEMAP_ORBITER_MIN_INTERVAL,
                                                   TILEMAP_ORBITER_MAX_INTERVAL)

        if self._currentPoint == None:
            # Pick a random point
            self._currentPoint = coordToRealPosition(
                                    self._tileMap.getRandomFloor())
            # Randomly pick our angle in a range:
            self._currentTheta = random.uniform(
                                    TILEMAP_ORBITER_MIN_VERTICAL_ANGLE,
                                    TILEMAP_ORBITER_MAX_VERTICAL_ANGLE)
            # Randomly choose our distance in a range:
            self._currentDistance = random.uniform(TILEMAP_ORBITER_MIN_DIST,
                                                   TILEMAP_ORBITER_MAX_DIST)
        else:
            # Keep Rotating around point
            self._currentPhi += deltaTime * TILEMAP_ORBITER_SPEED
            # Set the position based on the previous values:
            newPos = calculateOrbit (self._currentTheta, self._currentPhi,
                                     self._currentDistance, self._currentPoint)
            self._camInstance.setPos(newPos)
            self._camInstance.lookAt(self._currentPoint)
        return task.cont

    def destroy(self):
        """ Destroys this object and cleans up the orbiting task. """
        taskMgr.remove(self._orbiterTask)
        del self
