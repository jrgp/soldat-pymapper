# apt-get install python-qt4-gl python-opengl
from __future__ import division
from PyQt4 import QtOpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL import *
from ui.image_loader import ImageLoader
import itertools
import math

from pms.constants import T_Spawntype


class MapWidget(QtOpenGL.QGLWidget):

  '''
    Render map and interact with it using OpenGl. All of this was pieced together
    from various tutorials on the internet and ancient soldat forums threads, as
    well as the polyworks source.
  '''

  def __init__(self):
    QtOpenGL.QGLWidget.__init__(self)
    self.pms = None
    self.images = None
    self.zoom = .3

    self.show_items = dict(
        textures=True,
        polygons=True,
        scenery=True,
        wireframe=False,
        spawns=False,
        grid=False,
        background=True
    )

    self.scroll_x = 0
    self.scroll_y = 0

  def render_map(self, pms, soldat_path):
    self.pms = pms
    self.update()
    self.images = ImageLoader(soldat_path)

  # Zoom on scroll wheel
  def wheelEvent(self, event):
    self.zoom -= event.delta() / 5000
    if self.zoom <= .1:
      self.zoom = .1
    self.update()

  def _background_gradient(self):

    # When showing backgroun is disabled just make it solid white
    if self.show_items['background']:
      top_color = self.pms.header.BackgroundColorTop.for_gl_color
      bottom_color = self.pms.header.BackgroundColorBottom.for_gl_color
    else:
      top_color = bottom_color = 1, 1, 1, 1

    glDisable(GL_TEXTURE_2D)
    glBegin(GL_POLYGON)
    glColor4f(*top_color)
    glVertex2f(self.pms.min_x, -self.pms.max_y)
    glVertex2f(self.pms.max_x, -self.pms.max_y)
    glColor4f(*bottom_color)
    glVertex2f(self.pms.max_x, -self.pms.min_y)
    glVertex2f(self.pms.min_x, -self.pms.min_y)
    glEnd()
    glEnable(GL_TEXTURE_2D)

  def _polys(self):

    if not self.show_items['polygons']:
      return

    glShadeModel(GL_SMOOTH)

    if self.show_items['textures']:
      img = self.images.load_image('textures', self.pms.header.Texture.filename())
      if img:
        glTexImage2D(GL_TEXTURE_2D, 0, 3, img['x'], img['y'], 0, GL_RGB, GL_UNSIGNED_BYTE, img['ref'])
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    if self.show_items['wireframe']:
      glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    glBegin(GL_TRIANGLES)
    for polygon in self.pms.polygons:
      for vertex in polygon.Vertexes:
        glColor4f(*vertex.color.for_gl_color)
        if self.show_items['textures']:
          glTexCoord3f(vertex.tu, vertex.tv, vertex.rhw)
        glVertex3f(vertex.x, vertex.y, 0)
    glEnd()

    if self.show_items['wireframe']:
      glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

  def _props(self, select=lambda x: True):
    if not self.show_items['scenery']:
      return

    for prop in itertools.ifilter(select, self.pms.props):
      try:
        filename = self.pms.sceneries[prop.Style].filename
      except IndexError:
        print 'Couldn\'t lookup scenery {} in list of sceneries ({} long)'.format(prop.Style, len(self.pms.sceneries))
        continue

      img = self.images.load_image('scenery-gfx', filename)
      if not img:
        continue

      glPushMatrix()
      glTranslatef(prop.x, prop.y, 0.0)
      glRotatef(-math.degrees(prop.Rotation), 0.0, 0.0, 1.0)
      glScalef(prop.ScaleX, prop.ScaleY, 0.0)
      glTexImage2D(GL_TEXTURE_2D, 0, 3, img['x'], img['y'], 0, GL_RGB, GL_UNSIGNED_BYTE, img['ref'])
      glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
      glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

      glBegin(GL_QUADS)

      glColor4f(*prop.Color.for_gl_color)

      glTexCoord2f(0.0, 0.0); glVertex2f(0.0, 0.0)
      glTexCoord2f(0.0, 1.0); glVertex2f(0.0, prop.Height)
      glTexCoord2f(1.0, 1.0); glVertex2f(prop.Width, prop.Height)
      glTexCoord2f(1.0, 0.0); glVertex2f(prop.Width, 0.0)

      glEnd()
      glPopMatrix()

  def _spawns(self):

    if not self.show_items['spawns']:
      return

    avail_pics = [
        'alpha', 'bravo', 'general', 'alpha_flag', 'bravo_flag', 'yellow_flag',
        'medkit', 'cluster', 'grenades', 'vest', 'predator', 'berserker', 'flamer']

    for spawn in self.pms.spawnpoints:
      if T_Spawntype[spawn.Type] not in avail_pics:
        continue

      img = self.images.load_image('res', '{}.png'.format(T_Spawntype[spawn.Type]))
      if not img:
        print 'Failed loading image for {}'.format(T_Spawntype[spawn.Type])
        continue

      glPushMatrix()
      glTranslatef(spawn.x, spawn.y, 0.0)
      glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img['x'], img['y'], 0, GL_RGB, GL_UNSIGNED_BYTE, img['ref'])
      glBegin(GL_QUADS)
      glColor4f(1, 1, 1, .9)
      glTexCoord2f(0.0, 0.0); glVertex2f(0.0, 0.0)
      glTexCoord2f(0.0, 1.0); glVertex2f(0.0, img['y'])
      glTexCoord2f(1.0, 1.0); glVertex2f(img['x'], img['y'])
      glTexCoord2f(1.0, 0.0); glVertex2f(img['x'], 0.0)

      glEnd()
      glPopMatrix()


  def _grid(self):
    if not self.show_items['grid']:
      return
    spacing = 100
    glBegin(GL_LINES)
    glColor4f(0, 0, 0, .2)
    for x in range(self.pms.min_x, self.pms.max_x, spacing):
      for y in range(self.pms.min_y, self.pms.max_y, spacing):
        glVertex3f(x, self.pms.min_y, 0)
        glVertex3f(x, self.pms.max_y, 0)
        glVertex3f(self.pms.min_x, y, 0)
        glVertex3f(self.pms.max_x, y, 0)
    glEnd()

  def paintGL(self):
    if not self.pms:
      return

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluOrtho2D(self.pms.min_x * self.zoom, self.pms.max_x * self.zoom, -self.pms.min_y * self.zoom, -self.pms.max_y * self.zoom)
    glTranslatef(-self.scroll_x, -self.scroll_y, 0.0)
    glEnable(GL_BLEND)
    glEnable(GL_TEXTURE_2D)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glClear(GL_COLOR_BUFFER_BIT)

    self._background_gradient()
    self._props(lambda x: x.LevelText != 'None')
    self._polys()
    self._spawns()
    self._props(lambda x: x.LevelText == 'None')
    self._grid()

    glLoadIdentity()
    glFlush()

  def resizeGL(self, h, w):
    if w > h:
      new_w = w - h
    else:
      new_w = 0

    glViewport(0, new_w, max(w, h), max(w, h))
