import pygame as pg

# this class is responsible for the game view
# it follows a rect and moves all other sprites
# relative to the targeted sprite
class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.c = (1,1)
        self.width = width
        self.height = height

    # keeps target on center or
    # stops on edge of map edges
    def update(self, level):
        target = level.PC
        self.mapSize(level.mapHeight, level.mapWidth)
        x = target.origin.x + target.rect.width/2 - self.width/2
        y = target.origin.y + target.rect.height - int(self.height / 2)
        # limit scrolling to map size
        y = min(self.mapHeight - self.height, y)  # top
        x = min((self.mapWidth - self.width), x)  # right
        x = max(0, x)  # left
        y = max(0, y)  # bottom
        # -y because pyglet coordinates are upside down from pygame
        self.camera = pg.Rect(x, -y, self.width, self.height)

    def moved(self):
        moved = (self.c[0] != self.camera.x or self.c[1] != self.camera.y)
        self.c = (self.camera.x, self.camera.y)
        return moved
 
    # define map edges
    def mapSize(self, height, width):
        self.mapHeight = height
        self.mapWidth = width