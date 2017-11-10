from direct.gui.DirectGui import DirectFrame, DirectButton, DirectLabel
from panda3d.core import TextNode
from panda3d.core import TransparencyAttrib
from objects.defaultConfig.DefaultConfig import *
import sys
from objects.mainMenu.JoinGameDialogue import JoinGameDialogue

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
        buttonContainer.setColor(0.5,1,0.5,1) # TODO Set this to favorite color

        buttons = [
            ("Host Game", self._onButtonHostGame),
            ("Join Party", self._onButtonJoinGame),
            ("Options", self._onButtonOptions),
            ("Exit", self._onButtonExit)
        ]
        textColor = (1, 1, 1, 1)
        topAndBottomMargin = 0.155
        sidesMargin = 0.0275
        buttonHeight = 0.25
        buttonBackgroundColor = (0,0,0,1)
        # Create buttons:
        index = 0
        for button in buttons:
            newButton = DirectButton(parent=buttonContainer,
                                      pos=(0.5, 0,
                                      -topAndBottomMargin-buttonHeight*index),
                                      frameColor=buttonBackgroundColor,
                                      frameSize=(-0.5+sidesMargin,
                                                 0.5-sidesMargin,
                                                 -buttonHeight/2,
                                                 buttonHeight/2),
                                      text=button[0],
                                      text_font=self._buttonFont,
                                      text_scale=(0.15, 0.15),
                                      text_fg=textColor,
                                      text_pos=(0, -0.03),
                                      text_align=TextNode.ACenter,
                                      command=button[1])
            index += 1

    def _onButtonHostGame (self):
        """
            Called when the Host Game button is pressed.
            Signals to gameManager that the player wishes to host game.
        """
        self._gameManager.startHostGame()

    def _onButtonJoinGame (self):
        """
            Called when the Join Game button is pressed.
            Brings up the join game dialogue.
        """
        joinDialogue = JoinGameDialogue(self._onJoinGameDialogueConfirmed)

    def _onJoinGameDialogueConfirmed (self):
        """
            Called when the join game dialogue is finished with confirm.
            Starts the gameManager's NetworkClient with the chosen parameters.
        """
        print("UNIMPLEMENTED")

    def _onButtonOptions (self):
        """
            Called when the Options button is pressed.
            Brings up the options menu.
        """
        pass

    def _onButtonExit (self):
        """
            Quits the game.
        """
        sys.exit()
