import json
import logging

log = logging.getLogger(__name__)


def add_ora_info_to_db(ora_log, session, File):
    base_file_counter = 0
    for num, f in enumerate(ora_log["files"]):
        file = File()
        if session.query(File).filter(File.path == f["file"]["path"]).first():
            logging.warning("{} is already in the DB".format(f["file"]["path"]))
            continue
        else:
            file.path = f["file"]["path"]
            file.timestamp = f["timestamp"]
            file.base_file_info = json.dumps(f["file"])
            session.add(file)
            if num % 1000 == 0:
                session.commit()
            base_file_counter += 1

    session.commit()
    logging.info(
        "{} base_file entries uploaded to DB".format(base_file_counter))
    print("{} base_file entries uploaded to DB".format(base_file_counter))


def load_json(log_path):
    """
    Reads the file integrity file
    :param dpms_log_path: takes the path to the file integrity file
    :return: returns the file as json
    """
    with open(log_path, "r") as log:
        log_json = json.load(log)
        log.close()
    return log_json


def write_merged_f_log(session, File, output_file):
    db_files = session.query(File).all()
    for f in db_files:
        merged_output = {f.path: {"timestamp": f.timestamp,
                                  "file": json.loads(f.base_file_info), }}
        if f.siegfried_file_info is not None:
            merged_output[f.path].update(json.loads(f.siegfried_file_info))
        if f.pdf_info is not None:
            merged_output[f.path].update({
                "pdf_info": json.loads(f.pdf_info)})
        if f.exif_file_info is not None:
            merged_output[f.path].update(
                {"exif": json.loads(f.exif_file_info)})
        if f.mediainfo_file_info is not None:
            merged_output[f.path].update({
                "mediainfo": json.loads(f.mediainfo_file_info)})

        with open(output_file, "a", encoding="utf-8") as open_f:
            for file_info in merged_output.values():
                open_f.write(json.dumps(file_info, sort_keys=True, ensure_ascii=True) + '\n')


def read_key_list(key_list_f):
    """
    :param key_list_f: text file with keys per line
    :return: list with keys
    """
    if key_list_f:
        with open(key_list_f) as f:
            keys = f.read().splitlines()
            f.close()
        return keys


# def logg_keys_with_occurence(f_log, field_keys_in_f_log):
#     """
#     :param f_log: log of a file as dict
#     :param field_keys_in_f_log: a dict to store the keys with their occurrence
#     :return:
#     """
#     for key in f_log.keys():
#         if key not in field_keys_in_f_log:
#             field_keys_in_f_log[key] = 1
#             print(field_keys_in_f_log)
#         else:
#             field_keys_in_f_log[key] += 1
#     sorted_field_keys_in_f_log = {k: v for k, v in
#                                   sorted(field_keys_in_f_log.items(),
#                                          key=lambda item: item[1])}
#     return sorted_field_keys_in_f_log

def logg_keys_with_occurence(f, field_keys_in_f):
    for key in f.keys():
        if key not in field_keys_in_f:
            field_keys_in_f[key] = 1
        else:
            field_keys_in_f[key] += 1
    return field_keys_in_f
