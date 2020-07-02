import pygame as pg
import pyglet as pl

from superSpriteGroup import SuperSpriteGroup as sg
from triggerGroup import TriggerContainer as tc
from debug import VertexRectangle

# the level class holds the layers of sprites to draw
# it also executes commands of the current controller context


class Level:
    # length of music fadein/out
    _fadeTime_ms = 1000

    def __init__(self, layerNum = 7, name = "NoName"):
        self.tileHeight, self.tileWidth = 0,0

        # drawing batch for level
        self.batch = pl.graphics.Batch()

        # filenames
        self.name = name

        #index in game level
        self.index = 0

        # ensure that there is only one of each controller
        self.controllers = set()

        # start bg music
        self.bgMusic = None

        # list of sounds to be played during update
        self.soundBuffer = list()

        # display constants
        self.PC = None
        self.text_box = None

        # things that block PC from moving
        self.solid_sprites = dict()
        self.npc_sprites = dict() #so you can access individual NPCs -- may not be needed because of super sprite groups
        
        self.talking_sprites = list()

        # things that should move with camera
        self.movable_sprites = list()
        
        # things that animate
        self.animated_sprites = list()

        self.exit_triggers = tc()
        #raytrace stuff
        # coordinates of where rays project to
        self.ray_anchors = dict()

        # things that block rays
        self.ray_reflect = dict()

        # draw layers
        self.layers = list()
        
        # add drawing layer orders for basics
        for _ in range(layerNum):
            self.layers.append(sg(self.batch))
        self.layers.append(self.exit_triggers)

        try:
            self.BACKGROUND = self.layers[0] # background image
            self.NPC_LAYER = self.layers[1] # draw NPC next
            self.WALL_LAYER = self.layers[2] # level walls
            self.RAY_LAYER = self.layers[3] # if layer change also change SetPC()
            self.PC_LAYER = self.layers[4] # draw pc
            self.OVER_LAYER = self.layers[5] # things overhead - bridges/roof
            self.WEATHER_LAYER = self.layers[6] # small alpha effects -- rain, clouds, etc.
            self.TRIGGER_LAYER = self.layers[7]
            # sprites that need to be updated with camera movement
            self.movable_sprites = self.layers[:layerNum]
        except:
            print("Number of layers must be greater than 7")

    # audio functions
    def backgroundMusic(self, filename):
        self.bgMusic = pg.mixer.Sound(filename)

    # runs through all controllers and controls the PC
    # sends the button presses to the PC
    def doCommands(self, controllers):
        # get inputs from all controllers
        for controller in controllers:
            buttons = controller.getInput()
            for button in buttons:
                self.context.doCommand(button)

    # sets all controller(s)
    def setControllers(self, controllers):
          self.controllers.update(controllers)

    def removeControllers(self):
        self.controllers.clear()

    def removeController(self, controller):
        self.controllers.discard(controller)

    # the context is what the camera follows
    def setContext(self, context):
        self.context = context

    def setScreenSize(self, height, width):
        self.screenHeight = height
        self.screenWidth = width

    def setBackground(self, background):
        self.mapHeight = background.image.height
        self.mapWidth = background.image.width
        self.BACKGROUND.add(background)

    # sets playable PC -- @TODO: setup for multiplayer
    def setPC(self, PC, x, y):
        # if PC is presnet then remove from all groups
        if self.PC:
            self.PC.kill()
            self.animated_sprites.remove(self.PC)
            self.movable_sprites.remove(self.PC)

        # attach PC to level
        self.PC = PC
        self.PC_LAYER.add(self.PC)
        self.setContext(self.PC)
        self.animated_sprites.append(self.PC)
        rect = self.PC.interactionBox

        # DEBUG
        #self.v = VertexRectangle(rect.x, rect.y, rect.width, rect.height,  (0,0,0))

        #eventualy move to tile
        self.PC.moveTo(x, y)

    def checkForText(self):
        # Check if any NPCs in range have something to say
        if self.PC.textNotify:

            talkingSprite = self.PC.collideRect(self.PC.interactionBox, self.npc_sprites.values())
            if talkingSprite:

                # check to see if you're facing the talking sprite
                if self.PC.anySideCollision(talkingSprite.rect):
                    self.setContext(self.text_box)
                    self.text_box.setText(talkingSprite.text[0])
                    self.text_box.showText()
                    # game should pause when control is handed over to text box

            self.PC.textNotify = False

            
        if self.text_box.done:
            self.setContext(self.PC)
            self.text_box.done = False

    # executes controller inputs to the current level
    def doCommands(self, controllers):
        for controller in controllers:
            inputs = controller.getInput()
            for button in inputs:
                self.context.commands[button]()

    # signals to level can be read to screen and game from here
    def update(self, dt):
        if self.text_box:
            self.checkForText()
            self.text_box.update(dt)
            # if the text box updates then don't do layer update.
        
        for layer in self.layers:
            layer.update(dt)

        self.PC.controllerMove(self.solid_sprites.values(), self.exit_triggers)

        self.updateSound()
        self.animate()
        # DEBUG
        #self.v.move_absolute(self.PC.interactionBox.x, self.PC.interactionBox.y)

    def updateOffset(self, offset):
        for layer in self.layers:
            layer.updateDrawingOffset(offset)
        # DEBUG
        #self.v.move_relative(-offset[0], -offset[1])

    def updateSound(self):
        self.soundBuffer.clear()
        # go through sprite gorups and call their sound functions
        # add all sounds from a given sprite
        for sprite in self.PC_LAYER:
            self.soundBuffer += sprite.currentSounds

    # Animate all sprites in the animation group
    def animate(self):
        for sprite in self.animated_sprites:
            sprite.animate()

    def centerLevel(self, screenWidth, mapWidth):

        for layer in self.layers:
            layer.updateDrawingOffset(screenWidth - mapWidth , 0)

    # is the map too small for the screen dimensions? 
    # Needed for smallUpdate()
    def is_small(self, height, width):
        return self.mapWidth < width or self.mapHeight < height

    def draw(self):
        self.batch.draw()

        #DEBUG
        #self.v.draw()