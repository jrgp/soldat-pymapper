from pms import PmsReader


def main():
  filename = 'maps/ctf_Ash.pms'
  soldat_map = PmsReader(filename)
  soldat_map.parse()
  print 'Map name: ' + soldat_map.name
  print 'Texture: ' + soldat_map.texture

  print 'Scenery files used:'
  for scenery in soldat_map.sceneries.values():
    print scenery.filename

if __name__ == '__main__':
  main()
