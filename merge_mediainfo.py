import json
from helper import replace_none_values, read_key_list


def merge_mediainfo(base_log, mediainfo_log, f_key_list, matching_key):
    field_keys = read_key_list(f_key_list)
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
    mediainfo_dict = {}
    for entry in mediainfo_entries:
        for k in field_keys:
            if k in entry:
                # this builds the media_info_dict and ensures that the type is
                # there not sure if thats feasible maybe it will create
                # duplicates
                mediainfo_dict.update({"@type": entry["@type"], k: entry[k]})
        mediainfo_list.append(replace_none_values(mediainfo_dict))
    return mediainfo_list
