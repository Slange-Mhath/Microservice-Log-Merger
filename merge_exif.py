from helper import replace_none_values, read_key_list, logg_keys_with_occurence
import json
import logging
from pprint import pprint


# def x_merge_exif_to_base_log(exif_log, base_log, f_key_list, matching_key):
#     field_keys = read_key_list(f_key_list)
#     enriching_exif_log = {}
#     enriched_base_log = base_log
#     with open(exif_log) as json_file:
#         json_obj = json.load(json_file)
#         json_file.close()
#         for f in json_obj:
#             if f[matching_key] in base_log:
#                 for k in field_keys:
#                     if k in f:
#                         enriching_exif_log[k] = f[k]
#                         enriched_base_log[f[matching_key]].update(
#                             {"exif": replace_none_values(enriching_exif_log)})
#     return enriched_base_log


def merge_exif_to_base_log(occurrence_of_keys, exif_log, base_log, f_key_list, matching_key):
    field_keys = read_key_list(f_key_list)
    enriched_base_log = base_log
    field_keys_in_f_log = {}
    with open(exif_log) as json_file:
        json_obj = json.load(json_file)
        json_file.close()
        for f in json_obj:
            if f[matching_key] in base_log:
                # start adding the fieldkeys which are in the merged dicts here
                if occurrence_of_keys:
                    logg_keys_with_occurence(f, field_keys_in_f_log)
                enriching_exif = create_enriching_exif(f, field_keys)
                enriched_base_log[f[matching_key]].update(
                    {"exif": replace_none_values(enriching_exif)})
    return enriched_base_log


def create_enriching_exif(exif_dict, field_keys):
    enriching_exif = {}
    for key in field_keys:
        try:
            enriching_exif[key] = exif_dict[key]
        except KeyError:
            logging.info(f"{key} is not in the exif log")
    return enriching_exif
