from acb import *
def parse_binary(acb_file: open):
    utf = UTFTable(acb_file)
    cue = TrackList(utf)
    embedded_awb = io.BytesIO(utf.rows[0]["AwbFile"])
    data_source = AFSArchive(embedded_awb)
    
    return [
        T("parsed_acb", ("track", "binary", "extension"))(
            track=track,
            binary=io.BytesIO(data_source.file_data_for_cue_id(track.wav_id)),
            extension=wave_type_ftable.get(track.enc_type, track.enc_type)[1:]
        )
        for track in cue.tracks
    ]

def parse_bytes(acb_bytes: bytes):
    return parse_binary(io.BytesIO(acb_bytes))
