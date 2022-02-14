import pytest
from merge_exif import add_exif_info_to_db, create_enriching_exif
from helper import load_json, read_key_list
from merge_siegfried import add_sf_info_to_db
from merge_analysed_pdfs import add_pdf_info_to_db
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, \
    update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from main import File, add_ora_info_to_db
import json

Base = declarative_base()


class File(Base):
    __tablename__ = "file"
    path = Column("path", String, primary_key=True)
    timestamp = Column("timestamp", String)
    base_file_info = Column("base_file_info", String)
    siegfried_file_info = Column("siegfried_file_info", String)
    exif_file_info = Column("exif_file_info", String)
    mediainfo_file_info = Column("mediainfo_file_info", String)
    pdf_info = Column("pdf_info", String)


# engine = create_engine("sqlite:///mlm.db", )
engine = create_engine(
    'postgresql+psycopg2://postgres:postgres@localhost/mlmdb')
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
file = File()


@pytest.fixture()
def test_pdf_log():
    pdf_logs = "tests/dummy_logs/multiple_pdf_new.json"
    return pdf_logs


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
def test_sf_log():
    sf_log = "tests/dummy_logs/sf.log"
    return sf_log


@pytest.fixture()
def test_exif_log():
    sf_log = "tests/dummy_logs/multiple_exif_dir.log"
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
        "ModifyDate": "2016:05:23 09:53:07Z",
        "Author": ""
    }
    return example_log


@pytest.fixture()
def test_key_list_file():
    key_list_file = "tests/dummy_logs/key_list.log"
    return key_list_file


@pytest.fixture()
def test_occurrence_of_keys():
    occurence_of_keys = True
    return occurence_of_keys


def test_add_ora_info_into_db(test_ora_log, test_session, test_db_file):
    base_log_json = load_json(test_ora_log)
    add_ora_info_to_db(base_log_json, test_session, test_db_file)


def test_add_sf_info_into_db(test_sf_log, test_session, test_db_file):
    add_sf_info_to_db(test_sf_log, test_session, test_db_file)


def test_add_pdf_info_to_db(test_pdf_log, test_session, test_db_file):
    add_pdf_info_to_db(test_pdf_log, test_session, test_db_file)
    pdf_info_objs = session.query(test_db_file).all()
    for pdf_info_obj in pdf_info_objs:
        if pdf_info_obj.path == "test_pdfs/A+study+of+the+Middle+English+treatises+on+grammar+(Part+2+-+file+1)":
            pdf_info_json = json.loads(pdf_info_obj.pdf_info)
            assert pdf_info_json["isImage"] is False
            # Check if json information has keys: isImage, list_of_fonts, tool_version_info, word_count
            json_keys = ["isImage", "list_of_fonts", "tool_version_info", "word_count"]
            for key in json_keys:
                assert key in pdf_info_json.keys()


