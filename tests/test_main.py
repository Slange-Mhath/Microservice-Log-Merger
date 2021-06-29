import pytest
from main import read_integrity_log_json
from main import replace_none_values
from main import relabel_log
from main import merge_logs


@pytest.fixture()
def test_ora_log():
    ora_logs = "tests/dummy_logs/ora.log"
    return ora_logs


@pytest.fixture()
def test_sf_log():
    sf_log = "tests/dummy_logs/sf.log"
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


def test_read_integrity_log_json(test_file):
    file_data = read_integrity_log_json(test_file)
    assert isinstance(file_data, dict)


def test_replace_non_value(dict_with_none_value):
    replaced_dict = replace_none_values(dict_with_none_value)
    for item in replaced_dict.items():
        assert item is not None


def test_relabel_log(test_log):
    relabeled_log = relabel_log(test_log, sf_version="42.0")
    for k in relabeled_log.keys():
        assert k is not "errors" or "filename" or "filesize" or "modified"
    for v in relabeled_log.items():
        assert v is not None


def test_merge_logs(test_ora_log, test_sf_log):
    merged_logs = merge_logs(read_integrity_log_json(test_ora_log), test_sf_log)
    for head_k in merged_logs.keys():
        assert head_k == merged_logs[head_k]["file"]["path"]
        for v in merged_logs[head_k].values():
            assert v is not None






