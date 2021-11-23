import json
import logging
from helper import read_key_list

log = logging.getLogger(__name__)


def replace_none_values(log_dict):
    """
    Replaces 'None' values from a dict with 'unknown' String to make it easier
    to search for it etc.
    :param log_dict: takes the dict where the values should be replaced. (In our
    case thats the Siegfried output part)
    :return: returns the replaced dict
    """
    if isinstance(log_dict, dict):
        log_dict = {k: "unknown" if v is None or not str(v) else v for k, v in
                    log_dict.items()}
    return log_dict


def add_mediainfo_info_to_db(f_key_list, mediainfo_log_path, session, File):
    field_keys = read_key_list(f_key_list)
    with open(mediainfo_log_path, "r") as mediainfo_log:
        for line in mediainfo_log:
            mediainfo_json = json.loads(line)
            for num, f in enumerate(mediainfo_json):
                session.query(File).filter(File.path == f["media"]["@ref"]).update(
                    {File.mediainfo_file_info: get_selected_mediainfo(field_keys,
                                                                      f)},
                    synchronize_session=False)
                if num % 1000 == 0:
                    session.commit()
            session.commit()


def get_selected_mediainfo(field_keys, raw_mediainfo):
    mediainfo_entries = raw_mediainfo["media"]["track"]
    selected_mediainfo_entry = {}
    for entry in mediainfo_entries:
        selected_mediainfo_entry.update(create_selected_mediainfo_entry(field_keys,
                                                                   entry))

    return json.dumps(selected_mediainfo_entry)


def create_selected_mediainfo_entry(field_keys, entry):
    selected_mediainfo_entry = {}
    mediainfo_keys_dict = {}
    # if mediainfo is added "@type" is a mandatory field so it needs to be added
    if "@type" not in field_keys:
        field_keys.append("@type")
    for k in field_keys:
        try:
            selected_mediainfo_entry["@type"] = entry["@type"]
            mediainfo_keys_dict[k] = entry[k]
            if selected_mediainfo_entry["@type"] == mediainfo_keys_dict[
                "@type"]:
                selected_mediainfo_entry[
                    mediainfo_keys_dict["@type"]] = mediainfo_keys_dict
                del selected_mediainfo_entry["@type"]
        except KeyError:
            logging.info(f"{k} is not in the mediainfo log")
    return selected_mediainfo_entry
