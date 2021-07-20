from helper import replace_none_values, read_key_list, delete_keys_with_str_seq
import json


def relabel_exif_log(log, f_keys_to_del):
    """
    Relabels the Siegfried output to fit our needs. Therefore deletes
    superficial keys and replaces the 'matches' key with the siegfried version
    as head key and targets the siegfried output as dict by assuming it will
    always be at index 0 of the array 'matches'. Finally replaces the none
    values from the dict.
    :param log: takes the siegfried log as json
    :param sf_version: takes the siegfried version
    :return: returns the adjusted siegfried output
    """
    useless_keys = ["FileName", "Directory", "FileSize", "FileModifyDate",
                    "FileAccessDate", "FileInodeChangeDate", "FilePermissions",
                    "FileType",
                    "FileTypeExtension", "MIMEType"]
    keys_to_delete = read_key_list(f_keys_to_del)
    if keys_to_delete:
        useless_keys = list(set(useless_keys + keys_to_delete))
    for key in useless_keys:
        if key in log:
            del log[key]
    # In case of empty values from the SF log, apply unknown instead of nothing
    log = replace_none_values(log)
    exif_output = {"exif": log}
    if exif_output["exif"]:
        exif_output["exif"] = replace_none_values(exif_output["exif"])
        exif_output["exif"] = delete_keys_with_str_seq(exif_output["exif"], useless_keys)
    return exif_output


def merge_exif_logs(base_log, enriching_log, matching_key, f_keys_to_del):
    """
    Uses dict comprehension to create a new dict which adds the siegfried output
    at the matching file paths.
    For every file in siegfried output which is in the comprehended new dict
    relabel the siegfried output and update it to the now with siegfried output
    enriched output.
    :param integrity_log: takes the read integrity log
    :param sf_log: takes the read siegfried log (sf_log)
    :param matching_key: is the key which stores the value that maps to the
    respective file in the base_log
    :return: returns the now with siegfried output enriched integrity file.
    """
    enriched_base_log = base_log
    # uses the file_path to become the parent key of the enriched_output to have
    # a anchor point to map the log files which will enrich the enriched output.
    with open(enriching_log) as json_file:
        json_obj = json.load(json_file)
        json_file.close()
        for f in json_obj:
            if f[matching_key] in enriched_base_log:
                enriched_base_log[f[matching_key]].update(
                    relabel_exif_log(f, f_keys_to_del))
    return enriched_base_log
