from direct.showbase.ShowBase import ShowBase
from objects.gameManager.GameManager import GameManager

class App(ShowBase):
    def __init__(self):
        ShowBase.__init__(self) # Call init on super
        gameManager = GameManager()
        gameManager.startMainMenu()

if __name__ == "__main__":
    app = App()
    app.run()
