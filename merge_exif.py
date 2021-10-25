from helper import replace_none_values, read_key_list, logg_keys_with_occurence
import ijson
import logging


def merge_exif_to_base_log(exif_log, base_log, f_key_list, occurrence_of_keys, matching_key):
    field_keys = read_key_list(f_key_list)
    enriched_base_log = base_log
    f = open(exif_log, "rb")
    objects = ijson.items(f, 'item')
    files = (o for o in objects if o["SourceFile"] in base_log)
    for file in files:
        enriched_base_log[file["SourceFile"]]["exif"] = create_enriching_exif(file, field_keys)
    return enriched_base_log


def create_enriching_exif(exif_dict, field_keys):
    enriching_exif = {}
    for key in field_keys:
        try:
            enriching_exif[key] = exif_dict[key]
        except KeyError:
            logging.info(f"{key} is not in the exif log")
    return enriching_exif
