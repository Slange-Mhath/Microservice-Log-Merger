import json


def load_json(log_path):
    """
    Reads the file integrity file
    :param dpms_log_path: takes the path to the file integrity file
    :return: returns the file as json
    """
    dpms_log_f = open(log_path, "r")
    dpms_log_json = json.load(dpms_log_f)
    return dpms_log_json


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


def merge_logs(integrity_log, sf_log):
    """
    Uses dict comprehension to create a new dict which adds the siegfried output
    at the matching file paths.
    For every file in siegfried output which is in the comprehended new dict
    relabel the siegfried output and update it to the now with siegfried output
    enriched output.
    :param integrity_log: takes the read integrity log
    :param sf_log: takes the read siegfried log (sf_log)
    :return: returns the now with siegfried output enriched integrity file.
    """
    sf_enriched_output = {}
    for f in integrity_log["files"]:
        sf_enriched_output[f["file"]["path"]] = f
    for output in open(sf_log, "r"):
        json_output = json.loads(output)
        try:
            sf_version = json_output["siegfried"]
        except KeyError:
            sf_version = "unknown"
        for f in json_output["files"]:
            if f["filename"] in sf_enriched_output:
                sf_enriched_output[f["filename"]].update(relabel_log(f, sf_version))
    # merged_logs = []
    # for f in sf_enriched_output.values():
    #     merged_logs.append(f)
    return sf_enriched_output


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