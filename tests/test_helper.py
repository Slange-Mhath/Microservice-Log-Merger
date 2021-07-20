import pytest
from helper import load_json, replace_none_values, read_key_list, delete_keys_with_str_seq



@pytest.fixture()
def test_ora_log():
    ora_logs = "tests/dummy_logs/ora.json"
    return ora_logs


@pytest.fixture()
def test_sf_log():
    sf_log = "tests/dummy_logs/sf.log"
    return sf_log


@pytest.fixture()
def test_file():
    path_to_ora_file = "tests/dummy_logs/dpms-ora-truncated.json"
    return path_to_ora_file


@pytest.fixture()
def test_key_list_file():
    key_list_file = "tests/dummy_logs/key_list.log"
    return key_list_file


@pytest.fixture()
def test_list_of_str_seq():
    list_of_seq = ["ExifZ*", "ExifA*", "Exif12*", "ExifT*"]
    return list_of_seq


@pytest.fixture()
def test_exif_dict():
    example_log = {
        "SourceFile": "/ORA/PRD/DATA/ora_var/fedora/objects/2008/0520/10/26/uuid_7a79f51b-509f-476f-b1d0-1466dbfd9c78",
        "ExifToolVersion": 12.16,
        "FileName": "2_PEARCE_Qualitative_collated_themes.xlsx",
        "Directory": "/ORA4/PRD/PUBLIC/00/98/95/76/uuid:00989576-dd33-458b-b8cd-e49b7e845ee6",
        "FileSize": "108 KiB",
        "ZipRequiredVersion": 20,
        "ZipBitFlag": "0x0006",
        "ZipCompression": "Deflated",
        "ZipModifyDate": "1980:01:01 00:00:00",
        "ZipCRC": "0x78c4a176",
        "ZipCompressedSize": 448,
        "ZipUncompressedSize": 4226,
        "ZipFileName": "[Content_Types].xml",
        "ScaleCrop": "No",
        "HeadingPairs": [
            "Worksheets",
            23
        ],
        "TitlesOfParts": [
            "20_integration_into_life",
            "21_motivation",
            "22_localresources"
        ],
        "LastModifiedBy": "Eiluned Pearce",
        "CreateDate": "2016:03:11 15:17:02Z",
        "ModifyDate": "2016:05:23 09:53:07Z",
        "ExifZitteraal": "Udo",
        "ExifZementmaschine": "Ulf",
        "ExifZentralrat": "Urs",
        "ExifZimmermann": "Rolf",
        "ExifZwangsehe": "Hannah",
        "ExifZalamanda": "Feuer",

    }
    return example_log


@pytest.fixture()
def dict_with_none_value():
    example_dict = {"ns": "pronom", "id": "UNKNOWN", "format": "",
                    "version": "", "mime": "", "basis": "",
                    "warning": "no match"}
    return example_dict


@pytest.fixture()
def test_log():
    example_log = {'errors': '',
                   'filename': '/ORA/PRD/DATA/ora_var/fedora/objects/2008/0520/10/26/uuid_f07ecc49-0e77-43d3-bbaa-a69a515f8c0c',
                   'filesize': 19685,
                   'matches': [{'basis': 'byte match at 0, 19',
                                'format': 'Extensible Markup Language',
                                'id': 'fmt/101',
                                'mime': 'application/xml',
                                'ns': 'pronom',
                                'version': '1.0',
                                'warning': 'extension mismatch'}],
                   'modified': '2018-03-19T01:02:04Z'}
    return example_log


def test_load_json(test_file):
    file_data = load_json(test_file)
    assert isinstance(file_data, dict)


def test_replace_non_value(dict_with_none_value):
    replaced_dict = replace_none_values(dict_with_none_value)
    for item in replaced_dict.items():
        assert item is not None


def test_read_key_list(test_key_list_file):
    list_of_keys = read_key_list(test_key_list_file)
    assert isinstance(list_of_keys, list)
    assert len(list_of_keys) is not 0


def test_delete_keys_with_string_seq(test_exif_dict, test_list_of_str_seq):
    cleaned_dict = delete_keys_with_str_seq(test_exif_dict, test_list_of_str_seq)
    assert cleaned_dict is not None


