from level import Level
import objectRW
from superSprite import SuperSprite
from superSpriteGroup import SuperSpriteGroup as sg
from PC import PC
import npc
import levelTransition
import levelTile
import textBox

from spritesheet import spritesheet

import pyglet as pl
import pygame as pg
import csv
import os
import json

class PackedLevel:

    def __init__(self, name = "",  image_path = "../images", data_path = "../data"):
        self.level = Level()
        self.level.name = name

        self.data = list()
        self.startupCommands = list()
        pl.resource.path = [image_path]
        pl.resource.reindex()
        self.dataPath = data_path

    def loadTileSheet(self, spriteSheetPath, tileHeight, tileWidth):
        imageList = pl.resource.image(spriteSheetPath)
        self.tileHeight = tileHeight
        self.tileWidth =  tileWidth
        self.level.tileHeight = tileHeight
        self.level.tileWidth = tileWidth
        self.rows = imageList.height // self.tileHeight
        self.cols = imageList.width // self.tileWidth
        # should be it's own class
        self.tiles = pl.image.ImageGrid(imageList, rows=self.rows, columns=self.cols)

    def getTile(self, tileIndex):
        row = self.rows - (tileIndex // self.cols) - 1
        col = tileIndex % self.cols
        return self.tiles[row, col]

    # Level has a map class to help design levels
    def loadData(self, filename):
        filename = os.path.join(self.dataPath, filename)
        data = list()
        if filename.endswith(".txt"):
            with open(filename, 'rt') as f:
                for line in f:
                    data.append(line.strip())
        elif filename.endswith(".csv"):
            with open(filename, 'rt') as f:
                reader = csv.reader(f, delimiter=',')
                for row in reader:
                    data.append(row)
        else:
            print("Can't open: " + filename)
        #reverse because Tiled enumerates backwards from what pyglet expects
        return reversed(data)

    def loadBackground(self, backgroundImage = None):
        #load image on bottom left
        background = SuperSprite(0, 0, backgroundImage, 1)
        self.level.setBackground(background)


    def loadWalls(self, filename):
        data = self.loadData(filename)
        for row, tiles in enumerate(data):
                    for col, tile in enumerate(tiles):
                        if int(tile) > -1:
                            ent = levelTile.LevelTile(x = col * self.tileHeight, y = row *self.tileWidth, \
                                image = self.getTile(int(tile)), key = int(tile))
                            self.level.WALL_LAYER.add(ent)
                            self.level.solid_sprites[(col, -row)] = ent

    def loadOverhead(self, filename):
        data = self.loadData(filename)
        for row, tiles in enumerate(data):
                    for col, tile in enumerate(tiles):
                        if int(tile) > -1:
                            ent = levelTile.LevelTile(x = col * self.tileHeight, y = row * self.tileWidth, \
                                image = self.getTile(int(tile)), key = int(tile))
                            self.level.OVER_LAYER.add(ent)

    def loadNPCs(self, filename):
        npc_index = 0
        data = self.loadData(filename)
        for row, tiles in enumerate(data):
                    for col, tile in enumerate(tiles):
                        if int(tile) > -1:
                            ent = npc.NPC(col * self.tileHeight, row * self.tileWidth, self.getTile(int(tile)), 1, 0, 0, 0, 0, 0, 0)
                            self.level.NPC_LAYER.add(ent)
                            self.level.npc_sprites[str(npc_index)] = ent
                            self.level.solid_sprites[(col, -row)] = ent
                            ent.setText("NPC index: " + str(npc_index))
                            npc_index += 1


    def setNPCText(self, index, text):
        self.level.npc_sprites[str(index)].setText(text)
        self.level.talking_sprites.add(self.level.npc_sprites[str(index)])

    def loadJSON(self, path):
        # should cause an error because it won't be dynamic
        try:
            with open(path, "r") as read_file:
                return json.load(read_file)
        except:
            print("Can't open: " + path)

    def loadNPCText(self, path):
        data = self.loadJSON(path)
        npc_id = str(data["NPC ID"])
        text = data["text"]
        if npc_id in self.level.npc_sprites:
            self.level.npc_sprites[npc_id].setText(text)
        else:
            print("Could not set text for data in :" + path)

    def setTextBox(self, x, y, image, text):
        self.level.text_box = textBox.TextBox(self.level.batch, x, y, image, text)

    def loadTriggers(self, filename):
        data = self.loadData(filename)
        for row, tiles in enumerate(data):
                    for col, tile in enumerate(tiles):
                        if int(tile) > -1:
                            ent = trigger.Trigger(x = col * self.tileHeight, y = row * self.tileWidth, \
                                height = self.tileHeight, width = self.tileWidth)
                            self.level.TRIGGER_LAYER.add(ent)

    def setTriggerCommand(self, index, command):
        # command must be a lambda function
        self.level.TRIGGER_LAYER.get_sprite(index).setInteraction(command)

    def loadLevelTriggers(self, filename):
        data = self.loadData(filename)
        for row, tiles in enumerate(data):
                    for col, tile in enumerate(tiles):
                        if int(tile) > -1:
                            ent = levelTransition.LevelTransition(x = col * self.tileHeight, y = row * self.tileWidth, \
                                height = self.tileHeight, width = self.tileWidth)
                            self.level.exit_triggers.add(ent)

    def setLevelChange(self, transition_index, level_index, pcx, pcy, pcdir):
        self.level.exit_triggers.get_sprite(transition_index).setLevel(level_index, pcx, pcy, pcdir)

    def setRayAnchors(self, filename):
        data = self.loadData(filename)
        for row, tiles in enumerate(data):
                    for col, tile in enumerate(tiles):
                        if int(tile) > -1:
                            ent = rayAnchor.RayAnchor((col * self.tileHeight, row * self.tileWidth), self.tileWidth, self.tileHeight)
                            self.level.ray_anchors[(col, -row)] = ent

    def loadTextBox(self, sprite):
        self.level.text_box = sprite


    def loadAnimatedSprite(self, sprite):
        self.level.NPC_LAYER.add(sprite)
        self.level.all_sprites.add(sprite)
        #self.level.solid_sprites.add(sprite)
        self.level.animated_sprites.add(sprite)

    def setBacgroundMusic(self, filename):
        self.level.backgroundMusic(filename)

#---------- PACK COMMANDS -----------
# These functions "spring load" image loading

    def unpackLevel(self):
        for command in self.startupCommands:
            command()
        return self.level

    