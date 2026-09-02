from typing import *

def parse_binary(acb_file: open, awb_file: Optional[open] = None):
    import io
    from .acb import ACBFile, wave_type_ftable
    from collections import namedtuple as T
    with ACBFile(acb_file, extern_awb=awb_file) as acb:
        return [
            T("parsed_acb", ("track", "binary", "extension", "subkey"))(
                track=track,
                binary=io.BytesIO(acb.get_track_data(track)),
                extension=wave_type_ftable.get(track.enc_type, "")[1:],
                subkey = None if acb.embedded_awb is None else acb.embedded_awb.mix_key
            )
            for track in acb.track_list.tracks
        ]

def parse_bytes(acb_bytes: bytes, awb_bytes: Optional[bytes] = None):
    import io
    return parse_binary(io.BytesIO(acb_bytes), io.BytesIO(awb_bytes) if awb_bytes is not None else None)