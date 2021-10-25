from helper import read_key_list, logg_keys_with_occurence
import json
import logging


def add_exif_info_to_db(exif_log_path, session, File, f_key_list, occurrence_of_keys):
    field_keys = read_key_list(f_key_list)
    field_keys_in_f_log = {}
    with open(exif_log_path, "r") as exif_log:
        exif_json = json.load(exif_log)
        exif_log.close()
        for f in exif_json:
            if occurrence_of_keys:
                sorted_field_keys_in_f_log = logg_keys_with_occurence(f,
                                                                      field_keys_in_f_log)
                for k, v in sorted_field_keys_in_f_log.items():
                    logging.info(k, v)
                    print(k, v)
            session.query(File).filter(File.path == f["SourceFile"]).update(
                {File.exif_file_info: json.dumps(create_enriching_exif(f, field_keys))}, synchronize_session=False)
            session.commit()


def create_enriching_exif(exif_dict, field_keys):
    enriching_exif = {}
    for key in field_keys:
        try:
            enriching_exif[key] = exif_dict[key]
        except KeyError:
            logging.info(f"{key} is not in the exif log")
    return enriching_exif
