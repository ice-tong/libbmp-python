
"""
bmp format reference: https://en.wikipedia.org/wiki/BMP_file_format
"""

from .libbmp import BMPFile
from .bmp_colors import *
from .bmp_headers import *


def load_bmp(bmp_fname):
    bmp = BMPFile()
    bmp.read_bmp(bmp_fname)
    return bmp
