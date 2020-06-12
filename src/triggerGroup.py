
from functools import partial

class TriggerContainer:

    @staticmethod
    def offset(offset, tile):
        tile.rect.x += offset[0]
        tile.rect.y += offset[1]
        return tile

    def __init__(self):
        self.tiles = list()

    def add(self, tile):
        self.tiles.append(tile)

    def update(self, dt):
        pass

    def __iter__(self):
        for tile in self.tiles:
            yield tile

    def updateDrawingOffset(self, offsetCoords):
        # offset is constant each iteration so it can be curried
        foffset = partial(TriggerContainer.offset, offsetCoords)
        self.tiles = [foffset(tile) for tile in self.tiles]