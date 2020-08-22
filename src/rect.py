from ctypes import c_float
from c_funcs import C_RECT, C_POINT

#probably not needed

class Rect:
    def __init__(self, left, bottom, height, width):


        self._bottom, self._left, self._height, self._width = bottom, left, height, width

        # for c functions
        self._data = C_RECT(C_POINT(c_float(self._left), c_float(self._bottom + self._height)), \
                          C_POINT(c_float(self._left + self._width), c_float(self._bottom)))

    # get pointer to data -- used for c_functions
    @property
    def data(self):
        return self._data

    @property
    def bottom(self):
        return self._bottom

    @bottom.setter
    def bottom(self, value):
        if(self._bottom != value):
            self._bottom = int(value)
            self._data.upper_left.y = c_float(self._bottom + self._height)
            self._data.lower_right.y = c_float(self._bottom)


    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, value):
        if(self._left != value):
            self._left = int(value)
            self._data.upper_left.x = c_float(self._left)
            self._data.lower_right.x = c_float(self._left + self._width)

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if(self._height != value):
            self._height = int(value)
            self._data.upper_left.y = c_float(self._bottom + self._height)

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if(self._width != value):
            self._width = int(value)
            self._data.lower_right.x = c_float(self._left + self._width)

    @property
    def right(self):
        return self.left + self._width

    @property
    def top(self):
        return self.bottom + self._height
    