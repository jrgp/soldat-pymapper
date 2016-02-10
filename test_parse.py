from pms import PmsReader
from pms.constants import T_Spawntype

def main():
  filename = 'maps/ctf_Ash.pms'
  soldat_map = PmsReader(filename)
  soldat_map.parse()
  print soldat_map.name
  print soldat_map.texture

  for scenery in soldat_map.sceneries:
    print scenery.filename()


if __name__ == '__main__':
  main()
