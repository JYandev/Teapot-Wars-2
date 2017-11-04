from direct.gui.DirectGui import DirectFrame, DirectButton, DirectEntry
from panda3d.core import TextNode
from panda3d.core import TransparencyAttrib
from objects.defaultConfig.DefaultConfig import *

TITLE_SCREEN_BACKGROUND_PATH = "objects/mainMenu/TitleScreen.png"
PIERCEROMAN_FONT_PATH = "objects/mainMenu/PierceRoman.otf"
TITLE_SCREEN_CONTAINER_PATH = "objects/mainMenu/TitleScreenContainer.png"

class MainMenu ():
    """
        Handles all main menu functionality including drawing and starting the
         game.
    """
    def __init__ (self, gameManager):
        self._gameManager = gameManager
        self._buttonFont = loader.loadFont(PIERCEROMAN_FONT_PATH)
        self._ipAddress = DEFAULT_IP_ADDRESS

    def draw(self):
        """
            Sets up main menu and draws GUI to screen.
            Only supports aspect ratios >= 1 (where width is at least height)
        """
        # Set background color to black to cover any possible incorrect scaling:
        #base.setBackgroundColor(0,0,0)
        winWidth = base.getAspectRatio() * 2
        winHeight = 2
        backgroundFrame = DirectFrame(parent=base.a2dTopLeft,
                                      frameSize=(0,winWidth, -winHeight, 0),
                                      frameTexture=TITLE_SCREEN_BACKGROUND_PATH)
        bCStartX, bCStartY = winWidth*(2/3), winHeight*(1/3)
        bCSizeX, bCSizeY = winWidth-bCStartX, winHeight-bCStartY
        buttonContainer = DirectFrame(parent=backgroundFrame,
                                      pos=(bCStartX, 0, -bCStartY),
                                      frameSize=(0, bCSizeX, -bCSizeY, 0),
                                      frameTexture=TITLE_SCREEN_CONTAINER_PATH)
        buttonContainer.setTransparency(TransparencyAttrib.MAlpha)
        buttonContainer.setColor(0.5,1,0.5,1)
        # TODO Set this to favorite color


        #TODO: Change buttons to an image. Will be easier to animate, color etc.
        textColor = (1, 1, 1, 1)
        topMargin = 0.25
        hostButton = DirectButton(parent=buttonContainer,
                                  pos=(0.5, 0, -topMargin),
                                  frameColor=(0,0,0,0),
                                  text="Host Game",
                                  text_font=self._buttonFont,
                                  text_scale=(0.15, 0.15),
                                  text_fg=textColor,
                                  text_align=TextNode.ACenter,
                                  command=self._onButtonHostGame)

        ipEntry = DirectEntry(parent=buttonContainer,
                              pos=(0, 0, -topMargin*3),
                              frameSize=(0, 1, -0.5, 0),
                              text_scale=(0.15, 0.15),
                              text="", initialText=self._ipAddress,
                              entryFont=self._buttonFont, numLines=1,
                              command=self._onIPEntrySet,
                              focusOutCommand=self._onIPEntrySet)

    def _onButtonHostGame (self):
        """
            Called when the Host Game button is pressed.
            Signals to gameManager that the player wishes to host game.
        """
        self._gameManager.startHostGame()

    def _onIPEntrySet (self, textEntered):
        self._ipAddress = textEntered
