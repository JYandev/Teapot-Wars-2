from direct.showbase.ShowBase import ShowBase
from objects.tile.Tile import Tile
from objects.player.Player import Player
from panda3d.core import DirectionalLight
from panda3d.core import LPoint3f
from external.PyBSP_Dungeon_Generator import pybsp

class App(ShowBase):
    def __init__(self):
        ShowBase.__init__(self) # Call init on super
        base.disableMouse() # Disables default Panda3D camera control
        localPlayer = Player(LPoint3f(0,0,0))

        # --- TEST CODE TODO: REMOVE ---
        newDungeon = pybsp.generateDungeon2DList()
        for rowNum in range(len(newDungeon)):
            for colNum in range(len(newDungeon[0])):
                if newDungeon[rowNum][colNum] == 1:
                    newTile = Tile((rowNum,colNum,0))
        dlight = DirectionalLight('my dlight')
        dlnp = render.attachNewNode(dlight)
        dlnp.setHpr(0, -60, 0)
        render.setLight(dlnp)
        # --- ---
if __name__ == "__main__":
    app = App()
    app.run()
