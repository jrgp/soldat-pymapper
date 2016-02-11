from struct import unpack

from pms.header import T_Header
from pms.prop import T_Prop
from pms.scenery import T_Scenery
from pms.polygon import T_Polygon
from pms.collider import T_Collider
from pms.spawnpoint import T_Spawnpoint
from pms.waypoint import T_Waypoint


class PmsReader(object):
  '''
    Parse a Soldat pms map file
  '''

  def __init__(self, filename):
    self.filename = filename
    self.props = []
    self.sceneries = []
    self.polygons = []
    self.colliders = []
    self.spawnpoints = []
    self.waypoints = []
    self.header = None

  def _get_long(self, handle):
    return unpack('<l', handle.read(4))[0]

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
      self._get_long(h)
      num_sectors = self._get_long(h)
      for i in xrange(((num_sectors * 2) + 1) * ((num_sectors * 2) + 1)):
        sector_polys = unpack('H', h.read(2))[0]
        for j in xrange(sector_polys):
          h.read(2)

      # All props (scenery placements)
      prop_count = self._get_long(h)
      for i in xrange(prop_count):
        prop = T_Prop()
        h.readinto(prop)
        self.props.append(prop)

      # All sceneries (map prop style to scenery filename)
      scenery_count = self._get_long(h)
      for i in xrange(scenery_count):
        scenery = T_Scenery()
        h.readinto(scenery)
        self.sceneries.append(scenery)

      # Colliders
      collider_count = self._get_long(h)
      for i in xrange(collider_count):
        collider = T_Collider()
        h.readinto(collider)
        self.colliders.append(collider)

      # Spawnpoints
      spawnpoint_count = self._get_long(h)
      for i in xrange(spawnpoint_count):
        spawnpoint = T_Spawnpoint()
        h.readinto(spawnpoint)
        self.spawnpoints.append(spawnpoint)

      # Waypoints
      waypoint_count = self._get_long(h)
      for i in xrange(waypoint_count):
        waypoint = T_Waypoint()
        h.readinto(waypoint)
        self.waypoints.append(waypoint)

  @property
  def name(self):
    return self.header.Name.name()

  @property
  def texture(self):
    return self.header.Texture.filename()
