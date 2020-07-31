import pygame as pg
import pyglet as pl 

class LevelTile(pl.sprite.Sprite):

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
        self.x, self.y = x,y
        self.rect.x = x
        self.rect.y = y
        self.hitbox = self.rect
        self.origin = pg.Vector2(self.x, self.y)
        
    # should only be used for movable tiles
    def updateTime(self, dt):
        pass

    def glLoad(self, image):
        self.glimage = pl.image.load(image)


    def drawGl(self):
        self.glimage.draw()