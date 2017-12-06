from direct.gui.DirectGui import DirectFrame, DirectButton, DirectLabel
from panda3d.core import TextNode, TransparencyAttrib
from objects.defaultConfig.Consts import *

class GameGuide ():
    """
        A display container for the instructions to the game.
    """

    def __init__ (self):
        self._root = None
        self._font = loader.loadFont(PIERCEROMAN_FONT)
        self._draw()

    def _draw (self):
        # Draw fade frame (translucent screen covering):
        winWidth = base.getAspectRatio()
        winHeight = 2
        fColor = (0, 0, 0, 0.5)
        self._root = DirectFrame(pos=(0, 0, 0),
                                      frameSize=(-winWidth, winWidth,
                                                 -winHeight, winHeight),
                                      frameColor=fColor)

        contentHeight = GAMEGUIDE_CONTENT_HEIGHT_PERCENTAGE * winHeight
        contentWidth = GAMEGUIDE_CONTENT_WIDTH_PERCENTAGE * winWidth
        contentText = GAMEGUIDE_TEXT
        guideText = DirectLabel(parent=self._root,
                                pos=(0, 0, 0),
                                frameSize=(-contentWidth, contentWidth,
                                           -contentHeight/2, contentHeight/2),
                                text=contentText,
                                text_scale=GAMEGUIDE_FONT_SIZE,
                                text_font=self._font,
                                text_align=TextNode.ACenter,
                                text_pos=GAMEGUIDE_TEXT_OFFSET,
                                frameTexture=UI_WINDOW,
                                frameColor=(1,1,1,1))
        guideText.setTransparency(TransparencyAttrib.MAlpha)

        cBOffset = GAMEGUIDE_CLOSE_BUTTON_OFFSET
        cbWidth = GAMEGUIDE_CLOSE_BUTTON_SIZE_X
        cbHeight = GAMEGUIDE_CLOSE_BUTTON_SIZE_Y
        closeButton = DirectButton(parent=self._root,
                                   pos=(cBOffset[0], 0, cBOffset[1]),
                                   frameSize=(-cbWidth, cbWidth, -cbHeight,
                                              cbHeight),
                                   text="Close Guide",
                                   text_scale=GAMEGUIDE_FONT_SIZE,
                                   text_font=self._font,
                                   text_pos=GAMEGUIDE_CLOSE_BUTTON_TEXT_OFFSET,
                                   command=self.close,
                                   borderWidth=GAMEGUIDE_BUTTON_BORDER_WIDTH)

    def close(self):
        self._root.destroy()
        del self
