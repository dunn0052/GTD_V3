from ctypes import *
from random import randint
import time
from rect import C_RECT, C_POINT

# load c library
c_lib = CDLL("c_funcs.so")

# rectangle_collide
c_lib.rectangle_collide.argtypes = [c_int]*8
c_lib.rectangle_collide.restype = c_int

# collide_group
c_lib.collide_group.argtypes = [c_int]*4 + [POINTER(c_int)] + [c_int] 
c_lib.collide_group.restype = c_int

# collide_rects - natively detects C_RECT collision
c_lib.collide_rects.argtypes = [POINTER(C_RECT), POINTER(C_RECT), c_int]
# return index of overlap or -1 if not found
c_lib.collide_rect.restype = c_int

#collide_points
c_lib.update_points.argtypes = [c_int]*2 + [POINTER(C_POINT)] + [c_int]

# update_group_coords(int x, int y, int draw_coords[][8], int length)
c_lib.update_group_coords.argtypes = [c_int]*2 + [POINTER(c_int*8)] + [c_int]

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

def collide_group(caller, group):
    rect_array = (C_RECT * len(group))(*group)
    return c_lib.collide_rects(caller, rect_array, c_int(len(group)))


def update_points(x, y, group):
    point_array = (C_POINT * len(group))(*group)
    c_lib.update_points(x, y, point_array, len(group))

def update_sprite_group(x, y, sprite_coords):
    return c_lib.update_group_coords(x, y, sprite_coords, len(sprite_coords))