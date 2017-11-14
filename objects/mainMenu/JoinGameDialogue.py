from direct.gui.DirectGui import DirectFrame, DirectButton, DirectEntry,\
                                 DirectLabel
from panda3d.core import TransparencyAttrib, TextNode
from objects.defaultConfig.DefaultConfig import *
from objects.defaultConfig.Consts import *

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
        self._userNameEntry = None # Reference to the User Name Text Entry
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

        self._drawControls(dialogueFrame) # Draw options for the pop-up frame.

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
                                             buttonHeight/2),
                                  command=self._onConnectButton)
        # Add parent elements to be deleted in self._close()
        self._elements.extend([blockingFrame, dialogueFrame])

    def _drawControls (self, dialogueFrame):
        """ Draw Helper that draws client settings controls """
        iTopMrgn = JOPTS_CONTROL_TOP_MARGIN
        spacing = JOPTS_CONTROL_SPACING
        height = JOPTS_CONTROL_HEIGHT
        width = dialogueFrame.getWidth()
        # Create containers for UI:
        ipFrame = DirectFrame(parent=dialogueFrame,
                              pos=(width/2, 0, -iTopMrgn - spacing),
                              frameSize=(-width/2, width/2, -height/2,
                                         height/2))
        nameFrame = DirectFrame(parent=dialogueFrame,
                                pos=(width/2, 0, -iTopMrgn - spacing * 2),
                                frameSize=(-width/2, width/2, -height/2,
                                           height/2))
        # Create the UI:
        ctrlWidth = ipFrame.getWidth()*(1/3)
        ctrlFontSize = (0.15, 0.15)
        self._ipAddressEntry = DirectEntry(parent=ipFrame,
                               pos=(ctrlWidth/2-ctrlWidth*1, 0, 0),
                               frameSize=(0, ctrlWidth*2, -height/2, height/2),
                               text_font=self._font,
                               text_scale=ctrlFontSize,
                               text_pos=PIERCEROMAN_OFFSET,
                               initialText=DEFAULT_IP_ADDRESS,
                               width=8,
                               cursorKeys=1,
                               numLines=1)
        ipLabel = DirectLabel(parent=ipFrame,
                              pos=(ctrlWidth-ctrlWidth*2, 0, 0),
                              frameSize=(-ctrlWidth/2, ctrlWidth/2, -height/2,
                                         height/2),
                              text="Host IP:",
                              text_font=self._font,
                              text_scale=ctrlFontSize,
                              text_pos=PIERCEROMAN_OFFSET,
                              frameColor=(0.25,0.5,0.5,1))

        self._userNameEntry = DirectEntry(parent=nameFrame,
                              pos=(ctrlWidth/2-ctrlWidth*1, 0, 0),
                              frameSize=(0, ctrlWidth*2, -height/2, height/2),
                              text_font=self._font,
                              text_scale=ctrlFontSize,
                              text_pos=PIERCEROMAN_OFFSET,
                              width=8,
                              cursorKeys=1,
                              numLines=1)
        nmLabel = DirectLabel(parent=nameFrame,
                              pos=(ctrlWidth-ctrlWidth*2, 0, 0),
                              frameSize=(-ctrlWidth/2, ctrlWidth/2, -height/2,
                                         height/2),
                              text="User Name:",
                              text_font=self._font,
                              text_scale=(0.12, 0.12),
                              text_pos=PIERCEROMAN_OFFSET,
                              frameColor=(0.25,0.5,0.5,1))

    def _onConnectButton (self):
        """
            Called when the connect button is pressed.
            Read the user's inputs and tell the gameManager to create a client.
        """
        targetIP = str(self._ipAddressEntry.get())
        userName = self._userNameEntry.get()
        self._confirmHandler(targetIP, userName)

    def _close(self):
        """
            Closes this window and deletes all elements inside.
        """
        for element in self._elements:
            element.destroy()
        del self #Destroy this instance
