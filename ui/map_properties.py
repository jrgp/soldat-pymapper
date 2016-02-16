from PyQt4 import QtGui, QtCore, uic

class MapPropertiesWindow(QtGui.QMainWindow):

  '''
    Class corresponding to the main window. Try to delegate as much logic to
    outside classes as possible and just keep this a high level shim tying
    everything together
  '''

  def __init__(self, state):
    super(MapPropertiesWindow, self).__init__()
    self.ui = uic.loadUi('ui/map_properties.ui', self)
    self.state = state

  def update_info(self):
    self.ui.mapNameBox.setText(self.state.pms_object.name)
