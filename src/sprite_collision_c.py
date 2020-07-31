from ctypes import *
from random import randint
import time

c_lib = CDLL("c_collision.so")

c_lib.rectangle_collide.argtypes = [c_int]*8
c_lib.rectangle_collide.restype = c_int

c_lib.collide_group.argtypes = [c_int]*4 + [POINTER(c_int)] + [c_int] 
c_lib.collide_group.restype = c_int


def rect_to_int(rect):
    return (rect.top, rect.left, rect.bottom, rect.right)

def get_coords(group):
    for sprite in group:
        yield sprite.rect.top 
        yield sprite.rect.left 
        yield sprite.rect.bottom 
        yield sprite.rect.right

def get_h_coords(group):
    for sprite in group:
        yield sprite.hitbox.top 
        yield sprite.hitbox.left 
        yield sprite.hitbox.bottom 
        yield sprite.hitbox.right

# caller = sprite, group = iterable of sprites
def collide_rect_group(caller, group):
    coordinate_array = (c_int*(len(group)*4))(*list(get_coords(group)))
    return c_lib.collide_group(caller.rect.top, caller.rect.left, caller.rect.bottom, caller.rect.right, coordinate_array, len(group))

def collide_hitbox_group(caller, group):
    coordinate_array = (c_int*(len(group)*4))(*list(get_h_coords(group)))
    return c_lib.collide_group(caller.hitbox.top, caller.hitbox.left, caller.hitbox.bottom, caller.hitbox.right, coordinate_array, len(group))