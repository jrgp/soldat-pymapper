import os
import sys
import signal
from PyQt4 import QtGui, QtCore, uic
from ui.state import MapState, LoadMapException
from ui.renderer import MapWidget
from ui.map_properties import MapPropertiesWindow


class MainWindow(QtGui.QMainWindow):

  '''
    Class corresponding to the main window. Try to delegate as much logic to
    outside classes as possible and just keep this a high level shim tying
    everything together
  '''

  APP_NAME = 'Soldat PyMapper'

  def __init__(self):
    super(MainWindow, self).__init__()
    self.ui = uic.loadUi('ui/mainwindow.ui', self)

    # Register all navbar calls..
    self.ui.actionOpen_Map.triggered.connect(self.open)
    self.ui.actionSave_Map.triggered.connect(self.save)
    self.ui.actionMap_Properties.triggered.connect(self.show_properties)
    self.ui.actionQuit.triggered.connect(self.quit)

    # View item checkboxes
    self.ui.texturesCheckBox.stateChanged.connect(lambda: self.toggle_item('textures', self.ui.texturesCheckBox))
    self.ui.sceneryCheckBox.stateChanged.connect(lambda: self.toggle_item('scenery', self.ui.sceneryCheckBox))
    self.ui.polygonsCheckBox.stateChanged.connect(lambda: self.toggle_item('polygons', self.ui.polygonsCheckBox))
    self.ui.wireframeCheckBox.stateChanged.connect(lambda: self.toggle_item('wireframe', self.ui.wireframeCheckBox))
    self.ui.backgroundCheckBox.stateChanged.connect(lambda: self.toggle_item('background', self.ui.backgroundCheckBox))
    self.ui.spawnsCheckBox.stateChanged.connect(lambda: self.toggle_item('spawns', self.ui.spawnsCheckBox))
    self.ui.gridCheckBox.stateChanged.connect(lambda: self.toggle_item('grid', self.ui.gridCheckBox))

    # Keep all app state in this class..
    self.state = MapState()

    # Our OpenGL renderer should take up most of the internal window
    self.map_widget = MapWidget()
    self.setCentralWidget(self.map_widget)
    self.map_widget.show()

    # Our map properties window that has stuff like texture and name and stuff
    self.map_properties = MapPropertiesWindow(self.state)

  @QtCore.pyqtSlot()
  def open(self):
    self._load_map(QtGui.QFileDialog.getOpenFileName())

  @QtCore.pyqtSlot()
  def save(self):
    pass

  @QtCore.pyqtSlot()
  def quit(self):
    sys.exit(0)

  @QtCore.pyqtSlot()
  def show_properties(self):
    self.map_properties.update_info()
    self.map_properties.show()

  @QtCore.pyqtSlot()
  def toggle_item(self, item, element):
    self.map_widget.show_items[item] = element.isChecked()
    self.map_widget.update()

  def _load_map(self, path):

    if not path:
      return

    try:
      self.state.load_map(path)
    except LoadMapException as e:
      QtGui.QMessageBox.critical(None, 'Failed loading map', str(e))
      return

    self.setWindowTitle('{} - {}'.format(self.state.pms_object.name, self.APP_NAME))
    self.map_widget.render_map(self.state.pms_object, self.state.soldat_path)
    self.ui.statusbar.showMessage(os.path.abspath(str(path)))

  def keyPressEvent(self, event):
    if type(event) != QtGui.QKeyEvent:
      return

    key = event.key()

    if key == QtCore.Qt.Key_A:
      self.map_widget.scroll_x -= 200
    elif key == QtCore.Qt.Key_D:
      self.map_widget.scroll_x += 200
    elif key == QtCore.Qt.Key_W:
      self.map_widget.scroll_y -= 200
    elif key == QtCore.Qt.Key_S:
      self.map_widget.scroll_y += 200
    else:
      return

    self.map_widget.update()


def main():
  signal.signal(signal.SIGINT, signal.SIG_DFL)
  app = QtGui.QApplication(sys.argv)
  window = MainWindow()
  window.show()
  if len(sys.argv) > 1:
    window._load_map(sys.argv[1])
  sys.exit(app.exec_())
