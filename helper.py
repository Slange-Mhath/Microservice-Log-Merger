import json
from merge_mediainfo import get_selected_mediainfo


def add_ora_info_to_db(ora_log, session, File):
    for num, f in enumerate(ora_log["files"]):
        file = File()
        file.path = f["file"]["path"]
        file.timestamp = f["timestamp"]
        file.base_file_info = json.dumps(f["file"])
        session.add(file)

        if num % 1000 == 0:
            session.commit()

    session.commit()


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


def write_merged_f_log(session, File, output_file, f_key_list):
    field_keys = read_key_list(f_key_list)
    merged_output = {}
    db_files = session.query(File).all()
    for f in db_files:
        merged_output[f.path] = {"timestamp": f.timestamp,
                                 "file": json.loads(f.base_file_info), }
        if f.siegfried_file_info is not None:
            merged_output[f.path].update(json.loads(f.siegfried_file_info))
        if f.exif_file_info is not None:
            merged_output[f.path].update(
                {"exif": json.loads(f.exif_file_info)})
        if f.mediainfo_file_info is not None:
            mediainfo_file_info_dict = json.loads(f.mediainfo_file_info)
            merged_output[f.path].update({
                "mediainfo": get_selected_mediainfo(
                    field_keys,
                    mediainfo_file_info_dict)})
    output = open(output_file, "w", encoding="utf-8")
    for f in merged_output.values():
        json.dump(f, output, sort_keys=True, ensure_ascii=True)
        output.write("\n")


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


def delete_keys_with_str_seq(log_dict, list_of_keys):
    """
    :param log_dict: takes a dict with the superficial keys
    :param list_of_keys: takes a list of keys
    :return: cleaned log_dict from the keys that matches the seq with*
    """
    if list_of_keys:
        # This creates a list of wildcards from the list of keys
        # This could possibly be an extra function
        list_of_str_seq = [k for k in list_of_keys if k.endswith("*")]
        # filters every key which ends of * and saves it to a list of str seqs
        if list_of_str_seq:
            for str_seq in list_of_str_seq:
                for key in list(log_dict.keys()):
                    if key.startswith(str_seq[:-1]):
                        # this checks if the key in the log starts with the wildcard
                        # sequence while ignoring the *
                        key_to_delete = key
                        del log_dict[key_to_delete]
        return log_dict


def logg_keys_with_occurence(f_log, field_keys_in_f_log):
    """
    :param f_log: log of a file as dict
    :param field_keys_in_f_log: a dict to store the keys with their occurrence
    :return:
    """
    for key in f_log.keys():
        if key not in field_keys_in_f_log:
            field_keys_in_f_log[key] = 1
        else:
            field_keys_in_f_log[key] += 1
    sorted_field_keys_in_f_log = {k: v for k, v in
                                  sorted(field_keys_in_f_log.items(),
                                         key=lambda item: item[1])}
    return sorted_field_keys_in_f_log
