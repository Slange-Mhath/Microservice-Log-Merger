from helper import read_key_list, logg_keys_with_occurence
from merge_mediainfo import replace_none_values
import json
import logging


def add_exif_info_to_db(exif_log_path, session, File, f_key_list, occurrence_of_keys):
    field_keys = read_key_list(f_key_list)
    field_keys_in_f_log = {}
    with open(exif_log_path, "r") as exif_log:
        exif_json = json.load(exif_log)
        exif_log.close()
        for f in exif_json:
            print("first for loop per file in exif")
            # TODO: Here seems to be an error cause thats not how we expect the log to work
            # Proofed: this runs per file in exif_json. Means we get the k,v stats per file which can be endlessly long.
            if occurrence_of_keys:
                sorted_field_keys_in_f_log = logg_keys_with_occurence(f,
                                                                      field_keys_in_f_log)
                for k, v in sorted_field_keys_in_f_log.items():
                    logging.info(k, v)
                    print("second for loop per key value in exif")
                    print(k, v)
            session.query(File).filter(File.path == f["SourceFile"]).update(
                {File.exif_file_info: json.dumps(create_enriching_exif(f, field_keys))}, synchronize_session=False)
            session.commit()


# # TODO: This is the desperate try to implement the replace non values func which is a big problem cause it causes errors with the try and error and I dont get why
# def slim_exif(session, File):
#     db_files = session.query(File).all()
#     for f in db_files:
#         exif = {"exif": f.exif_file_info}
#         print(exif)


# def merge_exif_to_base_log(session, File):
#     enriched_base_log = {}
#     db_files = session.query(File).all()
#     for f in db_files:
#         enriched_base_log[f.path] = {"timestamp": f.timestamp,
#                                      "file": json.loads(f.base_file_info)}
#         if f.siegfried_file_info is not None:
#             enriched_base_log[f.path].update(json.loads(f.siegfried_file_info))
#         if f.exif_file_info is not None:
#             enriched_base_log[f.path].update(
#                 {"exif": json.loads(f.exif_file_info)})
#     #TODO: Somehow implement the replace non values func
#     #TODO: Somehow implement the key_list_func ... both probably rather in the
#     # add to db then somewhere else. Well we could argue that it would be nice
#     # to have it bulletproofed in the db however we dont have that for
#     # siegfried either. But we could also run the functions in the iteration
#     # which returns the exif info for the respective file. Would probably most
#     # efficient cause then we wont need to run those functions for all those
#     # files we dont want.
#     # On the other hand if we wont store it in the db in the format we desire
#     # we cant call that like we call the siegfried file info here or we would
#     # have to run that again and again as soon as we want to have exif in
#     # another merged log e.g. if we start with mediainfo
#     return enriched_base_log


def create_enriching_exif(exif_dict, field_keys):
    enriching_exif = {}
    for key in field_keys:
        try:
            enriching_exif[key] = exif_dict[key]
        except KeyError:
            logging.info(f"{key} is not in the exif log")
    return enriching_exif
