import pygame as pg 
from level import Level
from audio import Audio

# this class holds levels and manages level
# transitions, controllers, etc..
class Game:
    
    def __init__(self):
        self.levels = list()
        self.controllers = set()
        self.currentLevel = None
        self.PC = None
        self.audio = Audio()
        self.title = ""

    #everything needed to start a new level
    def start(self):
        # be safe
        if self.PC.level_index <= len(self.levels):
            self.currentLevel = self.levels[self.PC.level_index]
            self.currentLevel.setPC(self.PC, self.PC.x, self.PC.y)
            #initate sound buffer for game
            self.audio.setSoundBuffer(self.currentLevel.soundBuffer)
            self.audio.playMusic(self.currentLevel.bgMusic)


    # controllers are in a set in case the same one is added more than once
    def addControllers(self, controllers):
        self.controllers.update(controllers)

    def loadLevel(self, levelPath):
        levelBuffer = loadObject(levelPath)
        self.addLevel(levelBuffer.unpack())

    def setPC(self, PC):
        self.PC = PC

    def changeLevel(self):
        self.currentLevel.soundBuffer.clear()
        self.start()

    # adds level on deck
    def addLevel(self, level):
        if self.PC:
            self.levels.append(level)
            self.levels[-1].index = len(self.levels) -1
        else:
            print("Need to set a PC first")

    def doCommands(self):
        self.currentLevel.doCommands(self.controllers)

    # pass information about a level/game to the screen
    def update(self, dt):
        # handle level transitions
        if self.isLevelChanged():
            self.changeLevel()
        self.currentLevel.update(dt)
        self.playAudio()

    def updateOffset(self, offset):
        self.currentLevel.updateOffset(offset)

    def playAudio(self):
        self.audio.play()

    def isLevelChanged(self):
        # the PC has changed it's level index - notify game to change level to it
        return self.currentLevel.index != self.currentLevel.PC.level_index

    def getLevelIndex(self):
        return self.currentLevel.PC.getLevelIndex()

    def setTitle(self, title):
        self.title = title

    def draw(self):
        self.currentLevel.draw()