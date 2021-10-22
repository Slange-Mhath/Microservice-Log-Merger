import ijson
import logging


def load_base_log_json(log_path):
    """
    Reads the file integrity file
    :param dpms_log_path: takes the path to the file integrity file
    :return: returns the file as json
    """
    f = open(log_path, "rb")
    objects = ijson.items(f, 'files.item.file')
    files = (o for o in objects)
    base_log = {}
    for file in files:
        base_log[file["path"]] = file
    print(base_log)


def replace_none_values(log_dict):
    """
    Replaces 'None' values from a dict with 'unknown' String to make it easier
    to search for it etc.
    :param log_dict: takes the dict where the values should be replaced. (In our
    case thats the Siegfried output part)
    :return: returns the replaced dict
    """
    if isinstance(log_dict, dict):
        log_dict = {k: "unknown" if v is None or not str(v) else v for k, v in
                    log_dict.items()}
    return log_dict


def write_merged_f_log(merged_log, dest_file):
    """
    Writes the merged and enriched integrity file to a specified output file.
    :param merged_log: takes the merged and enriched file
    :param dest_file: takes the output file
    """
    output = open(dest_file, "w", encoding="utf-8")
    for f in merged_log.values():
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
