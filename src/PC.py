from superSprite import SuperSprite
from math import sqrt
import pygame as pg
from pygame import Vector2 as v2
import pyglet as pl
from sprite_collision_c import *

class PC(SuperSprite):
    # in theory these should be passed from SuperSPrite
    # used for diagonal distance calculations
    __i_sqrt_2 = 1/sqrt(2)

    # directions coordinate the direction frame collections
    __UP = 3
    __DOWN = 0
    __LEFT = 1
    __RIGHT = 2

    # level index because this class is sent
    # through level instances
    level_index = 0

    def __init__(self, image, frames: int, x: int, y: int, \
        speed: int, starting_direction: int, upFrame = 0, \
        downFrame = 0, leftFrame = 0, rightFrame = 0, \
        controllerIndex: int = 0, level_index = 0, buffer = 20):

        #init the super sprite
        super(PC, self).__init__(x, y, image, frames, speed, \
        starting_direction, upFrame, downFrame, leftFrame, rightFrame)

        # Set the controller that owns this PC
        self.controllerIndex = controllerIndex
        self.level_index = level_index

        # the interaction buffer size -- how many px around char rect to consider
        # an "interaction"
        self.buffer = buffer
        # make a rect that is slightly bigger than the sprite rect 
        # so that it can detect if things are close to it
        self.interactionBox = \
            pg.Rect(self.x - self.buffer, \
            self.y - self.buffer, self.rect.width + 2*self.buffer, \
            self.rect.height + 2*self.buffer)

        self.radius_2 = (self.rect.width + self.buffer)**2

        # Var to let the level know that PC is looking for someone to talk to
        self.textNotify = False

    def isSolid(self, coord, solidObjects):
        return coord in solidObjects
        
    #---- movement commands ----
    def doDOWN(self):
        #  First dir
        self.changeDirection(self.__DOWN)
        self.vy = -self.speed
        self.move_flag_y = True

    def doLEFT(self):
        self.changeDirection(self.__LEFT)
        self.vx = -self.speed
        self.move_flag_x = True

    def doRIGHT(self):
        self.changeDirection(self.__RIGHT)
        self.vx = self.speed
        self.move_flag_x = True

    def doUP(self):
        self.changeDirection(self.__UP)
        self.vy = self.speed
        self.move_flag_y = True

    def doSELECT(self):
        return self.transition(not self.level_index)

    def doA(self):
        self.openTextBox()

    def doX(self):
        print(self.x, self.y)

    def updateTime(self, dt):
        self.currentSounds.clear()
        self.dt = dt

    # move PC if needed
    def controllerMove(self, solid_group = list(), trigger_group = list()):
        moved = self.move_flag_x or self.move_flag_y
        if self.move_flag_x:
            self.movementUpdateX(self.move_flag_y, solid_group)
        if self.move_flag_y:
            self.movementUpdateY(self.move_flag_x, solid_group)

        if moved:
            self.levelTriggerCollision(trigger_group)
        else:
            # reset to starting position
            self.changeImage(self.frame_start[self.direction])
        self.vx, self.vy = 0,0
        self.move_flag_x, self.move_flag_y = False, False

    # change level and move the PC to the defined position
    def levelTriggerCollision(self, group):
        transition = self.collideRect(self.rect, group)
        if transition:
            if transition.index > -1:
                self.x = transition.PC_x
                self.y = transition.PC_y
                self.transition(transition.index)

    
    def anySideCollision(self, rectangle):
        # ugly but quick
        # interaction only when facing npc
        # flip rectangle top/bottom because rectangle coordinates are upsideown
        return \
            (self.direction == self.__DOWN and self.pointInCircle(rectangle.center[0], rectangle.bottom)) or \
            (self.direction == self.__UP and self.pointInCircle(rectangle.center[0], rectangle.top)) or \
            (self.direction == self.__RIGHT and self.pointInCircle(rectangle.left, rectangle.center[1])) or \
            (self.direction == self.__LEFT and self.pointInCircle(rectangle.right, rectangle.center[1]))

    def movementUpdateY(self, diagonal, group):
        y_distance = self.vy * self.dt
        # move sqrt 2 in each direction to offset both x and y velocities
        if diagonal:
            y_distance *= self.__i_sqrt_2
        #reverse b
        self.origin.y += y_distance
        self.rect.y = self.origin.y
        self.hitbox.y = self.origin.y
        self.c_rect.bottom = self.origin.y
        self.interactionBox.y = self.origin.y - self.buffer
        self.collideY(self.collideRect(self.hitbox, group))

    def movementUpdateX(self, diagonal, group):
        x_distance = self.vx * self.dt
        if diagonal:
            x_distance *= self.__i_sqrt_2
        self.origin.x += x_distance
        self.rect.x = self.origin.x
        self.hitbox.x = self.origin.x
        self.c_rect.left = self.origin.x
        self.interactionBox.x = self.origin.x - self.buffer
        #s = collide_hitbox_group(self, group)
        #h = list(group)[s] if s != -1 else None
        s = collide_group(self.c_rect.data, list(sprite.c_rect.data for sprite in group))
        h = list(group)[s] if s != -1 else None
        self.collideX(h)

    # if colliding with something move PC to the edge of it
    def collideX(self, ent):
        if not ent:
            return None
        if self.vx > 0:
            # should be based on self c_rect width
            self.origin.x = ent.c_rect.left - self.rect.width
        if self.vx < 0:
            self.origin.x = ent.c_rect.right + self.rect.width
        self.rect.x = self.origin.x
        self.interactionBox.x = self.origin.x - self.buffer
        self.hitbox.x = self.origin.x
        self.c_rect.left = self.origin.x
        print(ent.x, ent.y)

        #ent.playSound("bump")

    def collideY(self, ent):
        if not ent:
            return None
        if self.vy > 0:
            self.origin.y = ent.rect.top - self.hitbox.height
        if self.vy < 0:
            self.origin.y = ent.rect.bottom
        self.rect.y = self.origin.y
        self.interactionBox.y = self.origin.y - self.buffer
        self.hitbox.y = self.origin.y
        self.c_rect.bottom = self.origin.y

        #ent.playSound("bump")

    # level is set by the index of the PC on every frame
    # somehow faster than an if statement check
    def transition(self, levelNum):
        self.level_index = levelNum

    # request to open dialog with the nearest NPC
    def openTextBox(self):
        self.textNotify = True


    # updates directional frame index if enough time has elapsed
    def animate(self):
        if self.animation_timer < self.animation_time_until_next:
            self.animation_timer += self.dt
        else:
            self.current_frame = (self.current_frame+1)%self.animation_cycles[self.direction]              # Loop on end
            self.animation_timer = 0



