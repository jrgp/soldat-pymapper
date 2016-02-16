import os
import Image


class ImageLoader:

  def __init__(self, soldat_path):
    self.soldat_path = soldat_path
    self.images = {}

  def _find_file(self, folder, filename):

    if folder == 'res':
      path = os.path.join(folder, filename)
      return path

    path = os.path.join(self.soldat_path, folder, filename)
    if not os.path.exists(path):
      if path.split('.')[-1] == 'bmp':
        path = '.'.join(path.split('.')[:-1] + ['png'])
        if not os.path.exists(path):
          return None
    return path

  def _transparency(self, img):
    pix = img.load()
    found = False

    for x in xrange(img.size[0]):
      for y in xrange(img.size[1]):
        if not isinstance(pix[x, y], tuple):
          continue

        if pix[x, y] == (0, 255, 0):
          pix[x, y] = (255, 255, 255, 0)
          found = True
          continue
    return found

  def load_image(self, folder, filename):
    key = (folder, filename)
    if key in self.images:
      return self.images[key]

    path = self._find_file(*key)

    if not path:
      print 'Couldn\'t find {} file {}'.format(folder, filename)
      self.images[key] = None
      return self.images[key]

    try:
      img = Image.open(path)
    except IOError:
      self.images[key] = None
      return self.images[key]
    # img.convert('RGBA')

    # if self._transparency(img):
    #  print '{} uses fake transparency'.format(path)

    try:
      self.images[key] = dict(
          x=img.size[0],
          y=img.size[1],
          ref=img.tostring('raw', 'RGB', 0, 1)
      )
    except SystemError as e:
      print 'Failed encoding {}: {}'.format(path, e)
      self.images[key] = None

    return self.images[key]
