from pms import PmsReader
import os


class LoadMapException(Exception):
  pass


class MapState:

  def __init__(self):
    self.pms_path = ''
    self.pms_object = ''
    self.soldat_path = self.find_soldat_path()

  def find_soldat_path(self):
    path = os.path.expanduser('~/.wine/drive_c/Soldat')

    if os.path.exists(path) and os.path.isdir(path):
      return path

    return None

  def load_map(self, path):
    if not os.path.exists(path):
      raise LoadMapException('File not found')
    self.pms_object = PmsReader(path)
    self.pms_object.parse()
