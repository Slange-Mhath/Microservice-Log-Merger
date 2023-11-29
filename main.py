from argparse import ArgumentParser
from helper import load_json, add_ora_info_to_db, write_merged_f_log, get_database_url
from merge_siegfried import add_sf_info_to_db
from merge_exif import add_exif_info_to_db
from merge_mediainfo import add_mediainfo_info_to_db
from merge_analysed_pdfs import add_pdf_info_to_db
from merge_jpylyzer import add_jpylyzer_info_to_db
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
    jpylyzer_file_info = Column("jpylyzer_file_info", String)
    pdf_info = Column("pdf_info", String)


# # Connect to Postgres
# engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost/mlmdb')
# # Drop old DB
# Base.metadata.drop_all(engine)
# Base.metadata.create_all(bind=engine)
# Session = sessionmaker(bind=engine)
# session = Session()
# file = File()


def main(db_name, db_user, db_password, db_host, base_log_path, sf_log,
         exif_log, pdf_analyser_log, f_key_list=None, output_file=None,
         mediainfo_log=None, jpylyzer_log=None, occurrence_of_keys=None,
         persist_db=False):
    """
    Calls the different functions in order to merge and write the final output
    :param jpylyzer_log: takes the path to the jpylyzer log file
    :param dpms_log_path: takes the path to the file integrity file
    :param sf_log: takes the path to the siegfried log file
    :param output_file: takes an optional user specified output file
    :return:
    """
    # Connect to Postgres

    connection_string = get_database_url(
        db_name,
        db_user,
        db_password,
        db_host
    )
    engine = create_engine(
        connection_string)
    # Drop old DB
    if not persist_db:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine)()
    file = File()
    logging.info("Memory (Before): {}Mb".format(mem_profile.memory_usage()))
    # print("Memory (Before): {}Mb".format(mem_profile.memory_usage()))
    t1 = time.process_time()
    base_log_json = load_json(base_log_path)
    add_ora_info_to_db(base_log_json, session, File)
    if sf_log:
        add_sf_info_to_db(sf_log, session, File)
    if pdf_analyser_log:
        add_pdf_info_to_db(pdf_analyser_log, session, File)
    if exif_log:
        add_exif_info_to_db(exif_log, session, File, f_key_list, occurrence_of_keys)
        if not f_key_list:
            logging.error(
                "Please provide a file with the keys if you want to merge "
                "the Exif log.")
            return
    if mediainfo_log:
        add_mediainfo_info_to_db(f_key_list, mediainfo_log, session, File)
        if not f_key_list:
            logging.error(
                "Please provide a file with the keys if you want to merge "
                "the Mediainfo log.")
            return
    if jpylyzer_log:
        add_jpylyzer_info_to_db(jpylyzer_log, session, File)
    if output_file:
        write_merged_f_log(session, File, output_file)
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
    parser.add_argument("-pdf_analyser_log_path", "--pdf_analyser_log_path",
                        dest="pdf_analyser_log_path",
                        help="Path to the pdf analyser log file")
    parser.add_argument("-dest_file_path", "--dest_file_path",
                        dest="dest_file_path",
                        help="Path to write the merged file log")
    parser.add_argument("-f_key_list", "--f_key_list", dest="f_key_list",
                        help="Path to a file with keys we want to store in our "
                             "exif log")
    parser.add_argument("-mediainfo_log_path", "--mediainfo_log_path",
                        dest="mediainfo_log_path",
                        help="Path to the mediainfo log file")
    parser.add_argument("-jpylyzer_log_path", "--jpylyzer_log_path",
                        dest="jpylyzer_log_path",
                        help="Path to the jpylyzer log file")
    parser.add_argument("-occurrence_of_keys", "--occurrence_of_keys",
                        dest="occurrence_of_keys", default=False,
                        help="Set to true if you want to get information about "
                             "the occurrence of the keys in the log")
    parser.add_argument("-persist_db", "--persist_db", dest="persist_db",
                        help="Set to true if you want to persist the DB from "
                             "the last execution")
    parser.add_argument('-db_name', type=str, help='Name of the database',
                        default="mlmdb")
    parser.add_argument('-db_user', type=str, help='Database user', default="postgres")
    parser.add_argument('-db_password', type=str, help='User password',
                        default="postgres")
    parser.add_argument('-db_host', type=str, help='Database host address',
                        default="localhost")
    args = parser.parse_args()
    main(args.db_name, args.db_user, args.db_password, args.db_host,
         args.base_log_path, args.sf_log_path, args.exif_log_path, args.pdf_analyser_log_path,
         args.f_key_list, args.dest_file_path, args.mediainfo_log_path,
         args.jpylyzer_log_path, args.occurrence_of_keys, args.persist_db)
