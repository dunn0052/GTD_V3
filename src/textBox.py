import pygame as pg 
import pyglet as pl 
from superSpriteGroup import SuperSpriteGroup as sg
from context import Context

# debug box
class Rectangle(object):
    '''Draws a rectangle into a batch.'''
    def __init__(self, x1, y1, x2, y2, batch):
        self.vertex_list = batch.add(4, pl.gl.GL_QUADS, None,
            ('v2i', [x1, y1, x2, y1, x2, y2, x1, y2]),
            ('c4B', [200, 200, 220, 255] * 4)
        )


class Text:

    def __init__(self, text):
        self.originalText = text
        self._text = list(text)
        self._len = len(self._text)
        self._index = 0
        self.done = False

    def __iter__(self):
        for letter in self._text:
            yield letter

    def __next__(self):
        if self._index < self._len:
            letter = self._text[self._index]
            self._index += 1
            return letter
        else:
            self.done = True
            return ""

class TextBox(Context):

    BoxGroup = None
    TextGroup = None

    def __init__(self, batch, image, x, y, message = "", \
                 fontName = 'Times New Roman', fontSize = 98, xBuffer = 80, yBuffer = 60):
        
        # make textbox controllable
        Context.__init__(self)

        # make drawable batches for box and then text
        self.textBoxSuperSpriteGroup = sg(batch)
        self.textSuperSpriteGroup = sg(batch)

        # the text box image
        image = pl.resource.image(image)
        self.box = pl.sprite.Sprite(image, x, y)
        self.textBoxSuperSpriteGroup.add(self.box)
    
        # to hold the text chunks to fit the string
        self.chunks = list()
        self.chunkIndex = 0                                         

        # document holds the text
        self.document = pl.text.document.UnformattedDocument("")
        self.document.set_style\
            (0, len(self.document.text), dict(color=(255, 0, 0, 255), \
             font_size=50, background_color = (0,0,255, 0), font = fontName))

        # get fonts spacing to make virtual text box
        self.font = self.document.get_font()
        fontHeight = self.font.ascent - self.font.descent
        fontWidth = self.font.max_glyph_width
        
        numLines = self.box.height//fontHeight - 1
        docHeight = numLines * fontHeight

        numLetters = self.box.width//fontWidth
        docWidth = numLetters * fontWidth

        # Number of total characters per text box.
        # Used to figure out how to chunk the message
        self.maxChars = numLines * fontWidth

        # the pyglet text image
        self.layout = pl.text.layout.IncrementalTextLayout\
            (self.document, self.box.width - xBuffer * 2, docHeight, \
             multiline=True, dpi=96, wrap_lines = True, \
             batch = self.textSuperSpriteGroup.batch, \
             group = self.textSuperSpriteGroup.group)
                     
        # should have an x,y bufer to overlay box
        self.layout.x = self.box.x + xBuffer
        self.layout.y = self.box.y + yBuffer

        self.setText(message)
        self.hideText()
        self.done = False

    def screenChunks(self, text):
        chunks = list()
        words = text.split(' ')
        sb = ""
        for word in words:
            # get word chunk + space
            if len(sb) + len(word) < self.maxChars:
                sb += word + " "
            else:
                chunks.append(Text(sb))
                sb = ""
        chunks.append(Text(sb))
        return chunks

    def showText(self):
        self.box.visible = True
        self.update = self.writeText
        self.done = False

    def hideText(self):
        self.box.visible = False
        self.document.delete_text(0, len(self.document.text))
        self.update = self.pauseText
        self.done = True

    def setText(self, message):
        self.text = message
        self.chunks = self.screenChunks(message)
        self.chunk = self.chunks[0]

    def update(self, dt):
        pass

    def nextChunk(self):
        self.chunkIndex += 1
        self.chunk = self.chunks[self.chunkIndex]

    def doA(self):
        # check that current chunk is done and there are more chunks
        if self.chunk.done and self.chunkIndex < len(self.chunks) -1:
            self.nextChunk()
        else:
        # all chunks are finished - let level know it is finished
            self.chunks.clear()
            self.done = True
            self.hideText()

    def pauseText(self, dt):
        pass

    def writeText(self, dt):
        if not self.chunk.done:
            self.document.insert_text(len(self.document.text), next(self.chunk))
        else:
            pass

    def showAllChunk(self):
        self.document.text = self.chunk.originalText
        self.chunk.done = True
