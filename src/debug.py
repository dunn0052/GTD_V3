import pyglet

class VertexRectangle:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        r = color[0]
        g = color[1]
        b = color[2]
        self.vertex_list = pyglet.graphics.vertex_list(4, 'v2f', 'c3B')
        self.vertex_list.vertices = [x, y,
                                   x + width, y,
                                   x + width, y + height,
                                   x, y + height]
        self.vertex_list.colors = [r, g, b,
                                   r, g, b,
                                   r, g, b,
                                   r, g, b]
        self.draw_mode = pyglet.gl.GL_QUADS

    def draw(self):
        self.vertex_list.draw(self.draw_mode)

    def move_relative(self, dx, dy):
        self.__init__(self.x+dx, self.y+dy, self.width, self.height, self.color)

    def move_absolute(self, x, y):
        self.__init__(x, y, self.width, self.height, self.color)

    def width_absolute(self, w):
        self.__init__(self.x, self.y , w, self.height,
                      self.color)

    def width_relative(self, dw):
        self.__init__(self.x, self.y, self.width + dw, self.height,
                      self.color)