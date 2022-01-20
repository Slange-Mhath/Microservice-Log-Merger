from helper import read_key_list, logg_keys_with_occurence
import json
import logging

log = logging.getLogger(__name__)


def add_exif_info_to_db(exif_log_path, session, File, f_key_list,
                        occurrence_of_keys):
    field_keys = read_key_list(f_key_list)
    field_keys_in_f_log = {}
    sorted_field_keys_in_f_log = {}
    exif_counter = 0
    with open(exif_log_path, "r") as exif_log:
        exif_json = json.load(exif_log)
        exif_log.close()
        for num, f in enumerate(exif_json):
            if session.query(File).filter(File.path == f["SourceFile"]).count() > 0:
                session.query(File).filter(File.path == f["SourceFile"]).update(
                    {File.exif_file_info: json.dumps(
                        create_enriching_exif(f, field_keys))},
                    synchronize_session=False)
                exif_counter += 1
            if occurrence_of_keys == "True":
                sorted_field_keys_in_f_log = logg_keys_with_occurence(f, field_keys_in_f_log)
            if num % 1000 == 0:
                session.commit()
        session.commit()
        logging.info(
            "{} exif entries uploaded into the DB".format(exif_counter))
        print("{} exif entries uploaded into the DB".format(exif_counter))
        for k, v in sorted_field_keys_in_f_log.items():
            print(f"The field {k} occurs {v} times")
            logging.info(f"The field {k} occurs {v} times")


def create_enriching_exif(exif_dict, field_keys):
    enriching_exif = {}
    for key in field_keys:
        try:
            if check_field_for_excessive_data(exif_dict[key]) is False:
                enriching_exif[key] = exif_dict[key]
            else:
                logging.warning(f"{key} contains excessive data "
                                f"and will not be saved!")
        except KeyError:
            logging.info(
                f"{key} is not in the exif file for {exif_dict['SourceFile']}")
    return enriching_exif


def check_field_for_excessive_data(field):
    return len(str(field)) > 5000
