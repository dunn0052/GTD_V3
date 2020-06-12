from trigger import Trigger

class LevelTransition(Trigger):

    def __init__(self, x, y, height, width):
        super().__init__(x, y, height, width)
        self.index = 0
        self.PC_dir = 0
        self.PC_x = 0
        self.PC_y = 0

    # Load the info a PC needs to position itself in the level index
    def setLevel(self, index = -1, x = 0, y = 0, direction = 0):
        self.index = index
        self.PC_x, self.PC_y = x, y
        self.PC_dir = direction