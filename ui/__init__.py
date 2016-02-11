from __future__ import division
import os
import sys
import signal
from PyQt4 import QtGui, QtCore, uic
from ui.state import MapState, LoadMapException
from ui.renderer import MapWidget


class MainWindow(QtGui.QMainWindow):

  '''
    Class corresponding to the main window. Try to delegate as much logic to
    outside classes as possible and just keep this a high level shim tying
    everything together
  '''

  APP_NAME = 'Soldat MapWizard'

  def __init__(self):
    super(MainWindow, self).__init__()
    self.ui = uic.loadUi('ui/mainwindow.ui', self)

    # Register all navbar calls..
    self.connect(self.ui.actionOpen_Map, QtCore.SIGNAL('triggered()'), self, QtCore.SLOT('open()'))
    self.connect(self.ui.actionSave_Map, QtCore.SIGNAL('triggered()'), self, QtCore.SLOT('save()'))
    self.connect(self.ui.actionQuit, QtCore.SIGNAL('triggered()'), self, QtCore.SLOT('quit()'))

    # Keep all app state in this class..
    self.state = MapState()

    # Our OpenGL renderer should take up most of the internal window
    self.map_widget = MapWidget()
    self.setCentralWidget(self.map_widget)
    self.map_widget.show()

  @QtCore.pyqtSlot()
  def open(self):
    self._load_map(QtGui.QFileDialog.getOpenFileName())

  @QtCore.pyqtSlot()
  def save(self):
    print 'Will save map'

  @QtCore.pyqtSlot()
  def quit(self):
    sys.exit(0)

  def _load_map(self, path):
    try:
      self.state.load_map(path)
    except LoadMapException as e:
      # XXX: make this an error dialog
      print 'Failed loading map' + e
      return

    # At this point, we have a working map object
    self.setWindowTitle('{} - {}'.format(self.state.pms_object.name, self.APP_NAME))

    # Pass off... everything to the renderer class
    self.map_widget.render_map(self.state.pms_object, self.state.soldat_path)

  def wheelEvent(self, event):
    self.map_widget.alter_zoom(event.delta() / 1000)


def main():
  signal.signal(signal.SIGINT, signal.SIG_DFL)
  app = QtGui.QApplication(sys.argv)
  window = MainWindow()
  window.show()
  if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
    window._load_map(sys.argv[1])
  sys.exit(app.exec_())
