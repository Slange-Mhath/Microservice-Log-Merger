from argparse import ArgumentParser
from helper import load_json, write_merged_f_log
from merge_siegfried import merge_sf_logs
from merge_exif import merge_exif_logs


def main(base_log_path, sf_log, exif_log, output_file=None, f_keys_to_del=None):
    """
    Calls the different functions in order to merge and write the final output
    :param dpms_log_path: takes the path to the file integrity file
    :param sf_log: takes the path to the siegfried log file
    :param output_file: takes an optional user specified output file
    :return:
    """
    merged_log_files = {}
    base_log_json = load_json(base_log_path)
    if sf_log:
        merged_log_files = merge_sf_logs(base_log_json, sf_log, "filename")
        if exif_log:
            merged_log_files = merge_exif_logs(merged_log_files, exif_log,
                                               matching_key="SourceFile",
                                               f_keys_to_del=f_keys_to_del)

    write_merged_f_log(merged_log_files, output_file)


# TODO: Maybe I want to use a control structure to get rid of the messy if clauses

if __name__ == "__main__":
    parser = ArgumentParser(description="...")
    parser.add_argument("-base_log_path", metavar="base_log_path",
                        help="Path to the base log file which should be "
                             "merged with the others")
    parser.add_argument("-sf_log_path", metavar="sf_log_path",
                        help="Path to the Siegfried output file")
    parser.add_argument("-exif_log_path", "--exif_log_path", dest="exif_log_path",
                        help="Path to the exif log file")
    parser.add_argument("-dest_file_path", "--dest_file_path", dest="dest_file_path",
                        help="Path to write the merged file log")
    parser.add_argument("-f_keys_to_del_path", "--f_keys_to_del_path",
                        dest="f_keys_to_del_path",
                        help="Path to a file with keys we don't want to have "
                             "in the exif log")
    args = parser.parse_args()
    main(args.base_log_path, args.sf_log_path, args.exif_log_path, args.dest_file_path,
         args.f_keys_to_del_path)
