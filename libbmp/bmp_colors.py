
from .sim_ctype import SimByte


__all__ = ["Pixel16", "Pixel24", "Pixel32", "ColorTrue24", "ColorTrue32"]


class Pixel:

    __slots__ = ["color_b", "color_g", "color_r"]

    def __init__(self):
        for attr in self.__slots__:
            setattr(self, attr, None)
    
    @property
    def byte_size(self):
        return SimByte.byte_size * len(self.__slots__)

    def read_from_buffers(self, buffers):

        assert len(buffers) == self.byte_size, \
            "Except bytes length %s, get %s."% (self.byte_size, len(buffers))

        buffer_idx = 0

        for attr in self.__slots__:

            buffer = buffers[buffer_idx:buffer_idx+SimByte.byte_size]
            value = SimByte.from_bytes(buffer)

            setattr(self, attr, value)

            buffer_idx += SimByte.byte_size
    
    def to_buffers(self):

        # NOTE: Since the `+=` op of bytes obejct is so slow, use bytearray.
        buffers = bytearray(0)

        for attr in self.__slots__:
            value = getattr(self, attr)
            buffers += SimByte.to_bytes(value)

        return buffers
    
    def __str__(self, ishex=True):
        colors = []
        for attr in self.__slots__:
            color = getattr(self, attr)
            colors.append(hex(color) if ishex else str(color))
        return "(%s)" % ", ".join(colors)
    
    def __getitem__(self, index):
        return getattr(self, self.__slots__[index])


class Pixel16(Pixel):

    @property
    def byte_size(self):
        return 2
    
    # def read_from_buffers(self, buffers):
        
    #     assert len(buffers) == self.byte_size, \
    #         "Except bytes length %s, get %s."% (self.byte_size, len(buffers))

    #     buffer_idx = 0

    #     for attr in self.__slots__:

    #         buffer = buffers[buffer_idx:buffer_idx+SimByte.byte_size]
    #         value = sim_ctype.from_bytes(buffer)

    #         setattr(self, attr, value)

    #         buffer_idx += SimByte.byte_size


class Pixel24(Pixel):
    ...


class Pixel32(Pixel):
    __slots__ = ["color_a", "color_b", "color_g", "color_r"]


class ColorTrue:

    pixel = Pixel24

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.width_pad_size = (4 - width * self.pixel().byte_size % 4) % 4

        self.data: "[[Pixel, ...], ...]" = []

    @property
    def byte_size(self):
        pixel_num = abs(self.height * self.width)
        pad_byte_size = self.width_pad_size * self.height
        return self.pixel().byte_size * pixel_num + pad_byte_size

    def read_from_buffers(self, buffers):
 
        assert len(buffers) == self.byte_size, \
            "Except bytes length %s, get %s." % (len(buffers), self.byte_size)

        buffer_idx = 0

        for row_idx in range(self.height):

            row: "[Pixel, ...]" = []

            for col_idx in range(self.width):
                pixel = self.pixel()
                buffer = buffers[buffer_idx:buffer_idx+pixel.byte_size]
                pixel.read_from_buffers(buffer)
                row.append(pixel)
                buffer_idx += pixel.byte_size
            
            self.data.append(row)
            buffer_idx += self.width_pad_size
    
    def to_buffers(self):

        # NOTE: Since the `+=` op of bytes obejct is so slow, use bytearray.
        buffers = bytearray(0)

        for row_idx in range(self.height):

            for col_idx in range(self.width):
                pixel = self.data[row_idx][col_idx]
                buffers += pixel.to_buffers()

            buffers += bytes(self.width_pad_size)
        
        return buffers 
    
    def __str__(self):
        return "<%s Color Data @ (%s, %s)>" % (
            self.__class__.__name__, self.width, self.height)
    
    def __getitem__(self, index):
        return self.data[index]


class ColorTrue24(ColorTrue):
    ...


class ColorTrue32(ColorTrue):

    pixel = Pixel32
