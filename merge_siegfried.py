import logging
from helper import replace_none_values
import json


def relabel_siegfried_log(log, sf_version):
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
    del log["errors"]
    del log["filename"]
    del log["filesize"]
    del log["modified"]
    try:
        log["matches"][0]["siegfried_version"] = sf_version
    except IndexError:
        logging.warning("Siegfried didn't return any output")
    # In case of empty values from the SF log, apply unknown instead of nothing
    log = replace_none_values(log)
    sf_output = {"siegfried": log["matches"][0]}
    if sf_output["siegfried"]:
        sf_output["siegfried"] = replace_none_values(sf_output["siegfried"])
    return sf_output


def merge_sf_logs(base_log, enriching_log, matching_key):
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
            if f[matching_key] in enriched_base_log:
                enriched_base_log[f[matching_key]].update(
                    relabel_siegfried_log(f, sf_version))
    return enriched_base_log
