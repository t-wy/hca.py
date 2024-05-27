# https://github.com/summertriangle-dev/acb.py/blob/master/acb/acb.py
# Commit: 9fb4bb098b03804d8bab78c6803b262d76028819

import struct
import functools
import itertools
import os
import io
import re
from collections import namedtuple as T
from typing import Optional, Union, BinaryIO, Tuple, List, Callable

COLUMN_STORAGE_MASK = 0xF0
COLUMN_STORAGE_PERROW = 0x50
COLUMN_STORAGE_CONSTANT = 0x30
COLUMN_STORAGE_CONSTANT2 = 0x70
COLUMN_STORAGE_ZERO = 0x10

COLUMN_TYPE_MASK = 0x0F
COLUMN_TYPE_DATA = 0x0B
COLUMN_TYPE_STRING = 0x0A
COLUMN_TYPE_FLOAT = 0x08
COLUMN_TYPE_8BYTE = 0x06
COLUMN_TYPE_4BYTE2 = 0x05
COLUMN_TYPE_4BYTE = 0x04
COLUMN_TYPE_2BYTE2 = 0x03
COLUMN_TYPE_2BYTE = 0x02
COLUMN_TYPE_1BYTE2 = 0x01
COLUMN_TYPE_1BYTE = 0x00

WAVEFORM_ENCODE_TYPE_ADX = 0
WAVEFORM_ENCODE_TYPE_HCA = 2
WAVEFORM_ENCODE_TYPE_VAG = 7
WAVEFORM_ENCODE_TYPE_ATRAC3 = 8
WAVEFORM_ENCODE_TYPE_BCWAV = 9
WAVEFORM_ENCODE_TYPE_NINTENDO_DSP = 13


# string and data fields require more information
def promise_data(r):
    offset = r.uint32_t()
    size = r.uint32_t()
    return lambda h: r.bytes(size, at=h.data_offset + 8 + offset)


def promise_string(r):
    offset = r.uint32_t()
    return lambda h: r.string0(at=h.string_table_offset + 8 + offset)


column_data_dtable = {
    COLUMN_TYPE_DATA: promise_data,
    COLUMN_TYPE_STRING: promise_string,
    COLUMN_TYPE_FLOAT: lambda r: r.float32_t(),
    COLUMN_TYPE_8BYTE: lambda r: r.uint64_t(),
    COLUMN_TYPE_4BYTE2: lambda r: r.int32_t(),
    COLUMN_TYPE_4BYTE: lambda r: r.uint32_t(),
    COLUMN_TYPE_2BYTE2: lambda r: r.int16_t(),
    COLUMN_TYPE_2BYTE: lambda r: r.uint16_t(),
    COLUMN_TYPE_1BYTE2: lambda r: r.int8_t(),
    COLUMN_TYPE_1BYTE: lambda r: r.uint8_t()}

column_data_stable = {
    COLUMN_TYPE_DATA: "8s",
    COLUMN_TYPE_STRING: "4s",
    COLUMN_TYPE_FLOAT: "f",
    COLUMN_TYPE_8BYTE: "Q",
    COLUMN_TYPE_4BYTE2: "i",
    COLUMN_TYPE_4BYTE: "I",
    COLUMN_TYPE_2BYTE2: "h",
    COLUMN_TYPE_2BYTE: "H",
    COLUMN_TYPE_1BYTE2: "b",
    COLUMN_TYPE_1BYTE: "B"}

wave_type_ftable = {
    WAVEFORM_ENCODE_TYPE_ADX: ".adx",
    WAVEFORM_ENCODE_TYPE_HCA: ".hca",
    WAVEFORM_ENCODE_TYPE_VAG: ".vag",
    WAVEFORM_ENCODE_TYPE_ATRAC3: ".at3",
    WAVEFORM_ENCODE_TYPE_BCWAV: ".bcwav",
    WAVEFORM_ENCODE_TYPE_NINTENDO_DSP: ".dsp"}

BYTE_ZERO = 0
def JOIN_BYTE_ARRAY(sr):
    return bytes(sr)

def readfunc(fmt):
    a = struct.Struct(fmt)
    b = a.size
    def f(f, at=None):
        if at is not None:
            back = f.tell()
            f.seek(at)
            d = a.unpack(f.read(b))[0]
            f.seek(back)
            return d
        else:
            return a.unpack(f.read(b))[0]

    return f

def latebinder(f):
    return lambda s: f(s.f)

class R(object):
    """ file reader based on types """
    def __init__(self, file, *, encoding="utf-8"):
        self.f = file
        self.encoding = encoding

    int8_t = latebinder(readfunc(">b"))
    uint8_t = latebinder(readfunc(">B"))
    int16_t = latebinder(readfunc(">h"))
    uint16_t = latebinder(readfunc(">H"))
    int32_t = latebinder(readfunc(">i"))
    uint32_t = latebinder(readfunc(">I"))
    int64_t = latebinder(readfunc(">q"))
    uint64_t = latebinder(readfunc(">Q"))
    float32_t = latebinder(readfunc(">f"))

    le_int8_t = latebinder(readfunc("<b"))
    le_uint8_t = latebinder(readfunc("<B"))
    le_int16_t = latebinder(readfunc("<h"))
    le_uint16_t = latebinder(readfunc("<H"))
    le_int32_t = latebinder(readfunc("<i"))
    le_uint32_t = latebinder(readfunc("<I"))
    le_int64_t = latebinder(readfunc("<q"))
    le_uint64_t = latebinder(readfunc("<Q"))
    le_float32_t = latebinder(readfunc("<f"))

    def tell(self):
        return self.f.tell()

    def seek(self, at, where=os.SEEK_SET):
        self.f.seek(at, where)

    def struct(self, struct, at=None):
        if at is not None:
            back = self.f.tell()
            self.f.seek(at)
            d = self.struct(struct)
            self.f.seek(back)
            return d

        return struct.unpack(self.f.read(struct.size))

    def bytes(self, size, at=None):
        if at is not None:
            back = self.f.tell()
            self.f.seek(at)
            d = self.bytes(size)
            self.f.seek(back)
            return d

        return self.f.read(size)

    def bytesinto(self, inbuf, at=None):
        if at is not None:
            back = self.f.tell()
            self.f.seek(at)
            self.bytesinto(inbuf)
            self.f.seek(back)
            return

        self.f.readinto(inbuf)

    def string0(self, at=None):
        if at is not None:
            back = self.f.tell()
            self.f.seek(at)
            d = self.string0()
            self.f.seek(back)
            return d

        bk = self.f.tell()
        tl = 0
        sr = []
        while 1:
            b = self.f.read(16)
            tl += len(b)

            if len(b) == 0:
                raise Exception("EOF")

            for c in b:
                if c != BYTE_ZERO:
                    sr.append(c)
                else:
                    break
            else:
                continue
            break
        string = JOIN_BYTE_ARRAY(sr)
        self.f.seek(bk + len(string) + 1)
        return string.decode(self.encoding)

class Struct(struct.Struct):
    """ struct with an output filter (usually a namedtuple) """
    def __init__(self, fmt, out_type):
        struct.Struct.__init__(self, fmt)
        self.out_type = out_type

    def unpack(self, buf):
        return self.out_type(* struct.Struct.unpack(self, buf))

utf_header_t = Struct(">IHHIIIHHI",
    T("utf_header_t", ("table_size", "u1", "row_offset", "string_table_offset",
    "data_offset", "table_name_offset", "number_of_fields", "row_size", "number_of_rows")))

class UTFTable(object):
    def __init__(self, file, *, encoding="sjis"):
        buf = R(file, encoding=encoding)
        magic = buf.uint32_t()
        if magic != 0x40555446:
            raise ValueError("bad magic")

        self.header = buf.struct(utf_header_t)
        self.name = buf.string0(at=self.header.string_table_offset + 8 + self.header.table_name_offset)
        self.encoding = encoding

        buf.seek(0x20)
        self.read_schema(buf)

        buf.seek(self.header.row_offset + 8)
        self.rows = list(self.iter_rows(buf))

    def read_schema(self, buf):
        buf.seek(0x20)

        dynamic_keys = []
        format = ">"
        constants = {}

        for _ in range(self.header.number_of_fields):
            field_type = buf.uint8_t()
            name_offset = buf.uint32_t()

            occurrence = field_type & COLUMN_STORAGE_MASK
            type_key = field_type & COLUMN_TYPE_MASK

            if occurrence in (COLUMN_STORAGE_CONSTANT, COLUMN_STORAGE_CONSTANT2):
                name = buf.string0(at=self.header.string_table_offset + 8 + name_offset)
                val = column_data_dtable[type_key](buf)
                constants[name] = val
            else:
                dynamic_keys.append(buf.string0(at=self.header.string_table_offset + 8 + name_offset))
                format += column_data_stable[type_key]

        for k in constants.keys():
            if callable(constants[k]):
                constants[k] = constants[k](self.header)

        self.dynamic_keys = dynamic_keys
        self.struct_format = format
        self.constants = constants

    def resolve(self, buf, *args):
        ret = []
        for val in args:
            if isinstance(val, bytes):
                if len(val) == 8:
                    offset, size = struct.unpack(">II", val)
                    ret.append(buf.bytes(size, at=self.header.data_offset + 8 + offset))
                else:
                    offset = struct.unpack(">I", val)[0]
                    ret.append(buf.string0(at=self.header.string_table_offset + 8 + offset))
            else:
                ret.append(val)
        return tuple(ret)

    def iter_rows(self, buf):
        sfmt = Struct(self.struct_format, functools.partial(self.resolve, buf))
        for n in range(self.header.number_of_rows):
            values = buf.struct(sfmt)
            ret = {k: v for k, v in zip(self.dynamic_keys, values)}
            ret.update(self.constants)
            yield ret

    def __repr__(self):
        return "<UTFTable '{1}' with {0} rows >".format(len(self.rows), self.name)

track_t = T("track_t", ("cue_id", "name", "memory_wav_id", "external_wav_id", "enc_type", "is_stream"))

class TrackList(object):
    def __init__(self, utf):
        cue_handle = io.BytesIO(utf.rows[0]["CueTable"])
        nam_handle = io.BytesIO(utf.rows[0]["CueNameTable"])
        wav_handle = io.BytesIO(utf.rows[0]["WaveformTable"])
        syn_handle = io.BytesIO(utf.rows[0]["SynthTable"])

        cues = UTFTable(cue_handle, encoding=utf.encoding)
        nams = UTFTable(nam_handle, encoding=utf.encoding)
        wavs = UTFTable(wav_handle, encoding=utf.encoding)
        syns = UTFTable(syn_handle, encoding=utf.encoding)

        self.tracks: List[track_t] = []

        name_map = {}
        for row in nams.rows:
            name_map[row["CueIndex"]] = row["CueName"]

        for ind, row in enumerate(cues.rows):
            if row["ReferenceType"] not in {3, 8}:
                raise RuntimeError("ReferenceType {0} not implemented.".format(row["ReferenceType"]))

            r_data = syns.rows[row["ReferenceIndex"]]["ReferenceItems"]
            a, b = struct.unpack(">HH", r_data)

            wav_id = wavs.rows[b].get("Id")
            if wav_id is None:
                wav_id = wavs.rows[b]["MemoryAwbId"]
            extern_wav_id = wavs.rows[b]["StreamAwbId"]
            enc = wavs.rows[b]["EncodeType"]
            is_stream = wavs.rows[b]["Streaming"]

            self.tracks.append(track_t(row["CueId"], name_map.get(ind, "UNKNOWN"), wav_id,
                extern_wav_id, enc, is_stream))

def align(n):
    def _align(number):
        return (number + n - 1) & ~(n - 1)
    return _align


afs2_file_ent_t = T("afs2_file_ent_t", ("cue_id", "offset", "size"))


class AFSArchive(object):
    def __init__(self, file: BinaryIO, *, encoding: Optional[str] = None):
        # Note: we don't do anything involving strings here so encoding is not actually required
        buf = R(file, encoding=encoding or "utf-8")

        magic = buf.uint32_t()
        if magic != 0x41465332:
            raise ValueError("bad magic")

        version = buf.bytes(4)
        file_count = buf.le_uint32_t()

        if version[0] >= 0x02:
            self.alignment: int = buf.le_uint16_t()
            self.mix_key: Optional[int] = buf.le_uint16_t()
        else:
            self.alignment: int = buf.le_uint32_t()
            self.mix_key: Optional[int] = None

        #print("afs2:", file_count, "files in ar")
        #print("afs2: aligned to", self.alignment, "bytes")

        self.offset_size: int = version[1]
        self.offset_mask: int = int("FF" * self.offset_size, 16)
        cue_id_size = version[2]
        #print("afs2: a file offset is", self.offset_size, "bytes")

        self.files: List[afs2_file_ent_t] = []
        self.create_file_entries(buf, file_count, cue_id_size, self.offset_size, self.offset_mask)
        self.src = buf

    def _struct_format(self, size):
        if size == 2:
            return "H"
        elif size == 4:
            return "I"

    def create_file_entries(self, buf, file_count, cue_id_size, offset_size, offset_mask):
        buf.seek(0x10)
        read_cue_ids = struct.Struct("<" + (self._struct_format(cue_id_size) * file_count))
        read_raw_offs = struct.Struct("<" + (self._struct_format(offset_size) * (file_count + 1)))

        # read all in one go
        cue_ids = buf.struct(read_cue_ids)
        raw_offs = buf.struct(read_raw_offs)
        # apply the mask
        unaligned_offs = tuple(map(lambda x: x & offset_mask, raw_offs))
        aligned_offs = tuple(map(align(self.alignment), unaligned_offs))
        offsets_for_length_calculating = unaligned_offs[1:]
        lengths = itertools.starmap(
            lambda my_offset, next_offset: next_offset - my_offset,
            zip(aligned_offs, offsets_for_length_calculating))

        self.files = list(itertools.starmap(afs2_file_ent_t, zip(cue_ids, aligned_offs, lengths)))

    def file_data_for_cue_id(self, cue_id, rw=False):
        for f in self.files:
            if f.cue_id == cue_id:
                if rw:
                    buf = bytearray(f.size)
                    self.src.bytesinto(buf, at=f.offset)
                    return buf
                else:
                    return self.src.bytes(f.size, at=f.offset)
        else:
            raise ValueError("id {0} not found in archive".format(cue_id))

AnyFile = Union[str, os.PathLike, BinaryIO]
Uninitialized = object()

def _get_file_obj(name: AnyFile) -> Tuple[BinaryIO, bool]:
    if isinstance(name, (str, os.PathLike)):
        return open(name, "rb"), True
    else:
        return name, False

class ACBFile(object):
    def __init__(self, acb_file: AnyFile, extern_awb: Optional[AnyFile] = None, encoding: Optional[str] = None):
        self.acb_handle, self.acb_handle_owned = _get_file_obj(acb_file)

        if extern_awb is None:
            self.awb_handle = None
            self.awb_handle_owned = False
        else:
            self.awb_handle, self.awb_handle_owned = _get_file_obj(extern_awb)

        self.encoding = encoding or "sjis"
        try:
            utf = UTFTable(self.acb_handle, encoding=encoding or "sjis")
            self.track_list = TrackList(utf)
        except UnicodeDecodeError:
            if encoding is None:
                self.encoding = "utf-8"
                utf = UTFTable(self.acb_handle, encoding="utf-8")
                self.track_list = TrackList(utf)
            else:
                raise

        if len(utf.rows[0]["AwbFile"]) > 0:
            self.embedded_awb = AFSArchive(io.BytesIO(utf.rows[0]["AwbFile"]), encoding=self.encoding)
        else:
            self.embedded_awb = None # type: ignore

        if self.awb_handle:
            self.external_awb = AFSArchive(self.awb_handle, encoding=self.encoding)
        else:
            self.external_awb = None # type: ignore

        self.closed = False

    def get_track_data(self, track: track_t) -> bytearray:
        """ Gets encoded audio data as a bytearray.
            Arguments:
            - track: The track to get data for, from .track_list.
        """
        if self.closed:
            raise ValueError("ACBFile is closed")

        if track.is_stream:
            if not self.external_awb:
                raise ValueError("Track {0} is streamed, but there's no external AWB attached.".format(track))

            buf = self.external_awb.file_data_for_cue_id(track.external_wav_id, rw=True)
        else:
            if not self.embedded_awb:
                raise ValueError("Track {0} is internal, but this ACB file has no internal AWB.".format(track))

            buf = self.embedded_awb.file_data_for_cue_id(track.memory_wav_id, rw=True)
        return buf

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        """ Close any open files held by ACBFile. If you passed file objects
            instead of paths when creating the ACBFile instance, they will
            not be closed.
            Can be called multiple times; subsequent calls will have no effect.
        """
        if self.acb_handle_owned:
            self.acb_handle.close()
            self.acb_handle_owned = False
        if self.awb_handle_owned and self.awb_handle:
            self.awb_handle.close()
            self.awb_handle_owned = False
        self.closed = True

    def __del__(self):
        self.close()


def find_awb(path):
    if path.endswith(".acb"):
        awb_path = path[:-4] + ".awb"
        if os.path.exists(awb_path):
            return awb_path

def name_gen_default(track):
    return "{0}{1}".format(track.name, wave_type_ftable.get(track.enc_type, track.enc_type))

def extract_acb(
    acb_file: AnyFile,
    target_dir: str,
    extern_awb: Optional[AnyFile] = None,
    name_gen: Callable[[track_t], str] = name_gen_default,
    encoding: Optional[str] = None
):
    if isinstance(acb_file, str) and extern_awb is None:
        extern_awb = find_awb(acb_file)

    with ACBFile(acb_file, extern_awb=extern_awb, encoding=encoding) as acb:
        for track in acb.track_list.tracks:
            name = name_gen(track)

            with open(os.path.join(target_dir, name), "wb") as out_file:
                out_file.write(acb.get_track_data(track))