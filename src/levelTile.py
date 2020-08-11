import pygame as pg
import pyglet as pl 
from fastSprite import FastSprite

from rect import Rect

class LevelTile(FastSprite):

    _images = dict()
    _plImages = dict()
    _moved = True

    @staticmethod
    def getRect(image):
        # translate from pygame to pyglet coordinates since (x,y) is bottom left instead of top left
        return pg.Rect(image.x, image.y + image.height, image.width, image.height)

    def __init__(self, x, y, image, key):
        super().__init__(image, x, y)
        self.key = key
        self._images[self.key] = image
        #self.mask = pg.mask.from_surface(self._images[self.key])
        self.rect = self.getRect(image)
        self._c_rect = self.getCRect(x, y, self._images[self.key])
        self.x, self.y = x,y
        self.rect.x = x
        self.rect.y = y
        self.hitbox = self.rect
        self.origin = pg.Vector2(self.x, self.y)


    @staticmethod
    def getCRect(x, y, image):
        return Rect(x, y, image.height, image.width)
        
    # should only be used for movable tiles
    def updateTime(self, dt):
        pass

    def glLoad(self, image):
        self.glimage = pl.image.load(image)


    def drawGl(self):
        self.glimage.draw()