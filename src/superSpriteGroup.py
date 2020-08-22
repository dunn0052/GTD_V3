import pygame as pg
import pyglet as pl 
from c_funcs import update_sprite_group_coords, update_sprite_group_vertices, C_COORD
from ctypes import POINTER, c_float, pointer, byref

class SuperSpriteGroup:

    _moved = True
    _batch = None
    # draw order will be determined by creation
    _orderNumber = 0

    _coords = None
    _allData = list()
    _allSprites = list()
    _allVertices = list()

    @staticmethod
    def draw():
        SuperSpriteGroup._batch.draw()

    @staticmethod
    def updateOffset(offset):
        update_sprite_group_coords(offset[0], offset[1], SuperSpriteGroup._coords)

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
        self.sprite_coords = list()
        self.data = None        

    def add(self, sprite):
        self.sprites.append(sprite)
        sprite.batch = self.batch
        sprite.group = self.group
        sprite.spriteGroup = self.sprites

        # must be done in this thread?
        sprite.create_coords()

        #sprite.p[0] = 127.0  
        # all sprites
        SuperSpriteGroup._allSprites.append(sprite)
        SuperSpriteGroup._allData.append(sprite._data)

        #SuperSpriteGroup._allVertices.append(sprite._vertex_list.vertices)
        SuperSpriteGroup._coords = None
        SuperSpriteGroup._coords = ((POINTER(POINTER(C_COORD))) * len(SuperSpriteGroup._allData))(*list(self.get_data()))
        #SuperSpriteGroup._vertices = ((POINTER(c_float * 8)) * len(SuperSpriteGroup._allVertices))(*list(self.get_verts()))
        test = 1

    def update(self, dt):
        for sprite in self.sprites:
            sprite.updateTime(dt)

    def updateDrawingOffset(self, offsetCoords):
        #slow here
        #self.sprites = [SuperSpriteGroup.offset(offsetCoords, sprite) for sprite in self.sprites]
        update_sprite_group_coords(offsetCoords[0], offsetCoords[1], SuperSpriteGroup._coords)
        after = 1

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

    def get_verts(self):
        for sprite in SuperSpriteGroup._allSprites:
            yield pointer(sprite._vertex_list.vertices)

    def get_data(self):
        for sprite in SuperSpriteGroup._allSprites:
            yield pointer(sprite._data)