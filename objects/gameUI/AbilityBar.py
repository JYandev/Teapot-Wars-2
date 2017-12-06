from direct.gui.DirectGui import DirectFrame, DirectButton
from panda3d.core import TextNode
from objects.defaultConfig.Consts import *
from direct.gui import DirectGuiGlobals as DGG

class AbilityBar ():
    """
        Displays the player's abilities and their numbered hotkeys.
    """

    def __init__ (self, parentController):
        self._parentController = parentController
        self._root = None
        self._abilityIcons = [] # We tint these when player activates ability
        self._font = loader.loadFont(PIERCEROMAN_FONT)
        self._draw(self._parentController.getClass())

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
        cY = -winHeight/2 + hkSize/2
        for ability in cClass.classAbilities:
            icon = ability.actionIcon
            cX = bCXStart + count * hkSize
            if count != 0: # Add spacing after first element:
                cX += ABILITYBAR_SPACING
            newHotkey = DirectButton(pos=(cX, 0, cY),
                                     frameSize=(-hkSize/2, hkSize/2, -hkSize/2,
                                               hkSize/2),
                                     frameTexture=icon,
                                     text=str(count+1),
                                     text_font=self._font,
                                     text_scale=ABILITYBAR_HOTKEY_SCALE,
                                     text_pos=ABILITYBAR_HOTKEY_OFFSET,
                                     text_align=TextNode.ACenter,
                                     relief=DGG.FLAT,
                                     command=self._activateAbility,
                                     extraArgs=[count],
                                     suppressMouse=1,
                                     frameColor=ABILITYBAR_DEFAULT_COLOR)
            self._abilityIcons.append(newHotkey)
            count += 1

    def _activateAbility (self, abilityIndex):
        """
            User clicked to activate an ability, let the playercontroller know!
        """
        self._parentController.activateAbility(abilityIndex)

    def onAbilityActivated (self, abilityIndex):
        # Deactivate all abilities:
        self.deactivateAbilities()
        # Activate the one at abilityIndex:
        self._abilityIcons[abilityIndex]['frameColor'] = ABILITYBAR_ACTIVE_COLOR

    def deactivateAbilities (self):
        for icon in self._abilityIcons:
            icon['frameColor'] = ABILITYBAR_DEFAULT_COLOR

    def close (self):
        self._root.destroy()
        for icon in self._abilityIcons:
            icon.destroy()
        del self
