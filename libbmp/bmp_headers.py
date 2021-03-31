from .sim_ctype import SimWord, SimDWord


__all__ = ["BITMAPFILEHEADER", "BITMAPINFOHEADER"]


class HEADERBase:

    __slots__ = []
    _member_type_map = {}

    def __init__(self):
        for attr in self.__slots__:
            setattr(self, attr, 0)
    
    @property
    def byte_size(self):
        _byte_size = 0
        for attr in self.__slots__:
            _byte_size += self._member_type_map[attr].byte_size
        return _byte_size

    def read_from_buffers(self, buffers):

        assert len(buffers) == self.byte_size, \
            "Except bytes length %s, get %s." % (len(buffers), self.byte_size)

        buffer_idx = 0

        for attr in self.__slots__:

            sim_ctype: "SimCTypeBase" = self._member_type_map[attr]
            buffer = buffers[buffer_idx:buffer_idx+sim_ctype.byte_size]
            value = sim_ctype.from_bytes(buffer)

            setattr(self, attr, value)

            buffer_idx += sim_ctype.byte_size
    
    def to_buffers(self):

        # NOTE: Since the `+=` op of bytes obejct is so slow, use bytearray.
        buffers = bytearray(0)

        for attr in self.__slots__:
            value = getattr(self, attr)
            sim_ctype: "SimCTypeBase" = self._member_type_map[attr]
            buffers += sim_ctype.to_bytes(value)
    
        return buffers

    def __str__(self, ishex=True):
        members = []
        for attr in self.__slots__:
            value = getattr(self, attr)
            members.append("%s=%s" % (attr, hex(value) if ishex else value))
        return "<%s @ (%s)>" % (self.__class__.__name__, ", ".join(members))


class BITMAPFILEHEADER(HEADERBase):

    __slots__ = ["bfType", "bfSize", "bfReserved1", "bfReserved2", "bfOffBits"]
    
    _member_type_map = {
        "bfType": SimWord, "bfSize": SimDWord,
        "bfReserved1": SimWord, "bfReserved2": SimWord,
        "bfOffBits": SimDWord
    }


class BITMAPINFOHEADER(HEADERBase):

    __slots__ = [
        "biSize", "biWidth", "biHeight", "biPlanes", "biBitCount",
        "biCompression", "biSizeImage", "biXPelsPerMeter",
        "biYPelsPerMeter", "biClrUsed", "biClrImportant"
        ]
    
    _member_type_map = {
        "biSize": SimDWord, "biWidth": SimDWord,
        "biHeight": SimDWord, "biPlanes": SimWord,
        "biBitCount": SimWord, "biCompression": SimDWord,
        "biSizeImage": SimDWord, "biXPelsPerMeter": SimDWord,
        "biYPelsPerMeter": SimDWord, "biClrUsed": SimDWord,
        "biClrImportant": SimDWord
    }
