from superSprite import SuperSprite
import json

class NPC(SuperSprite):

    def __init__(self, x = 0, y = 0, image = None, frames=1,  speed: int = 0, \
    starting_direction: int = 0, upFrame = 0, downFrame = 0, leftFrame = 0, \
    rightFrame = 0):

        # init the super sprite
        super(NPC, self).__init__(x, y, image, \
            frames, speed, starting_direction, \
            upFrame, downFrame, leftFrame, rightFrame)

        self.text = [""]


# should just load the csv path
    def setText(self, text):

        if isinstance(text, str):
            self.text = [text]
        elif isinstance(text, list):
            self.text = text
