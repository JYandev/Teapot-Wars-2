from panda3d.core import NodePath, TextNode, LVector3f
from direct.task import Task
from objects.defaultConfig.Consts import *
import random

class DamageText ():
    """
        Floating damage/healing text that changes color based on whether the
         given value is - (healing) or + (damage).
        Automatically destroys itself after some amount of time.
    """
    def __init__(self, originObj, value, offset=(0, 0, 1)):
            self._root = NodePath('damageText')
            # Offset this text node (most likely to above the origin)
            self._root.setPos(originObj, *offset)
            self._root.reparentTo(base.render)
            # Configure text and assign color:
            font = loader.loadFont(PIERCEROMAN_FONT)
            self._textNode = TextNode('DamageTextText')
            self._textNode.setText(str(value))
            self._textNode.setAlign(TextNode.ACenter)
            self._textNode.setFont(font)
            self._textNodePath = self._root.attachNewNode(self._textNode)
            self._textNodePath.setScale(DAMAGE_TEXT_SCALE)
            self._textNodePath.setColor(self._getColorByValue(value))
            # Set initial physics variables:
            self._dx = random.uniform(-1, 1) * DAMAGE_TEXT_JUMP_VARIATION
            self._dy = random.uniform(-1, 1) * DAMAGE_TEXT_JUMP_VARIATION
            self._dz = DAMAGE_TEXT_INITIAL_JUMP_VELOCITY

            # Make this bar face the camera at all times (bill-boarding):
            self._textNodePath.setBillboardPointEye()

            self._physicsTask = taskMgr.add(self._applyPhysicsTask,
                                            'damagetText_physics')

            # Set the object to die in a constant time:
            taskMgr.doMethodLater(DAMAGE_TEXT_DESPAWN_DELAY, self._destroyTask,
                                  'damageText_timedDespawn')

    def _applyPhysicsTask(self, task):
        """ Changes our velocity to simulate physics """
        deltaTime = globalClock.getDt()
        # Start physics simulation on object:
        self._dz += DAMAGE_TEXT_GRAVITY * deltaTime
        newTranslation = LVector3f(self._dx, self._dy, self._dz)
        self._root.setPos(self._root.getPos()+newTranslation)
        return task.cont

    def _getColorByValue (self, value):
        """ Returns a color dependent on value """
        if value < 0:
            return DAMAGE_TEXT_COLOR_HEAL
        elif value == 0:
            return DAMAGE_TEXT_COLOR_NEUTRAL
        else:
            return DAMAGE_TEXT_COLOR_DAMAGE

    def _destroyTask (self, task):
        """ Destroys this object """
        taskMgr.remove(self._physicsTask) # End the physics task
        self._root.removeNode()
        del self
