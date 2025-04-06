# TODO: further vectorize
# Python version by: t-wy

import io, numpy as np
from collections import namedtuple as T
class r(io.BytesIO):
    def readUInt(self, size):
        return int.from_bytes(self.read(size), byteorder='big')
    def readInt(self, size):
        thr = 1 << (size << 3)
        tmp = self.readUInt(size)
        return tmp - thr if tmp >= thr >> 1 else tmp
    def readStruct(self, form):
        import struct
        tmp = struct.Struct(form)
        return tmp.unpack(self.read(tmp.size))
    def readNullString(self):
        tmp = b""
        while True:
            c = self.read(1)
            if c[0] == 0:
                return tmp
            else:
                tmp += c
    def peek(self, size):
        pt = self.tell()
        tmp = self.read(size)
        self.seek(pt)
        return tmp


def combineBytes(src, name: str, cnt: int):
    src = src._asdict()
    src[name] = 0
    for i in range(cnt):
        src[name] <<= 8
        src[name] += src[name + str(i)]
        del src[name + str(i)]
    return T('GenericDict', src.keys())(**src)


def c(name: str, cnt: int):
    return ["{}{}".format(name, x) for x in range(cnt)]


def byteFloat(b):
    import struct
    return struct.Struct(">f").unpack(b)[0]


athList = [ # Absolute Threshold of Hearing
    0x78,0x5F,0x56,0x51,0x4E,0x4C,0x4B,0x49,0x48,0x48,0x47,0x46,0x46,0x45,0x45,0x45,
    0x44,0x44,0x44,0x44,0x43,0x43,0x43,0x43,0x43,0x43,0x42,0x42,0x42,0x42,0x42,0x42,
    0x42,0x42,0x41,0x41,0x41,0x41,0x41,0x41,0x41,0x41,0x41,0x41,0x40,0x40,0x40,0x40,
    0x40,0x40,0x40,0x40,0x40,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,
    0x3F,0x3F,0x3F,0x3E,0x3E,0x3E,0x3E,0x3E,0x3E,0x3D,0x3D,0x3D,0x3D,0x3D,0x3D,0x3D,
    0x3C,0x3C,0x3C,0x3C,0x3C,0x3C,0x3C,0x3C,0x3B,0x3B,0x3B,0x3B,0x3B,0x3B,0x3B,0x3B,
    0x3B,0x3B,0x3B,0x3B,0x3B,0x3B,0x3B,0x3B,0x3B,0x3B,0x3B,0x3B,0x3B,0x3B,0x3B,0x3B,
    0x3B,0x3B,0x3B,0x3B,0x3B,0x3B,0x3B,0x3B,0x3C,0x3C,0x3C,0x3C,0x3C,0x3C,0x3C,0x3C,
    0x3D,0x3D,0x3D,0x3D,0x3D,0x3D,0x3D,0x3D,0x3E,0x3E,0x3E,0x3E,0x3E,0x3E,0x3E,0x3F,
    0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,
    0x3F,0x3F,0x3F,0x3F,0x40,0x40,0x40,0x40,0x40,0x40,0x40,0x40,0x40,0x40,0x40,0x40,
    0x40,0x40,0x40,0x40,0x40,0x40,0x40,0x40,0x40,0x41,0x41,0x41,0x41,0x41,0x41,0x41,
    0x41,0x41,0x41,0x41,0x41,0x41,0x41,0x41,0x41,0x41,0x41,0x41,0x41,0x41,0x41,0x41,
    0x41,0x41,0x41,0x41,0x41,0x41,0x41,0x42,0x42,0x42,0x42,0x42,0x42,0x42,0x42,0x42,
    0x42,0x42,0x42,0x42,0x42,0x42,0x42,0x42,0x42,0x42,0x42,0x42,0x42,0x43,0x43,0x43,
    0x43,0x43,0x43,0x43,0x43,0x43,0x43,0x43,0x43,0x43,0x43,0x43,0x43,0x43,0x44,0x44,
    0x44,0x44,0x44,0x44,0x44,0x44,0x44,0x44,0x44,0x44,0x44,0x44,0x45,0x45,0x45,0x45,
    0x45,0x45,0x45,0x45,0x45,0x45,0x45,0x45,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,
    0x46,0x46,0x47,0x47,0x47,0x47,0x47,0x47,0x47,0x47,0x47,0x47,0x48,0x48,0x48,0x48,
    0x48,0x48,0x48,0x48,0x49,0x49,0x49,0x49,0x49,0x49,0x49,0x49,0x4A,0x4A,0x4A,0x4A,
    0x4A,0x4A,0x4A,0x4A,0x4B,0x4B,0x4B,0x4B,0x4B,0x4B,0x4B,0x4C,0x4C,0x4C,0x4C,0x4C,
    0x4C,0x4D,0x4D,0x4D,0x4D,0x4D,0x4D,0x4E,0x4E,0x4E,0x4E,0x4E,0x4E,0x4F,0x4F,0x4F,
    0x4F,0x4F,0x4F,0x50,0x50,0x50,0x50,0x50,0x51,0x51,0x51,0x51,0x51,0x52,0x52,0x52,
    0x52,0x52,0x53,0x53,0x53,0x53,0x54,0x54,0x54,0x54,0x54,0x55,0x55,0x55,0x55,0x56,
    0x56,0x56,0x56,0x57,0x57,0x57,0x57,0x57,0x58,0x58,0x58,0x59,0x59,0x59,0x59,0x5A,
    0x5A,0x5A,0x5A,0x5B,0x5B,0x5B,0x5B,0x5C,0x5C,0x5C,0x5D,0x5D,0x5D,0x5D,0x5E,0x5E,
    0x5E,0x5F,0x5F,0x5F,0x60,0x60,0x60,0x61,0x61,0x61,0x61,0x62,0x62,0x62,0x63,0x63,
    0x63,0x64,0x64,0x64,0x65,0x65,0x66,0x66,0x66,0x67,0x67,0x67,0x68,0x68,0x68,0x69,
    0x69,0x6A,0x6A,0x6A,0x6B,0x6B,0x6B,0x6C,0x6C,0x6D,0x6D,0x6D,0x6E,0x6E,0x6F,0x6F,
    0x70,0x70,0x70,0x71,0x71,0x72,0x72,0x73,0x73,0x73,0x74,0x74,0x75,0x75,0x76,0x76,
    0x77,0x77,0x78,0x78,0x78,0x79,0x79,0x7A,0x7A,0x7B,0x7B,0x7C,0x7C,0x7D,0x7D,0x7E,
    0x7E,0x7F,0x7F,0x80,0x80,0x81,0x81,0x82,0x83,0x83,0x84,0x84,0x85,0x85,0x86,0x86,
    0x87,0x88,0x88,0x89,0x89,0x8A,0x8A,0x8B,0x8C,0x8C,0x8D,0x8D,0x8E,0x8F,0x8F,0x90,
    0x90,0x91,0x92,0x92,0x93,0x94,0x94,0x95,0x95,0x96,0x97,0x97,0x98,0x99,0x99,0x9A,
    0x9B,0x9B,0x9C,0x9D,0x9D,0x9E,0x9F,0xA0,0xA0,0xA1,0xA2,0xA2,0xA3,0xA4,0xA5,0xA5,
    0xA6,0xA7,0xA7,0xA8,0xA9,0xAA,0xAA,0xAB,0xAC,0xAD,0xAE,0xAE,0xAF,0xB0,0xB1,0xB1,
    0xB2,0xB3,0xB4,0xB5,0xB6,0xB6,0xB7,0xB8,0xB9,0xBA,0xBA,0xBB,0xBC,0xBD,0xBE,0xBF,
    0xC0,0xC1,0xC1,0xC2,0xC3,0xC4,0xC5,0xC6,0xC7,0xC8,0xC9,0xC9,0xCA,0xCB,0xCC,0xCD,
    0xCE,0xCF,0xD0,0xD1,0xD2,0xD3,0xD4,0xD5,0xD6,0xD7,0xD8,0xD9,0xDA,0xDB,0xDC,0xDD,
    0xDE,0xDF,0xE0,0xE1,0xE2,0xE3,0xE4,0xE5,0xE6,0xE7,0xE8,0xE9,0xEA,0xEB,0xED,0xEE,
    0xEF,0xF0,0xF1,0xF2,0xF3,0xF4,0xF5,0xF7,0xF8,0xF9,0xFA,0xFB,0xFC,0xFD,0xFF,0xFF,
]
CRC16Table = [
    0x0000,0x8005,0x800F,0x000A,0x801B,0x001E,0x0014,0x8011,0x8033,0x0036,0x003C,0x8039,0x0028,0x802D,0x8027,0x0022,
    0x8063,0x0066,0x006C,0x8069,0x0078,0x807D,0x8077,0x0072,0x0050,0x8055,0x805F,0x005A,0x804B,0x004E,0x0044,0x8041,
    0x80C3,0x00C6,0x00CC,0x80C9,0x00D8,0x80DD,0x80D7,0x00D2,0x00F0,0x80F5,0x80FF,0x00FA,0x80EB,0x00EE,0x00E4,0x80E1,
    0x00A0,0x80A5,0x80AF,0x00AA,0x80BB,0x00BE,0x00B4,0x80B1,0x8093,0x0096,0x009C,0x8099,0x0088,0x808D,0x8087,0x0082,
    0x8183,0x0186,0x018C,0x8189,0x0198,0x819D,0x8197,0x0192,0x01B0,0x81B5,0x81BF,0x01BA,0x81AB,0x01AE,0x01A4,0x81A1,
    0x01E0,0x81E5,0x81EF,0x01EA,0x81FB,0x01FE,0x01F4,0x81F1,0x81D3,0x01D6,0x01DC,0x81D9,0x01C8,0x81CD,0x81C7,0x01C2,
    0x0140,0x8145,0x814F,0x014A,0x815B,0x015E,0x0154,0x8151,0x8173,0x0176,0x017C,0x8179,0x0168,0x816D,0x8167,0x0162,
    0x8123,0x0126,0x012C,0x8129,0x0138,0x813D,0x8137,0x0132,0x0110,0x8115,0x811F,0x011A,0x810B,0x010E,0x0104,0x8101,
    0x8303,0x0306,0x030C,0x8309,0x0318,0x831D,0x8317,0x0312,0x0330,0x8335,0x833F,0x033A,0x832B,0x032E,0x0324,0x8321,
    0x0360,0x8365,0x836F,0x036A,0x837B,0x037E,0x0374,0x8371,0x8353,0x0356,0x035C,0x8359,0x0348,0x834D,0x8347,0x0342,
    0x03C0,0x83C5,0x83CF,0x03CA,0x83DB,0x03DE,0x03D4,0x83D1,0x83F3,0x03F6,0x03FC,0x83F9,0x03E8,0x83ED,0x83E7,0x03E2,
    0x83A3,0x03A6,0x03AC,0x83A9,0x03B8,0x83BD,0x83B7,0x03B2,0x0390,0x8395,0x839F,0x039A,0x838B,0x038E,0x0384,0x8381,
    0x0280,0x8285,0x828F,0x028A,0x829B,0x029E,0x0294,0x8291,0x82B3,0x02B6,0x02BC,0x82B9,0x02A8,0x82AD,0x82A7,0x02A2,
    0x82E3,0x02E6,0x02EC,0x82E9,0x02F8,0x82FD,0x82F7,0x02F2,0x02D0,0x82D5,0x82DF,0x02DA,0x82CB,0x02CE,0x02C4,0x82C1,
    0x8243,0x0246,0x024C,0x8249,0x0258,0x825D,0x8257,0x0252,0x0270,0x8275,0x827F,0x027A,0x826B,0x026E,0x0264,0x8261,
    0x0220,0x8225,0x822F,0x022A,0x823B,0x023E,0x0234,0x8231,0x8213,0x0216,0x021C,0x8219,0x0208,0x820D,0x8207,0x0202,
] # 0x8005 / CRC-16-IBM
# v3.0
scalelist = [
    0x0E,0x0E,0x0E,0x0E,0x0E,0x0E,0x0D,0x0D,
    0x0D,0x0D,0x0D,0x0D,0x0C,0x0C,0x0C,0x0C,
    0x0C,0x0C,0x0B,0x0B,0x0B,0x0B,0x0B,0x0B,
    0x0A,0x0A,0x0A,0x0A,0x0A,0x0A,0x0A,0x09,
    0x09,0x09,0x09,0x09,0x09,0x08,0x08,0x08,
    0x08,0x08,0x08,0x07,0x06,0x06,0x05,0x04,
    0x04,0x04,0x03,0x03,0x03,0x02,0x02,0x02,
    0x02,0x01,0x01,0x01,0x01,0x01,0x01,0x01,
    0x01,0x01
]
"""
v2.0
scalelist = [
    0x0E,0x0E,0x0E,0x0E,0x0E,0x0E,0x0D,0x0D,
    0x0D,0x0D,0x0D,0x0D,0x0C,0x0C,0x0C,0x0C,
    0x0C,0x0C,0x0B,0x0B,0x0B,0x0B,0x0B,0x0B,
    0x0A,0x0A,0x0A,0x0A,0x0A,0x0A,0x0A,0x09,
    0x09,0x09,0x09,0x09,0x09,0x08,0x08,0x08,
    0x08,0x08,0x08,0x07,0x06,0x06,0x05,0x04,
    0x04,0x04,0x03,0x03,0x03,0x02,0x02,0x02,
    0x02,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
]
v1.3
scalelist = [
    0x0E,0x0E,0x0E,0x0E,0x0E,0x0E,0x0D,0x0D,
    0x0D,0x0D,0x0D,0x0D,0x0C,0x0C,0x0C,0x0C,
    0x0C,0x0C,0x0B,0x0B,0x0B,0x0B,0x0B,0x0B,
    0x0A,0x0A,0x0A,0x0A,0x0A,0x0A,0x0A,0x09,
    0x09,0x09,0x09,0x09,0x09,0x08,0x08,0x08,
    0x08,0x08,0x08,0x07,0x06,0x06,0x05,0x04,
    0x04,0x04,0x03,0x03,0x03,0x02,0x02,0x02,
    0x02,0x01,0x01,0x01,0x01,0x01,0x01,0x01,
]
"""
valueInt = [
    b"\x34\x2A\x8D\x26",b"\x34\x63\x3F\x89",b"\x34\x97\x65\x7D",b"\x34\xC9\xB9\xBE",b"\x35\x06\x64\x91",b"\x35\x33\x11\xC4",b"\x35\x6E\x99\x10",b"\x35\x9E\xF5\x32",
    b"\x35\xD3\xCC\xF1",b"\x36\x0D\x1A\xDF",b"\x36\x3C\x03\x4A",b"\x36\x7A\x83\xB3",b"\x36\xA6\xE5\x95",b"\x36\xDE\x60\xF5",b"\x37\x14\x26\xFF",b"\x37\x45\x67\x2A",
    b"\x37\x83\x83\x59",b"\x37\xAF\x3B\x79",b"\x37\xE9\x7C\x38",b"\x38\x1B\x8D\x3A",b"\x38\x4F\x43\x19",b"\x38\x8A\x14\xD5",b"\x38\xB7\xFB\xF0",b"\x38\xF5\x25\x7D",
    b"\x39\x23\x52\x0F",b"\x39\x59\x9D\x16",b"\x39\x90\xFA\x4D",b"\x39\xC1\x2C\x4D",b"\x3A\x00\xB1\xED",b"\x3A\x2B\x7A\x3A",b"\x3A\x64\x7B\x6D",b"\x3A\x98\x37\xF0",
    b"\x3A\xCA\xD2\x26",b"\x3B\x07\x1F\x62",b"\x3B\x34\x0A\xAF",b"\x3B\x6F\xE4\xBA",b"\x3B\x9F\xD2\x28",b"\x3B\xD4\xF3\x5B",b"\x3C\x0D\xDF\x04",b"\x3C\x3D\x08\xA4",
    b"\x3C\x7B\xDF\xED",b"\x3C\xA7\xCD\x94",b"\x3C\xDF\x96\x13",b"\x3D\x14\xF4\xF0",b"\x3D\x46\x79\x91",b"\x3D\x84\x3A\x29",b"\x3D\xB0\x2F\x0E",b"\x3D\xEA\xC0\xC7",
    b"\x3E\x1C\x65\x73",b"\x3E\x50\x63\x34",b"\x3E\x8A\xD4\xC6",b"\x3E\xB8\xFB\xAF",b"\x3E\xF6\x7A\x41",b"\x3F\x24\x35\x16",b"\x3F\x5A\xCB\x94",b"\x3F\x91\xC3\xD3",
    b"\x3F\xC2\x38\xD2",b"\x40\x01\x64\xD2",b"\x40\x2C\x68\x97",b"\x40\x65\xB9\x07",b"\x40\x99\x0B\x88",b"\x40\xCB\xEC\x15",b"\x41\x07\xDB\x35",b"\x41\x35\x04\xF3",
]
valueFloat = np.array([byteFloat(v) for v in valueInt])
scaleInt = [
    b"\x3F\x80\x00\x00",b"\x3F\x2A\xAA\xAB",b"\x3E\xCC\xCC\xCD",b"\x3E\x92\x49\x25",b"\x3E\x63\x8E\x39",b"\x3E\x3A\x2E\x8C",b"\x3E\x1D\x89\xD9",b"\x3E\x08\x88\x89",
    b"\x3D\x84\x21\x08",b"\x3D\x02\x08\x21",b"\x3C\x81\x02\x04",b"\x3C\x00\x80\x81",b"\x3B\x80\x40\x20",b"\x3B\x00\x20\x08",b"\x3A\x80\x10\x02",b"\x3A\x00\x08\x01",
]
scaleFloat = np.array([byteFloat(v) for v in scaleInt])
max_bit_table = [ 0,2,3,3,4,4,4,4,5,6,7,8,9,10,11,12 ]
read_bit_table = [
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
    1,1,2,2,0,0,0,0,0,0,0,0,0,0,0,0,
    2,2,2,2,2,2,3,3,0,0,0,0,0,0,0,0,
    2,2,3,3,3,3,3,3,0,0,0,0,0,0,0,0,
    3,3,3,3,3,3,3,3,3,3,3,3,3,3,4,4,
    3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,
    3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,
    3,3,4,4,4,4,4,4,4,4,4,4,4,4,4,4,
]
read_val_table = [
    +0,+0,+0,+0,+0,+0,+0,+0,+0,+0,+0,+0,+0,+0,+0,+0,
    +0,+0,+1,-1,+0,+0,+0,+0,+0,+0,+0,+0,+0,+0,+0,+0,
    +0,+0,+1,+1,-1,-1,+2,-2,+0,+0,+0,+0,+0,+0,+0,+0,
    +0,+0,+1,-1,+2,-2,+3,-3,+0,+0,+0,+0,+0,+0,+0,+0,
    +0,+0,+1,+1,-1,-1,+2,+2,-2,-2,+3,+3,-3,-3,+4,-4,
    +0,+0,+1,+1,-1,-1,+2,+2,-2,-2,+3,-3,+4,-4,+5,-5,
    +0,+0,+1,+1,-1,-1,+2,-2,+3,-3,+4,-4,+5,-5,+6,-6,
    +0,+0,+1,-1,+2,-2,+3,-3,+4,-4,+5,-5,+6,-6,+7,-7,
]
scale_conversion_table_hex = [[
    b"\x00\x00\x00\x00",b"\x00\x00\x00\x00",b"\x32\xA0\xB0\x51",b"\x32\xD6\x1B\x5E",b"\x33\x0E\xA4\x3A",b"\x33\x3E\x0F\x68",b"\x33\x7D\x3E\x0C",b"\x33\xA8\xB6\xD5",
    b"\x33\xE0\xCC\xDF",b"\x34\x15\xC3\xFF",b"\x34\x47\x8D\x75",b"\x34\x84\xF1\xF6",b"\x34\xB1\x23\xF6",b"\x34\xEC\x07\x19",b"\x35\x1D\x3E\xDA",b"\x35\x51\x84\xDF",
    b"\x35\x8B\x95\xC2",b"\x35\xB9\xFC\xD2",b"\x35\xF7\xD0\xDF",b"\x36\x25\x19\x58",b"\x36\x5B\xFB\xB8",b"\x36\x92\x8E\x72",b"\x36\xC3\x46\xCD",b"\x37\x02\x18\xAF",
    b"\x37\x2D\x58\x3F",b"\x37\x66\xF8\x5B",b"\x37\x99\xE0\x46",b"\x37\xCD\x07\x8C",b"\x38\x08\x98\x0F",b"\x38\x36\x00\x94",b"\x38\x72\x81\x77",b"\x38\xA1\x8F\xAF",
    b"\x38\xD7\x44\xFD",b"\x39\x0F\x6A\x81",b"\x39\x3F\x17\x9A",b"\x39\x7E\x9E\x11",b"\x39\xA9\xA1\x5B",b"\x39\xE2\x05\x5B",b"\x3A\x16\x94\x2D",b"\x3A\x48\xA2\xD8",
    b"\x3A\x85\xAA\xC3",b"\x3A\xB2\x1A\x32",b"\x3A\xED\x4F\x30",b"\x3B\x1E\x19\x6E",b"\x3B\x52\xA8\x1E",b"\x3B\x8C\x57\xCA",b"\x3B\xBA\xFF\x5B",b"\x3B\xF9\x29\x5A",
    b"\x3C\x25\xFE\xD7",b"\x3C\x5D\x2D\x82",b"\x3C\x93\x5A\x2B",b"\x3C\xC4\x56\x3F",b"\x3D\x02\xCD\x87",b"\x3D\x2E\x49\x34",b"\x3D\x68\x39\x6A",b"\x3D\x9A\xB6\x2B",
    b"\x3D\xCE\x24\x8C",b"\x3E\x09\x55\xEE",b"\x3E\x36\xFD\x92",b"\x3E\x73\xD2\x90",b"\x3E\xA2\x70\x43",b"\x3E\xD8\x70\x39",b"\x3F\x10\x31\xDC",b"\x3F\x40\x21\x3B",
],[
    b"\x3F\x80\x00\x00",b"\x3F\xAA\x8D\x26",b"\x3F\xE3\x3F\x89",b"\x40\x17\x65\x7D",b"\x40\x49\xB9\xBE",b"\x40\x86\x64\x91",b"\x40\xB3\x11\xC4",b"\x40\xEE\x99\x10",
    b"\x41\x1E\xF5\x32",b"\x41\x53\xCC\xF1",b"\x41\x8D\x1A\xDF",b"\x41\xBC\x03\x4A",b"\x41\xFA\x83\xB3",b"\x42\x26\xE5\x95",b"\x42\x5E\x60\xF5",b"\x42\x94\x26\xFF",
    b"\x42\xC5\x67\x2A",b"\x43\x03\x83\x59",b"\x43\x2F\x3B\x79",b"\x43\x69\x7C\x38",b"\x43\x9B\x8D\x3A",b"\x43\xCF\x43\x19",b"\x44\x0A\x14\xD5",b"\x44\x37\xFB\xF0",
    b"\x44\x75\x25\x7D",b"\x44\xA3\x52\x0F",b"\x44\xD9\x9D\x16",b"\x45\x10\xFA\x4D",b"\x45\x41\x2C\x4D",b"\x45\x80\xB1\xED",b"\x45\xAB\x7A\x3A",b"\x45\xE4\x7B\x6D",
    b"\x46\x18\x37\xF0",b"\x46\x4A\xD2\x26",b"\x46\x87\x1F\x62",b"\x46\xB4\x0A\xAF",b"\x46\xEF\xE4\xBA",b"\x47\x1F\xD2\x28",b"\x47\x54\xF3\x5B",b"\x47\x8D\xDF\x04",
    b"\x47\xBD\x08\xA4",b"\x47\xFB\xDF\xED",b"\x48\x27\xCD\x94",b"\x48\x5F\x96\x13",b"\x48\x94\xF4\xF0",b"\x48\xC6\x79\x91",b"\x49\x04\x3A\x29",b"\x49\x30\x2F\x0E",
    b"\x49\x6A\xC0\xC7",b"\x49\x9C\x65\x73",b"\x49\xD0\x63\x34",b"\x4A\x0A\xD4\xC6",b"\x4A\x38\xFB\xAF",b"\x4A\x76\x7A\x41",b"\x4A\xA4\x35\x16",b"\x4A\xDA\xCB\x94",
    b"\x4B\x11\xC3\xD3",b"\x4B\x42\x38\xD2",b"\x4B\x81\x64\xD2",b"\x4B\xAC\x68\x97",b"\x4B\xE5\xB9\x07",b"\x4C\x19\x0B\x88",b"\x4C\x4B\xEC\x15",b"\x00\x00\x00\x00",
]]
scale_conversion_table = np.array([byteFloat(v) for v in scale_conversion_table_hex[0]] + [byteFloat(v) for v in scale_conversion_table_hex[1]])
# v2.0
intensity_ratio_table_hex = [
    b"\x40\x00\x00\x00",b"\x3F\xED\xB6\xDB",b"\x3F\xDB\x6D\xB7",b"\x3F\xC9\x24\x92",b"\x3F\xB6\xDB\x6E",b"\x3F\xA4\x92\x49",b"\x3F\x92\x49\x25",b"\x3F\x80\x00\x00",
    b"\x3F\x5B\x6D\xB7",b"\x3F\x36\xDB\x6E",b"\x3F\x12\x49\x25",b"\x3E\xDB\x6D\xB7",b"\x3E\x92\x49\x25",b"\x3E\x12\x49\x25",b"\x00\x00\x00\x00",b"\x00\x00\x00\x00",
    b"\x00\x00\x00\x00",b"\x32\xA0\xB0\x51",b"\x32\xD6\x1B\x5E",b"\x33\x0E\xA4\x3A",b"\x33\x3E\x0F\x68",b"\x33\x7D\x3E\x0C",b"\x33\xA8\xB6\xD5",b"\x33\xE0\xCC\xDF",
    b"\x34\x15\xC3\xFF",b"\x34\x47\x8D\x75",b"\x34\x84\xF1\xF6",b"\x34\xB1\x23\xF6",b"\x34\xEC\x07\x19",b"\x35\x1D\x3E\xDA",b"\x35\x51\x84\xDF",b"\x35\x8B\x95\xC2",
    b"\x35\xB9\xFC\xD2",b"\x35\xF7\xD0\xDF",b"\x36\x25\x19\x58",b"\x36\x5B\xFB\xB8",b"\x36\x92\x8E\x72",b"\x36\xC3\x46\xCD",b"\x37\x02\x18\xAF",b"\x37\x2D\x58\x3F",
    b"\x37\x66\xF8\x5B",b"\x37\x99\xE0\x46",b"\x37\xCD\x07\x8C",b"\x38\x08\x98\x0F",b"\x38\x36\x00\x94",b"\x38\x72\x81\x77",b"\x38\xA1\x8F\xAF",b"\x38\xD7\x44\xFD",
    b"\x39\x0F\x6A\x81",b"\x39\x3F\x17\x9A",b"\x39\x7E\x9E\x11",b"\x39\xA9\xA1\x5B",b"\x39\xE2\x05\x5B",b"\x3A\x16\x94\x2D",b"\x3A\x48\xA2\xD8",b"\x3A\x85\xAA\xC3",
    b"\x3A\xB2\x1A\x32",b"\x3A\xED\x4F\x30",b"\x3B\x1E\x19\x6E",b"\x3B\x52\xA8\x1E",b"\x3B\x8C\x57\xCA",b"\x3B\xBA\xFF\x5B",b"\x3B\xF9\x29\x5A",b"\x3C\x25\xFE\xD7",
    # Necessary?
    b"\x3C\x5D\x2D\x82",b"\x3C\x93\x5A\x2B",b"\x3C\xC4\x56\x3F",b"\x3D\x02\xCD\x87",b"\x3D\x2E\x49\x34",b"\x3D\x68\x39\x6A",b"\x3D\x9A\xB6\x2B",b"\x3D\xCE\x24\x8C",
    b"\x3E\x09\x55\xEE",b"\x3E\x36\xFD\x92",b"\x3E\x73\xD2\x90",b"\x3E\xA2\x70\x43",b"\x3E\xD8\x70\x39",b"\x3F\x10\x31\xDC",b"\x3F\x40\x21\x3B",b"\x00\x00\x00\x00",
]
"""
v1.3
listInt4 = [
    b"\x40\x00\x00\x00",b"\x3F\xED\xB6\xDB",b"\x3F\xDB\x6D\xB7",b"\x3F\xC9\x24\x92",b"\x3F\xB6\xDB\x6E",b"\x3F\xA4\x92\x49",b"\x3F\x92\x49\x25",b"\x3F\x80\x00\x00",
    b"\x3F\x5B\x6D\xB7",b"\x3F\x36\xDB\x6E",b"\x3F\x12\x49\x25",b"\x3E\xDB\x6D\xB7",b"\x3E\x92\x49\x25",b"\x3E\x12\x49\x25",b"\x00\x00\x00\x00",b"\x00\x00\x00\x00",
]
"""
intensity_ratio_table = [byteFloat(v) for v in intensity_ratio_table_hex]
# cos(((2j+1) / 2^(i+3)) % (pi / 4))?
sin_table = [
    [
        b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",
        b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",
        b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",
        b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",
        b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",
        b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",
        b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",
        b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",b"\x3D\xA7\x3D\x75",
    ],[
        b"\x3F\x7B\x14\xBE",b"\x3F\x54\xDB\x31",b"\x3F\x7B\x14\xBE",b"\x3F\x54\xDB\x31",b"\x3F\x7B\x14\xBE",b"\x3F\x54\xDB\x31",b"\x3F\x7B\x14\xBE",b"\x3F\x54\xDB\x31",
        b"\x3F\x7B\x14\xBE",b"\x3F\x54\xDB\x31",b"\x3F\x7B\x14\xBE",b"\x3F\x54\xDB\x31",b"\x3F\x7B\x14\xBE",b"\x3F\x54\xDB\x31",b"\x3F\x7B\x14\xBE",b"\x3F\x54\xDB\x31",
        b"\x3F\x7B\x14\xBE",b"\x3F\x54\xDB\x31",b"\x3F\x7B\x14\xBE",b"\x3F\x54\xDB\x31",b"\x3F\x7B\x14\xBE",b"\x3F\x54\xDB\x31",b"\x3F\x7B\x14\xBE",b"\x3F\x54\xDB\x31",
        b"\x3F\x7B\x14\xBE",b"\x3F\x54\xDB\x31",b"\x3F\x7B\x14\xBE",b"\x3F\x54\xDB\x31",b"\x3F\x7B\x14\xBE",b"\x3F\x54\xDB\x31",b"\x3F\x7B\x14\xBE",b"\x3F\x54\xDB\x31",
        b"\x3F\x7B\x14\xBE",b"\x3F\x54\xDB\x31",b"\x3F\x7B\x14\xBE",b"\x3F\x54\xDB\x31",b"\x3F\x7B\x14\xBE",b"\x3F\x54\xDB\x31",b"\x3F\x7B\x14\xBE",b"\x3F\x54\xDB\x31",
        b"\x3F\x7B\x14\xBE",b"\x3F\x54\xDB\x31",b"\x3F\x7B\x14\xBE",b"\x3F\x54\xDB\x31",b"\x3F\x7B\x14\xBE",b"\x3F\x54\xDB\x31",b"\x3F\x7B\x14\xBE",b"\x3F\x54\xDB\x31",
        b"\x3F\x7B\x14\xBE",b"\x3F\x54\xDB\x31",b"\x3F\x7B\x14\xBE",b"\x3F\x54\xDB\x31",b"\x3F\x7B\x14\xBE",b"\x3F\x54\xDB\x31",b"\x3F\x7B\x14\xBE",b"\x3F\x54\xDB\x31",
        b"\x3F\x7B\x14\xBE",b"\x3F\x54\xDB\x31",b"\x3F\x7B\x14\xBE",b"\x3F\x54\xDB\x31",b"\x3F\x7B\x14\xBE",b"\x3F\x54\xDB\x31",b"\x3F\x7B\x14\xBE",b"\x3F\x54\xDB\x31",
    ],[
        b"\x3F\x7E\xC4\x6D",b"\x3F\x74\xFA\x0B",b"\x3F\x61\xC5\x98",b"\x3F\x45\xE4\x03",b"\x3F\x7E\xC4\x6D",b"\x3F\x74\xFA\x0B",b"\x3F\x61\xC5\x98",b"\x3F\x45\xE4\x03",
        b"\x3F\x7E\xC4\x6D",b"\x3F\x74\xFA\x0B",b"\x3F\x61\xC5\x98",b"\x3F\x45\xE4\x03",b"\x3F\x7E\xC4\x6D",b"\x3F\x74\xFA\x0B",b"\x3F\x61\xC5\x98",b"\x3F\x45\xE4\x03",
        b"\x3F\x7E\xC4\x6D",b"\x3F\x74\xFA\x0B",b"\x3F\x61\xC5\x98",b"\x3F\x45\xE4\x03",b"\x3F\x7E\xC4\x6D",b"\x3F\x74\xFA\x0B",b"\x3F\x61\xC5\x98",b"\x3F\x45\xE4\x03",
        b"\x3F\x7E\xC4\x6D",b"\x3F\x74\xFA\x0B",b"\x3F\x61\xC5\x98",b"\x3F\x45\xE4\x03",b"\x3F\x7E\xC4\x6D",b"\x3F\x74\xFA\x0B",b"\x3F\x61\xC5\x98",b"\x3F\x45\xE4\x03",
        b"\x3F\x7E\xC4\x6D",b"\x3F\x74\xFA\x0B",b"\x3F\x61\xC5\x98",b"\x3F\x45\xE4\x03",b"\x3F\x7E\xC4\x6D",b"\x3F\x74\xFA\x0B",b"\x3F\x61\xC5\x98",b"\x3F\x45\xE4\x03",
        b"\x3F\x7E\xC4\x6D",b"\x3F\x74\xFA\x0B",b"\x3F\x61\xC5\x98",b"\x3F\x45\xE4\x03",b"\x3F\x7E\xC4\x6D",b"\x3F\x74\xFA\x0B",b"\x3F\x61\xC5\x98",b"\x3F\x45\xE4\x03",
        b"\x3F\x7E\xC4\x6D",b"\x3F\x74\xFA\x0B",b"\x3F\x61\xC5\x98",b"\x3F\x45\xE4\x03",b"\x3F\x7E\xC4\x6D",b"\x3F\x74\xFA\x0B",b"\x3F\x61\xC5\x98",b"\x3F\x45\xE4\x03",
        b"\x3F\x7E\xC4\x6D",b"\x3F\x74\xFA\x0B",b"\x3F\x61\xC5\x98",b"\x3F\x45\xE4\x03",b"\x3F\x7E\xC4\x6D",b"\x3F\x74\xFA\x0B",b"\x3F\x61\xC5\x98",b"\x3F\x45\xE4\x03",
    ],[
        b"\x3F\x7F\xB1\x0F",b"\x3F\x7D\x3A\xAC",b"\x3F\x78\x53\xF8",b"\x3F\x71\x09\x08",b"\x3F\x67\x6B\xD8",b"\x3F\x5B\x94\x1A",b"\x3F\x4D\x9F\x02",b"\x3F\x3D\xAE\xF9",
        b"\x3F\x7F\xB1\x0F",b"\x3F\x7D\x3A\xAC",b"\x3F\x78\x53\xF8",b"\x3F\x71\x09\x08",b"\x3F\x67\x6B\xD8",b"\x3F\x5B\x94\x1A",b"\x3F\x4D\x9F\x02",b"\x3F\x3D\xAE\xF9",
        b"\x3F\x7F\xB1\x0F",b"\x3F\x7D\x3A\xAC",b"\x3F\x78\x53\xF8",b"\x3F\x71\x09\x08",b"\x3F\x67\x6B\xD8",b"\x3F\x5B\x94\x1A",b"\x3F\x4D\x9F\x02",b"\x3F\x3D\xAE\xF9",
        b"\x3F\x7F\xB1\x0F",b"\x3F\x7D\x3A\xAC",b"\x3F\x78\x53\xF8",b"\x3F\x71\x09\x08",b"\x3F\x67\x6B\xD8",b"\x3F\x5B\x94\x1A",b"\x3F\x4D\x9F\x02",b"\x3F\x3D\xAE\xF9",
        b"\x3F\x7F\xB1\x0F",b"\x3F\x7D\x3A\xAC",b"\x3F\x78\x53\xF8",b"\x3F\x71\x09\x08",b"\x3F\x67\x6B\xD8",b"\x3F\x5B\x94\x1A",b"\x3F\x4D\x9F\x02",b"\x3F\x3D\xAE\xF9",
        b"\x3F\x7F\xB1\x0F",b"\x3F\x7D\x3A\xAC",b"\x3F\x78\x53\xF8",b"\x3F\x71\x09\x08",b"\x3F\x67\x6B\xD8",b"\x3F\x5B\x94\x1A",b"\x3F\x4D\x9F\x02",b"\x3F\x3D\xAE\xF9",
        b"\x3F\x7F\xB1\x0F",b"\x3F\x7D\x3A\xAC",b"\x3F\x78\x53\xF8",b"\x3F\x71\x09\x08",b"\x3F\x67\x6B\xD8",b"\x3F\x5B\x94\x1A",b"\x3F\x4D\x9F\x02",b"\x3F\x3D\xAE\xF9",
        b"\x3F\x7F\xB1\x0F",b"\x3F\x7D\x3A\xAC",b"\x3F\x78\x53\xF8",b"\x3F\x71\x09\x08",b"\x3F\x67\x6B\xD8",b"\x3F\x5B\x94\x1A",b"\x3F\x4D\x9F\x02",b"\x3F\x3D\xAE\xF9",
    ],[
        b"\x3F\x7F\xEC\x43",b"\x3F\x7F\x4E\x6D",b"\x3F\x7E\x13\x24",b"\x3F\x7C\x3B\x28",b"\x3F\x79\xC7\x9D",b"\x3F\x76\xBA\x07",b"\x3F\x73\x14\x47",b"\x3F\x6E\xD8\x9E",
        b"\x3F\x6A\x09\xA7",b"\x3F\x64\xAA\x59",b"\x3F\x5E\xBE\x05",b"\x3F\x58\x48\x53",b"\x3F\x51\x4D\x3D",b"\x3F\x49\xD1\x12",b"\x3F\x41\xD8\x70",b"\x3F\x39\x68\x42",
        b"\x3F\x7F\xEC\x43",b"\x3F\x7F\x4E\x6D",b"\x3F\x7E\x13\x24",b"\x3F\x7C\x3B\x28",b"\x3F\x79\xC7\x9D",b"\x3F\x76\xBA\x07",b"\x3F\x73\x14\x47",b"\x3F\x6E\xD8\x9E",
        b"\x3F\x6A\x09\xA7",b"\x3F\x64\xAA\x59",b"\x3F\x5E\xBE\x05",b"\x3F\x58\x48\x53",b"\x3F\x51\x4D\x3D",b"\x3F\x49\xD1\x12",b"\x3F\x41\xD8\x70",b"\x3F\x39\x68\x42",
        b"\x3F\x7F\xEC\x43",b"\x3F\x7F\x4E\x6D",b"\x3F\x7E\x13\x24",b"\x3F\x7C\x3B\x28",b"\x3F\x79\xC7\x9D",b"\x3F\x76\xBA\x07",b"\x3F\x73\x14\x47",b"\x3F\x6E\xD8\x9E",
        b"\x3F\x6A\x09\xA7",b"\x3F\x64\xAA\x59",b"\x3F\x5E\xBE\x05",b"\x3F\x58\x48\x53",b"\x3F\x51\x4D\x3D",b"\x3F\x49\xD1\x12",b"\x3F\x41\xD8\x70",b"\x3F\x39\x68\x42",
        b"\x3F\x7F\xEC\x43",b"\x3F\x7F\x4E\x6D",b"\x3F\x7E\x13\x24",b"\x3F\x7C\x3B\x28",b"\x3F\x79\xC7\x9D",b"\x3F\x76\xBA\x07",b"\x3F\x73\x14\x47",b"\x3F\x6E\xD8\x9E",
        b"\x3F\x6A\x09\xA7",b"\x3F\x64\xAA\x59",b"\x3F\x5E\xBE\x05",b"\x3F\x58\x48\x53",b"\x3F\x51\x4D\x3D",b"\x3F\x49\xD1\x12",b"\x3F\x41\xD8\x70",b"\x3F\x39\x68\x42",
    ],[
        b"\x3F\x7F\xFB\x11",b"\x3F\x7F\xD3\x97",b"\x3F\x7F\x84\xAB",b"\x3F\x7F\x0E\x58",b"\x3F\x7E\x70\xB0",b"\x3F\x7D\xAB\xCC",b"\x3F\x7C\xBF\xC9",b"\x3F\x7B\xAC\xCD",
        b"\x3F\x7A\x73\x02",b"\x3F\x79\x12\x98",b"\x3F\x77\x8B\xC5",b"\x3F\x75\xDE\xC6",b"\x3F\x74\x0B\xDD",b"\x3F\x72\x13\x52",b"\x3F\x6F\xF5\x73",b"\x3F\x6D\xB2\x93",
        b"\x3F\x6B\x4B\x0C",b"\x3F\x68\xBF\x3C",b"\x3F\x66\x0F\x88",b"\x3F\x63\x3C\x5A",b"\x3F\x60\x46\x21",b"\x3F\x5D\x2D\x53",b"\x3F\x59\xF2\x6A",b"\x3F\x56\x95\xE5",
        b"\x3F\x53\x18\x49",b"\x3F\x4F\x7A\x1F",b"\x3F\x4B\xBB\xF8",b"\x3F\x47\xDE\x65",b"\x3F\x43\xE2\x00",b"\x3F\x3F\xC7\x67",b"\x3F\x3B\x8F\x3B",b"\x3F\x37\x3A\x23",
        b"\x3F\x7F\xFB\x11",b"\x3F\x7F\xD3\x97",b"\x3F\x7F\x84\xAB",b"\x3F\x7F\x0E\x58",b"\x3F\x7E\x70\xB0",b"\x3F\x7D\xAB\xCC",b"\x3F\x7C\xBF\xC9",b"\x3F\x7B\xAC\xCD",
        b"\x3F\x7A\x73\x02",b"\x3F\x79\x12\x98",b"\x3F\x77\x8B\xC5",b"\x3F\x75\xDE\xC6",b"\x3F\x74\x0B\xDD",b"\x3F\x72\x13\x52",b"\x3F\x6F\xF5\x73",b"\x3F\x6D\xB2\x93",
        b"\x3F\x6B\x4B\x0C",b"\x3F\x68\xBF\x3C",b"\x3F\x66\x0F\x88",b"\x3F\x63\x3C\x5A",b"\x3F\x60\x46\x21",b"\x3F\x5D\x2D\x53",b"\x3F\x59\xF2\x6A",b"\x3F\x56\x95\xE5",
        b"\x3F\x53\x18\x49",b"\x3F\x4F\x7A\x1F",b"\x3F\x4B\xBB\xF8",b"\x3F\x47\xDE\x65",b"\x3F\x43\xE2\x00",b"\x3F\x3F\xC7\x67",b"\x3F\x3B\x8F\x3B",b"\x3F\x37\x3A\x23",
    ],[
        b"\x3F\x7F\xFE\xC4",b"\x3F\x7F\xF4\xE6",b"\x3F\x7F\xE1\x29",b"\x3F\x7F\xC3\x8F",b"\x3F\x7F\x9C\x18",b"\x3F\x7F\x6A\xC7",b"\x3F\x7F\x2F\x9D",b"\x3F\x7E\xEA\x9D",
        b"\x3F\x7E\x9B\xC9",b"\x3F\x7E\x43\x23",b"\x3F\x7D\xE0\xB1",b"\x3F\x7D\x74\x74",b"\x3F\x7C\xFE\x73",b"\x3F\x7C\x7E\xB0",b"\x3F\x7B\xF5\x31",b"\x3F\x7B\x61\xFC",
        b"\x3F\x7A\xC5\x16",b"\x3F\x7A\x1E\x84",b"\x3F\x79\x6E\x4E",b"\x3F\x78\xB4\x7B",b"\x3F\x77\xF1\x10",b"\x3F\x77\x24\x17",b"\x3F\x76\x4D\x97",b"\x3F\x75\x6D\x97",
        b"\x3F\x74\x84\x22",b"\x3F\x73\x91\x3F",b"\x3F\x72\x94\xF8",b"\x3F\x71\x8F\x57",b"\x3F\x70\x80\x66",b"\x3F\x6F\x68\x30",b"\x3F\x6E\x46\xBE",b"\x3F\x6D\x1C\x1D",
        b"\x3F\x6B\xE8\x58",b"\x3F\x6A\xAB\x7B",b"\x3F\x69\x65\x91",b"\x3F\x68\x16\xA8",b"\x3F\x66\xBE\xCC",b"\x3F\x65\x5E\x0B",b"\x3F\x63\xF4\x73",b"\x3F\x62\x82\x10",
        b"\x3F\x61\x06\xF2",b"\x3F\x5F\x83\x27",b"\x3F\x5D\xF6\xBE",b"\x3F\x5C\x61\xC7",b"\x3F\x5A\xC4\x50",b"\x3F\x59\x1E\x6A",b"\x3F\x57\x70\x26",b"\x3F\x55\xB9\x93",
        b"\x3F\x53\xFA\xC3",b"\x3F\x52\x33\xC6",b"\x3F\x50\x64\xAF",b"\x3F\x4E\x8D\x90",b"\x3F\x4C\xAE\x79",b"\x3F\x4A\xC7\x7F",b"\x3F\x48\xD8\xB3",b"\x3F\x46\xE2\x2A",
        b"\x3F\x44\xE3\xF5",b"\x3F\x42\xDE\x29",b"\x3F\x40\xD0\xDA",b"\x3F\x3E\xBC\x1B",b"\x3F\x3C\xA0\x03",b"\x3F\x3A\x7C\xA4",b"\x3F\x38\x52\x16",b"\x3F\x36\x20\x6C",
    ]
]
sin_table = np.array([[byteFloat(y) for y in x] for x in sin_table])
cos_table = [
    [
        b"\xBD\x0A\x8B\xD4",b"\x3D\x0A\x8B\xD4",b"\x3D\x0A\x8B\xD4",b"\xBD\x0A\x8B\xD4",b"\x3D\x0A\x8B\xD4",b"\xBD\x0A\x8B\xD4",b"\xBD\x0A\x8B\xD4",b"\x3D\x0A\x8B\xD4",
        b"\x3D\x0A\x8B\xD4",b"\xBD\x0A\x8B\xD4",b"\xBD\x0A\x8B\xD4",b"\x3D\x0A\x8B\xD4",b"\xBD\x0A\x8B\xD4",b"\x3D\x0A\x8B\xD4",b"\x3D\x0A\x8B\xD4",b"\xBD\x0A\x8B\xD4",
        b"\x3D\x0A\x8B\xD4",b"\xBD\x0A\x8B\xD4",b"\xBD\x0A\x8B\xD4",b"\x3D\x0A\x8B\xD4",b"\xBD\x0A\x8B\xD4",b"\x3D\x0A\x8B\xD4",b"\x3D\x0A\x8B\xD4",b"\xBD\x0A\x8B\xD4",
        b"\xBD\x0A\x8B\xD4",b"\x3D\x0A\x8B\xD4",b"\x3D\x0A\x8B\xD4",b"\xBD\x0A\x8B\xD4",b"\x3D\x0A\x8B\xD4",b"\xBD\x0A\x8B\xD4",b"\xBD\x0A\x8B\xD4",b"\x3D\x0A\x8B\xD4",
        b"\x3D\x0A\x8B\xD4",b"\xBD\x0A\x8B\xD4",b"\xBD\x0A\x8B\xD4",b"\x3D\x0A\x8B\xD4",b"\xBD\x0A\x8B\xD4",b"\x3D\x0A\x8B\xD4",b"\x3D\x0A\x8B\xD4",b"\xBD\x0A\x8B\xD4",
        b"\xBD\x0A\x8B\xD4",b"\x3D\x0A\x8B\xD4",b"\x3D\x0A\x8B\xD4",b"\xBD\x0A\x8B\xD4",b"\x3D\x0A\x8B\xD4",b"\xBD\x0A\x8B\xD4",b"\xBD\x0A\x8B\xD4",b"\x3D\x0A\x8B\xD4",
        b"\xBD\x0A\x8B\xD4",b"\x3D\x0A\x8B\xD4",b"\x3D\x0A\x8B\xD4",b"\xBD\x0A\x8B\xD4",b"\x3D\x0A\x8B\xD4",b"\xBD\x0A\x8B\xD4",b"\xBD\x0A\x8B\xD4",b"\x3D\x0A\x8B\xD4",
        b"\x3D\x0A\x8B\xD4",b"\xBD\x0A\x8B\xD4",b"\xBD\x0A\x8B\xD4",b"\x3D\x0A\x8B\xD4",b"\xBD\x0A\x8B\xD4",b"\x3D\x0A\x8B\xD4",b"\x3D\x0A\x8B\xD4",b"\xBD\x0A\x8B\xD4",
    ],[
        b"\xBE\x47\xC5\xC2",b"\xBF\x0E\x39\xDA",b"\x3E\x47\xC5\xC2",b"\x3F\x0E\x39\xDA",b"\x3E\x47\xC5\xC2",b"\x3F\x0E\x39\xDA",b"\xBE\x47\xC5\xC2",b"\xBF\x0E\x39\xDA",
        b"\x3E\x47\xC5\xC2",b"\x3F\x0E\x39\xDA",b"\xBE\x47\xC5\xC2",b"\xBF\x0E\x39\xDA",b"\xBE\x47\xC5\xC2",b"\xBF\x0E\x39\xDA",b"\x3E\x47\xC5\xC2",b"\x3F\x0E\x39\xDA",
        b"\x3E\x47\xC5\xC2",b"\x3F\x0E\x39\xDA",b"\xBE\x47\xC5\xC2",b"\xBF\x0E\x39\xDA",b"\xBE\x47\xC5\xC2",b"\xBF\x0E\x39\xDA",b"\x3E\x47\xC5\xC2",b"\x3F\x0E\x39\xDA",
        b"\xBE\x47\xC5\xC2",b"\xBF\x0E\x39\xDA",b"\x3E\x47\xC5\xC2",b"\x3F\x0E\x39\xDA",b"\x3E\x47\xC5\xC2",b"\x3F\x0E\x39\xDA",b"\xBE\x47\xC5\xC2",b"\xBF\x0E\x39\xDA",
        b"\x3E\x47\xC5\xC2",b"\x3F\x0E\x39\xDA",b"\xBE\x47\xC5\xC2",b"\xBF\x0E\x39\xDA",b"\xBE\x47\xC5\xC2",b"\xBF\x0E\x39\xDA",b"\x3E\x47\xC5\xC2",b"\x3F\x0E\x39\xDA",
        b"\xBE\x47\xC5\xC2",b"\xBF\x0E\x39\xDA",b"\x3E\x47\xC5\xC2",b"\x3F\x0E\x39\xDA",b"\x3E\x47\xC5\xC2",b"\x3F\x0E\x39\xDA",b"\xBE\x47\xC5\xC2",b"\xBF\x0E\x39\xDA",
        b"\xBE\x47\xC5\xC2",b"\xBF\x0E\x39\xDA",b"\x3E\x47\xC5\xC2",b"\x3F\x0E\x39\xDA",b"\x3E\x47\xC5\xC2",b"\x3F\x0E\x39\xDA",b"\xBE\x47\xC5\xC2",b"\xBF\x0E\x39\xDA",
        b"\x3E\x47\xC5\xC2",b"\x3F\x0E\x39\xDA",b"\xBE\x47\xC5\xC2",b"\xBF\x0E\x39\xDA",b"\xBE\x47\xC5\xC2",b"\xBF\x0E\x39\xDA",b"\x3E\x47\xC5\xC2",b"\x3F\x0E\x39\xDA",
    ],[
        b"\xBD\xC8\xBD\x36",b"\xBE\x94\xA0\x31",b"\xBE\xF1\x5A\xEA",b"\xBF\x22\x67\x99",b"\x3D\xC8\xBD\x36",b"\x3E\x94\xA0\x31",b"\x3E\xF1\x5A\xEA",b"\x3F\x22\x67\x99",
        b"\x3D\xC8\xBD\x36",b"\x3E\x94\xA0\x31",b"\x3E\xF1\x5A\xEA",b"\x3F\x22\x67\x99",b"\xBD\xC8\xBD\x36",b"\xBE\x94\xA0\x31",b"\xBE\xF1\x5A\xEA",b"\xBF\x22\x67\x99",
        b"\x3D\xC8\xBD\x36",b"\x3E\x94\xA0\x31",b"\x3E\xF1\x5A\xEA",b"\x3F\x22\x67\x99",b"\xBD\xC8\xBD\x36",b"\xBE\x94\xA0\x31",b"\xBE\xF1\x5A\xEA",b"\xBF\x22\x67\x99",
        b"\xBD\xC8\xBD\x36",b"\xBE\x94\xA0\x31",b"\xBE\xF1\x5A\xEA",b"\xBF\x22\x67\x99",b"\x3D\xC8\xBD\x36",b"\x3E\x94\xA0\x31",b"\x3E\xF1\x5A\xEA",b"\x3F\x22\x67\x99",
        b"\x3D\xC8\xBD\x36",b"\x3E\x94\xA0\x31",b"\x3E\xF1\x5A\xEA",b"\x3F\x22\x67\x99",b"\xBD\xC8\xBD\x36",b"\xBE\x94\xA0\x31",b"\xBE\xF1\x5A\xEA",b"\xBF\x22\x67\x99",
        b"\xBD\xC8\xBD\x36",b"\xBE\x94\xA0\x31",b"\xBE\xF1\x5A\xEA",b"\xBF\x22\x67\x99",b"\x3D\xC8\xBD\x36",b"\x3E\x94\xA0\x31",b"\x3E\xF1\x5A\xEA",b"\x3F\x22\x67\x99",
        b"\xBD\xC8\xBD\x36",b"\xBE\x94\xA0\x31",b"\xBE\xF1\x5A\xEA",b"\xBF\x22\x67\x99",b"\x3D\xC8\xBD\x36",b"\x3E\x94\xA0\x31",b"\x3E\xF1\x5A\xEA",b"\x3F\x22\x67\x99",
        b"\x3D\xC8\xBD\x36",b"\x3E\x94\xA0\x31",b"\x3E\xF1\x5A\xEA",b"\x3F\x22\x67\x99",b"\xBD\xC8\xBD\x36",b"\xBE\x94\xA0\x31",b"\xBE\xF1\x5A\xEA",b"\xBF\x22\x67\x99",
    ],[
        b"\xBD\x48\xFB\x30",b"\xBE\x16\x40\x83",b"\xBE\x78\xCF\xCC",b"\xBE\xAC\x7C\xD4",b"\xBE\xDA\xE8\x80",b"\xBF\x03\x9C\x3D",b"\xBF\x18\x7F\xC0",b"\xBF\x2B\xEB\x4A",
        b"\x3D\x48\xFB\x30",b"\x3E\x16\x40\x83",b"\x3E\x78\xCF\xCC",b"\x3E\xAC\x7C\xD4",b"\x3E\xDA\xE8\x80",b"\x3F\x03\x9C\x3D",b"\x3F\x18\x7F\xC0",b"\x3F\x2B\xEB\x4A",
        b"\x3D\x48\xFB\x30",b"\x3E\x16\x40\x83",b"\x3E\x78\xCF\xCC",b"\x3E\xAC\x7C\xD4",b"\x3E\xDA\xE8\x80",b"\x3F\x03\x9C\x3D",b"\x3F\x18\x7F\xC0",b"\x3F\x2B\xEB\x4A",
        b"\xBD\x48\xFB\x30",b"\xBE\x16\x40\x83",b"\xBE\x78\xCF\xCC",b"\xBE\xAC\x7C\xD4",b"\xBE\xDA\xE8\x80",b"\xBF\x03\x9C\x3D",b"\xBF\x18\x7F\xC0",b"\xBF\x2B\xEB\x4A",
        b"\x3D\x48\xFB\x30",b"\x3E\x16\x40\x83",b"\x3E\x78\xCF\xCC",b"\x3E\xAC\x7C\xD4",b"\x3E\xDA\xE8\x80",b"\x3F\x03\x9C\x3D",b"\x3F\x18\x7F\xC0",b"\x3F\x2B\xEB\x4A",
        b"\xBD\x48\xFB\x30",b"\xBE\x16\x40\x83",b"\xBE\x78\xCF\xCC",b"\xBE\xAC\x7C\xD4",b"\xBE\xDA\xE8\x80",b"\xBF\x03\x9C\x3D",b"\xBF\x18\x7F\xC0",b"\xBF\x2B\xEB\x4A",
        b"\xBD\x48\xFB\x30",b"\xBE\x16\x40\x83",b"\xBE\x78\xCF\xCC",b"\xBE\xAC\x7C\xD4",b"\xBE\xDA\xE8\x80",b"\xBF\x03\x9C\x3D",b"\xBF\x18\x7F\xC0",b"\xBF\x2B\xEB\x4A",
        b"\x3D\x48\xFB\x30",b"\x3E\x16\x40\x83",b"\x3E\x78\xCF\xCC",b"\x3E\xAC\x7C\xD4",b"\x3E\xDA\xE8\x80",b"\x3F\x03\x9C\x3D",b"\x3F\x18\x7F\xC0",b"\x3F\x2B\xEB\x4A",
    ],[
        b"\xBC\xC9\x0A\xB0",b"\xBD\x96\xA9\x05",b"\xBD\xFA\xB2\x73",b"\xBE\x2F\x10\xA2",b"\xBE\x60\x5C\x13",b"\xBE\x88\x8E\x93",b"\xBE\xA0\x9A\xE5",b"\xBE\xB8\x44\x2A",
        b"\xBE\xCF\x7B\xCA",b"\xBE\xE6\x33\x75",b"\xBE\xFC\x5D\x27",b"\xBF\x08\xF5\x9B",b"\xBF\x13\x68\x2A",b"\xBF\x1D\x7F\xD1",b"\xBF\x27\x36\x56",b"\xBF\x30\x85\xBB",
        b"\x3C\xC9\x0A\xB0",b"\x3D\x96\xA9\x05",b"\x3D\xFA\xB2\x73",b"\x3E\x2F\x10\xA2",b"\x3E\x60\x5C\x13",b"\x3E\x88\x8E\x93",b"\x3E\xA0\x9A\xE5",b"\x3E\xB8\x44\x2A",
        b"\x3E\xCF\x7B\xCA",b"\x3E\xE6\x33\x75",b"\x3E\xFC\x5D\x27",b"\x3F\x08\xF5\x9B",b"\x3F\x13\x68\x2A",b"\x3F\x1D\x7F\xD1",b"\x3F\x27\x36\x56",b"\x3F\x30\x85\xBB",
        b"\x3C\xC9\x0A\xB0",b"\x3D\x96\xA9\x05",b"\x3D\xFA\xB2\x73",b"\x3E\x2F\x10\xA2",b"\x3E\x60\x5C\x13",b"\x3E\x88\x8E\x93",b"\x3E\xA0\x9A\xE5",b"\x3E\xB8\x44\x2A",
        b"\x3E\xCF\x7B\xCA",b"\x3E\xE6\x33\x75",b"\x3E\xFC\x5D\x27",b"\x3F\x08\xF5\x9B",b"\x3F\x13\x68\x2A",b"\x3F\x1D\x7F\xD1",b"\x3F\x27\x36\x56",b"\x3F\x30\x85\xBB",
        b"\xBC\xC9\x0A\xB0",b"\xBD\x96\xA9\x05",b"\xBD\xFA\xB2\x73",b"\xBE\x2F\x10\xA2",b"\xBE\x60\x5C\x13",b"\xBE\x88\x8E\x93",b"\xBE\xA0\x9A\xE5",b"\xBE\xB8\x44\x2A",
        b"\xBE\xCF\x7B\xCA",b"\xBE\xE6\x33\x75",b"\xBE\xFC\x5D\x27",b"\xBF\x08\xF5\x9B",b"\xBF\x13\x68\x2A",b"\xBF\x1D\x7F\xD1",b"\xBF\x27\x36\x56",b"\xBF\x30\x85\xBB",
    ],[
        b"\xBC\x49\x0E\x90",b"\xBD\x16\xC3\x2C",b"\xBD\x7B\x2B\x74",b"\xBD\xAF\xB6\x80",b"\xBD\xE1\xBC\x2E",b"\xBE\x09\xCF\x86",b"\xBE\x22\xAB\xB6",b"\xBE\x3B\x6E\xCF",
        b"\xBE\x54\x15\x01",b"\xBE\x6C\x9A\x7F",b"\xBE\x82\x7D\xC0",b"\xBE\x8E\x9A\x22",b"\xBE\x9A\xA0\x86",b"\xBE\xA6\x8F\x12",b"\xBE\xB2\x63\xEF",b"\xBE\xBE\x1D\x4A",
        b"\xBE\xC9\xB9\x53",b"\xBE\xD5\x36\x41",b"\xBE\xE0\x92\x4F",b"\xBE\xEB\xCB\xBB",b"\xBE\xF6\xE0\xCB",b"\xBF\x00\xE7\xE4",b"\xBF\x06\x4B\x82",b"\xBF\x0B\x9A\x6B",
        b"\xBF\x10\xD3\xCD",b"\xBF\x15\xF6\xD9",b"\xBF\x1B\x02\xC6",b"\xBF\x1F\xF6\xCB",b"\xBF\x24\xD2\x25",b"\xBF\x29\x94\x15",b"\xBF\x2E\x3B\xDE",b"\xBF\x32\xC8\xC9",
        b"\x3C\x49\x0E\x90",b"\x3D\x16\xC3\x2C",b"\x3D\x7B\x2B\x74",b"\x3D\xAF\xB6\x80",b"\x3D\xE1\xBC\x2E",b"\x3E\x09\xCF\x86",b"\x3E\x22\xAB\xB6",b"\x3E\x3B\x6E\xCF",
        b"\x3E\x54\x15\x01",b"\x3E\x6C\x9A\x7F",b"\x3E\x82\x7D\xC0",b"\x3E\x8E\x9A\x22",b"\x3E\x9A\xA0\x86",b"\x3E\xA6\x8F\x12",b"\x3E\xB2\x63\xEF",b"\x3E\xBE\x1D\x4A",
        b"\x3E\xC9\xB9\x53",b"\x3E\xD5\x36\x41",b"\x3E\xE0\x92\x4F",b"\x3E\xEB\xCB\xBB",b"\x3E\xF6\xE0\xCB",b"\x3F\x00\xE7\xE4",b"\x3F\x06\x4B\x82",b"\x3F\x0B\x9A\x6B",
        b"\x3F\x10\xD3\xCD",b"\x3F\x15\xF6\xD9",b"\x3F\x1B\x02\xC6",b"\x3F\x1F\xF6\xCB",b"\x3F\x24\xD2\x25",b"\x3F\x29\x94\x15",b"\x3F\x2E\x3B\xDE",b"\x3F\x32\xC8\xC9",
    ],[
        b"\xBB\xC9\x0F\x88",b"\xBC\x96\xC9\xB6",b"\xBC\xFB\x49\xBA",b"\xBD\x2F\xE0\x07",b"\xBD\x62\x14\x69",b"\xBD\x8A\x20\x0A",b"\xBD\xA3\x30\x8C",b"\xBD\xBC\x3A\xC3",
        b"\xBD\xD5\x3D\xB9",b"\xBD\xEE\x38\x76",b"\xBE\x03\x95\x02",b"\xBE\x10\x08\xB7",b"\xBE\x1C\x76\xDE",b"\xBE\x28\xDE\xFC",b"\xBE\x35\x40\x98",b"\xBE\x41\x9B\x37",
        b"\xBE\x4D\xEE\x60",b"\xBE\x5A\x39\x97",b"\xBE\x66\x7C\x66",b"\xBE\x72\xB6\x51",b"\xBE\x7E\xE6\xE1",b"\xBE\x85\x86\xCE",b"\xBE\x8B\x95\x07",b"\xBE\x91\x9D\xDD",
        b"\xBE\x97\xA1\x17",b"\xBE\x9D\x9E\x78",b"\xBE\xA3\x95\xC5",b"\xBE\xA9\x86\xC4",b"\xBE\xAF\x71\x3A",b"\xBE\xB5\x54\xEC",b"\xBE\xBB\x31\xA0",b"\xBE\xC1\x07\x1E",
        b"\xBE\xC6\xD5\x29",b"\xBE\xCC\x9B\x8B",b"\xBE\xD2\x5A\x09",b"\xBE\xD8\x10\x6B",b"\xBE\xDD\xBE\x79",b"\xBE\xE3\x63\xFA",b"\xBE\xE9\x00\xB7",b"\xBE\xEE\x94\x79",
        b"\xBE\xF4\x1F\x07",b"\xBE\xF9\xA0\x2D",b"\xBE\xFF\x17\xB2",b"\xBF\x02\x42\xB1",b"\xBF\x04\xF4\x84",b"\xBF\x07\xA1\x36",b"\xBF\x0A\x48\xAD",b"\xBF\x0C\xEA\xD0",
        b"\xBF\x0F\x87\x84",b"\xBF\x12\x1E\xB0",b"\xBF\x14\xB0\x39",b"\xBF\x17\x3C\x07",b"\xBF\x19\xC2\x00",b"\xBF\x1C\x42\x0C",b"\xBF\x1E\xBC\x12",b"\xBF\x21\x2F\xF9",
        b"\xBF\x23\x9D\xA9",b"\xBF\x26\x05\x0A",b"\xBF\x28\x66\x05",b"\xBF\x2A\xC0\x82",b"\xBF\x2D\x14\x69",b"\xBF\x2F\x61\xA5",b"\xBF\x31\xA8\x1D",b"\xBF\x33\xE7\xBC",
    ]
]
cos_table = np.array([[byteFloat(y) for y in x] for x in cos_table])
imdct_window = [
    [
        b"\x3A\x35\x04\xF0",b"\x3B\x01\x83\xB8",b"\x3B\x70\xC5\x38",b"\x3B\xBB\x92\x68",b"\x3C\x04\xA8\x09",b"\x3C\x30\x82\x00",b"\x3C\x61\x28\x4C",b"\x3C\x8B\x3F\x17",
        b"\x3C\xA8\x39\x92",b"\x3C\xC7\x7F\xBD",b"\x3C\xE9\x11\x10",b"\x3D\x06\x77\xCD",b"\x3D\x19\x8F\xC4",b"\x3D\x2D\xD3\x5C",b"\x3D\x43\x46\x43",b"\x3D\x59\xEC\xC1",
        b"\x3D\x71\xCB\xA8",b"\x3D\x85\x74\x1E",b"\x3D\x92\xA4\x13",b"\x3D\xA0\x78\xB4",b"\x3D\xAE\xF5\x22",b"\x3D\xBE\x1C\x9E",b"\x3D\xCD\xF2\x7B",b"\x3D\xDE\x7A\x1D",
        b"\x3D\xEF\xB6\xED",b"\x3E\x00\xD6\x2B",b"\x3E\x0A\x2E\xDA",b"\x3E\x13\xE7\x2A",b"\x3E\x1E\x00\xB1",b"\x3E\x28\x7C\xF2",b"\x3E\x33\x5D\x55",b"\x3E\x3E\xA3\x21",
        b"\x3E\x4A\x4F\x75",b"\x3E\x56\x63\x3F",b"\x3E\x62\xDF\x37",b"\x3E\x6F\xC3\xD1",b"\x3E\x7D\x11\x38",b"\x3E\x85\x63\xA2",b"\x3E\x8C\x72\xB7",b"\x3E\x93\xB5\x61",
        b"\x3E\x9B\x2A\xEF",b"\x3E\xA2\xD2\x6F",b"\x3E\xAA\xAA\xAB",b"\x3E\xB2\xB2\x22",b"\x3E\xBA\xE7\x06",b"\x3E\xC3\x47\x37",b"\x3E\xCB\xD0\x3D",b"\x3E\xD4\x7F\x46",
        b"\x3E\xDD\x51\x28",b"\x3E\xE6\x42\x5C",b"\x3E\xEF\x4E\xFF",b"\x3E\xF8\x72\xD7",b"\x3F\x00\xD4\xA9",b"\x3F\x05\x76\xCA",b"\x3F\x0A\x1D\x3B",b"\x3F\x0E\xC5\x48",
        b"\x3F\x13\x6C\x25",b"\x3F\x18\x0E\xF2",b"\x3F\x1C\xAA\xC2",b"\x3F\x21\x3C\xA2",b"\x3F\x25\xC1\xA5",b"\x3F\x2A\x36\xE7",b"\x3F\x2E\x99\x98",b"\x3F\x32\xE7\x05",
    ],[
        b"\xBF\x37\x1C\x9E",b"\xBF\x3B\x37\xFE",b"\xBF\x3F\x36\xF2",b"\xBF\x43\x17\x80",b"\xBF\x46\xD7\xE6",b"\xBF\x4A\x76\xA4",b"\xBF\x4D\xF2\x7C",b"\xBF\x51\x4A\x6F",
        b"\xBF\x54\x7D\xC5",b"\xBF\x57\x8C\x03",b"\xBF\x5A\x74\xEE",b"\xBF\x5D\x38\x87",b"\xBF\x5F\xD7\x07",b"\xBF\x62\x50\xDA",b"\xBF\x64\xA6\x99",b"\xBF\x66\xD9\x08",
        b"\xBF\x68\xE9\x0E",b"\xBF\x6A\xD7\xB1",b"\xBF\x6C\xA6\x11",b"\xBF\x6E\x55\x62",b"\xBF\x6F\xE6\xE7",b"\xBF\x71\x5B\xEF",b"\xBF\x72\xB5\xD1",b"\xBF\x73\xF5\xE6",
        b"\xBF\x75\x1D\x89",b"\xBF\x76\x2E\x13",b"\xBF\x77\x28\xD7",b"\xBF\x78\x0F\x20",b"\xBF\x78\xE2\x34",b"\xBF\x79\xA3\x4C",b"\xBF\x7A\x53\x97",b"\xBF\x7A\xF4\x39",
        b"\xBF\x7B\x86\x48",b"\xBF\x7C\x0A\xCE",b"\xBF\x7C\x82\xC8",b"\xBF\x7C\xEF\x26",b"\xBF\x7D\x50\xCB",b"\xBF\x7D\xA8\x8E",b"\xBF\x7D\xF7\x37",b"\xBF\x7E\x3D\x86",
        b"\xBF\x7E\x7C\x2A",b"\xBF\x7E\xB3\xCC",b"\xBF\x7E\xE5\x07",b"\xBF\x7F\x10\x6C",b"\xBF\x7F\x36\x83",b"\xBF\x7F\x57\xCA",b"\xBF\x7F\x74\xB6",b"\xBF\x7F\x8D\xB6",
        b"\xBF\x7F\xA3\x2E",b"\xBF\x7F\xB5\x7B",b"\xBF\x7F\xC4\xF6",b"\xBF\x7F\xD1\xED",b"\xBF\x7F\xDC\xAD",b"\xBF\x7F\xE5\x79",b"\xBF\x7F\xEC\x90",b"\xBF\x7F\xF2\x2E",
        b"\xBF\x7F\xF6\x88",b"\xBF\x7F\xF9\xD0",b"\xBF\x7F\xFC\x32",b"\xBF\x7F\xFD\xDA",b"\xBF\x7F\xFE\xED",b"\xBF\x7F\xFF\x8F",b"\xBF\x7F\xFF\xDF",b"\xBF\x7F\xFF\xFC",
    ]
]
imdct_window = np.array([[byteFloat(y) for y in x] for x in imdct_window])

def checkSum(f, cnt: int):
    temp = f.peek(cnt)
    sums = 0
    for i in range(cnt):
        sums = ((sums << 8) ^ CRC16Table[(sums >> 8) ^ temp[i]]) & 0xffff
    return sums


class clData:
    def __init__(self, data):
        self.data = data
        self.size = len(data) * 8 - 16
        self.bit = 0
    def checkBit(self, bitSize):
        v = 0
        if self.bit + bitSize <= self.size:
            mask = [ 0xFFFFFF,0x7FFFFF,0x3FFFFF,0x1FFFFF,0x0FFFFF,0x07FFFF,0x03FFFF,0x01FFFF ]
            datatmp = self.data[self.bit >> 3: (self.bit >> 3) + 3]
            datatmp += [0] * (3 - len(datatmp))
            v = (datatmp[0] << 16) | (datatmp[1] << 8) | datatmp[2]
            v &= mask[self.bit & 7]
            v >>= 24 - (self.bit & 7) - bitSize
        return v
    def getBit(self, bitSize):
        v = self.checkBit(bitSize)
        self.bit += bitSize
        return v
    def addBit(self, bitSize):
        self.bit += bitSize


def hca_decode(data, cipher=None, subkey=None, compile=True):
    import platform
    is_windows = platform.system() == 'Windows'
    def check_exists(path):
        try:
            subprocess.check_output(['where' if is_windows else 'which', path], cwd=rcwd) # windows
            return True
        except Exception as e:
            return False
    def fallback():
        return hca_decode_fallback(data, cipher, subkey)
    import os
    rpath = os.path.dirname(__file__) + "/"
    rcwd = rpath
    if rpath == "/":
        rpath = ""
        rcwd = None
    import subprocess
    if compile and os.path.exists(rpath + "hca_src"):
        decoder = ("" if is_windows else "./") + 'HCADecoder'
        # find executable
        if not check_exists(decoder):
            if check_exists("g++"):
                # compile
                try:
                    subprocess.check_output(['g++', '-w', '-o', '../HCADecoder', 'clHCA.cpp', 'HCADecoder.cpp'], cwd=rpath + "hca_src")
                except:
                    pass
        if check_exists(decoder):
            from random import randrange
            nonce1 = randrange(10 ** 24)
            fname1 = rpath + "hca_src/{}.wav".format(nonce1)
            nonce2 = randrange(10 ** 24)
            fname2 = rpath + "hca_src/{}.hca".format(nonce2)
            with open(fname2, "wb") as f:
                f.write(data)
                f.flush()
            try:
                decoderabs = rpath + 'HCADecoder'
                subprocess.check_output([decoderabs, fname2, '-k', "{:016x}".format(cipher), '-s', str(subkey), '-o', fname1], cwd=rcwd)
            except:
                import traceback
                traceback.print_exc()
            os.remove(fname2)
            if os.path.exists(fname1):
                import io
                with open(fname1, "rb") as f:
                    arr = io.BytesIO(f.read())
                arr.seek(0)
                os.remove(fname1)
                return arr
            else:
                return fallback()
        else:
            return fallback()
    else:
        return fallback()

def build_ath_table(_type, sampling_rate):
    if _type == 0:
        return tuple([0] * 0x80)
    else:
        return tuple((0xff if index >= 0x28e else athList[index]) for i in range(0x80) for index in [(sampling_rate * i) >> 13])

def build_cipher_table(_type, cipher=None, subkey=None):
    if _type == 0:
        return tuple(range(256))
    if _type == 1: # encrypted
        v = 0
        _ciphertable = [0]
        for i in range(254):
            v = (v * 13 + 11) & 0xff
            if v in (0, 0xff):
                v = (v * 13 + 11) & 0xff
            _ciphertable.append(v)
        _ciphertable.append(0xff)
        return tuple(_ciphertable)
    if _type == 56:
        if subkey is not None and subkey != 0:
            cipher = (cipher * ((subkey << 16) | (((subkey & 0xFFFF) ^ 0xFFFF) + 2))) & 0xFFFFFFFFFFFFFFFF
        cipher = (cipher - 1) & 0xFFFFFFFFFFFFFFFF
        t1 = []
        for i in range(7):
            t1.append(cipher & 0xff)
            cipher >>= 8
        t2 = [
            t1[1], t1[1] ^ t1[6], t1[2] ^ t1[3],
            t1[2], t1[2] ^ t1[1], t1[3] ^ t1[4],
            t1[3], t1[3] ^ t1[2], t1[4] ^ t1[5],
            t1[4], t1[4] ^ t1[3], t1[5] ^ t1[6],
            t1[5], t1[5] ^ t1[4], t1[6] ^ t1[1],
            t1[6]
        ]
        def createPRNGTable(seed):
            temp = []
            a = ((seed & 1) << 3) | 5
            c = (seed & 0xe) | 1
            seed = seed >> 4
            for _ in range(16):
                seed = (seed * a + c) & 0xf
                temp.append(seed)
            return temp
        t3 = []
        high = createPRNGTable(t1[0])
        for i in range(16):
            low = createPRNGTable(t2[i])
            high_mask = high[i] << 4
            for j in range(16):
                t3.append(high_mask | low[j])
        _ciphertable = [0]
        v = 17
        for i in range(254):
            while t3[v] in (0, 0xff):
                v = (v + 17) & 0xff
            _ciphertable.append(t3[v])
            v = (v + 17) & 0xff
        _ciphertable.append(0xff)
        return tuple(_ciphertable)
    raise ValueError("Invalid Cipher Type")

def hca_parse(data, cipher=None, subkey=None):
    reader = r(data)
    hca_mask = 0x7f7f7f7f # not 0xffffffff as chunks' magic may be obfuscated when encrypted with key
    # HCA
    _header = T("header", ("hca", "version", "dataOffset"))(*reader.readStruct(">IHH"))
    if _header.hca & hca_mask != 0x48434100:
        raise ValueError("Incorrect Header")
    # FMT
    _format = T("format", ("fmt", "channel_count", *c("sampling_rate", 3),
                           "block_count", "mute_header", "mute_footer"))(*reader.readStruct(">IB3BIHH"))
    _format = combineBytes(_format, "sampling_rate", 3)
    if _format.fmt & hca_mask != 0x666D7400:
        raise ValueError("Incorrect Format")
    tmp = int.from_bytes(reader.peek(4), byteorder='big')
    if tmp & hca_mask == 0x636F6D70:
        # COMP
        _comp = T("compress", ("comp", "block_size", "min_resolution", "max_resolution", "trackCount", "channel_config", "total_band_count", "base_band_count", "stereo_band_count", "bands_per_hfr_group", "ms_stereo", "reserved"))(*reader.readStruct(">IH10B"))
    elif tmp & hca_mask == 0x64656300:
        # DEC
        _dec = T("decode", ("dec", "block_size", "min_resolution", "max_resolution", "total_band_count", "base_band_count", "temp", "stereoType"))(*reader.readStruct(">IH6B"))
        _dec.total_band_count += 1
        _dec.base_band_count += 1
        if _dec.stereoType == 0:
            _dec.base_band_count = _dec.total_band_count
        _stereo_band_count = _dec.total_band_count - _dec.base_band_count
        _comp = T("compress", ("comp", "block_size", "min_resolution", "max_resolution", "trackCount", "channel_config", "total_band_count", "base_band_count", "stereo_band_count", "bands_per_hfr_group", "ms_stereo", "reserved"))(_dec.dec, _dec.block_size, _dec.min_resolution, _dec.max_resolution, _dec.temp >> 4, _dec.temp & 0xf, _dec.total_band_count, _dec.base_band_count, _stereo_band_count, 0, 0, 0)
    else:
        raise ValueError("Neither Compress nor Decode")
    if _comp.trackCount == 0:
        _comp = _comp._replace(trackCount=1)
    if _header.version <= 0x200:
        if (_comp.min_resolution, _comp.max_resolution) != (1, 15):
            raise ValueError("Invalid Compress")
    else:
        if _comp.min_resolution > _comp.max_resolution or _comp.max_resolution > 15:
            raise ValueError("Invalid Compress")
    # VBR
    _vbr = T("vbr", ("vbr", "r01", "r02"))
    if int.from_bytes(reader.peek(4), byteorder='big') & hca_mask == 0x76627200:
        _vbr = _vbr(*reader.readStruct(">IHH"))
    else:
        _vbr = _vbr(0, 0, 0)
    # ATH
    _ath = T("ath", ("ath", "type"))
    if int.from_bytes(reader.peek(4), byteorder='big') & hca_mask == 0x61746800:
        _ath = _ath(*reader.readStruct(">IH"))
    else:
        _ath = _ath(0, int(_header.version < 0x200))
    # LOOP
    _loop = T("loop", ("loop", "start", "end", "count", "r01", "flag"))
    if int.from_bytes(reader.peek(4), byteorder='big') & hca_mask == 0x6c6f6f70:
        _loop = _loop(*reader.readStruct(">IIIHH"), True)
    else:
        _loop = _loop(0, 0, 0, 0, 0x400, False)
    # CIPH
    _ciph = T("cipher", ("ciph", "type"))
    if int.from_bytes(reader.peek(4), byteorder='big') & hca_mask == 0x63697068:
        _ciph = _ciph(*reader.readStruct(">IH"))
    else:
        _ciph = _ciph(0, 0)
    # RVA - relative volume adjustment
    _rva = T("rva", ("rva", "volume"))
    if int.from_bytes(reader.peek(4), byteorder='big') & hca_mask == 0x72766100:
        _rva = _rva(*reader.readStruct(">If"))
    else:
        _rva = _rva(0, 1)
    # COMM
    _comm = T("comm", ("comm", "len", "comment"))
    if int.from_bytes(reader.peek(4), byteorder='big') & hca_mask == 0x636f6d6d:
        _comm = _comm(*reader.readStruct(">IB"), reader.readNullString())
    else:
        _comm = _comm(0, 1, None)
    if _ciph.type not in (0, 1, 56):
        raise ValueError("Invalid Cipher Type")

    # all extra information that stays unchanged during extraction
    _ciphertable = build_cipher_table(_ciph.type, cipher, subkey)
    _athtable = build_ath_table(_ath.type, _format.sampling_rate)
    ceil2 = lambda a, b: (a // b + bool(a % b)) if b > 0 else 0
    _hfr_group_count = ceil2(_comp.total_band_count - (_comp.base_band_count + _comp.stereo_band_count), _comp.bands_per_hfr_group)

    # 0: discrete, 1: primary, 2: secondary
    channels_per_track = _format.channel_count // _comp.trackCount
    channel_type = [0] * 0x10
    if _comp.stereo_band_count and channels_per_track > 1:
        cursor = 0
        for i in range(_comp.trackCount):
            if channels_per_track in [2, 3]:
                channel_type[cursor: cursor+2] = [1, 2]
            elif channels_per_track == 4:
                channel_type[cursor: cursor+2] = [1, 2]
                if _comp.channel_config == 0:
                    channel_type[cursor+2: cursor+4] = [1, 2]
            elif channels_per_track == 5:
                channel_type[cursor: cursor+2] = [1, 2]
                if _comp.channel_config <= 2:
                    channel_type[cursor+3: cursor+5] = [1, 2]
            elif channels_per_track in [6, 7]:
                channel_type[cursor: cursor+2] = [1, 2]
                channel_type[cursor+4: cursor+6] = [1, 2]
            elif channels_per_track == 8:
                channel_type[cursor: cursor+2] = [1, 2]
                channel_type[cursor+4: cursor+8] = [1, 2, 1, 2]
            cursor += channels_per_track
    start_band = _comp.base_band_count + _comp.stereo_band_count
    coded_count = [_comp.base_band_count + (_comp.stereo_band_count if channel_type[i] != 2 else 0) for i in range(_format.channel_count)]

    return T("HCAFile", ("header", "format", "comp", "vbr", "ath", "loop", "ciph", "rva", "comm", "ciphertable", "athtable", "hfr_group_count", "channels_per_track", "start_band", "coded_count", "channel_type", "random"))(_header, _format, _comp, _vbr, _ath, _loop, _ciph, _rva, _comm, _ciphertable, _athtable, _hfr_group_count, channels_per_track, start_band, coded_count, channel_type, {"state": 1})

def hca_decode_fallback(data, cipher, subkey):
    # file should implement "write", "flush", and "seek"
    hca_file = hca_parse(data, cipher, subkey)
    # initialize all variables to be used
    _channels = {
        "scale_factors": [[0] * 0x80 for _ in range(hca_file.format.channel_count)],
        "intensity": [[0] * 0x08 for _ in range(hca_file.format.channel_count)],
        "resolution": [[0] * 0x80 for _ in range(hca_file.format.channel_count)],
        "noise": [[0] * 0x80 for _ in range(hca_file.format.channel_count)],
        "noise_count": [0 for _ in range(hca_file.format.channel_count)],
        "valid_count": [0 for _ in range(hca_file.format.channel_count)],
        "gain": np.zeros((hca_file.format.channel_count, 0x80)),
        "spectra": np.zeros((hca_file.format.channel_count, 0x80)),
        "wav3": np.zeros((hca_file.format.channel_count, 0x80)),
        "wave": np.zeros((hca_file.format.channel_count, 8, 0x80)),
    }
    import wave, io
    file = io.BytesIO()
    wavfile = wave.open(file, "wb")
    wavfile.setparams(({
        "nchannels": hca_file.format.channel_count,
        "sampwidth": 2, # 16 bit
        "framerate": hca_file.format.sampling_rate,
        # each block contains 1024 (8 * 0x80) samples for each channel
        "nframes": hca_file.format.block_count << 10,
        "comptype": 'NONE',
        "compname": 'not compressed',
    }).values())

    f = r(data)
    for l in range(hca_file.format.block_count):
        address = hca_file.header.dataOffset + hca_file.comp.block_size * l
        f.seek(address)
        if checkSum(f, hca_file.comp.block_size):
            raise ValueError("Checksum not = 0")
        dec_reader = clData([hca_file.ciphertable[i] for i in f.read(hca_file.comp.block_size)])
        magic = dec_reader.getBit(16)
        if magic == 0xffff:
            acc_noise_level = dec_reader.getBit(9)
            eval_bound = dec_reader.getBit(7)
            packed_noise_level = (acc_noise_level << 8) - eval_bound
            for i in range(hca_file.format.channel_count):
                _channels["noise_count"][i], _channels["valid_count"][i] = decode1(dec_reader, hca_file.hfr_group_count, packed_noise_level, hca_file.athtable, hca_file.channel_type[i], _channels["gain"][i], hca_file.coded_count[i], _channels["resolution"][i], _channels["scale_factors"][i], _channels["intensity"][i], _channels["noise"][i], hca_file.header.version, hca_file.comp.max_resolution, hca_file.comp.min_resolution)
            for i in range(8):
                for j in range(hca_file.format.channel_count):
                    decode2(dec_reader, _channels["spectra"][j], _channels["gain"][j], hca_file.coded_count[j], _channels["resolution"][j]) # expensive
                for j in range(hca_file.format.channel_count):
                    decode3a(_channels["spectra"][j], hca_file.channel_type[j], _channels["scale_factors"][j], hca_file.comp.min_resolution, _channels["noise_count"][j], _channels["valid_count"][j], _channels["noise"][j], hca_file.comp.ms_stereo, hca_file.random)
                    decode3b(hca_file.hfr_group_count, hca_file.comp.bands_per_hfr_group, hca_file.start_band, hca_file.comp.total_band_count, _channels["spectra"][j], hca_file.channel_type[j], _channels["scale_factors"][j], hca_file.header.version)
                for j in range(hca_file.format.channel_count - 1):
                    decode4(_channels["intensity"][j + 1][i], hca_file.comp.total_band_count, hca_file.comp.base_band_count, hca_file.comp.stereo_band_count, _channels["spectra"][j], _channels["spectra"][j + 1], hca_file.channel_type[j], hca_file.comp.ms_stereo)
                decode5(i, _channels["spectra"], _channels["wav3"], _channels["wave"]) # expensive
        wav = _channels["wave"].reshape((hca_file.format.channel_count, -1)).T.ravel()
        wavfile.writeframes((wav.clip(-1, 1) * 0x7FFF).astype("<i2").tobytes())
    wavfile.close()
    file.seek(0)
    return file

def bit16(inp):
    inp = inp & 0xffff
    return bytes([inp & 0xff, inp >> 8])

def decode1(data, hfr_group_count, packed_noise_level, athTable, channeltype, gain, coded_count, resolution, scale_factors, intensity, noise, version, max_res, min_res):
    # unpack scalefactors
    delta_bits = data.getBit(3)
    c_count = coded_count
    # extra_count added in v300
    if channeltype == 2 or hfr_group_count <= 0 or version <= 0x200:
        extra_count = 0
    else:
        extra_count = hfr_group_count
        c_count += extra_count
        assert c_count <= 128
    if delta_bits >= 6:
        for i in range(c_count):
            scale_factors[i] = data.getBit(6)
    elif delta_bits:
        value = data.getBit(6)
        expected_delta = (1 << delta_bits) - 1
        half_expected_delta = expected_delta >> 1
        scale_factors[0] = value
        for i in range(1, c_count):
            delta = data.getBit(delta_bits)
            if delta != expected_delta:
                value += delta - half_expected_delta
                value &= 0x3f # added in v300
            else:
                value = data.getBit(6)
            scale_factors[i] = value
    else:
        for i in range(0x80):
            scale_factors[i] = 0
    # extra_count added in v300
    for i in range(extra_count):
        scale_factors[0x7f - i] = scale_factors[c_count - i]
    # unpack intensity
    if channeltype == 2:
        if version <= 0x200:
            value = data.checkBit(4)
            intensity[0] = value
            if value < 15:
                for i in range(8):
                    intensity[i] = data.getBit(4)
        else:
            value = data.getBit(4)
            if value < 15:
                delta_bits = data.getBit(2)
                intensity[0] = value
                if delta_bits == 3:
                    for i in range(1, 8):
                        intensity[i] = data.getBit(4)
                else:
                    bmax = (2 << delta_bits) - 1
                    bits = delta_bits + 1
                    for i in range(1, 8):
                        delta = data.getBit(bits)
                        if delta == bmax:
                            value = data.getBit(4)
                        else:
                            value += delta - (bmax >> 1)
                            assert value <= 0x0f
                        intensity[i] = value
            else:
                for i in range(8):
                    intensity[i] = 7
    else:
        if version <= 0x200:
            for i in range(hfr_group_count):
                # scale_factors[_value3 + i] = data.getBit(6) # v200
                scale_factors[0x80 - hfr_group_count + i] = data.getBit(6) # v300 lib
    # calculate resolution
    # restore coded_count
    c_count = coded_count
    noise_count = 0
    valid_count = 0
    for i in range(c_count):
        scalefactor = scale_factors[i]
        if scalefactor:
            noise_level = athTable[i] + ((packed_noise_level + i) >> 8)
            curve_position = noise_level + 1 - ((scalefactor * 5) >> 1)
            if curve_position < 0:
                new_resolution = 15
            elif curve_position > 0x41: # > 0x39 => 1 for v200
                new_resolution = 0
            else:
                new_resolution = scalelist[curve_position]
            # added in v300 (min_res = 1 before so)
            if new_resolution > max_res:
                new_resolution = max_res
            elif new_resolution < min_res:
                new_resolution = min_res
            if new_resolution < 1:
                noise[noise_count] = i
                noise_count += 1
            else:
                noise[0x7f - valid_count] = i
                valid_count += 1
            resolution[i] = new_resolution
        else:
            resolution[i] = 0
    for i in range(c_count, 0x80):
        resolution[i] = 0
    # calculate_gain
    gain[:c_count] = valueFloat[scale_factors[:c_count]] * scaleFloat[resolution[:c_count]]
    return noise_count, valid_count


def decode2(data, spectra, gain, coded_count, resolution):
    # dequantize_coefficients
    spectra[:] = 0
    for i in range(coded_count):
        res = resolution[i]
        bitSize = max_bit_table[res]
        code = data.getBit(bitSize)
        if res <= 7:
            code += res << 4
            data.addBit(read_bit_table[code] - bitSize)
            qc = read_val_table[code]
        else:
            qc = code = (-1 if code & 1 else 1) * (code >> 1)
            if not code:
                data.addBit(-1)
        spectra[i] = gain[i] * qc

def decode3a(spectra, channeltype, scale_factors, min_res, noise_count, valid_count, noise, ms_stereo, random):
    # reconstruct_noise
    if min_res > 0:
        return
    if valid_count <= 0 or noise_count <= 0:
        return
    if ms_stereo and channeltype != 1:
        return
    for i in range(noise_count):
        random_temp = (0x343FD * random["state"] + 0x269EC3) & 0x7fffffff
        random["state"] = random_temp
        random_index = 0x80 - valid_count + (((random_temp & 0x7fff) * valid_count) >> 15)
        noise_index = noise[i]
        valid_index = noise[random_index]
        sc_index = 0x3e + scale_factors[noise_index] - scale_factors[valid_index]
        sc_index &= ~(sc_index >> 31)
        sc_index += 1
        spectra[noise_index] = scale_conversion_table[sc_index] * spectra[valid_index]

def decode3b(hfr_group_count, bands_per_hfr_group, start_band, total_band_count, spectra, channeltype, scale_factors, version):
    # reconstruct_high_frequency
    if bands_per_hfr_group == 0:
        return
    if channeltype == 2:
        return
    highband = start_band
    lowband = start_band - 1
    # offset = start_band # v200
    offset = 128 - hfr_group_count # v300 lib
    if version <= 0x200:
        group_limit = hfr_group_count
    else:
        group_limit = hfr_group_count + (hfr_group_count < 0)
        group_limit >>= 1
    for group in range(hfr_group_count):
        lowband_sub = int(group < group_limit)
        for i in range(bands_per_hfr_group):
            if highband >= total_band_count or lowband < 0:
                break
            sc_index = 0x3F + scale_factors[offset + group] - scale_factors[lowband]
            sc_index &= ~(sc_index >> 31) # v300 lib
            sc_index += 1
            spectra[highband] = scale_conversion_table[sc_index] * spectra[lowband]
            highband += 1
            lowband -= lowband_sub
    spectra[-1] = 0


def decode4(intensity, total_band_count, base_band_count, stereo_band_count, spectra, nextspectra, channeltype, ms_stereo):
    # apply_intensity_stereo
    if channeltype == 1: # and stereo_band_count:
        ratio_l = intensity_ratio_table[intensity]
        nextspectra[base_band_count:total_band_count] = spectra[base_band_count:total_band_count] * (2 - ratio_l) # (ratio_l - 2)
        spectra[base_band_count:total_band_count] *= ratio_l
    # apply_ms_stereo
    if channeltype == 1 and ms_stereo:
        ratio = byteFloat(bytes.fromhex("3F3504F3")) # 1 / sqrt(2)
        coef_l = (spectra[base_band_count:total_band_count] + nextspectra[base_band_count:total_band_count]) * ratio
        coef_r = (spectra[base_band_count:total_band_count] - nextspectra[base_band_count:total_band_count]) * ratio
        spectra[base_band_count:total_band_count] = coef_l
        nextspectra[base_band_count:total_band_count] = coef_r

def decode5(index, spectra, wav3, wave):
    # imdct_transform (DCT-IV)
    count1 = 1
    count2 = 0x40
    a = spectra
    for i in range(7):
        a = a.reshape((-1, count2, 2))
        tmp0, tmp1 = a[:, :, 0], a[:, :, 1]
        a[:, :, 0], a[:, :, 1] = tmp0 + tmp1, tmp0 - tmp1
        a = a.transpose((0, 2, 1))
        count1 <<= 1
        count2 >>= 1
    count1 = 0x40
    count2 = 1
    for i in range(7):
        a = a.reshape((-1, count1, 2, count2))
        tmp0, tmp1 = a[:,:,0], a[:,:,1]
        c, d = sin_table[i].reshape((-1, count2)), cos_table[i].reshape((-1, count2))
        a[:,:,0], a[:,:,1] = tmp0 * c - tmp1 * d, (tmp0 * d + tmp1 * c)[:,:,::-1]
        count1 >>= 1
        count2 <<= 1
    a = a.reshape((-1, 0x80))
    wave[:,index,:0x40] = a[:,0x40:] * imdct_window[0] + wav3[:,:0x40]
    wave[:,index, 0x40:] = a[:,:0x3f:-1] * imdct_window[1] - wav3[:,0x40:]
    wav3[:,:0x40] = a[:,0x3f::-1] * imdct_window[1][::-1]
    wav3[:,0x40:] = a[:,:0x40] * imdct_window[0][::-1]

if __name__ == '__main__':
    import os, time
    if __name__ == '__main__':
        # absolute import
        from acb_wrapper import parse_bytes
    else:
        # relative import
        from .acb_wrapper import parse_bytes
    acbname = "test" # test.acb
    with open("{}.acb".format(acbname), "rb") as f:
        acbfile = f.read()
    acbcontent = parse_bytes(acbfile)
    os.makedirs(acbname, exist_ok=True)
    starttime = time.time()
    for file in acbcontent:
        filename = "{}.{}".format(file.track.name, file.extension)
        content = file.binary.read()
        with open("{}/{}".format(acbname, filename), "wb") as f:
            f.write(content)
        if file.extension == "hca":
            wav = hca_decode(content, 0x89abcdef, 0x01234567, False)
            with open("{}/{}.wav".format(acbname, file.track.name), "wb") as f:
                f.write(wav.read())
    print("Time elapsed: {:.3f}s".format(time.time() - starttime))

