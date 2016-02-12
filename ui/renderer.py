# apt-get install python-qt4-gl python-opengl
from __future__ import division
from PyQt4 import QtOpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL import *
from ui.image_loader import ImageLoader


class MapWidget(QtOpenGL.QGLWidget):
  def __init__(self, parent=None):
    self.parent = parent
    QtOpenGL.QGLWidget.__init__(self, parent)
    self.pms = None
    self.images = None
    self.zoom = .3

  def render_map(self, pms, soldat_path):
    self.pms = pms
    self.update()
    self.images = ImageLoader(soldat_path)

  def alter_zoom(self, delta):
    self.zoom -= delta
    if self.zoom <= .1:
      self.zoom = .1
    self.update()

  def _background_gradient(self):
    glDisable(GL_TEXTURE_2D)
    glBegin(GL_POLYGON)
    glColor4f(*self.pms.header.BackgroundColorTop.for_gl_color())
    glVertex2f(self.pms.min_x, -self.pms.max_y)
    glVertex2f(self.pms.max_x, -self.pms.max_y)
    glColor4f(*self.pms.header.BackgroundColorBottom.for_gl_color())
    glVertex2f(self.pms.max_x, -self.pms.min_y)
    glVertex2f(self.pms.min_x, -self.pms.min_y)
    glEnd()
    glEnable(GL_TEXTURE_2D)

  def _polys(self):
    glShadeModel(GL_SMOOTH)
    img = self.images.load_image('textures', self.pms.header.Texture.filename())
    if img:
      glTexImage2D(GL_TEXTURE_2D, 0, 3, img['x'], img['y'], 0, GL_RGB, GL_UNSIGNED_BYTE, img['ref'])
      glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
      glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    glBegin(GL_TRIANGLES)
    for polygon in self.pms.polygons:
      for vertex in polygon.Vertexes:
        glColor4f(*vertex.color.for_gl_color())
        glTexCoord3f(vertex.tu, vertex.tv, vertex.rhw)
        glVertex3f(vertex.x, vertex.y, 0)
    glEnd()

  def paintGL(self):
    if not self.pms:
      return

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluOrtho2D(self.pms.min_x * self.zoom, self.pms.max_x * self.zoom, -self.pms.min_y * self.zoom, -self.pms.max_y * self.zoom)
    glEnable(GL_BLEND)
    glEnable(GL_TEXTURE_2D)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glClear(GL_COLOR_BUFFER_BIT)

    # The two polygons making up the background gradient
    self._background_gradient()

    # Place all polys
    self._polys()

    glLoadIdentity()
    glTranslatef(0.0, 0.0, 0.0)
    glFlush()

  # Let us zoom
  def wheelEvent(self, event):
    self.alter_zoom(event.delta() / 5000)
