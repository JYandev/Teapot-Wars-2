from objects.defaultConfig.Consts import *
from panda3d.core import TextNode, TransparencyAttrib
from direct.gui.DirectGui import DirectFrame, DirectLabel, DirectButton

class WinScreen ():
    """
        When created, a respawn screen starts a respawn timer that lets the
         player respawn at a random location.
    """

    def __init__ (self, gameManager, winnerData):
        self._gameManager = gameManager
        self._fadeFrame = None
        self._font = loader.loadFont(PIERCEROMAN_FONT)
        self._draw(winnerData) # Draw our GUI

    def _draw (self, winnerData):
        # Draw fade frame (translucent screen covering):
        winWidth = base.getAspectRatio()
        winHeight = 2
        fColor = (0, 0, 0, 0.5)
        self._fadeFrame = DirectFrame(pos=(0, 0, 0),
                                      frameSize=(-winWidth, winWidth,
                                                 -winHeight, winHeight),
                                      frameColor=fColor)

        contentHeight = WINSCREEN_CONTENT_HEIGHT_PERCENTAGE * winHeight
        contentWidth = WINSCREEN_CONTENT_WIDTH_PERCENTAGE * winWidth
        winnerText = ("%s Has Obtained the Legendary Bag of Tea - Plus Three."\
                "\nSubmit Now to Your New Ruler, Mortals!") % winnerData.cName
        self._winnerText = DirectLabel(parent=self._fadeFrame,
                                pos=(0, 0, WINSCREEN_WINTEXT_Y_OFFSET),
                                frameSize=(-contentWidth, contentWidth,
                                           -contentHeight, contentHeight),
                                text=winnerText,
                                text_scale=WINSCREEN_FONT_SIZE,
                                text_font=self._font,
                                text_align=TextNode.ACenter,
                                text_pos=WINSCREEN_WINTEXT_TEXT_OFFSET,
                                frameTexture=IMG_GRADIENT_1,
                                frameColor=(1,1,1,1))
        self._winnerText.setTransparency(TransparencyAttrib.MAlpha)

    def close(self):
        self._fadeFrame.destroy()
        del self
