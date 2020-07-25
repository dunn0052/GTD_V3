import pygame as pg
import pyglet as pl 
import pyglet.gl.glext_nv as nv

from superSpriteGroup import SuperSpriteGroup as sg
from camera import Camera
from audio import Audio

# must be added for reaching outside of src
pl.resource.path = ['../images']
pl.resource.reindex()


class Console:

    def __init__(self, Width = 1920, Height = 1080, fps = 60, refresh = 10, Title = "Cat Mystery Dungeon"):
        pg.init()
        self.width = Width
        self.height = Height

        self.controllers = set()

        # camera size of screen
        self.camera = Camera(Width, Height)

        # vsync = False for max FPS
        self.screen = pl.window.Window(Width, Height,visible=True, vsync = False, fullscreen=True)
        self.clock = pl.clock
        self.fps_display = pl.window.FPSDisplay(window=self.screen)
        self.on_draw = self.screen.event(self.on_draw)
        self.clock.schedule(self.loopUpdate)

    def loopUpdate(self, dt):
        self.doCommands()
        self.update(dt)

    def doCommands(self):
        self.game.doCommands()

    # updates the game and moves the camera
    def update(self, dt): 
        self.scroll()
        self.game.update(dt)
        self.camera.update(self.game.currentLevel)

    def scroll(self):
        self.game.updateOffset(self.camera.camera.topleft)

        #DEBUG
        #self.game.currentLevel.v.move_relative(self.camera.camera.left, self.camera.camera.top)

    def on_draw(self):
        self.screen.clear()
        self.game.draw()
        self.fps_display.draw()


    def set_controller(self, controller):
        self.controllers.add(controller)
        if controller.keyboard:
            self.screen.push_handlers(controller.getKeyboardHandler())

    def run(self):
        pl.app.run()

    # will be used when level loading is created
    def loadGame(self, game):
        self.game = game
        self.game.addControllers(self.controllers)
        self.screen.set_caption(self.game.title)
        self.game.start()
        self.loadLevel()

    # sets up a level to be displayed
    def loadLevel(self):
        #self.camera.mapSize(self.game.currentLevel.mapHeight, self.game.currentLevel.mapWidth)
        self.game.currentLevel.setScreenSize(self.height, self.width)
