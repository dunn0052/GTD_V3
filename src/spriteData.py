from ctypes import c_float, Structure
from rect import Rect
from c_funcs import C_RECT, C_POINT, C_COORD

NUM_SPRITE_COORDS = 8


    
class SpriteData:

    def __init__(self, x1, y1, x2, y2,, coordinate_array):
        self._data = C_COORD(C_RECT((x1, y1), (x2, y2)), coordinate_array)

        self._data.coords[0] = x1
        self._data.coords[1] = y1
        # eh finish later
