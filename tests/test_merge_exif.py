import pytest
from merge_exif import relabel_exif_log, merge_exif_logs
from helper import read_key_list, load_json
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
def test_file():
    path_to_ora_file = "logs/dpms-ora-truncated.json"
    return path_to_ora_file


@pytest.fixture()
def dict_with_none_value():
    example_dict = {"ns": "pronom", "id": "UNKNOWN", "format": "",
                    "version": "", "mime": "", "basis": "",
                    "warning": "no match"}
    return example_dict


@pytest.fixture()
def test_exif_dict():
    example_log = {
        "SourceFile": "/ORA/PRD/DATA/ora_var/fedora/objects/2008/0520/10/26/uuid_7a79f51b-509f-476f-b1d0-1466dbfd9c78",
        "ExifToolVersion": 12.16,
        "FileName": "2_PEARCE_Qualitative_collated_themes.xlsx",
        "Directory": "/ORA4/PRD/PUBLIC/00/98/95/76/uuid:00989576-dd33-458b-b8cd-e49b7e845ee6",
        "FileSize": "108 KiB",
        "FileModifyDate": "2018:03:14 18:57:25+00:00",
        "FileAccessDate": "2018:03:14 18:57:25+00:00",
        "FileInodeChangeDate": "2018:03:14 18:57:25+00:00",
        "FilePermissions": "rw-r--r--",
        "FileType": "XLSX",
        "FileTypeExtension": "xlsx",
        "MIMEType": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "ZipRequiredVersion": 20,
        "ZipBitFlag": "0x0006",
        "ZipCompression": "Deflated",
        "ZipModifyDate": "1980:01:01 00:00:00",
        "ZipCRC": "0x78c4a176",
        "ZipCompressedSize": 448,
        "ZipUncompressedSize": 4226,
        "ZipFileName": "[Content_Types].xml",
        "PreviewImage": "(Binary data 29920 bytes, use -b option to extract)",
        "Application": "Microsoft Macintosh Excel",
        "DocSecurity": "None",
        "ScaleCrop": "No",
        "HeadingPairs": [
            "Worksheets",
            23
        ],
        "TitlesOfParts": [
            "Key",
            "1_self(re)discovery",
            "2_likecomfortableself",
            "3_Timeout",
            "4_Transitions",
            "5_Abilities",
            "6_voice",
            "7_acceptchallenges",
            "8_initiative",
            "9_socialconfidence",
            "10_role",
            "11_belonging",
            "12_reinforceRSinClass",
            "13_expandnetwork",
            "14_diversity_openness",
            "15_share",
            "16_comparison",
            "17_substructure",
            "18_mood",
            "19_phys",
            "20_integration_into_life",
            "21_motivation",
            "22_localresources"
        ],
        "Company": "",
        "LinksUpToDate": "No",
        "SharedDoc": "No",
        "HyperlinksChanged": "No",
        "AppVersion": 14.0300,
        "Creator": "Eiluned Pearce",
        "LastModifiedBy": "Eiluned Pearce",
        "CreateDate": "2016:03:11 15:17:02Z",
        "ModifyDate": "2016:05:23 09:53:07Z"
    }
    return example_log


@pytest.fixture()
def test_key_list_file():
    key_list_file = "tests/dummy_logs/key_list.log"
    return key_list_file


def test_relabel_exif_log_for_superficial_keys(test_exif_dict,
                                               test_key_list_file):
    relabeled_log = relabel_exif_log(test_exif_dict, test_key_list_file)
    keys_to_delete = read_key_list(test_key_list_file)
    for k in relabeled_log["exif"].keys():
        assert k not in keys_to_delete


def test_relabel_exif_log_for_none_values(test_exif_dict, test_key_list_file):
    relabeled_log = relabel_exif_log(test_exif_dict, test_key_list_file)
    for k in relabeled_log["exif"].values():
        assert k is not None


def test_merge_exif_logs(test_ora_log, test_sf_log, test_exif_log):
    merged_sf_log = merge_sf_logs(load_json(test_ora_log), test_sf_log,
                                  "filename")
    merged_logs_with_exif = merge_exif_logs(merged_sf_log, test_exif_log,
                                            "SourceFile", None)
    # log_file_tools stores the different keys of the merged log file. This is
    # why we can make the assumption that exif and siegfried are both stored in
    # this list (timestamp and file are superficial in this purpose but wont
    # hurt for validation)
    log_file_tools = []
    for keys in merged_logs_with_exif.values():
        for key in keys.keys():
            log_file_tools.append(key)
    assert "exif" in log_file_tools
