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

    def __getitem__(self, index):
        return self.tiles[index]

    def updateDrawingOffset(self, offsetCoords):
        self.tiles = [TriggerContainer.offset(offsetCoords, tile) for tile in self.tiles]