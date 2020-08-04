from ctypes import c_int, byref, Structure, pointer
# ctypes structs for c functions
class C_POINT(Structure):
    _fields_ = [("x", c_int), 
                ("y", c_int)]

class C_RECT(Structure):
    _fields_ = [("upper_left", C_POINT), 
                ("lower_right", C_POINT)]

class Rect:
    def __init__(self, left, bottom, height, width):


        self._bottom, self._left, self._height, self._width = bottom, left, height, width

        # for c functions
        self._data = C_RECT(C_POINT(c_int(self._left), c_int(self._bottom + self._height)), \
                          C_POINT(c_int(self._left + self._width), c_int(self._bottom)))

    # get pointer to data -- used for c_functions
    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        # can only have values set after creation
        pass

    @property
    def bottom(self):
        return self._bottom

    @bottom.setter
    def bottom(self, value):
        if(self._bottom != value):
            self._bottom = int(value)
            self._data.upper_left.y = c_int(self._bottom + self._height)
            self._data.lower_right.y = c_int(self._bottom)


    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, value):
        if(self._left != value):
            self._left = int(value)
            self._data.upper_left.x = c_int(self._left)
            self._data.lower_right.x = c_int(self._left + self._width)

    @property
    def height(self):
        return self._height

    @bottom.setter
    def height(self, value):
        if(self._height != value):
            self._height = int(value)
            self._data.upper_left.y = c_int(self._bottom + self._height)

    @property
    def width(self):
        return self._width

    @bottom.setter
    def width(self, value):
        if(self._width != value):
            self._width = int(value)
            self._data.lower_right.x = c_int(self._left + self._width)

    @property
    def right(self):
        return self.left + self.width

    @property
    def top(self):
        return self.bottom + self.height
    