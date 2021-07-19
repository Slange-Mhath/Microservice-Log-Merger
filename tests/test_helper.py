import pytest
from helper import load_json
from helper import replace_none_values
from helper import read_key_list


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