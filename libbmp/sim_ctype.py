

__all__ = ["SimByte", "SimWord", "SimDWord", "SimCTypeBase"]


class SimCTypeBase:

    byte_size = 1  # byte size
    signed = False
    endness = "little"

    @classmethod
    def from_bytes(self, buffer: bytes):
        return int.from_bytes(
            buffer, byteorder=self.endness, signed=self.signed)

    @classmethod
    def to_bytes(self, value: int):
        return int.to_bytes(
            value, self.byte_size, self.endness, signed=self.signed)


class SimByte(SimCTypeBase):
    ...


class SimWord(SimCTypeBase):
    byte_size = 2
    signed = False


class SimDWord(SimCTypeBase):
    byte_size = 4
    signed = True
