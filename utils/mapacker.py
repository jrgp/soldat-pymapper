from pms import PmsReader
from zipfile import ZipFile
import os
import sys


def main():
  maps = sys.argv[1:]

  if not maps:
    print 'Provide me map files as arguments'
    return

  if len(maps) == 1:
    outfile = os.path.basename(maps[0]).split('.')[0] + '.zip'
  else:
    outfile = 'maps.zip'

  soldat_path = os.path.dirname(os.path.dirname(maps[0]))

  scenery_files = set()
  texture_files = set()
  map_files = set()

  for mapfile in maps:

    pms = PmsReader(mapfile)
    pms.parse()

    scenery_files |= set(scenery.filename for scenery in pms.sceneries.values())
    texture_files |= set([pms.texture])
    map_files |= set([mapfile])

  with ZipFile(outfile, 'w') as archive:

    for mapfile in map_files:
      archive.write(mapfile, os.path.join('maps', os.path.basename(mapfile)))

    for pic in scenery_files:
      orig_path = os.path.join(soldat_path, 'scenery-gfx', pic)
      if not os.path.exists(orig_path):
        print 'Missing scenery file {0}'.format(pic)
        continue

      archive.write(orig_path, os.path.join('scenery-gfx', pic))

    for pic in texture_files:
      orig_path = os.path.join(soldat_path, 'textures', pic)
      if not os.path.exists(orig_path):
        print 'Missing texture file {0}'.format(pic)
        continue

      archive.write(orig_path, os.path.join('textures', pic))
