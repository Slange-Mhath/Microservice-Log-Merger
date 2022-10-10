import json

import pytest
from merge_siegfried import relabel_siegfried_log, add_sf_info_to_db
from helper import load_json
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from main import File, add_ora_info_to_db
from merge_jpylyzer import relabel_jpylyzer_log, add_jpylyzer_info_to_db

Base = declarative_base()


class File(Base):
    __tablename__ = "file"
    path = Column("path", String, primary_key=True)
    timestamp = Column("timestamp", String)
    base_file_info = Column("base_file_info", String)
    siegfried_file_info = Column("siegfried_file_info", String)
    exif_file_info = Column("exif_file_info", String)
    jpylyzer_file_info = Column("jpylyzer_file_info", String)
    pdf_info = Column("pdf_info", String)
    mediainfo_file_info = Column("mediainfo_file_info", String)


# engine = create_engine("sqlite:///mlm.db", )
engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost/mlmdb')
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
file = File()


@pytest.fixture()
def test_db_file():
    return File


@pytest.fixture()
def test_session():
    return session


@pytest.fixture()
def test_ora_log():
    ora_logs = "tests/dummy_logs/ora.json"
    return ora_logs


@pytest.fixture()
def test_jpylyzer_log():
    jpylyzer_log = "tests/dummy_logs/jpylyzer_log.json"
    return jpylyzer_log


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


# def test_relabel_siegfried_log(test_log):
#     relabeled_log = relabel_siegfried_log(test_log, sf_version="42.0")
#     for k in relabeled_log.keys():
#         assert k is not "errors" or "filename" or "filesize" or "modified"
#     for v in relabeled_log.items():
#         assert v is not None


# def test_merge_sf_logs(test_ora_log, test_sf_log):
#     merged_logs = merge_sf_logs(load_json(test_ora_log), test_sf_log,
#                                 "filename")
#     for head_k in merged_logs.keys():
#         assert head_k == merged_logs[head_k]["file"]["path"]
#         for v in merged_logs[head_k].values():
#             assert v is not None

def test_add_ora_info_into_db(test_ora_log, test_session, test_db_file):
    base_log_json = load_json(test_ora_log)
    add_ora_info_to_db(base_log_json, test_session, test_db_file)
    ora_files = session.query(test_db_file).all()
    for ora_f in ora_files:
        ora_f_file_info = json.loads(ora_f.base_file_info)
        assert ora_f_file_info["path"] == ora_f.path
        if ora_f.path == "/AORTA/PRD/DATA/ora_var/fedora/objects/2008/0520/10/26/uuid_7a79f51b-509f-476f-b1d0-1466dbfd9c78":
            assert ora_f_file_info["size"] == "20004"


def test_add_sf_info_into_db(test_sf_log, test_session, test_db_file):
    add_sf_info_to_db(test_sf_log, test_session, test_db_file)
    sf_files = session.query(test_db_file).all()
    for sf_file in sf_files:
        if sf_file.siegfried_file_info:
            sf_file_info = json.loads(sf_file.siegfried_file_info)
            if sf_file.path == "/ORA4/PRD/REVIEW/ff/85/03/ff85037813a09ea793b4bc2d860324d65184c20f":
                assert sf_file_info["siegfried"]["format"] == "PDF"


def test_add_jpylyzer_log_into_db(test_jpylyzer_log, test_session, test_db_file):
    add_jpylyzer_info_to_db(test_jpylyzer_log, test_session, test_db_file)
    jp_files = session.query(test_db_file).all()
    for jp_f in jp_files:
        if jp_f.jpylyzer_file_info:
            jp_file_info = json.loads(jp_f.jpylyzer_file_info)
            if jp_f.path == "/DIGITAL/PRD/BodleianImaging/pairtree_root/00/00/96/dd/-1/0f/0-/47/9d/-b/1e/5-/ad/fc/66/22/1e/72/obj/__latest/full_lossless.jp2":
                assert jp_file_info['properties']["contiguousCodestreamBox"]['cod']['levels'] == 6

