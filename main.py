from direct.showbase.ShowBase import ShowBase
from objects.tile.Tile import Tile
from objects.player.Player import Player
from panda3d.core import DirectionalLight
from panda3d.core import LPoint3f

class App(ShowBase):
    def __init__(self):
        ShowBase.__init__(self) # Call init on super
        base.disableMouse() # Disables default Panda3D camera control
        localPlayer = Player(LPoint3f(0,0,0))

        # --- TEST CODE TODO: REMOVE ---
        for i in range(10):
            for j in range(10):
                newTile = Tile((i,j,0))
        dlight = DirectionalLight('my dlight')
        dlnp = render.attachNewNode(dlight)
        dlnp.setHpr(0, -60, 0)
        render.setLight(dlnp)
        # --- ---
if __name__ == "__main__":
    app = App()
    app.run()
