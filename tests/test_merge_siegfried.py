import pytest
from merge_siegfried import relabel_siegfried_log
from merge_siegfried import merge_sf_logs
from helper import load_json


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
def dict_with_none_value():
    example_dict = {"ns": "pronom", "id": "UNKNOWN", "format": "",
                    "version": "", "mime": "", "basis": "",
                    "warning": "no match"}
    return example_dict


@pytest.fixture()
def test_log():
    example_log = {'errors': '',
                   'filename': '/ORA/PRD/DATA/ora_var/fedora/objects/2008'
                               '/0520/10/26/uuid_f07ecc49-0e77-43d3-bbaa'
                               '-a69a515f8c0c',
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


def test_relabel_siegfried_log(test_log):
    relabeled_log = relabel_siegfried_log(test_log, sf_version="42.0")
    for k in relabeled_log.keys():
        assert k is not "errors" or "filename" or "filesize" or "modified"
    for v in relabeled_log.items():
        assert v is not None


def test_merge_sf_logs(test_ora_log, test_sf_log):
    merged_logs = merge_sf_logs(load_json(test_ora_log), test_sf_log,
                                "filename")
    for head_k in merged_logs.keys():
        assert head_k == merged_logs[head_k]["file"]["path"]
        for v in merged_logs[head_k].values():
            assert v is not None
