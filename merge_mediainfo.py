import json
from helper import replace_none_values, read_key_list
import logging


def add_mediainfo_info_to_db(mediainfo_log_path, session, File):
    with open(mediainfo_log_path, "r") as mediainfo_log:
        mediainfo_json = json.load(mediainfo_log)
        mediainfo_log.close()
        for f in mediainfo_json:
            session.query(File).filter(File.path == f["media"]["@ref"]).update(
                {File.mediainfo_file_info: json.dumps(f)}, synchronize_session=False)
            session.commit()


def merge_mediainfo(base_log, mediainfo_log, f_key_list, matching_key):
    field_keys = read_key_list(f_key_list)
    if "@type" not in field_keys:
        field_keys.append("@type")
    enriched_base_log = base_log
    with open(mediainfo_log) as json_file:
        json_obj = json.load(json_file)
        json_file.close()
        for f in json_obj:
            if f["media"][matching_key] in base_log:
                enriched_base_log[f["media"][matching_key]].update(
                    {"mediainfo": get_selected_mediainfo(field_keys, f)})
    return enriched_base_log


def get_selected_mediainfo(field_keys, raw_mediainfo):
    mediainfo_entries = raw_mediainfo["media"]["track"]
    mediainfo_list = []
    for entry in mediainfo_entries:
        mediainfo_dict = create_enriching_mediainfo(field_keys, entry)
        mediainfo_list.append(replace_none_values(mediainfo_dict))
    return mediainfo_list


def create_enriching_mediainfo(field_keys, mediainfo_entry):
    enriching_mediainfo = {}
    mediainfo_keys_dict = {}
    for k in field_keys:
        try:
            enriching_mediainfo["@type"] = mediainfo_entry["@type"]
            mediainfo_keys_dict[k] = mediainfo_entry[k]
            if enriching_mediainfo["@type"] == mediainfo_keys_dict["@type"]:
                enriching_mediainfo[mediainfo_keys_dict["@type"]] = mediainfo_keys_dict
                del enriching_mediainfo["@type"]
        except KeyError:
            logging.info(f"{k} is not in the mediainfo log")
    return enriching_mediainfo
