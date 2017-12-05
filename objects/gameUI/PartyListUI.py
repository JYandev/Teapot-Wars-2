from direct.gui.DirectGui import DirectFrame, DirectLabel, DirectWaitBar
from panda3d.core import TextNode
from objects.defaultConfig.Consts import *

class PartyListUI ():
    """
        A UI container element that appears to the top right, detailing
         connected party members.
    """

    def __init__ (self):
        self._frame = None
        self._partyIcons = []
        self._draw()

    def _draw (self):
        winWidth = base.getAspectRatio()
        winHeight = 2
        # Draw the container - Top Right of the Screen origin:
        containerWidth = winWidth * PARTY_LIST_WIDTH_PERCENTAGE
        containerHeight = winHeight * PARTY_LIST_HEIGHT_PERCENTAGE
        cX = winWidth - containerWidth/2
        cY = 1 # This is the top of the screen from the center
        cColor = (0.5, 0.5, 0.5, PARTY_LIST_ALPHA) #TODO #Eventually style this to player's chosen color
        self._frame = DirectFrame(pos=(cX, 0, cY),
                                frameSize=(-containerWidth/2, containerWidth/2,
                                           -containerHeight, 0),
                                frameColor=cColor)

    def updateInfo (self, info, myID):
        """
            Updates info for all connected party members.
            Essentially redraws all UIs
        """
        for node in self._partyIcons:
            node.close()

        count = 0
        for playerConn in info:
            if playerConn == myID: #Skip ourselves
                continue
            # Create a UIIcon using playerConn as a key:
            newPartyIcon = PartyIcon(self._frame, info[playerConn], count)
            self._partyIcons.append(newPartyIcon)
            count += 1

    def close (self):
        #TODO Implement closing for PartyListUI
        pass

class PartyIcon ():
    """
        The icon and info that is displayed for a connected party member.
    """

    def __init__ (self, parent, info, numPos):
        self._font = loader.loadFont(PIERCEROMAN_FONT)
        self._root = None
        self._nameText = None
        self._icon = None
        self._healthBar = None
        self._draw(parent, numPos)
        self._updateValues(info)

    def _draw (self, parent, numPos):
        # Draw the main frame:
        sizeY = parent.getHeight() / (MAX_PLAYERS-1)
        sizeX = parent.getWidth()
        cX = 0 # Relative to parent
        cY = -sizeY * numPos
        self._root = DirectFrame(parent=parent, pos=(cX, 0, cY),
                                 frameSize=(-sizeX/2, sizeX/2, -sizeY, 0))
        # Draw player name:
        nameSizeY = sizeY * PARTY_LIST_NAME_PARTITION
        nameColor = (0.5,0.5,0.5,0.25)
        self._nameText = DirectLabel(parent=self._root, pos=(0, 0, 0),
                           frameSize=(-sizeX/2, sizeX/2, -nameSizeY, 0),
                           frameColor=nameColor,
                           text="",
                           text_font=self._font,
                           text_scale=PARTY_NAME_FONT_SIZE,
                           text_pos=PARTY_NAME_FONT_OFFSET,
                           text_align=TextNode.ACenter)
        # Draw Icon:
        iconY = -nameSizeY
        iconSizeY = sizeY * PARTY_LIST_ICON_PARTITION
        self._icon = DirectFrame(parent=self._root, pos=(0, 0, iconY),
                                 frameSize=(-sizeX/2, sizeX/2, -iconSizeY, 0))
        # Draw HP Bar:
        healthY = -nameSizeY-iconSizeY
        healthSizeY = sizeY * PARTY_LIST_HEALTH_PARTITION
        self._healthBar = DirectWaitBar(parent=self._root, pos=(0, 0, healthY),
                             frameSize=(-sizeX/2, sizeX/2, -healthSizeY, 0),
                             frameColor=PARTY_LIST_HEALTH_BG_COLOR,
                             barColor=PARTY_LIST_HEALTH_FG_COLOR,
                             range=1, value=0)

    def _updateValues(self, info):
        """ Updates text or values depending on the info passed to this """
        if info.cName != None:
            if len(info.cName) > PARTY_NAME_MAX:
                self._nameText['text'] = info.cName[0:PARTY_NAME_MAX-1] + "..."
            else:
                self._nameText['text'] = info.cName
        if info.cClass != None:
            self._icon['frameTexture'] = CLASSES_DICT[info.cClass].classIcon
            pass
        if info.cColor != None:
            #TODO set icon color.
            pass
        # Set health:
        hValue = info.health / info.maxHealth
        self._healthBar['value'] = hValue

    def close (self):
        self._root.destroy()
        del self
