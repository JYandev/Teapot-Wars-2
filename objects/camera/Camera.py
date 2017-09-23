from direct.showbase import DirectObject
from direct.task import Task
from math import sin, cos, pi
from panda3d.core import LPoint3f

CAM_INITIAL_TARGET_DISTANCE = 15 #TODO: Replace with config
CAM_INTERPOLATION_SPEED = 1 #TODO: Replace with a config
CAMERA_ORBIT_SENSITIVITY = 1 #TODO: REPLACE WITH CONFIG
CAM_INITIAL_RELATIVE_ANGLE = (0.5, 0)

class Camera (DirectObject.DirectObject):
    """
        Accepts input and controls the camera based on an orbit around a target.
    """
    def __init__ (self, cam, target=None):
        self.target = None # This will be a node
        if target:
            self.setTarget(target)
        self.cameraInstance = cam
        # --- Right Mouse Orbit Control ---:
        self.accept("mouse3", self._onRightMouseButtonDown)
        self.accept("mouse3-up", self._onRightMouseButtonUp)
        self._lastMousePosX = 0
        self._lastMousePosY = 0
        self._currentUpdateOrbitTask = None
        self._currentTheta = CAM_INITIAL_RELATIVE_ANGLE[0] # In radians
        self._currentPhi = CAM_INITIAL_RELATIVE_ANGLE[1] # In radians
        self._currentTargetPosition = LPoint3f(0,0,0)
        self._currentDistance = CAM_INITIAL_TARGET_DISTANCE
        # --- ---

        # If we were given a target to initialize with, we look at that target:
        if self.target:
            self._currentTargetPosition = calculateOrbit(
                                            self._currentTheta,
                                            self._currentPhi,
                                            self._currentDistance,
                                            self.target.getPos())

        taskMgr.add(self._cameraFollowTask, "CameraFollowTask")

        #TODO: Eventually optimize this to End once it gets close enough and
        # start when something moves!

    def _onRightMouseButtonDown (self):
        """
            When the right mouse button is pressed, start orbiting the cam.
        """
        # Record the initial mouse position (This is so the cam won't jump):
        self._lastMousePosX = base.mouseWatcherNode.getMouseX()
        self._lastMousePosY = base.mouseWatcherNode.getMouseY()

        if self._currentUpdateOrbitTask == None:
            self._currentUpdateOrbitTask = taskMgr.add(self._updateOrbitTask,
                                                       "UpdateOrbitTask")

    def _onRightMouseButtonUp (self):
        """
            When the right mouse button is released, stop calculating orbit.
        """
        if self._currentUpdateOrbitTask != None:
            taskMgr.remove(self._currentUpdateOrbitTask)
            self._currentUpdateOrbitTask = None

    def setTarget (self, target):
        self.target = target

    def _updateOrbitTask (self, task):
        """
            Called every frame while the right mouse button is down.
            Updates the camera's target position by mouse drag.
            Note, this does not change the camera's position - just the goal.
        """
        if base.mouseWatcherNode.hasMouse() and self.target != None:
            # Get change in mouse position since last frame:
            currentX = base.mouseWatcherNode.getMouseX()
            currentY = base.mouseWatcherNode.getMouseY()
            deltaX = currentX-self._lastMousePosX
            deltaY = currentY-self._lastMousePosY
            self._currentTheta += deltaY * CAMERA_ORBIT_SENSITIVITY
            self._currentPhi -= deltaX * CAMERA_ORBIT_SENSITIVITY
            # Make sure to clamp our values to their proper limits:
            self._clampInputAngles()
            # Calculate our target position:
            self._currentTargetPosition = calculateOrbit(self._currentTheta,
                                                         self._currentPhi,
                                                         self._currentDistance,
                                                         self.target.getPos())
            # Now update our mouse position:
            self._lastMousePosX = currentX
            self._lastMousePosY = currentY
        # Repeat task until we are manually destroyed
        return task.cont

    def _cameraFollowTask (self, task):
        """
            Once started, this task interpolates camera position to reach the
             currentTargetPosition.
        """
        deltaTime = globalClock.getDt()
        newPosition = self.cameraInstance.getPos() * (1-deltaTime) + \
            self._currentTargetPosition * deltaTime
        self.cameraInstance.setPos(newPosition)
        # Aim the camera to face the target:
        self.cameraInstance.lookAt(self.target)
        # Repeat task indefinitely.
        return task.cont

    def _clampInputAngles (self):
        """
            A helper that clamps this instance's currentTheta and Phi.
            Theta, which determines vertical orbit, must be: 0 < phi <= pi/2
            Phi, which determines horizontal orbit, can be any value, but we
             will wrap the numbers around 0 and 2pi anyways.
        """
        # Clamp Theta between [0, pi/2]
        if self._currentTheta < 0.001:
            self._currentTheta = 0.001
        elif self._currentTheta > pi/2:
            self._currentTheta = pi/2
        # Wrap values of Phi around:
        if self._currentPhi < 0:
            self._currentPhi += 2 * pi
        elif self._currentPhi > 2 * pi:
            self._currentPhi -= 2*pi

def calculateOrbit (Theta, Phi, distance, origin):
    """
        Given a 3d position, center, calculates the new point the object will
         occupy given a mouse movement.
    """

    posX = origin[0] + distance * sin(Theta) * cos(Phi)
    posY = origin[1] + distance * sin(Theta) * sin(Phi)
    posZ = origin[2] + distance * cos(Theta)

    return LPoint3f(posX, posY, posZ)
