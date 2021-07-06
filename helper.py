import json


def load_json(log_path):
    """
    Reads the file integrity file
    :param dpms_log_path: takes the path to the file integrity file
    :return: returns the file as json
    """
    log = open(log_path, "r")
    log_json = json.load(log)
    return log_json


def replace_none_values(log_dict):
    """
    Replaces 'None' values from a dict with 'unknown' String to make it easier
    to search for it etc.
    :param log_dict: takes the dict where the values should be replaced. (In our
    case thats the Siegfried output part)
    :return: returns the replaced dict
    """
    if isinstance(log_dict, dict):
        log_dict = {k: "unknown" if not v else v for k, v in log_dict.items()}
    return log_dict


def write_merged_f_log(merged_log, dest_file):
    """
    Writes the merged and enriched integrity file to a specified output file.
    :param merged_log: takes the merged and enriched file
    :param dest_file: takes the output file
    """
    output = open(dest_file, "w", encoding="utf-8")
    for f in merged_log.values():
        json.dump(f, output, sort_keys=True, ensure_ascii=False)
        output.write("\n")