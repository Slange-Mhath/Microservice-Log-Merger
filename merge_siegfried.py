import logging
from merge_mediainfo import replace_none_values
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


def add_sf_info_to_db(sf_log_path, session, File):
    with open(sf_log_path, "r") as sf_log:
        for line in sf_log:
            sf_file_json = json.loads(line)
            try:
                sf_version = sf_file_json["siegfried"]
            except KeyError:
                sf_version = "unknown"
            for f in sf_file_json['files']:
                session.query(File).filter(File.path == f["filename"]).update(
                    {File.siegfried_file_info: json.dumps(relabel_siegfried_log(f, sf_version))},
                    synchronize_session=False)
                session.commit()
