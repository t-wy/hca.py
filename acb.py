# https://github.com/summertriangle-dev/acb.py/blob/master/acb/acb.py
# Commit: 9fb4bb098b03804d8bab78c6803b262d76028819

import struct
import functools
import itertools
import os
import io
from collections import namedtuple as T
from typing import Optional, Union, BinaryIO, Tuple, List, Callable

COLUMN_STORAGE_MASK = 0xF0

COLUMN_STORAGE_ZERO = 0x10
COLUMN_STORAGE_CONSTANT = 0x30
COLUMN_STORAGE_PERROW = 0x50
COLUMN_STORAGE_CONSTANT2 = 0x70

WAVEFORM_ENCODE_TYPE_ADX = 0
WAVEFORM_ENCODE_TYPE_HCA = 2
WAVEFORM_ENCODE_TYPE_HCA_ALT = 6
WAVEFORM_ENCODE_TYPE_VAG = 7
WAVEFORM_ENCODE_TYPE_ATRAC3 = 8
WAVEFORM_ENCODE_TYPE_BCWAV = 9
WAVEFORM_ENCODE_TYPE_ATRAC9 = 11
WAVEFORM_ENCODE_TYPE_NINTENDO_DSP = 13

COLUMN_TYPE_MASK = 0x0F

COLUMN_TYPE_UCHAR = 0x00
COLUMN_TYPE_SCHAR = 0x01
COLUMN_TYPE_USHORT = 0x02
COLUMN_TYPE_SSHORT = 0x03
COLUMN_TYPE_UINT = 0x04
COLUMN_TYPE_SINT = 0x05
COLUMN_TYPE_ULONG = 0x06
COLUMN_TYPE_SLONG = 0x07
COLUMN_TYPE_FLOAT = 0x08
COLUMN_TYPE_DOUBLE = 0x09
COLUMN_TYPE_STRING = 0x0A
COLUMN_TYPE_DATA = 0x0B

column_data_stable = {
    COLUMN_TYPE_UCHAR: "B",
    COLUMN_TYPE_SCHAR: "b",
    COLUMN_TYPE_USHORT: "H",
    COLUMN_TYPE_SSHORT: "h",
    COLUMN_TYPE_UINT: "I",
    COLUMN_TYPE_SINT: "i",
    COLUMN_TYPE_ULONG: "Q",
    COLUMN_TYPE_SLONG: "q",
    COLUMN_TYPE_FLOAT: "f",
    COLUMN_TYPE_DOUBLE: "d",
    COLUMN_TYPE_STRING: "4s",
    COLUMN_TYPE_DATA: "8s",
}

wave_type_ftable = {
    WAVEFORM_ENCODE_TYPE_ADX: ".adx",
    WAVEFORM_ENCODE_TYPE_HCA: ".hca",
    WAVEFORM_ENCODE_TYPE_HCA_ALT: ".hca",
    WAVEFORM_ENCODE_TYPE_VAG: ".vag",
    WAVEFORM_ENCODE_TYPE_ATRAC3: ".at3",
    WAVEFORM_ENCODE_TYPE_ATRAC9: ".at9",
    WAVEFORM_ENCODE_TYPE_BCWAV: ".bcwav",
    WAVEFORM_ENCODE_TYPE_NINTENDO_DSP: ".dsp"
}

REFERENCE_EMPTY = 0
REFERENCE_WAVEFORM = 1
REFERENCE_SYNTH = 2
REFERENCE_SEQUENCE = 3
REFERENCE_BLOCK_SEQUENCE = 8

BYTE_ZERO = 0

EVENT_END = 0
EVENT_NOTE_ON = 2000 # SYNTH = 2, SEQUENCE = 3
EVENT_DELAY_MS = 2001 # milliseconds (unsigned int)
EVENT_SET_SYNTH_OR_WAVEFORM = 2002
EVENT_NOTE_ON_WITH_NO = 2003
EVENT_NOTE_ON_WITH_DURATION = 2004
EVENT_DELAY_US = 2005 # microseconds (signed short)

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
    float64_t = latebinder(readfunc(">d"))

    le_int8_t = latebinder(readfunc("<b"))
    le_uint8_t = latebinder(readfunc("<B"))
    le_int16_t = latebinder(readfunc("<h"))
    le_uint16_t = latebinder(readfunc("<H"))
    le_int32_t = latebinder(readfunc("<i"))
    le_uint32_t = latebinder(readfunc("<I"))
    le_int64_t = latebinder(readfunc("<q"))
    le_uint64_t = latebinder(readfunc("<Q"))
    le_float32_t = latebinder(readfunc("<f"))
    le_float64_t = latebinder(readfunc("<d"))

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

        back = self.f.tell()
        parts = []
        while True:
            b = self.f.read(16)
            if len(b) == 0:
                raise Exception("EOF")
            null_pos = b.find(b"\x00")
            if null_pos != -1:
                parts.append(b[:null_pos])
                break
            parts.append(b)
        string = b"".join(parts)
        self.f.seek(back + len(string) + 1)
        return string.decode(self.encoding)

class Struct(struct.Struct):
    """ struct with an output filter (usually a namedtuple) """
    def __init__(self, fmt, out_type):
        struct.Struct.__init__(self, fmt)
        self.out_type = out_type

    def unpack(self, buf):
        return self.out_type(* struct.Struct.unpack(self, buf))

utf_header_t = Struct(">IHHIIIHHI",
    T("utf_header_t", (
        "table_size", "version", "row_offset", "string_offset",
        "data_offset", "name_offset", "field_count", "row_size", "row_count"
    ))
)

class UTFTable(object):
    def __init__(self, file, *, encoding="cp932"):
        buf = R(file, encoding=encoding)
        magic = buf.uint32_t()
        if magic != 0x40555446: # @UTF
            raise ValueError("bad magic")

        self.header = buf.struct(utf_header_t)
        self.name = buf.string0(
            at = (
                self.header.string_offset + 8 +
                self.header.name_offset
            )
        )
        self.encoding = encoding

        buf.seek(0x20)
        self.read_schema(buf)

        buf.seek(self.header.row_offset + 8)
        self.rows = list(self.iter_rows(buf))

    def read_schema(self, buf):
        buf.seek(0x20)
        body_offset = 8

        dynamic_keys = []
        format = ">"
        constants = {}

        for _ in range(self.header.field_count):
            field_type = buf.uint8_t()
            name_offset = buf.uint32_t()

            storage_type = field_type & COLUMN_STORAGE_MASK
            type_key = field_type & COLUMN_TYPE_MASK

            if type_key not in column_data_stable:
                raise Exception("Unknown column type: " + hex(type_key))

            name = buf.string0(
                at = self.header.string_offset + body_offset + name_offset
            )
            field_format = column_data_stable[type_key]
            constant = None
            if storage_type in (
                COLUMN_STORAGE_CONSTANT, COLUMN_STORAGE_CONSTANT2
            ):
                constant = buf.struct(
                    self._build_struct(buf, ">" + field_format)
                )[0]
            elif storage_type == COLUMN_STORAGE_ZERO:
                constant = (
                    "" if type_key == COLUMN_TYPE_STRING else
                    b"" if type_key == COLUMN_TYPE_DATA else
                    0.0 if type_key in (COLUMN_TYPE_FLOAT, COLUMN_TYPE_DOUBLE) else
                    0
                )
            else:
                dynamic_keys.append(name)
                format += field_format
                continue
            constants[name] = constant

        self.dynamic_keys = dynamic_keys
        self.struct_format = format
        self.constants = constants
    
    def _build_struct(self, buf, format):
        return Struct(format, functools.partial(self.resolve, buf))
    
    def _resolve(self, buf, val):
        body_offset = 8
        if isinstance(val, bytes):
            if len(val) == 8: # COLUMN_TYPE_DATA
                offset, size = struct.unpack(">II", val)
                return buf.bytes(
                    size, at=self.header.data_offset + body_offset + offset
                )
            else: # COLUMN_TYPE_STRING
                offset = struct.unpack(">I", val)[0]
                return buf.string0(
                    at=self.header.string_offset + body_offset + offset
                )
        return val

    def resolve(self, buf, *args):
        return tuple(
            self._resolve(buf, val)
            for val in args
        )

    def iter_rows(self, buf):
        sfmt = self._build_struct(buf, self.struct_format)
        for n in range(self.header.row_count):
            ret = {
                k: v for k, v in
                zip(self.dynamic_keys, buf.struct(sfmt))
            }
            ret.update(self.constants)
            yield ret

    def __repr__(self):
        return "<UTFTable '{1}' with {0} rows >".format(len(self.rows), self.name)

track_t = T("track_t", ("cue_id", "name", "enc_type", "is_stream"))

class TrackList(object):
    def __init__(self, utf: UTFTable):
        self.utf = utf
        cues = self.get_table("CueTable")
        nams = self.get_table("CueNameTable")
        self.wavs = self.get_table("WaveformTable")
        self.syns = self.get_table("SynthTable")
        self.seqs = self.get_table("SequenceTable")
        self.blk_seqs = self.get_table("BlockSequenceTable")
        self.blks = self.get_table("BlockTable")
        self.trks = self.get_table("TrackTable")
        self.evts = self.get_table("TrackEventTable")
        if len(self.evts) == 0:
            self.evts = self.get_table("CommandTable")

        self.tracks: List[track_t] = []

        name_map = {}
        for row in nams:
            name_map[row["CueIndex"]] = row["CueName"]

        for cue_index, row in enumerate(cues):
            cue_name = name_map.get(
                cue_index,
                "UNKNOWN_{}".format(row.get("CueId", cue_index))
            )
            ref_type = row["ReferenceType"]
            ref_index = row["ReferenceIndex"]
            wav_indices = self.resolve_reference(ref_type, ref_index, set())
            num_related = row.get("NumRelatedWaveforms")
            if num_related is not None and num_related != len(wav_indices):
                print(
                    "Expected {} waveforms, resolved {}".format(
                        num_related, len(wav_indices)
                    )
                )
            if len(wav_indices) == 1:
                for wav_index in wav_indices:
                    self.append_track(cue_name, wav_index)
            else:
                for i, wav_index in enumerate(wav_indices):
                    suffix = "_{:>02}".format(i + 1)
                    self.append_track(cue_name + suffix, wav_index)

    
    def get_table(self, table_name: str):
        table = self.utf.rows[0].get(table_name)
        if table is None or len(table) == 0:
            return []
        return UTFTable(
            io.BytesIO(table),
            encoding=self.utf.encoding
        ).rows
    
    def resolve_reference(self, ref_type, ref_index, visited):
        key = (ref_type, ref_index)
        if key in visited:
            return []
        visited.add(key)
        if ref_type == REFERENCE_EMPTY:
            return []
        if ref_type == REFERENCE_WAVEFORM:
            if ref_index >= len(self.wavs):
                print("Invalid Waveform Index {}".format(ref_index))
                return []
            return [ref_index]
        if ref_type == REFERENCE_SYNTH:
            if ref_index >= len(self.syns):
                print("Invalid Synth Index {}".format(ref_index))
                return []
            ref_items = self.short_list(self.syns[ref_index].get("ReferenceItems"))
            return [
                entry
                for a, b in zip(
                    ref_items[::2],
                    ref_items[1:2]
                )
                for entry in self.resolve_reference(a, b, visited)
            ]
        if ref_type == REFERENCE_SEQUENCE:
            if ref_index >= len(self.seqs):
                print("Invalid Sequence Index {}".format(ref_index))
                return []
            return self.resolve_sequence(
                self.short_list(
                    self.seqs[ref_index].get("TrackIndex")
                ),
                visited
            )
        if ref_type == REFERENCE_BLOCK_SEQUENCE:
            if ref_index >= len(self.blk_seqs):
                print("Invalid Block Sequence Index {}".format(ref_index))
                return []
            blk_seq = self.blk_seqs[ref_index]
            return self.resolve_sequence(
                self.short_list(
                    blk_seq.get("TrackIndex")
                ),
                visited
            ) + [
                track_index
                for block_index in self.short_list(
                    blk_seq.get("BlockIndex")
                )
                if block_index < len(self.blks)
                for track_index in self.resolve_sequence(
                    self.short_list(
                        self.blks[block_index].get("TrackIndex")
                    ),
                    visited
                )
            ]
        print("Unimplemented Reference Type {}".format(ref_type))
        return []
    
    def resolve_sequence(self, track_indices: Tuple[int, ...], visited):
        result = []
        for track_index in track_indices:
            if track_index >= len(self.trks):
                print("Invalid track Index {}".format(track_index))
                continue
            track = self.trks[track_index]
            event_index = track.get("EventIndex", track.get("CommandIndex"))
            if (
                event_index is None or
                event_index == 0xffff or # -1
                event_index >= len(self.evts)
            ):
                continue
            event = self.evts[event_index]
            commands = event.get("Command")
            if commands is None:
                continue
            cursor = 0
            while cursor + 3 <= len(commands):
                data = commands[cursor : cursor + 3]
                if len(data) < 3:
                    break
                code = (data[0] << 8) | data[1]
                size = data[2]
                cursor += 3
                payload = commands[cursor : cursor + size]
                cursor += size
                if code in (
                    EVENT_NOTE_ON,
                    EVENT_NOTE_ON_WITH_NO
                ) and len(payload) >= 4:
                    result.extend(self.resolve_reference(
                        (payload[0] << 8) | payload[1],
                        (payload[2] << 8) | payload[3],
                        visited
                    ))
                if code == EVENT_END:
                    break
        return result

    def short_list(self, data: Optional[bytes]) -> Tuple[int, ...]:
        if not data:
            return []
        size = len(data) >> 1
        return struct.unpack(
            ">" + "H" * size,
            data[:size << 1]
        )
    
    def append_track(self, cue_name, wav_index):
        wav = self.wavs[wav_index]
        memory_awb_id = wav.get("Id")
        if memory_awb_id is None:
            memory_awb_id = wav["MemoryAwbId"]
        stream_awb_id = wav["StreamAwbId"]
        enc = wav["EncodeType"]
        is_stream = wav["Streaming"]
        awb_id = stream_awb_id if is_stream else memory_awb_id

        self.tracks.append(track_t(
            awb_id, cue_name, enc, is_stream
        ))


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
        if size == 1:
            return "B"
        elif size == 2:
            return "H"
        elif size == 4:
            return "I"
        raise ValueError(f"unsupported AFS2 width: {size}")

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
            zip(aligned_offs, offsets_for_length_calculating)
        )

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

        self.encoding = encoding or "cp932"
        current_pos = self.acb_handle.tell()
        try:
            utf = UTFTable(self.acb_handle, encoding=encoding or "cp932")
            self.track_list = TrackList(utf)
        except UnicodeDecodeError:
            if encoding is None:
                self.encoding = "utf-8"
                self.acb_handle.seek(current_pos)
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

            buf = self.external_awb.file_data_for_cue_id(
                track.cue_id, rw=True
            )
        else:
            if not self.embedded_awb:
                raise ValueError("Track {0} is internal, but this ACB file has no internal AWB.".format(track))

            buf = self.embedded_awb.file_data_for_cue_id(
                track.cue_id, rw=True
            )
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
    if path.lower().endswith(".acb"):
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