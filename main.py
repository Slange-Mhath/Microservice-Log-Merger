import json
from argparse import ArgumentParser
from helper import load_json, merge_logs, write_merged_f_log
import logging


# def read_integrity_log_json(dpms_log_path):
#     """
#     Reads the file integrity file
#     :param dpms_log_path: takes the path to the file integrity file
#     :return: returns the file as json
#     """
#     dpms_log_f = open(dpms_log_path, "r")
#     dpms_log_json = json.load(dpms_log_f)
#     return dpms_log_json
#
#
# def replace_none_values(log_dict):
#     """
#     Replaces 'None' values from a dict with 'unknown' String to make it easier
#     to search for it etc.
#     :param log_dict: takes the dict where the values should be replaced. (In our
#     case thats the Siegfried output part)
#     :return: returns the replaced dict
#     """
#     if isinstance(log_dict, dict):
#         log_dict = {k: "unknown" if not v else v for k, v in log_dict.items()}
#     return log_dict
#
#
# def relabel_log(log, sf_version):
#     """
#     Relabels the Siegfried output to fit our needs. Therefore deletes
#     superficial keys and replaces the 'matches' key with the siegfried version
#     as head key and targets the siegfried output as dict by assuming it will
#     always be at index 0 of the array 'matches'. Finally replaces the none
#     values from the dict.
#     :param log: takes the siegfried log as json
#     :param sf_version: takes the siegfried version
#     :return: returns the adjusted siegfried output
#     """
#     del log["errors"]
#     del log["filename"]
#     del log["filesize"]
#     del log["modified"]
#     try:
#         log["matches"][0]["siegfried_version"] = sf_version
#     except IndexError:
#         logging.warning("Siegfried didn't return any output")
#     # In case of empty values from the SF log, apply unknown instead of nothing
#     log = replace_none_values(log)
#     sf_output = {"siegfried": log["matches"][0]}
#     if sf_output["siegfried"]:
#         sf_output["siegfried"] = replace_none_values(sf_output["siegfried"])
#     return sf_output
#
#
# def merge_logs(integrity_log, sf_log):
#     """
#     Uses dict comprehension to create a new dict which adds the siegfried output
#     at the matching file paths.
#     For every file in siegfried output which is in the comprehended new dict
#     relabel the siegfried output and update it to the now with siegfried output
#     enriched output.
#     :param integrity_log: takes the read integrity log
#     :param sf_log: takes the read siegfried log (sf_log)
#     :return: returns the now with siegfried output enriched integrity file.
#     """
#     sf_enriched_output = {}
#     for f in integrity_log["files"]:
#         sf_enriched_output[f["file"]["path"]] = f
#     for output in open(sf_log, "r"):
#         json_output = json.loads(output)
#         try:
#             sf_version = json_output["siegfried"]
#         except KeyError:
#             sf_version = "unknown"
#         for f in json_output["files"]:
#             if f["filename"] in sf_enriched_output:
#                 sf_enriched_output[f["filename"]].update(relabel_log(f, sf_version))
#     # merged_logs = []
#     # for f in sf_enriched_output.values():
#     #     merged_logs.append(f)
#     return sf_enriched_output
#
#
# def write_merged_f_log(merged_log, dest_file):
#     """
#     Writes the merged and enriched integrity file to a specified output file.
#     :param merged_log: takes the merged and enriched file
#     :param dest_file: takes the output file
#     """
#     output = open(dest_file, "w", encoding="utf-8")
#     for f in merged_log.values():
#         json.dump(f, output, sort_keys=True, ensure_ascii=False)
#         output.write("\n")


def main(base_log_path, sf_log, output_file=None):
    """
    Calls the different functions in order to merge and write the final output
    :param dpms_log_path: takes the path to the file integrity file
    :param sf_log: takes the path to the siegfried log file
    :param output_file: takes an optional user specified output file
    :return:
    """
    base_log_json = load_json(base_log_path)
    merged_log_files = merge_logs(base_log_json, sf_log)
    write_merged_f_log(merged_log_files, output_file)


if __name__ == "__main__":
    parser = ArgumentParser(description="...")
    parser.add_argument("base_log_path", metavar="base_log_path", help="Path to the base log file which should be merged with the others")
    parser.add_argument("sf_log", metavar="sf_log", help="Path to the Siegfried output file")
    parser.add_argument("-o", "--dest_file", dest="dest_file", help="Path to write the merged file log")
    args = parser.parse_args()
    main(args.dpms_log_path, args.sf_log, args.dest_file)
