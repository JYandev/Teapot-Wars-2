from panda3d.core import NodePath, TextNode
from objects.defaultConfig.Consts import *

class NameDisplay ():
    """
        Floating name display above a creature.
    """
    def __init__(self, originObj, offset, name):
            self._root = NodePath('nameDisplay')
            # Offset this text node (most likely to above the origin)
            self._root.setPos(originObj, *offset)
            self._root.reparentTo(base.render)
            # Configure text and assign color:
            font = loader.loadFont(PIERCEROMAN_FONT)
            self._textNode = TextNode('NameDisplayText')
            self._textNode.setText(name)
            self._textNode.setAlign(TextNode.ACenter)
            self._textNode.setFont(font)
            self._textNodePath = self._root.attachNewNode(self._textNode)
            self._textNodePath.setScale(NAME_DISPLAY_SCALE)
            self._textNodePath.setColor(NAME_DISPLAY_COLOR)
            # Make this bar face the camera at all times (bill-boarding):
            self._textNodePath.setBillboardPointEye()

    def destroy (self):
        """ Destroys this object """
        self._root.removeNode()
        del self
