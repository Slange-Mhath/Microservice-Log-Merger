import json
from helper import replace_none_values
from pprint import pprint


def create_mediainfo(mediainfo_dict):
    mediainfo = {"mediainfo": mediainfo_dict}
    mediainfo = replace_none_values(mediainfo)
    return mediainfo


def merge_mediainfo(base_log, mediainfo_log, matching_key):
    enriched_base_log = base_log
    with open(mediainfo_log) as json_file:
        json_obj = json.load(json_file)
        json_file.close()
        for f in json_obj:
            if f["media"][matching_key] in base_log:
                enriched_base_log[f["media"][matching_key]].update(create_mediainfo(f))
    return enriched_base_log