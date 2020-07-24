import pygame as pg
import pyglet as pl 

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

    def __init__(self, batch, width = 1920, height = 1024):
        self.sprites = list()
        self.batch = batch
        self.group = pl.graphics.OrderedGroup(SuperSpriteGroup._orderNumber)
        SuperSpriteGroup._orderNumber += 1

    def add(self, sprite):
        self.sprites.append(sprite)
        sprite.batch = self.batch
        sprite.group = self.group
        sprite.spriteGroup = self.sprites

    def update(self, dt):
        for sprite in self.sprites:
            sprite.updateTime(dt)

    def updateDrawingOffset(self, offsetCoords):
        self.sprites = [SuperSpriteGroup.offset(offsetCoords, sprite) for sprite in self.sprites]

    def __iter__(self):
        for sprite in self.sprites:
            yield sprite

    def sprites(self):
        return self.sprites

    def sound(self):
        pass