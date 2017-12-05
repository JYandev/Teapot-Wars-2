from direct.gui.DirectGui import DirectFrame, DirectLabel
from panda3d.core import TextNode
from objects.defaultConfig.Consts import *

class AbilityBar ():
    """
        Displays the player's abilities and their numbered hotkeys.
    """

    def __init__ (self, cClass):
        self._root = None
        self._abilityIcons = [] # We tint these when player activates ability
        self._draw(cClass)

    def _draw (self, cClass):
        # Draw frame:
        winWidth = base.getAspectRatio()
        winHeight = 2

        cW = ABILITYBAR_WIDTH_PERCENTAGE * winWidth
        cH = ABILITYBAR_HEIGHT_PERCENTAGE * winHeight
        cColor = (0.5, 0.5, 0.5, ABILITYBAR_ALPHA)
        cX = winWidth - cW/2
        cY = -winHeight/2 + cH/2
        self._root = DirectFrame(pos=(cX, 0, cY),
                                 frameSize=(-cW/2, cW/2, -cH/2, cH/2),
                                 frameColor=cColor,
                                 suppressMouse=0)
        # Draw buttons and numbers based on the abilities of cClass:
        count = 0 # Hotkeys start from 1, so we will just add 1 to text.
        hkSize = ABILITYBAR_HOTKEY_SIZE
        bCXStart = winWidth - cW + hkSize
        for ability in cClass.classAbilities:
            icon = ability.actionIcon
            cX = bCXStart + count * hkSize
            newHotkey = DirectLabel(pos=(cX, 0, cY),
                                    frameSize=(-hkSize/2, hkSize/2, -hkSize/2,
                                               hkSize/2),
                                    frameTexture=icon)
            self._abilityIcons.append(newHotkey)
            count += 1

    def onAbilityActivated (self, abilityIndex):
        pass

    def close (self):
        print ("CLOSE UNIMPLEMENTED!") #TODO Implement close for AbilityBar
