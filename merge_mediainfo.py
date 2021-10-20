import json
import logging


def add_mediainfo_info_to_db(mediainfo_log_path, session, File):
    with open(mediainfo_log_path, "r") as mediainfo_log:
        mediainfo_json = json.load(mediainfo_log)
        mediainfo_log.close()
        for f in mediainfo_json:
            session.query(File).filter(File.path == f["media"]["@ref"]).update(
                {File.mediainfo_file_info: json.dumps(f)}, synchronize_session=False)
            session.commit()


# def merge_mediainfo(f_key_list, session, File):
#     field_keys = read_key_list(f_key_list)
#     if "@type" not in field_keys:
#         field_keys.append("@type")
#     enriched_base_log = {}
#     db_files = session.query(File).all()
#     for f in db_files:
#         enriched_base_log[f.path] = {"timestamp": f.timestamp,
#                                      "file": json.loads(f.base_file_info)}
#         if f.siegfried_file_info is not None:
#             enriched_base_log[f.path].update(
#                 json.loads(f.siegfried_file_info))
#         if f.exif_file_info is not None:
#             enriched_base_log[f.path].update(
#                 {"exif": json.loads(f.exif_file_info)})
#         if f.mediainfo_file_info is not None:
#             mediainfo_file_info_dict = json.loads(f.mediainfo_file_info)
#             # print(type(mediainfo_file_info_dict))
#             enriched_base_log[f.path].update({"mediainfo": get_selected_mediainfo(field_keys, mediainfo_file_info_dict)})
#     return enriched_base_log
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
    #ensure that type is in keylist
    if "@type" not in field_keys:
        field_keys.append("@type")
    for k in field_keys:
        try:
            enriching_mediainfo["@type"] = mediainfo_entry["@type"]
            mediainfo_keys_dict[k] = mediainfo_entry[k]
            # print(mediainfo_keys_dict) das gibts nicht
            if enriching_mediainfo["@type"] == mediainfo_keys_dict["@type"]:
                enriching_mediainfo[mediainfo_keys_dict["@type"]] = mediainfo_keys_dict
                del enriching_mediainfo["@type"]
        except KeyError:
            logging.info(f"{k} is not in the mediainfo log")
    return enriching_mediainfo
