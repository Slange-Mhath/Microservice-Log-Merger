from helper import replace_none_values
import json


def relabel_exif_log(log, custom_useless_keys):
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
    if custom_useless_keys:
        useless_keys = list(set(useless_keys + custom_useless_keys))
    for key in useless_keys:
        if key in log:
            del log[key]
    # In case of empty values from the SF log, apply unknown instead of nothing
    log = replace_none_values(log)
    exif_output = {"exif": log}
    if exif_output["exif"]:
        exif_output["exif"] = replace_none_values(exif_output["exif"])
    return exif_output


def merge_logs(base_log, enriching_log, matching_key):
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
    enriched_base_log = {}
    # uses the file_path to become the parent key of the enriched_output to have
    # a anchor point to map the log files which will enrich the enriched output.
    for f in base_log["files"]:
        enriched_base_log[f["file"]["path"]] = f
    for enriching_output in open(enriching_log, "r"):
        enriching_json = json.loads(enriching_output)
        try:
            sf_version = enriching_json["siegfried"]
        except KeyError:
            sf_version = "unknown"
        for f in enriching_json["files"]:
            # TODO: This is iterating over every file in the siegfried_output however, we cant be sure that every output is structured like that and it is unlikely that every output has a "file" key to iterate over
            if f[matching_key] in enriched_base_log:
                # TODO: filename in siegfried output is the path which should match to the key created in l.42-43. However not every output might call that filename maybe this has to be a variable given as parameter. Like matching_achnor or file_name if its everytime the filename which matches.
                # TODO: relabel shouldn't be called here but before the merge_logs file probably to modify the enriching log independent
                enriched_base_log[f[matching_key]].update(relabel_siegfried_log(f, sf_version)) # TODO: Update ... mit dem gelabelten enriching_output.
    return enriched_base_log