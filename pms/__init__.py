from struct import unpack

from pms.header import T_Header
from pms.prop import T_Prop
from pms.scenery import T_Scenery
from pms.polygon import T_Polygon


class PmsReader(object):
  '''
    Parse a Soldat pms map file
  '''

  def __init__(self, filename):
    self.filename = filename
    self.props = []
    self.sceneries = []
    self.polygons = []
    self.header = None

  def parse(self):
    with open(self.filename, 'rb') as h:

      # Map file header
      self.header = T_Header()
      h.readinto(self.header)

      # All polygons
      for i in xrange(self.header.PolyCount):
        polygon = T_Polygon()
        h.readinto(polygon)
        self.polygons.append(polygon)

      # Skip sector data we don't immediately care about
      sector_division = unpack('<l', h.read(4))[0]
      num_sectors = unpack('<l', h.read(4))[0]
      for i in xrange(((num_sectors * 2) + 1) * ((num_sectors * 2) + 1)):
        sector_polys = unpack('H', h.read(2))[0]
        for j in xrange(sector_polys):
          h.read(2)

      # All props (scenery placements)
      prop_count = unpack('<l', h.read(4))[0]
      for i in xrange(prop_count):
        prop = T_Prop()
        h.readinto(prop)
        self.props.append(prop)

      # All sceneries (map prop style to scenery filename)
      scenery_count = unpack('<l', h.read(4))[0]
      for i in xrange(scenery_count):
        scenery = T_Scenery()
        h.readinto(scenery)
        self.sceneries.append(scenery)

  @property
  def name(self):
    return self.header.Name.name()

  @property
  def texture(self):
    return self.header.Texture.filename()
