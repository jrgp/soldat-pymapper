from pms import PmsReader

def main():
  filename = 'ctf_Ash.pms'
  soldat_map = PmsReader(filename)
  soldat_map.parse()
  print soldat_map.name
  print soldat_map.texture

if __name__ == '__main__':
  main()
