class MusicSystem ():
    """
        Controller for all SFX and Music
    """

    def __init__ (self):
        # Temp music:
        gameMusic = base.loader.loadSfx(
            "objects/musicSystem/source/BATTLE_1.ogg")
        gameMusic.setLoop(True)
        gameMusic.play()
        #TODO Implement music system
