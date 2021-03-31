from .bmp_headers import BITMAPFILEHEADER, BITMAPINFOHEADER
from .bmp_colors import ColorTrue24, ColorTrue32
from .sim_ctype import SimByte, SimWord, SimDWord


COLOR_DATA_MAP = {
    24: ColorTrue24,
    32: ColorTrue32, 
}


class BMPFile:

    def __init__(self, bmp_fheader=None, bmp_iheader=None,
                 color_data=None):

        if bmp_fheader is None:
            self.bmp_fheader = BITMAPFILEHEADER()
        else:
            self.bmp_fheader = bmp_fheader
        
        if bmp_iheader is None:
            self.bmp_iheader = BITMAPINFOHEADER()
        else:
            self.bmp_fheader = bmp_fheader

        self.color_data = color_data

    @property
    def size(self):
        return self.bmp_iheader.biWidth, self.bmp_iheader.biHeight

    def __getitem__(self, index):
        if self.color_data is None:
            return None
        return self.color_data[index]
    
    def __len__(self):
        if self.color_data is None:
            return 0
        return len(self.color_data)

    #
    # I/O method.
    #

    def read_bmp(self, bmp_fname):

        with open(bmp_fname, "rb") as f:

            buffers = f.read(self.bmp_fheader.byte_size)
            self.bmp_fheader.read_from_buffers(buffers)

            buffers = f.read(self.bmp_iheader.byte_size)
            self.bmp_iheader.read_from_buffers(buffers)

            bit_count = self.bmp_iheader.biBitCount
            width, height = self.bmp_iheader.biWidth, self.bmp_iheader.biHeight
            width = - width if width < 0 else width
            height = - height if height < 0 else height

            if bit_count <= 8:
                # There must have used a color palette.
                raise NotImplementedError("There must have used a color palette.")
            
            if self.bmp_iheader.biCompression != 0:
                # Unsupport compression method.
                raise NotImplementedError(
                    "Sadly, only the `BI_RGB` compression method is support.")

            if self.bmp_fheader.bfOffBits != 0x36:
                # Except bfOffBits: 0x36.
                f.read(self.bmp_fheader.bfOffBits - 0x36)
                # raise NotImplementedError("Except bfOffBits: 0x36, get %#x."
                #     % self.bmp_fheader.bfOffBits)

            if bit_count in COLOR_DATA_MAP:
                self.color_data = COLOR_DATA_MAP[bit_count](width, height)
            else:
                # TODO: 1bit, 4bit, 6bit, 8bit and 16bit(555).
                raise NotImplementedError("TODO: 1bit, 4bit, 6bit, 8bit and 16bit(555).")

            buffers = f.read(self.color_data.byte_size)
            self.color_data.read_from_buffers(buffers)

            assert f.read() == b'', "Seems to be something worng..."

    def save_bmp(self, save_bmp_fname):

        with open(save_bmp_fname, "wb") as f:

            buffers = self.bmp_fheader.to_buffers()
            f.write(buffers)

            buffers = self.bmp_iheader.to_buffers()
            f.write(buffers)

            if self.bmp_iheader.biBitCount <= 8:
                # There must have used a color palette.
                raise NotImplementedError("There must have used a color palette.")
            
            if self.bmp_iheader.biCompression != 0:
                # Unsupport compression method.
                raise NotImplementedError(
                    "Sadly, only the `BI_RGB` compression method is support.")

            if self.bmp_fheader.bfOffBits != 0x36:
                # Except bfOffBits: 0x36.
                f.write(bytes(self.bmp_fheader.bfOffBits - 0x36))
                # raise NotImplementedError("Except bfOffBits: 0x36, get %#x."
                #     % self.bmp_fheader.bfOffBits)

            buffers = self.color_data.to_buffers()
            f.write(buffers)
