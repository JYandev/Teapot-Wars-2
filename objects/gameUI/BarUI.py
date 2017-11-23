from panda3d.core import CardMaker
from panda3d.core import NodePath

UI_BAR_SCALE = 1 # TODO: Throw into Consts

class BarUI (NodePath):
    """
        Class for creating a world-space floating bar UI.
        Health Bar code based on "Wannes" version here:
        https://www.panda3d.org/forums/viewtopic.php?p=19902
    """
    def __init__(self, parent, offset=(0, 0, 0), value=1, fgColor=(1,1,1,1),
                 bgColor=(0,0,0,1)):
            self.scale = UI_BAR_SCALE
            NodePath.__init__(self, 'healthbar')
            # Create the foreground rect:
            cmfg = CardMaker('fg')
            cmfg.setFrame(-self.scale,  self.scale,
                          -0.1 * self.scale, 0.1 * self.scale)
            self.fg = self.attachNewNode(cmfg.generate())
            # Create the background rect:
            cmbg = CardMaker('bg')
            cmbg.setFrame(-self.scale, self.scale,
                          -0.1 * self.scale, 0.1 * self.scale)
            self.bg = self.attachNewNode(cmbg.generate())
            """# Create the preview rect:
            cmpv = CardMaker('pv')
            cmpv.setFrame(-self.scale, self.scale,
                          -0.1 * self.scale, 0.1 * self.scale)
            self.pv = self.attachNewNode(cmpv.generate())"""

            # Set colors and values:
            self.fg.setColor(*fgColor)
            self.bg.setColor(*bgColor)
            """self.pv.setColor(*pvColor)"""
            self.setValue(value)
            # Set this bar to follow the transform of the parent.
            self.reparentTo(parent)
            # Offset this bar (most likely to above the parent)
            self.setPos(parent, offset)
            # Make this bar face the camera at all times (bill-boarding):
            self.setBillboardPointEye()

    def setValue(self, value):
            value = min(max(0, value), 1)
            self.fg.setScale(value * self.scale, 0.001, self.scale)
            self.bg.setScale(self.scale * (1.0 - value), 0.001, self.scale)
            self.fg.setX((value - 1) * self.scale * self.scale)
            self.bg.setX(value * self.scale * self.scale)
