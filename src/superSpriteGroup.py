import pygame as pg
import pyglet as pl 
from c_funcs import *

class SuperSpriteGroup:

    _moved = True
    _batch = None
    # draw order will be determined by creation
    _orderNumber = 0

    @staticmethod
    def draw():
        SuperSpriteGroup._batch.draw()

    @staticmethod
    def offset(offset, sprite):
        x = sprite.origin.x + offset[0]
        y = sprite.origin.y + offset[1]
        sprite.update(x = x, y = y)
        return sprite

    def fast_offset(self, offset):
        update_sprite_group(c_int(offset[0]), c_int(offset[1]), self.data)

    def __init__(self, batch, width = 1920, height = 1024):
        self.sprites = list()
        self.batch = batch
        self.group = pl.graphics.OrderedGroup(SuperSpriteGroup._orderNumber)
        SuperSpriteGroup._orderNumber += 1
        self.sprite_coords = list()
        self.data = None

    def add(self, sprite):
        self.sprites.append(sprite)
        sprite.batch = self.batch
        sprite.group = self.group
        sprite.spriteGroup = self.sprites
        self.sprite_coords.append(sprite.coord_data)
        self.data = ((c_int * 8) * len(self.sprite_coords))(*self.sprite_coords)

    def update(self, dt):
        for sprite in self.sprites:
            sprite.updateTime(dt)

    def updateDrawingOffset(self, offsetCoords):
        #slow here
        #self.sprites = [SuperSpriteGroup.offset(offsetCoords, sprite) for sprite in self.sprites]
        self.fast_offset(offsetCoords)

    def __iter__(self):
        for sprite in self.sprites:
            yield sprite

    def sprites(self):
        return self.sprites

    def sound(self):
        pass

    def collideAny(self, sprite):
        return collide_rect_group(sprite, self.sprites)

    def whichCollide(self, sprite):
        return self.sprites[collide_hitbox_group(sprite)]