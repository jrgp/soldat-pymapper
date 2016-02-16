import ctypes


class T_Spawnpoint(ctypes.Structure):
  _pack_ = 1
  _fields_ = [
      ('Active', ctypes.c_ubyte),
      ('_filler_', ctypes.c_ubyte * 3),
      ('x', ctypes.c_int),
      ('y', ctypes.c_int),
      ('Type', ctypes.c_int),
  ]
