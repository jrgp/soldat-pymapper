import os
import Image


class ImageLoader:

  def __init__(self, soldat_path):
    self.soldat_path = soldat_path
    self.images = {}

  def load_image(self, usage, filename):
    key = (usage, filename)
    if key in self.images:
      return self.images[key]
    path = os.path.join(self.soldat_path, 'textures', filename)

    if not os.path.exists(path):
      if path.split('.')[-1] == 'bmp':
        path = '.'.join(path.split('.')[:-1] + ['png'])
        if not os.path.exists(path):
          return None

    img = Image.open(path)
    self.images[key] = dict(
        x=img.size[0],
        y=img.size[1],
        ref=img.tostring('raw', 'RGB', 0, -1)
    )

    return self.images[key]
