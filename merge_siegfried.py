import logging
from helper import replace_none_values
import ijson


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


def merge_sf_logs(base_log, enriching_log):
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
    sf_version = None
    f = open(enriching_log, "rb")
    objects = ijson.items(f, 'siegfried')
    sf_log_head = (o for o in objects)
    for sf_v in sf_log_head:
        sf_version = sf_v
    f = open(enriching_log, "rb")
    objects = ijson.items(f, 'files.item')
    sf_files = (o for o in objects if o['filename'] in base_log)
    for sf_file in sf_files:
        sf_file['matches'][0]["siegfried_version"] = sf_version
        base_log[sf_file['filename']]['siegfried'] = sf_file['matches'][0]
    return base_log
