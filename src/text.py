import pygame as pg 
import pyglet as pl 
from superSpriteGroup import SuperSpriteGroup as sg
from context import Context


class Textbox(context):
    Boxgroup = None
    TextGroup = None

    def __init__(self, coord, text, fontName, fontSize, fontColor, batch):
        # make textbox controllable
        Context.__init__(self)

        self.text = text

        self._loadBatch(batch)

        self._makeWindow(image, coord)

        self._makeText(fontColor, fontSize, backgrounColor, fontFace)


    def _loadBatch(self, batch):
        # make drawable batches for box and then text
        self.textBoxSuperSpriteGroup = sg(batch)
        self.textSuperSpriteGroup = sg(batch) 

    # create backing window for display
    def _makeWindow(self, batch, image, coord):
        # load image
        image = pl.resource.image(image)

        # create sprite from image at coordinates
        self.box = pl.sprite.Sprite(image, coord[0], coord[1])

        # add the box to the group
        self.textBoxSuperSpriteGroup.add(self.box)

    def _makeText(self, fontColor = (0,0,0,255), fontSize = 50, backgrounColor = (255,255,255,255), fontName = 'Times New Roman'):

        self._document = pl.text.document.UnformattedDocument("")
                self.document.set_style\
            (0, len(self.document.text), dict(color=fontColor, \
             font_size = fontSize, background_color = backgrounColor, \
             font = fontName))

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):

        if self._text != value and self._fontwidth and self._boxwidth:
            self._text = value
            # lines in text to be shown - cleared if there was old text
            self.lines = list()

            # temp words that will make up a line
            wordlist = list()

            for word in self._text.split():
                # manual end line case
                if "\\n" in word:
                    endline = word.split("\\n")

                    for endword in endline:
                        # \\n will become a '' if there is not text (aka an intentional \\n)
                        if endword == '':
                            lines.append(" ".join(wordlist))
                            worrlist.clear()
                        else:
                            wordlist.append(endword)
                
                else:
                    # add next word
                    wordlist.append(word)

                    # check to see if the line is big enough to be cut off
                    if len(" ".join(wordlist)) * self._fontwidth > self._boxwidth:
                        # add the line without the word that makes it too big
                        lines.append(" ".join(wordlist[:-1]))

                        wordlist.clear()
                        # start new line
                        wordlist.append(word)

        # get last little bit
        if " ".join(wordlist) != '':
            lines.append(" ".join(wordlist))


    def doA(self):
