import pygame, math, sys, os
vec = pygame.math.Vector2
from math import sqrt
import keyboardInput as KB
import pyglet as pl
from context import Context
'''
This class is the base class for all game sprites
it has basic functions needed for sprites
There are virtual functions that can be used
for interaction with buttons
'''

class SuperSprite(pl.sprite.Sprite, Context):
    
    # used for diagonal distance calculations
    __i_sqrt_2 = 1/sqrt(2)

    # directions coordinate the direction frame collections
    __UP = 3
    __DOWN = 0
    __LEFT = 1
    __RIGHT = 2

    def __init__(self, x = 0, y = 0, image = None, frames=1,  speed: int = 0, \
        starting_direction: int = 0, upFrame = 0, downFrame = 0, leftFrame = 0, \
        rightFrame = 0):

        # draw group that is used to keep track of membership
        self.spriteGroup = None

        # need a list because the images are ordered
        self.images = []

        # slice the frames
        self.images = SuperSprite.createFrames(frames, image)

        # self.image is what is drawn
        img = self.images[0]

        # bad practice but workds
        super().__init__(img, x, y)
        Context.__init__(self)

        self.x, self.y = x, y
        # image width, if not a multiple of 4 for each direction
        self.frameWidth = img.width // frames
        self.frameHeight = img.height
        # set starting image
        self.currentImage = 0
        self.rect = self.getRect(self.image)
        self.radius_2 = self.rect.width**2/4 + self.rect.height**2/4
        # buffer used because hitboxes are too fat. 
        self.hitboxBuffer = 10
        self.hitbox = pygame.Rect(self.x + self.hitboxBuffer, self.y, self.rect.width - self.hitboxBuffer, self.rect.height//2)


        self.angle = 0
        self.scale = 1

        # need to modify for uneven frames
        self.animation_cycle = frames//4 if frames%4 == 0 else 1
        
        self.current_frame = 0

        self.animation_timer = 0
        self.animation_time_until_next = 0.15
        
        # finally move to proper position
        self.moveTo(self.x, self.y)
        self.origin = pygame.Vector2(self.x, self.y)

        #sounds
        self.sounds = dict()
        self.currentSounds = list()

        # velocity in each direction
        self.vx, self.vy = 0, 0

        self.dt = 0

        # speed in pixels per second
        self.speed = speed

        self.direction = starting_direction
        
        # User defined frames per direction
        self.animation_cycles = [downFrame, leftFrame, rightFrame, upFrame]
        
        # if none are defined then assume that they are evenly distributed
        if not any(self.animation_cycles):
            self.animation_cycles = [frames//4]*4


        
        self.move_flag_y = False
        self.move_flag_x = False

        # pre calculate which frame index each direction starts on
        self.frame_start = {self.__UP:self.animation_start(self.__UP),\
                            self.__DOWN:self.animation_start(self.__DOWN),\
                            self.__LEFT:self.animation_start(self.__LEFT),\
                            self.__RIGHT:self.animation_start(self.__RIGHT)}

#----- IMAGE FUNCTIONS -----#

    # load an image from a file path
    @staticmethod
    def loadImage(self,fileName: str):
        image = pl.image.load(fileName)
        # Return the image
        return image

    # split image into individual frames
    # @frames: number of equally sized animation frames
    # @img: full image of all frames to be spliced into frames
    @staticmethod
    def createFrames(frames: int, img):
        # if you pass in a path then load the image
        if isinstance(img, str):
            img = pl.resource.image(img)
        frame_list = pl.image.ImageGrid(img, rows=1, columns=frames)
        return frame_list

    @staticmethod
    def getRect(image):
        return pygame.Rect(image.x, image.y, image.width, image.height)

    # set image to specific frame
    def changeImage(self, index: int):
        self.currentImage = index
        self.image = self.images[index]
        oldcenter = self.rect.center
        self.rect = self.getRect(self.image)
        originalRect = self.getRect(self.images[self.currentImage])
        self.frameWidth = originalRect.width
        self.frameHeight = originalRect.height
        self.rect.center = oldcenter
        self.dirty = 1

    def nextFrame(self):
        self.currentImage += 1
        self.currentImage %= len(self.images)
        self.changeImage(self.currentImage)

    # in case you want to animate backwards?
    def prevFrame(self):
        self.currentImage -= 1
        self.currentImage %= len(self.images)
        self.changeImage(self.currentImage)

    def animation_start(self, dir):
        return sum(self.animation_cycles[:dir])

    def changeDirection(self, direction: int):
        self.direction = direction
        # start on current frame of specified direction
        self.changeImage(self.frame_start[self.direction] + self.current_frame%self.animation_cycles[self.direction])


# ---- MOVEMENT FUNCTIONS ------
# move from current position x, y distance
    def move(self, x: int, y: int):
        self.x += x
        self.y += y
        self.rect.x = self.x
        self.rect.y = self.y
        self.hitbox.x = self.x + self.hitboxBuffer
        self.hitbox.y = self.y + self.hitbox.height

# move to coordinates
    def moveTo(self, x, y):
        self.rect.x, self.x = x, x
        self.rect.y, self.y = y, y
        self.hitbox.x = self.x + self.hitboxBuffer
        self.hitbox.y = self.y + self.hitbox.height

    def moveToTile(self, x, y, tileWidth, tileHeight):
        self.moveTo(x * tileWidth, y * tileHeight)

    # are the centers touching? Way faster if you can do this
    # instead of the mask collide.
    def checkCollision(self, other, center = False):
        if center:
            return self.rect.collidepoint(other.rect.center)
        return self.rect.colliderect(other)

    def collideRect(self, box, group):
        for sprite in group:
            if sprite.rect.colliderect(box):
                return sprite

    def collideHitbox(self, other):
        return other.rect.colliderect(self.hitbox)

    def pointInCircle(self, x, y):
        k = (x - self.rect.centerx)**2 + (y - self.rect.centery)**2
        return (x - self.rect.centerx)**2 + (y - self.rect.centery)**2 < self.radius_2 

    def animate(self):
        if self.animation_timer < self.animation_time_until_next:
            # 10ms is max animation speed
            self.animation_timer += self.dt
        else:
            self.current_frame = (self.current_frame+1)%self.animation_cycle             # Loop on end
            self.animation_timer = 0
            self.nextFrame()

    def kill(self):
        self.batch = None
        self.group = None
        if self in self.spriteGroup:
            self.spriteGroup.remove(self)
            
# ------ BUTTON FUNCTIONS ------

    # A button input calls the command dictionary
    # and executes the command
    def doCommand(self, button):
        self.commands[button]()

    # take in a time delta to
    # use in calculating the real
    # time changes between game loops
    def updateTime(self, dt = 0):
        self.currentSounds.clear()
        self.dt = dt

    def setSound(self, key: str, sound: str):
        self.sounds[key] = pygame.mixer.Sound(sound)

    def getSound(self, key: str):
        if key in self.sounds:
            return self.sounds[key]

    def playSound(self, key):
        self.currentSounds.append(self.getSound(key))


# ------ LOADING FUNCTIONS ------
    # calls the packed lambda functions
    # that are needed to set a
    # superSprite up when loaded
    def unpackSprite(self):
        pass
