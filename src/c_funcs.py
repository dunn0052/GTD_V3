from ctypes import c_long, c_int, POINTER, Structure, CDLL, c_float, pointer, byref, c_void_p

class C_POINT(Structure):
    _fields_ = [("x", c_float), 
                ("y", c_float)]

class C_RECT(Structure):
    _fields_ = [("upper_left", C_POINT), 
                ("lower_right", C_POINT)]

# @TODO make define for number of points for coords
class C_COORD(Structure):
    _fields_ = [("origin", C_RECT), 
                ("coords",  POINTER(c_float))]


# load c library
c_lib = CDLL("c_funcs.so")

# collide_rects - natively detects C_RECT collision
c_lib.collide_rect.argtypes = [C_RECT, C_RECT]
# return 1 if collided or 0 if not
c_lib.collide_rect.restype = c_int

# given all rects in a group, check which one is colliding
c_lib.collide_sprite_group_rects.argtypes = [POINTER(C_COORD), POINTER(C_COORD), c_int]
# -1 if none found, or index of first collided C_COORD
c_lib.collide_sprite_group_rects.restype = c_int

# update_group_coords(int x, int y, int draw_coords[][8], int length)
# modifies a C_COORD coord array with and x, y offset
#c_lib.update_sprite_group_coords.argtypes = [c_float]*2 + [POINTER(POINTER(POINTER(C_COORD)))] + [c_int]
#return void
c_lib.update_sprite_group_vertices.argtypes = [c_float]*2 + [POINTER(POINTER(C_COORD)), POINTER(c_float)]


# initiate 
c_lib.initiate_coords.argtypes = [c_float]*4 + [POINTER(c_float), POINTER(C_COORD)]
c_lib.initiate_coords.restype = POINTER(C_COORD)


# move sprite by x,y and update it's drawing coordinates by that amount
c_lib.move_sprite.argtypes = [c_float]*2 + [POINTER(C_COORD)] + [c_float * 8]
# return void


def collide_rect(caller, other):
    return bool(c_lib.collide_rect(caller, other))

def collide_sprite_group_rects(caller, sprite_coords):
    return int(c_lib.collide_sprite_group_rects)

def update_sprite_group_coords(x, y, sprite_coords):
    c_lib.update_sprite_group_coords.argtypes = [c_float]*2 + [type(sprite_coords)] + [c_int]
    c_lib.update_sprite_group_coords(c_float(x), c_float(y), sprite_coords, c_int(len(sprite_coords)))
    after = 1

def update_sprite_group_vertices(x, y, sprite_coords):
    c_lib.update_sprite_group_coords.argtypes = [c_float]*2 + [type(sprite_coords)]
    c_lib.update_sprite_group_vertices(c_float(x), c_float(y), sprite_coords)


def initate_coords(x1, y1, x2, y2, vertex_array, coord):
    return c_lib.initiate_coords(c_float(x1), c_float(y1), c_float(x2), c_float(y2), byref(vertex_array), coord)

def move_sprite(x, y, sprite_coords):
    c_lib.move_sprite(c_float(x), c_float(y), sprite_coords)