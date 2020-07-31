from pygame import Vector2 as vec
from pygame import Rect
class Trigger:
    
    '''
    class similar to LeveTile, 
    but needs no image data
    '''

    _moved = True
    
    def __init__(self, x, y, height, width):
        self.x, self.y = x,y
        # no image to draw, just used for rect dimensions
        self.rect = Rect(x, y + height, width, height)
        self.rect.x = x 
        self.rect.y = y
        self.hitbox = self.rect
        self.origin = vec(self.x, self.y)

    # should only be used for movable tiles
    def updateTime(self, dt):
        pass