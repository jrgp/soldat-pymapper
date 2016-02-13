# apt-get install python-qt4-gl python-opengl
from __future__ import division
from PyQt4 import QtOpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL import *
from ui.image_loader import ImageLoader
import itertools
import math


class MapWidget(QtOpenGL.QGLWidget):
  def __init__(self):
    QtOpenGL.QGLWidget.__init__(self)
    self.pms = None
    self.images = None
    self.zoom = .3
    self.show_textures = True
    self.show_scenery = True
    self.show_wireframe = False

    self.scroll_x = 0
    self.scroll_y = 0

  def render_map(self, pms, soldat_path):
    self.pms = pms
    self.update()
    self.images = ImageLoader(soldat_path)

  # Let us zoom
  def wheelEvent(self, event):
    self.zoom -= event.delta() / 5000
    if self.zoom <= .1:
      self.zoom = .1
    self.update()


  def _background_gradient(self):
    glDisable(GL_TEXTURE_2D)
    glBegin(GL_POLYGON)
    glColor4f(*self.pms.header.BackgroundColorTop.for_gl_color)
    glVertex2f(self.pms.min_x, -self.pms.max_y)
    glVertex2f(self.pms.max_x, -self.pms.max_y)
    glColor4f(*self.pms.header.BackgroundColorBottom.for_gl_color)
    glVertex2f(self.pms.max_x, -self.pms.min_y)
    glVertex2f(self.pms.min_x, -self.pms.min_y)
    glEnd()
    glEnable(GL_TEXTURE_2D)

  def _polys(self):
    glShadeModel(GL_SMOOTH)

    if self.show_textures:
      img = self.images.load_image('textures', self.pms.header.Texture.filename())
      if img:
        glTexImage2D(GL_TEXTURE_2D, 0, 3, img['x'], img['y'], 0, GL_RGB, GL_UNSIGNED_BYTE, img['ref'])
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    if self.show_wireframe:
      glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    glBegin(GL_TRIANGLES)
    for polygon in self.pms.polygons:
      for vertex in polygon.Vertexes:
        glColor4f(*vertex.color.for_gl_color)
        if self.show_textures:
          glTexCoord3f(vertex.tu, vertex.tv, vertex.rhw)
        glVertex3f(vertex.x, vertex.y, 0)
    glEnd()

    if self.show_wireframe:
      glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

  def _props(self, select=lambda x: True):
    if not self.show_scenery:
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
      glRotatef(prop.Rotation * (180.0/math.pi), 0.0, 0.0, 1.0)
      glScalef(prop.ScaleX, prop.ScaleY, 0.0)
      glTexImage2D(GL_TEXTURE_2D, 0, 3, img['x'], img['y'], 0, GL_RGB, GL_UNSIGNED_BYTE, img['ref'])
      glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
      glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
      glBegin(GL_QUADS)

      glColor4f(*prop.Color.for_gl_color)

      glTexCoord2f(0.0, 0.0); glVertex2f(0.0, 0.0)
      glTexCoord2f(0.0, 1.0); glVertex2f(0, prop.Height)
      glTexCoord2f(1.0, 1.0); glVertex2f(prop.Width, prop.Height)
      glTexCoord2f(1.0, 0.0); glVertex2f(prop.Width, 0.0)


      glEnd()
      glPopMatrix()



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
    self._props(lambda x: x.LevelText == 'None')

    glLoadIdentity()
    glFlush()
