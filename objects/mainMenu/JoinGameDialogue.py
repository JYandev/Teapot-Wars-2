from direct.gui.DirectGui import DirectFrame, DirectButton, DirectEntry
from objects.defaultConfig.DefaultConfig import *
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
                                    frameColor=(0,0,0,0.25))

        # Draw Main Dialogue Frame:
        dFStartX, dFStartY = winWidth*(1/5), winHeight*(1/6)
        dFSizeX, dFSizeY = winWidth*(3/5), winHeight*(2/3)
        dialogueFrame = DirectFrame(parent=base.a2dTopLeft,
                                    pos=(dFStartX, 0, -dFStartY),
                                    frameSize=(0, dFSizeX, -dFSizeY, 0))
        # Draw Title Text:
        # Draw Back Button:
        # Draw Connect Button:
