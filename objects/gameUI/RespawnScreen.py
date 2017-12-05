from direct.task import Task
from objects.defaultConfig.Consts import *
from panda3d.core import TextNode, TransparencyAttrib
from direct.gui.DirectGui import DirectFrame, DirectLabel, DirectButton
from direct.gui import DirectGuiGlobals as DGG

class RespawnScreen ():
    """
        When created, a respawn screen starts a respawn timer that lets the
         player respawn at a random location.
    """

    def __init__ (self, parentController):
        self._parentController = parentController
        self._countdown = PLAYER_RESPAWN_DELAY
        self._timerText = None
        self._respawnButton = None
        self._fadeFrame = None
        self._font = loader.loadFont(PIERCEROMAN_FONT)
        self._draw() # Draw our GUI
        self._respawnDelayTask = taskMgr.add(self._respawnCountdown,
                                             'LocalPlayerRespawnCountdown')

    def _draw (self):
        # Draw fade frame (translucent screen covering):
        winWidth = base.getAspectRatio()
        winHeight = 2
        fColor = (0, 0, 0, 0.5)
        self._fadeFrame = DirectFrame(pos=(0, 0, 0),
                                      frameSize=(-winWidth, winWidth,
                                                 -winHeight, winHeight),
                                      frameColor=fColor)

        contentSpacing = RESPAWN_SCREEN_CONTENT_SPACING
        contentHeight = RESPAWN_SCREEN_CONTENT_HEIGHT_PERCENTAGE * winHeight
        contentWidth = RESPAWN_SCREEN_CONTENT_WIDTH_PERCENTAGE * winWidth
        # Draw Timer Text:
        tCY = contentSpacing + contentHeight/2
        self._timerText = DirectLabel(parent=self._fadeFrame,
                                pos=(0, 0, tCY),
                                frameSize=(-contentWidth, contentWidth,
                                           -contentHeight, contentHeight),
                                text="",
                                text_scale=RESPAWN_SCREEN_FONT_SIZE,
                                text_font=self._font,
                                text_align=TextNode.ACenter,
                                text_pos=RESPAWN_BUTTON_TEXT_OFFSET,
                                frameTexture=IMG_GRADIENT_1,
                                frameColor=(1,0,1,1))
        self._timerText.setTransparency(TransparencyAttrib.MAlpha)
        # Draw Respawn Button:
        rCY = -tCY
        self._respawnButton = DirectButton(parent=self._fadeFrame,
                                pos=(0, 0, rCY),
                                frameSize=(-contentWidth, contentWidth,
                                           -contentHeight, contentHeight),
                                command=self._onRespawnClicked,
                                text="Respawn",
                                text_scale=RESPAWN_SCREEN_FONT_SIZE,
                                text_font=self._font,
                                text_align=TextNode.ACenter,
                                text_pos=RESPAWN_BUTTON_TEXT_OFFSET)
        self._disableRespawnButton() # Disable the respawn to start

    def _respawnCountdown (self, task):
        deltaTime = globalClock.getDt()
        self._countdown -= deltaTime
        self._timerText['text'] = "%d seconds left until respawn available"\
            % int(self._countdown)
        # Check to see if the countdown has ended:
        if self._countdown <= 0:
            self._timerText['text'] = "Respawn available! Go get 'em!"
            self._enableRespawnButton()
            return task.done # Stop counting down
        else:
            return task.cont # Continue every frame

    def _disableRespawnButton(self):
        self._respawnButton['state'] = DGG.DISABLED
        self._respawnButton['relief'] = DGG.FLAT
        self._respawnButton['color'] = RESPAWN_BUTTON_DISABLED_COLOR

    def _enableRespawnButton(self):
        self._respawnButton['state'] = DGG.NORMAL
        self._respawnButton['relief'] = DGG.RAISED
        self._respawnButton['color'] = RESPAWN_BUTTON_ENABLED_COLOR

    def _onRespawnClicked (self):
        """
            Tells the player controller to respawn.
        """
        self._parentController.respawnRequest()

    def close(self):
        self._fadeFrame.destroy()
        del self
