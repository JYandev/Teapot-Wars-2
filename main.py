from direct.showbase.ShowBase import ShowBase
from objects.tile.Tile import Tile
from objects.player.Player import Player

class App(ShowBase):
    def __init__(self):
        ShowBase.__init__(self) # Call init on super
        base.disableMouse() # Disables default Panda3D camera control
        localPlayer = Player(self.cam, self.loader, self.render, (0,0,0))

        for i in range(10):
            for j in range(10):
                newTile = Tile(self.loader, self.render, (i*5,j*5,0))
                #TODO Remove test
if __name__ == "__main__":
    app = App()
    app.run()
