from acb import *
def parse_binary(acb_file: open, awb_file: open=None):
    with ACBFile(acb_file, extern_awb=awb_file) as acb:
        return [
            T("parsed_acb", ("track", "binary", "extension"))(
                track=track,
                binary=io.BytesIO(acb.get_track_data(track)),
                extension=wave_type_ftable.get(track.enc_type, track.enc_type)[1:]
            )
            for track in acb.track_list.tracks
        ]

def parse_bytes(acb_bytes: bytes, awb_bytes: bytes=None):
    return parse_binary(io.BytesIO(acb_bytes), io.BytesIO(awb_bytes) if awb_bytes is not None else None)