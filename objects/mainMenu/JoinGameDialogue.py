from direct.gui.DirectGui import DirectFrame, DirectButton, DirectEntry,\
                                 DirectLabel
from panda3d.core import TransparencyAttrib, TextNode
from objects.defaultConfig.DefaultConfig import *
from objects.defaultConfig.StaticPaths import *

class JoinGameDialogue ():
    """
        The options pop-up used when the player presses the MainMenu's
         "Join Party" button.
        The client can be configured in many ways, including:
         * Display Name
         * Host IP Address
         * Game Password
    """

    def __init__ (self, confirmHandler):
        # Draw this GUI on object creation.
        self._confirmHandler = confirmHandler # The callback handler to this GUI
        self._ipAddressEntry = None # Reference to the IP Address Text Entry
        self._font = loader.loadFont(PIERCEROMAN_FONT)
        self._elements = []
        self._draw()

    def _draw (self):
        """
            Draws this JoinGameDialogue
        """

        winWidth = base.getAspectRatio() * 2
        winHeight = 2
        # Draw translucent background frame to block clicks:
        blockingFrame = DirectFrame(parent=base.a2dTopLeft,
                                    frameSize=(0, winWidth, -winHeight, 0),
                                    frameColor=(0,0,0,0.5))
        # Draw Main Dialogue Frame:
        dFOffsetY = 0.05
        dFSizeX, dFSizeY = winWidth*(3/5), winHeight*(2/3)
        dialogueFrame = DirectFrame(pos=(-dFSizeX/2, 0, dFSizeY/2+dFOffsetY),
                                    frameSize=(0, dFSizeX, -dFSizeY, 0),
                                    frameTexture=UI_WINDOW)
        dialogueFrame.setTransparency(TransparencyAttrib.MAlpha)
        # Draw Title Text:
        verticalMargin = 0.102
        titleWidth = dFSizeX
        titleHeight = 0.15
        titleFontSize = (0.15, 0.15)
        dialogueTitle = DirectLabel(parent=dialogueFrame,
                                    pos=(dFSizeX/2, 0, -verticalMargin),
                                    frameSize=(-titleWidth/2,
                                               titleWidth/2,
                                               -titleHeight/2,
                                               titleHeight/2),
                                    text_align=TextNode.ACenter,
                                    text_font=self._font,
                                    text_scale=titleFontSize,
                                    text_pos=PIERCEROMAN_OFFSET,
                                    text="Join Party Configuration")
        # Draw Back Button:
        buttonVerticalMargin = 0.203
        buttonHeight = 0.2
        buttonPosY = -1 - buttonVerticalMargin
        sidesMargin = 0.1
        buttonWidth = dFSizeX/2 - sidesMargin/2
        backButton = DirectButton(parent=dialogueFrame,
                                  pos=(dFSizeX/2 - buttonWidth/2, 0,
                                       -1 - buttonVerticalMargin),
                                  frameSize=(-buttonWidth/2,
                                             buttonWidth/2,
                                             -buttonHeight/2,
                                             buttonHeight/2),
                                  command=self._close)
        # Draw Connect Button:
        connButton = DirectButton(parent=dialogueFrame,
                                  pos=(dFSizeX/2 + buttonWidth/2, 0,
                                       -1 - buttonVerticalMargin),
                                  frameSize=(-buttonWidth/2,
                                             buttonWidth/2,
                                             -buttonHeight/2,
                                             buttonHeight/2))
        # Add parent elements to be deleted in self._close()
        self._elements.extend([blockingFrame, dialogueFrame])

    def _close(self):
        """
            Closes this window and deletes all elements inside.
        """
        print("CLOSING UNIMPLEMENTED")
        for element in self._elements:
            print(element)
            element.destroy()
