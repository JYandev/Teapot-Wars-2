from direct.showbase.ShowBase import ShowBase
from objects.tile.Tile import Tile

class App(ShowBase):
    def __init__(self):
        ShowBase.__init__(self) # Call init on super
        newTile = Tile(self.loader, self.render, (0,0,0))

if __name__ == "__main__":
    app = App()
    app.run()
