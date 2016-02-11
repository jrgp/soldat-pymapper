# apt-get install python-qt4-gl python-opengl
from PyQt4 import QtOpenGL

# OpenGL methods
from OpenGL.GL import glClearColor, glColor3f, glColor4f, glBegin, glEnd, \
                      glVertex2f, glEnable, glMatrixMode, glLoadIdentity, \
                      glLoadIdentity, glTranslatef, glFlush, glBlendFunc, \
                      glClear, glDisable, glViewport, glClearDepth, \
                      glVertex3f

from OpenGL.GLU import gluOrtho2D, gluPerspective

# OpenGL constants
from OpenGL.GL import GL_POLYGON, GL_MODELVIEW, GL_BLEND, GL_TEXTURE_2D, \
                      GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_COLOR_BUFFER_BIT, \
                      GL_TRIANGLES


class MapWidget(QtOpenGL.QGLWidget):
  def __init__(self, parent=None):
    self.parent = parent
    QtOpenGL.QGLWidget.__init__(self, parent)
    self.setMinimumSize(500, 500)
    self.pms = None

  def render_map(self, pms, soldat_path):
    self.pms = pms
    self._soldat_path = soldat_path
    self.paintGL()


  def initializeGL(self):
    print 'init'

  def _background_gradient(self):
    glDisable(GL_TEXTURE_2D);
    glBegin(GL_POLYGON)
    glColor4f(*self.pms.header.BackgroundColorTop.for_gl_color())
    glVertex2f(self.pms.min_x, -self.pms.max_y)
    glVertex2f(self.pms.max_x, -self.pms.max_y)
    glColor4f(*self.pms.header.BackgroundColorBottom.for_gl_color())
    glVertex2f(self.pms.max_x, -self.pms.min_y)
    glVertex2f(self.pms.min_x, -self.pms.min_y)
    glEnd()
    glEnable(GL_TEXTURE_2D);

  def _polys(self):
    glBegin(GL_TRIANGLES)
    for polygon in self.pms.polygons:
      for i in range(3):
        glColor4f(*polygon.Vertexes[i].color.for_gl_color())
        #glTexCoord3f(polygon.Vertexes[i].tu, polygon.Vertexes[i].tv, polygon.Vertexes[i].rhw)
        glVertex3f(polygon.Vertexes[i].x, polygon.Vertexes[i].y, 0)
    glEnd()

    

  def paintGL(self):
    print 'paint'
    if not self.pms:
      return

    print 'showing things'

    sfactor = 1
    glClearColor(0.0, 0.0, 0.0, 0.0);
    glColor3f(0.0, 0.0, 1.0);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    gluOrtho2D(self.pms.min_x, self.pms.max_x, -self.pms.min_y, -self.pms.max_y);
    glEnable(GL_BLEND);
    glEnable(GL_TEXTURE_2D);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

    glClear(GL_COLOR_BUFFER_BIT);

    # The two polygons making up the background gradient
    self._background_gradient()

    # Place all polys
    self._polys()


    sfactor = 1

    glLoadIdentity();
    gluOrtho2D(self.pms.min_x, self.pms.max_x, self.pms.max_y, self.pms.min_y);
    glTranslatef(0.0, 0.0, 0.0)
    glFlush()


  def resizeGL(self, width, height):
    print 'resize'
