from console import Console 
from controllerIO import Controller 
import pyglet as pl
from game import Game
from levelSDK import PackedLevel
from PC import PC

if __name__ == '__main__':
    c = Controller(0, keyboard=True)

    l1 = PackedLevel()
    l1.loadTileSheet("NBIG.png", 80, 80)
    l1.loadBackground("ICE_TOWN_BG.png")
    l1.loadWalls("ICE_TOWN_Tile Layer 2.csv")
    l1.loadOverhead("ICE_TOWN_Tile Layer 3.csv")
    l1.setTextBox("textBackground.png", 0, 0, "super long text "*100)
    #l1.loadLevelTriggers("ICE_TOWN_Tile Layer 4.csv")
    l1.loadNPCs("ICE_TOWN_Tile Layer 5.csv")
    l1.loadNPCText("..\\json\\test.json") # ID/text in json
    char = PC("redPC.png", 10, 600, 450, 300, 0, 3, 3, 2, 2, 0,0)
    g = Game()
    g.setPC(char)
    g.setTitle("Cat Mystery Dungeon")
    s = Console()
    s.set_controller(c)
    g.addLevel(l1.unpackLevel())
    s.loadGame(g)
    s.run()