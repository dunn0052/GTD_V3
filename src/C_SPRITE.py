import sys
import math
from ctypes import c_float

from pyglet.gl import *
from pyglet import clock
from pyglet import event
from pyglet import graphics
from pyglet import image
from pyglet.sprite import SpriteGroup

from c_funcs import initate_coords, C_COORD

class SuperSprite(event.EventDispatcher, Context):

    # general batch all sprites initialize with
    _batch = None

    def __init__(self, img, x, y, batch):

        self._group = SpriteGroup(self._texture, blend_src, blend_dest, group)
        self._texture = self._create_texture(img)
        self._data = self._create_data(x, y)

    
    def _create_texture(self, image):
        # need to create multiple for animations
        return image.get_texture()

    def _create_data(self, x, y):
        # create vertex list for drawing     
        self._vertex_list = graphics.vertex_list(
            4, 'v2f/dynamic', 'c4B', ('t3f', self._texture.tex_coords))

self._vertex_list = self._batch.add(
                4, GL_QUADS, self._group, 'v2f/dynamic', 'c4B', ('t3f', self._texture.tex_coords))

        x1 = c_float(self._x)
        y1 = c_float(self._y)
        x2 = c_float(self._x + self._texture.width)
        y2 = c_float(self._y + self._texture.width)

        self._coords = C_COORD()
        self._data = c_lib.initate_coords(x1, y1, x2, y2, 
           cast(addressof(self._vertex_list.vertices), POINTER(c_float))
           byref(self._coords))

    
    def __del__(self):
        try:
            if self._vertex_list is not None:
                self._vertex_list.delete()
        except:
            pass 

    @property
    def batch(self):
        """Graphics batch.

        The sprite can be migrated from one batch to another, or removed from
        its batch (for individual drawing).  Note that this can be an expensive
        operation.

        :type: :py:class:`pyglet.graphics.Batch`
        """
        return self._batch

    @batch.setter
    def batch(self, batch):
        if self._batch == batch:
            return

        if batch is not None and self._batch is not None:
            self._batch.migrate(self._vertex_list, GL_QUADS, self._group, batch)
            self._batch = batch
        else:
            self._vertex_list.delete()
            self._batch = batch
            self._create_data()

    @property
    def group(self):
        """Parent graphics group.

        The sprite can change its rendering group, however this can be an
        expensive operation.

        :type: :py:class:`pyglet.graphics.Group`
        """
        return self._group.parent

    @group.setter
    def group(self, group):
        if self._group.parent == group:
            return
        self._group = SpriteGroup(self._texture,
                                  self._group.blend_src,
                                  self._group.blend_dest,
                                  group)
        if self._batch is not None:
            self._batch.migrate(self._vertex_list, GL_QUADS, self._group,
                                self._batch)

    def draw(self):
        """Draw the sprite at its current position.

        See the module documentation for hints on drawing multiple sprites
        efficiently.
        """
        self._group.set_state_recursive()
        self._vertex_list.draw(GL_QUADS)
        self._group.unset_state_recursive()