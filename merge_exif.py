from helper import replace_none_values, read_key_list, logg_keys_with_occurence
import json
import logging


def add_exif_info_to_db(exif_log_path, session, File):
    with open(exif_log_path, "r") as exif_log:
        exif_json = json.load(exif_log)
        exif_log.close()
        for f in exif_json:
            session.query(File).filter(File.path == f["SourceFile"]).update(
                {File.exif_file_info: json.dumps(f)}, synchronize_session=False)
            session.commit()


def merge_exif_to_base_log(f_key_list, occurrence_of_keys, session, File):
    enriched_base_log = {}
    field_keys = read_key_list(f_key_list)
    field_keys_in_f_log = {}
    db_files = session.query(File).all()
    for f in db_files:
        enriched_base_log[f.path] = {"timestamp": f.timestamp,
                                     "file": json.loads(f.base_file_info)}
        if f.siegfried_file_info is not None:
            enriched_base_log[f.path].update(json.loads(f.siegfried_file_info))
        if f.exif_file_info is not None:
            enriched_base_log[f.path].update(
                {"exif": json.loads(f.exif_file_info)})
    #TODO: Somehow implement the replace non values func
    #TODO: Somehow implement the key_list_func ... both probably rather in the
    # add to db then somewhere else. Well we could argue that it would be nice
    # to have it bulletproofed in the db however we dont have that for
    # siegfried either. But we could also run the functions in the iteration
    # which returns the exif info for the respective file. Would probably most
    # efficient cause then we wont need to run those functions for all those
    # files we dont want
    print(enriched_base_log)
    return enriched_base_log
    #             # start adding the fieldkeys which are in the merged dicts here
    #             if occurrence_of_keys:
    #                 sorted_field_keys_in_f_log = logg_keys_with_occurence(f, field_keys_in_f_log)
    #             enriching_exif = create_enriching_exif(f, field_keys)
    #             enriched_base_log[f[matching_key]].update(
    #                 {"exif": replace_none_values(enriching_exif)})
    # if occurrence_of_keys:
    #     for k, v in sorted_field_keys_in_f_log.items():
    #         logging.info(k, v)
    #         print(k, v)
    # return enriched_base_log


def create_enriching_exif(exif_dict, field_keys):
    enriching_exif = {}
    for key in field_keys:
        try:
            enriching_exif[key] = exif_dict[key]
        except KeyError:
            logging.info(f"{key} is not in the exif log")
    return enriching_exif
