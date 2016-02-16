from PyQt4 import QtGui, uic
from pms.constants import T_Steps, T_Weather


class MapPropertiesWindow(QtGui.QMainWindow):

  '''
    Small modal window which lets you change simple settings on the map
  '''

  def __init__(self, state):
    '''
      Localize state and populate drop downs with available values and
      register callbacks
    '''
    super(MapPropertiesWindow, self).__init__()
    self.ui = uic.loadUi('ui/map_properties.ui', self)
    self.state = state
    self.ui.weatherComboBox.addItems(T_Weather)
    self.ui.stepsComboBox.addItems(T_Steps)

    self.ui.saveButton.clicked.connect(self.save_info)

  def update_info(self):
    '''
      Set text fields and drop down indexes to what the map currently has
      configured
    '''
    self.ui.mapNameBox.setText(self.state.pms_object.name)
    self.ui.weatherComboBox.setCurrentIndex(self.state.pms_object.header.Weather)
    self.ui.stepsComboBox.setCurrentIndex(self.state.pms_object.header.Steps)
    self.ui.jetsSlider.setValue(self.state.pms_object.header.Jets)
    self.ui.grenadesSpinBox.setValue(self.state.pms_object.header.Grenades)
    self.ui.medkitsSpinBox.setValue(self.state.pms_object.header.Medkits)

  def save_info(self):
    print 'would save'
    self.close()
