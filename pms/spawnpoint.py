import ctypes


class T_Spawnpoint(ctypes.Structure):
  _pack_ = 1
  _fields_ = [
      ('Active', ctypes.c_ubyte),
      ('_filler_', ctypes.c_ubyte * 3),
      ('x', ctypes.c_uint32),
      ('y', ctypes.c_uint32),
      ('Type', ctypes.c_int),
  ]
