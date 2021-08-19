from merge_mediainfo import merge_mediainfo
import pytest
from merge_exif import merge_exif_to_base_log
from helper import load_json, read_key_list
from merge_siegfried import merge_sf_logs


@pytest.fixture()
def test_ora_log():
    ora_logs = "tests/dummy_logs/ora.json"
    return ora_logs


@pytest.fixture()
def test_sf_log():
    sf_log = "tests/dummy_logs/sf.log"
    return sf_log


@pytest.fixture()
def test_exif_log():
    sf_log = "tests/dummy_logs/multiple_exif_dir.log"
    return sf_log


@pytest.fixture()
def test_mediainfo_mult_f():
    mediainfo_log = "tests/dummy_logs/mediainfo_multiple_f.log"
    return mediainfo_log


@pytest.fixture()
def test_file():
    path_to_ora_file = "tests/dummy_logs/dpms-ora-truncated.json"
    return path_to_ora_file


@pytest.fixture()
def dict_with_none_value():
    example_dict = {"ns": "pronom", "id": "UNKNOWN", "format": "",
                    "version": "", "mime": "", "basis": "",
                    "warning": "no match"}
    return example_dict


@pytest.fixture()
def test_key_list_file():
    key_list_file = "tests/dummy_logs/key_list.log"
    return key_list_file


@pytest.fixture()
def test_exif_dict():
    example_log = {
        "media": {
            "@ref": "file_example_MP4_1920_18MG.mp4",
            "track": [{
                "@type": "General",
                "Count": "331",
                "StreamCount": "1",
                "StreamKind": "General",
                "StreamKind_String": "General",
                "StreamKindID": "0",
                "VideoCount": "1",
                "AudioCount": "1",
                "Video_Format_List": "AVC",
                "Video_Format_WithHint_List": "AVC",
                "Video_Codec_List": "AVC",
                "Audio_Format_List": "AAC LC",
                "Audio_Format_WithHint_List": "AAC LC",
                "Audio_Codec_List": "AAC LC",
                "CompleteName": "file_example_MP4_1920_18MG.mp4",
                "FileNameExtension": "file_example_MP4_1920_18MG.mp4",
                "FileName": "file_example_MP4_1920_18MG",
                "FileExtension": "mp4",
                "Format": "MPEG-4",
                "Format_String": "MPEG-4",
                "Format_Extensions": "braw mov mp4 m4v m4a m4b m4p m4r 3ga 3gpa 3gpp 3gp 3gpp2 3g2 k3g jpm jpx mqv ismv isma ismt f4a f4b f4v",
                "Format_Commercial": "MPEG-4",
                "Format_Profile": "Base Media",
                "InternetMediaType": "video/mp4",
                "CodecID": "mp42",
                "CodecID_String": "mp42 (mp42/mp41/isom/avc1)",
                "CodecID_Url": "http://www.apple.com/quicktime/download/standalone.html",
                "CodecID_Compatible": "mp42/mp41/isom/avc1",
                "FileSize": "17839845",
                "FileSize_String": "17.0 MiB",
                "FileSize_String1": "17 MiB",
                "FileSize_String2": "17 MiB",
                "FileSize_String3": "17.0 MiB",
                "FileSize_String4": "17.01 MiB",
                "Duration": "30.527",
                "Duration_String": "30 s 527 ms",
                "Duration_String1": "30 s 527 ms",
                "Duration_String2": "30 s 527 ms",
                "Duration_String3": "00:00:30.527",
                "Duration_String4": "00:00:30:01",
                "Duration_String5": "00:00:30.527 (00:00:30:01)",
                "OverallBitRate": "4675165",
                "OverallBitRate_String": "4 675 kb/s",
                "FrameRate": "30.000",
                "FrameRate_String": "30.000 FPS",
                "FrameCount": "901",
                "StreamSize": "19077",
                "StreamSize_String": "18.6 KiB (0%)",
                "StreamSize_String1": "19 KiB",
                "StreamSize_String2": "19 KiB",
                "StreamSize_String3": "18.6 KiB",
                "StreamSize_String4": "18.63 KiB",
                "StreamSize_String5": "18.6 KiB (0%)",
                "StreamSize_Proportion": "0.00107",
                "HeaderSize": "19069",
                "DataSize": "17820776",
                "FooterSize": "0",
                "IsStreamable": "Yes",
                "Encoded_Date": "UTC 2015-08-07 09:13:36",
                "Tagged_Date": "UTC 2015-08-07 09:13:36",
                "File_Modified_Date": "UTC 2021-08-17 09:17:09",
                "File_Modified_Date_Local": "2021-08-17 10:17:09"
            },
                {
                    "@type": "Video",
                    "Count": "378",
                    "StreamCount": "1",
                    "StreamKind": "Video",
                    "StreamKind_String": "Video",
                    "StreamKindID": "0",
                    "StreamOrder": "0",
                    "ID": "1",
                    "ID_String": "1",
                    "Format": "AVC",
                    "Format_String": "AVC",
                    "Format_Info": "Advanced Video Codec",
                    "Format_Url": "http://developers.videolan.org/x264.html",
                    "Format_Commercial": "AVC",
                    "Format_Profile": "High",
                    "Format_Level": "4",
                    "Format_Settings": "CABAC / 4 Ref Frames",
                    "Format_Settings_CABAC": "Yes",
                    "Format_Settings_CABAC_String": "Yes",
                    "Format_Settings_RefFrames": "4",
                    "Format_Settings_RefFrames_String": "4 frames",
                    "InternetMediaType": "video/H264",
                    "CodecID": "avc1",
                    "CodecID_Info": "Advanced Video Coding",
                    "Duration": "30.033",
                    "Duration_String": "30 s 33 ms",
                    "Duration_String1": "30 s 33 ms",
                    "Duration_String2": "30 s 33 ms",
                    "Duration_String3": "00:00:30.033",
                    "Duration_String4": "00:00:30:01",
                    "Duration_String5": "00:00:30.033 (00:00:30:01)",
                    "BitRate": "4500000",
                    "BitRate_String": "4 500 kb/s",
                    "Width": "1920",
                    "Width_String": "1 920 pixels",
                    "Height": "1080",
                    "Height_String": "1 080 pixels",
                    "Stored_Height": "1088",
                    "Sampled_Width": "1920",
                    "Sampled_Height": "1080",
                    "PixelAspectRatio": "1.000",
                    "DisplayAspectRatio": "1.778",
                    "DisplayAspectRatio_String": "16:9",
                    "Rotation": "0.000",
                    "FrameRate_Mode": "CFR",
                    "FrameRate_Mode_String": "Constant",
                    "FrameRate_Mode_Original": "VFR",
                    "FrameRate": "30.000",
                    "FrameRate_String": "30.000 FPS",
                    "FrameCount": "901",
                    "ColorSpace": "YUV",
                    "ChromaSubsampling": "4:2:0",
                    "ChromaSubsampling_String": "4:2:0",
                    "BitDepth": "8",
                    "BitDepth_String": "8 bits",
                    "ScanType": "Progressive",
                    "ScanType_String": "Progressive",
                    "BitsPixel_Frame": "0.072",
                    "StreamSize": "16843872",
                    "StreamSize_String": "16.1 MiB (94%)",
                    "StreamSize_String1": "16 MiB",
                    "StreamSize_String2": "16 MiB",
                    "StreamSize_String3": "16.1 MiB",
                    "StreamSize_String4": "16.06 MiB",
                    "StreamSize_String5": "16.1 MiB (94%)",
                    "StreamSize_Proportion": "0.94417",
                    "Encoded_Library": "x264 - core 146 r11M 121396c",
                    "Encoded_Library_String": "x264 core 146 r11M 121396c",
                    "Encoded_Library_Name": "x264",
                    "Encoded_Library_Version": "core 146 r11M 121396c",
                    "Encoded_Library_Settings": "cabac=1 / ref=4 / deblock=1:0:0 / analyse=0x3:0x113 / me=umh / subme=8 / psy=1 / psy_rd=1.00:0.00 / mixed_ref=1 / me_range=16 / chroma_me=1 / trellis=1 / 8x8dct=1 / cqm=0 / deadzone=21,11 / fast_pskip=1 / chroma_qp_offset=-2 / threads=48 / lookahead_threads=8 / sliced_threads=0 / nr=0 / decimate=1 / interlaced=0 / bluray_compat=0 / stitchable=1 / constrained_intra=0 / bframes=3 / b_pyramid=2 / b_adapt=2 / b_bias=0 / direct=3 / weightb=1 / open_gop=0 / weightp=2 / keyint=infinite / keyint_min=30 / scenecut=40 / intra_refresh=0 / rc_lookahead=50 / rc=2pass / mbtree=1 / bitrate=4500 / ratetol=1.0 / qcomp=0.60 / qpmin=5 / qpmax=69 / qpstep=4 / cplxblur=20.0 / qblur=0.5 / vbv_maxrate=4950 / vbv_bufsize=13500 / nal_hrd=none / filler=0 / ip_ratio=1.40 / aq=1:1.00",
                    "Encoded_Date": "UTC 2015-08-07 09:13:36",
                    "Tagged_Date": "UTC 2015-08-07 09:13:36",
                    "colour_description_present": "Yes",
                    "colour_description_present_Source": "Container / Stream",
                    "colour_range": "Limited",
                    "colour_range_Source": "Container / Stream",
                    "colour_primaries": "BT.709",
                    "colour_primaries_Source": "Container / Stream",
                    "transfer_characteristics": "BT.709",
                    "transfer_characteristics_Source": "Container / Stream",
                    "matrix_coefficients": "BT.709",
                    "matrix_coefficients_Source": "Container / Stream",
                    "extra": {
                        "CodecConfigurationBox": "avcC"
                    }
                },
                {
                    "@type": "Audio",
                    "Count": "280",
                    "StreamCount": "1",
                    "StreamKind": "Audio",
                    "StreamKind_String": "Audio",
                    "StreamKindID": "0",
                    "StreamOrder": "1",
                    "ID": "2",
                    "ID_String": "2",
                    "Format": "AAC",
                    "Format_String": "AAC LC",
                    "Format_Info": "Advanced Audio Codec Low Complexity",
                    "Format_Commercial": "AAC",
                    "Format_AdditionalFeatures": "LC",
                    "CodecID": "mp4a-40-2",
                    "Duration": "30.527",
                    "Duration_String": "30 s 527 ms",
                    "Duration_String1": "30 s 527 ms",
                    "Duration_String2": "30 s 527 ms",
                    "Duration_String3": "00:00:30.527",
                    "Duration_String4": "00:00:30:21",
                    "Duration_String5": "00:00:30.527 (00:00:30:21)",
                    "BitRate_Mode": "CBR",
                    "BitRate_Mode_String": "Constant",
                    "BitRate": "256008",
                    "BitRate_String": "256 kb/s",
                    "Channels": "2",
                    "Channels_String": "2 channels",
                    "ChannelPositions": "Front: L R",
                    "ChannelPositions_String2": "2/0/0",
                    "ChannelLayout": "L R",
                    "SamplesPerFrame": "1024",
                    "SamplingRate": "48000",
                    "SamplingRate_String": "48.0 kHz",
                    "SamplingCount": "1465296",
                    "FrameRate": "46.875",
                    "FrameRate_String": "46.875 FPS (1024 SPF)",
                    "FrameCount": "1431",
                    "Compression_Mode": "Lossy",
                    "Compression_Mode_String": "Lossy",
                    "StreamSize": "976896",
                    "StreamSize_String": "954 KiB (5%)",
                    "StreamSize_String1": "954 KiB",
                    "StreamSize_String2": "954 KiB",
                    "StreamSize_String3": "954 KiB",
                    "StreamSize_String4": "954.0 KiB",
                    "StreamSize_String5": "954 KiB (5%)",
                    "StreamSize_Proportion": "0.05476",
                    "Encoded_Date": "UTC 2015-08-07 09:13:36",
                    "Tagged_Date": "UTC 2015-08-07 09:13:36"
                }
            ]
        }
    }
    return example_log


def test_merge_mediainfo(test_ora_log, test_sf_log, test_exif_log,
                         test_mediainfo_mult_f, test_key_list_file):
    merged_sf_log = merge_sf_logs(load_json(test_ora_log), test_sf_log,
                                  "filename")

    merged_logs_with_exif = merge_exif_to_base_log(test_exif_log, merged_sf_log,
                                                   test_key_list_file,
                                                   "SourceFile")

    merged_mediainfo_with_sf = merge_mediainfo(merged_logs_with_exif,
                                               test_mediainfo_mult_f,
                                               test_key_list_file, "@ref")
    for f in merged_sf_log:
        assert "mediainfo" in merged_mediainfo_with_sf[f].keys()


def test_desired_mediainfo_keys(test_ora_log, test_sf_log, test_exif_log,
                                test_mediainfo_mult_f, test_key_list_file):
    merged_sf_log = merge_sf_logs(load_json(test_ora_log), test_sf_log,
                                  "filename")

    merged_logs_with_exif = merge_exif_to_base_log(test_exif_log, merged_sf_log,
                                                   test_key_list_file,
                                                   "SourceFile")

    merged_mediainfo_with_sf = merge_mediainfo(merged_logs_with_exif,
                                               test_mediainfo_mult_f,
                                               test_key_list_file, "@ref")
    desired_keys = read_key_list(test_key_list_file)
    for f in merged_mediainfo_with_sf:
        mediainfo_entries = merged_mediainfo_with_sf[f]["mediainfo"]
        for entry in mediainfo_entries:
            for type in entry.keys():
                for k in entry[type]:
                    if k != "@type":
                        assert k in desired_keys


def test_merge_mediainfo_without_exif(test_ora_log, test_sf_log, test_exif_log,
                                      test_mediainfo_mult_f,
                                      test_key_list_file):
    merged_sf_log = merge_sf_logs(load_json(test_ora_log), test_sf_log,
                                  "filename")

    merged_mediainfo_with_sf = merge_mediainfo(merged_sf_log,
                                               test_mediainfo_mult_f,
                                               test_key_list_file, "@ref")
    for f in merged_sf_log:
        assert "mediainfo" in merged_mediainfo_with_sf[f].keys()
