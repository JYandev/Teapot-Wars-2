from direct.gui.DirectGui import DirectFrame, DirectRadioButton, DirectLabel
from objects.defaultConfig.Consts import *
from panda3d.core import TransparencyAttrib, TextNode

class ClassPicker ():
    """
        A user interface that lets the character choose a class.
        4 Classes are drawn and only one at a time can be toggled/selected
    """

    def __init__ (self):
        self._font = loader.loadFont(PIERCEROMAN_FONT)
        self._draw()

    def _draw (self):
        winWidth = base.getAspectRatio() * 2
        winHeight = 2
        # Draw main container:
        cFSizeX, cFSizeY = winWidth/4, winHeight*(3/4)
        containFrame = DirectFrame(pos=(0, 0, cFSizeY*(2/3)),
                                    frameSize=(-cFSizeX, cFSizeX , -cFSizeY, 0),
                                    frameTexture=UI_WINDOW)
        containFrame.setTransparency(TransparencyAttrib.MAlpha)

        # Title:
        titleWidth, titleHeight = cFSizeX - CPKR_CONTROL_SIDES_MARGIN,\
                                  cFSizeY*CPKR_TITLE_HEIGHT_RATIO
        titleFontSize = (0.15, 0.15)
        title = DirectLabel(parent=containFrame,
                            pos=(0, 0, -CPKR_CONTROL_TOP_MARGIN),
                            frameSize=(-titleWidth, titleWidth,
                                       -titleHeight, 0),
                            text_align=TextNode.ACenter,
                            text_font=self._font,
                            text_scale=titleFontSize,
                            text_pos=CPKR_PIERCEROMAN_OFFSET_TC,
                            text="Choose a Class!")

        # Information Box:
        infoHeight = cFSizeY*CPKR_INFO_HEIGHT_RATIO
        # Calculate Button Frame vertical size first!
        bFSizeY = cFSizeY - (CPKR_CONTROL_TOP_MARGIN*2 + titleHeight\
                               + infoHeight)
        infoFontSize = (0.075, 0.075)
        info = DirectLabel(parent=containFrame,
                           pos=(0, 0,
                              -CPKR_CONTROL_TOP_MARGIN - titleHeight - bFSizeY),
                           frameSize=(-titleWidth, titleWidth,\
                                      -infoHeight, 0),
                           text_align=TextNode.ALeft,
                           text_font=self._font,
                           text_scale=infoFontSize,
                           text_pos=CPKR_PIERCEROMAN_OFFSET_TL,
                           text_wordwrap=CPKR_INFO_WRAP,
                           text="...adf asdf asd fasd fasd ...adf asdf asd fasd fasd...adf asdf asd fasd fasd...adf asdf asd fasd fasd...adf asdf asd fasd fasd")

        # Class Radio Button Frame:
        bFColor = (0.25,0.25,0.25,0.5)
        buttonFrame = DirectFrame(parent=containFrame,
                            pos=(0, 0, -CPKR_CONTROL_TOP_MARGIN - titleHeight),
                            frameSize=(-0.5, 0.5, -bFSizeY, 0),
                            frameColor=bFColor)

        # Class Radio Buttons



    def getSelected (self):
        pass

    def close (self):
        pass
