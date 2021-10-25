from argparse import ArgumentParser
from helper import load_base_log_json, write_merged_f_log
from merge_siegfried import merge_sf_logs
from merge_exif import merge_exif_to_base_log
from merge_mediainfo import merge_mediainfo
import logging
import memory_profiler as mem_profile
import time

def main(base_log_path, sf_log, exif_log, f_key_list=None, output_file=None,
         mediainfo_log=None, occurrence_of_keys=None):
    """
    Calls the different functions in order to merge and write the final output
    :param dpms_log_path: takes the path to the file integrity file
    :param sf_log: takes the path to the siegfried log file
    :param output_file: takes an optional user specified output file
    :return:
    """
    print("Memory (Before): {}Mb".format(mem_profile.memory_usage()))
    t1 = time.process_time()
    merged_log_files = {}
    base_log_json = load_base_log_json(base_log_path)
    if sf_log:
        merged_log_files = merge_sf_logs(base_log_json, sf_log)
        if exif_log:
            if not f_key_list:
                logging.error(
                    "Please provide a file with the keys if you want to merge "
                    "the Exif log.")
                return
            merged_log_files = merge_exif_to_base_log(
                                                      exif_log,
                                                      merged_log_files,
                                                      f_key_list, occurrence_of_keys,
                                                      matching_key="SourceFile",
                                                      )
        if mediainfo_log:
            if not f_key_list:
                logging.error(
                    "Please provide a file with the keys if you want to merge "
                    "the Mediainfo log.")
                return
            merged_log_files = merge_mediainfo(merged_log_files, mediainfo_log,
                                               f_key_list, matching_key="@ref")
    write_merged_f_log(merged_log_files, output_file)
    t2 = time.process_time()
    print("Memory (After): {}Mb".format(mem_profile.memory_usage()))
    print("Took {} Seconds".format(t2 - t1))



# TODO: Maybe I want to use a control structure to get rid of the messy if
#  clauses

if __name__ == "__main__":
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
