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
        self._draw()
        self._ipAddress = DEFAULT_IP_ADDRESS

    def _draw (self):
        """
            Draws this JoinGameDialogue
        """

        # Draw translucent background frame to block clicks:

        # Draw Main Dialogue Frame:
        winWidth = base.getAspectRatio() * 2
        winHeight = 2
        dFStartX, dFStartY = winWidth*(1/4), winHeight*(1/4)
        dFSizeX, dFSizeY = winWidth/2 - dFStartX, winHeight/2 - dFStartY
        dialogueFrame = DirectFrame(parent=base.a2dTopLeft,
                                    pos=(dFStartX, 0, -dFStartY),
                                    frameSize=(0,winWidth, -winHeight, 0))
        # Draw Back button :
        # Draw Connect button :

    def _onIPEntrySet (self, textEntered):
        self._ipAddress = textEntered
