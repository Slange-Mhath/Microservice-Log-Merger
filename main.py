from argparse import ArgumentParser
from helper import load_json, add_ora_info_to_db, write_merged_f_log
from merge_siegfried import add_sf_info_to_db
from merge_exif import add_exif_info_to_db
from merge_mediainfo import add_mediainfo_info_to_db

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import logging
import memory_profiler as mem_profile
import time
log = logging.getLogger(__name__)


Base = declarative_base()


class File(Base):
    __tablename__ = "file"
    path = Column("path", String, primary_key=True)
    timestamp = Column("timestamp", String)
    base_file_info = Column("base_file_info", String)
    siegfried_file_info = Column("siegfried_file_info", String)
    exif_file_info = Column("exif_file_info", String)
    mediainfo_file_info = Column("mediainfo_file_info", String)


# Connect to Postgres
engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost/mlmdb')
# Drop old DB
Base.metadata.drop_all(engine)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
file = File()


def main(base_log_path, sf_log, exif_log, f_key_list=None, output_file=None,
         mediainfo_log=None, occurrence_of_keys=None):
    """
    Calls the different functions in order to merge and write the final output
    :param dpms_log_path: takes the path to the file integrity file
    :param sf_log: takes the path to the siegfried log file
    :param output_file: takes an optional user specified output file
    :return:
    """
    logging.info("Memory (Before): {}Mb".format(mem_profile.memory_usage()))
    # print("Memory (Before): {}Mb".format(mem_profile.memory_usage()))
    t1 = time.process_time()
    base_log_json = load_json(base_log_path)
    add_ora_info_to_db(base_log_json, session, File)
    if sf_log:
        add_sf_info_to_db(sf_log, session, File)
    if exif_log:
        add_exif_info_to_db(exif_log, session, File, f_key_list, occurrence_of_keys)
        if not f_key_list:
            logging.error(
                "Please provide a file with the keys if you want to merge "
                "the Exif log.")
            return
    if mediainfo_log:
        add_mediainfo_info_to_db(mediainfo_log, session, File)
        if not f_key_list:
            logging.error(
                "Please provide a file with the keys if you want to merge "
                "the Mediainfo log.")
            return
    write_merged_f_log(session, File, output_file, f_key_list)
    t2 = time.process_time()
    # print("Memory (After): {}Mb".format(mem_profile.memory_usage()))
    logging.info("Memory (After): {}Mb".format(mem_profile.memory_usage()))
    # print("Took {} Seconds".format(t2-t1))
    logging.info("Took {} Seconds".format(t2-t1))


# TODO: Maybe I want to use a control structure to get rid of the messy if
#  clauses
if __name__ == "__main__":
    logging.basicConfig(filename="mlmlog.log",
                        filemode="a",
                        format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
                        datefmt='%H:%M:%S',
                        level=logging.INFO)
    parser = ArgumentParser(description="...")
    parser.add_argument("-base_log_path", metavar="base_log_path",
                        help="Path to the base log file which should be "
                             "merged with the others")
    parser.add_argument("-sf_log_path", metavar="sf_log_path",
                        help="Path to the Siegfried output file")
    parser.add_argument("-exif_log_path", "--exif_log_path",
                        dest="exif_log_path",
                        help="Path to the exif log file")
    parser.add_argument("-dest_file_path", "--dest_file_path",
                        dest="dest_file_path",
                        help="Path to write the merged file log")
    parser.add_argument("-f_key_list", "--f_key_list", dest="f_key_list",
                        help="Path to a file with keys we want to store in our "
                             "exif log")
    parser.add_argument("-mediainfo_log_path", "--mediainfo_log_path",
                        dest="mediainfo_log_path",
                        help="Path to the mediainfo log file")
    parser.add_argument("-occurrence_of_keys", "--occurrence_of_keys",
                        dest="occurrence_of_keys", default=False,
                        help="Set to true if you want to get information about "
                             "the occurrence of the keys in the log")
    args = parser.parse_args()
    main(args.base_log_path, args.sf_log_path, args.exif_log_path,
         args.f_key_list, args.dest_file_path, args.mediainfo_log_path, args.occurrence_of_keys)
