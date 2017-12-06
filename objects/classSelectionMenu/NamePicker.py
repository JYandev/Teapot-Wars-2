from direct.gui.DirectGui import DirectFrame, DirectEntry, DirectButton
from objects.defaultConfig.Consts import *
from panda3d.core import TransparencyAttrib, TextNode

class NamePicker ():
    """
        A UI element that lets the players pick their name.
        Also has a confirmation element to the right of the entry box.
    """
    def __init__ (self, classSelectionMenu):
        self._classSelectionMenu = classSelectionMenu
        self._nameEntry = None
        self._confirmButton = None
        self._rootFrame = None
        self._font = loader.loadFont(PIERCEROMAN_FONT)
        self._draw()

    def _draw (self):
        winWidth = base.getAspectRatio() * 2
        winHeight = 2
        # Draw container:
        frameHeight = winHeight * NPKR_HEIGHT_PERCENTAGE
        frameWidth = winWidth * NPKR_WIDTH_PERCENTAGE
        cFCenterY = -winHeight/2 + frameHeight/2
        self._rootFrame = DirectFrame(pos=(0, 0, cFCenterY),
                                   frameSize=(-frameWidth/2, frameWidth/2,
                                              -frameHeight/2, frameHeight/2),
                                   frameTexture=IMG_GRADIENT_1)
        self._rootFrame.setTransparency(TransparencyAttrib.MAlpha)
        # Draw Name Entry:
        entryWidth = self._rootFrame.getWidth() * NPKR_ENTRY_WIDTH_PERCENTAGE
        entryHeight = self._rootFrame.getHeight()
        entryCX = -(self._rootFrame.getWidth() - entryWidth)/2
        self._nameEntry = DirectEntry(parent=self._rootFrame,
                                      pos=(entryCX, 0, 0),
                                      frameSize=(-entryWidth/2, entryWidth/2,
                                                 -entryHeight/2, entryHeight/2),
                                      frameColor=(0.25,0.25,0.25,1),
                                      text_align=TextNode.ACenter,
                                      text_font=self._font,
                                      text_scale=NPKR_ENTRY_FONT_SIZE,
                                      text_pos=NPKR_ENTRY_FONT_OFFSET,
                                      initialText=NPKR_ENTRY_INITIAL_TEXT,
                                      numLines=1,
                                      focusOutCommand=self._syncName,
                                      focusInCommand=self._checkPlaceholderText,
                                      command=self._syncName,
                                      frameTexture=UI_WINDOW)
        # Draw Confirm Button:
        confirmWidth = self._rootFrame.getWidth()\
                            * (1-NPKR_ENTRY_WIDTH_PERCENTAGE)
        confirmHeight = self._rootFrame.getHeight()
        confirmCX = (self._rootFrame.getWidth() - confirmWidth)/2
        self._confirmButton = DirectButton(parent=self._rootFrame,
                                pos=(confirmCX, 0, 0),
                                frameSize=(-confirmWidth/2, confirmWidth/2,
                                           -confirmHeight/2, confirmHeight/2),
                                command=self._onConfirmPressed,
                                text_font=self._font,
                                text_scale=NPKR_BUTTON_FONT_SIZE,
                                text_pos=NPKR_BUTTON_FONT_OFFSET,
                                text="Create Character",
                                borderWidth=NPKR_BUTTON_BORDER_WIDTH)

    def getName (self):
        return str(self._nameEntry.get())

    def _onConfirmPressed (self):
        """ Reroutes this input to the parent ClassSelectionMenu """
        self._classSelectionMenu.createCharacter()

    def _checkPlaceholderText (self):
        """
            Makes the nameEntry behave more like a real name entry by removing
             the placeholder text when the player begins to interact.
        """
        # If the text entered is the placeholder text, simply remove it:
        if self._nameEntry.get() == NPKR_ENTRY_INITIAL_TEXT:
            self._nameEntry.set("")


    def _syncName (self, extraArgs=None):
        """ Syncs name with this game's host/client manager """
        self._classSelectionMenu.syncInfo(cName=self.getName())

    def close (self):
        self._rootFrame.destroy() # Destroy ui
        del self # Destroy this instance
