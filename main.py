from panda3d.core import loadPrcFile
loadPrcFile("config/Config.prc") # Load main config file.

from direct.showbase.ShowBase import ShowBase
from objects.gameManager.GameManager import GameManager

class App(ShowBase):
    def __init__(self):
        ShowBase.__init__(self) # Call init on super
        gameManager = GameManager() # Start Game State Manager
        gameManager.startMainMenu() # Start the main menu

if __name__ == "__main__":
    app = App()
    app.run()
