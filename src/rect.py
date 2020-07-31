import ctypes
# ctypes structs for c functions
class POINT(Structure):
    _fields_ = [("x", c_int), ("y", c_int)]

class RECT(Structure):
    _fields_ = [("upper_left", POINT), ("lower_right", POINT)]

class Rect:
    def __init__(self, top, left, bottom, right):

        self.top, self.left, self.bottom, self.right = top, left, bottom, right
        self.width = abs(self.right - self.left)
        self.height = abs(self.top - self.bottom)
        self.x, self.y = self.left, self.bottom

        # for c functions
        self._data = RECT(POINT(self.left, self.top), POINT(self.right, self.bottom))

    # get pointer to data
    def getData(self):
        return byref(self._data)