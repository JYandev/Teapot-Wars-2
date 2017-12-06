from direct.gui.DirectGui import DirectFrame, DirectButton
from panda3d.core import TransparencyAttrib, TextNode
from objects.defaultConfig.DefaultConfig import *
from objects.defaultConfig.Consts import *
import sys
from objects.mainMenu.JoinGameDialogue import JoinGameDialogue
from .GameGuide import GameGuide

class MainMenu ():
    """
        Handles all main menu functionality including drawing and starting the
         game.
    """
    def __init__ (self, gameManager):
        self._gameManager = gameManager
        self._buttonFont = loader.loadFont(PIERCEROMAN_FONT)
        self._joinDialogue = None
        self._elements = []

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
        # Draw Title:
        titleSize = winHeight-bCSizeY-TITLE_MARGIN*2
        title = DirectFrame(parent=backgroundFrame,
                            pos=(bCStartX, 0, -TITLE_MARGIN),
                            frameSize=(0, bCSizeX, -titleSize, 0),
                            frameTexture=TITLE_PATH)
        title.setTransparency(TransparencyAttrib.MAlpha)

        buttons = [
            ("Host Game", self._onButtonHostGame),
            ("Join Party", self._onButtonJoinGame),
            ("Guide", self._onButtonGuide),
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
                                      text_pos=PIERCEROMAN_OFFSET_MC,
                                      text_align=TextNode.ACenter,
                                      command=button[1],
                                      frameTexture=IMG_GRADIENT_1)
            index += 1
        self._elements.extend([backgroundFrame])

    def close (self):
        """ Closes the main menu """
        # Close the dialogue if there is one:
        if self._joinDialogue: self._joinDialogue.close()
        for element in self._elements:
            element.destroy()
        del self # Destroy this instance

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
        self._joinDialogue = JoinGameDialogue(self._onJoinGameDialogueConfirmed)

    def _onJoinGameDialogueConfirmed (self, ipAddress):
        """
            Called when the join game dialogue is finished with confirm.
            Starts the gameManager's NetworkClient with the chosen parameters.
        """
        self._gameManager.startJoinGame(ipAddress)

    def _onButtonGuide (self):
        """
            Called when the Guide button is pressed.
            Shows the guide.
        """
        self._guide = GameGuide()

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
