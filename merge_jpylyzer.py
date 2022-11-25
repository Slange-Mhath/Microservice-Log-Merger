import json
import logging


def add_jpylyzer_info_to_db(jp_f_log_path, session, File):
    jp_counter = 0
    with open(jp_f_log_path, "r") as jp_log:
        lines = jp_log.readlines()
        for num, line in enumerate(lines):
            jp_f = json.loads(line)
            if session.query(File).filter(File.path == jp_f['file']['fileInfo'][
                'filePath']).count() > 0:
                jp_counter += 1
                session.query(File).filter(
                    File.path == jp_f['file']['fileInfo']['filePath']).update(
                    {File.jpylyzer_file_info: json.dumps(
                        relabel_jpylyzer_log(jp_f['file']))},
                    synchronize_session=False)
                if num % 1000 == 0:
                    session.commit()
    session.commit()
    logging.info(" {} Jpylyzer entries uploaded to DB".format(jp_counter))
    print(" {} Jpylyzer entries uploaded to DB".format(jp_counter))


def relabel_jpylyzer_log(jp_f):
    relabled_log = {}
    try:
        relabled_log['is_valid'] = jp_f['isValid']
    except KeyError:
        logging.warning(
            f" {jp_f['fileInfo']['filePath']} has no Key 'isValid'")
    try:
        relabled_log['tool_info'] = jp_f['toolInfo']
    except KeyError:
        logging.warning(f" {jp_f['fileInfo']['filePath']} has no Key toolInfo")
    if jp_f['properties']:
        if 'contiguousCodestreamBox' in jp_f['properties']:
            if 'com' in jp_f['properties']['contiguousCodestreamBox']:
                try:
                    relabled_log['properties'] = {"contiguousCodestreamBox": {
                        "com": jp_f['properties'][
                            'contiguousCodestreamBox']['com']}}
                except KeyError:
                    logging.warning(
                        f" {jp_f['fileInfo']['filePath']} has no Key 'com'")
            if 'cod' in jp_f['properties']['contiguousCodestreamBox']:
                try:
                    relabled_log['properties']["contiguousCodestreamBox"][
                        'cod'] = {"order": jp_f['properties'][
                        'contiguousCodestreamBox']['cod']['order']}
                    relabled_log['properties'][
                        "contiguousCodestreamBox"]['cod']['sop'] = \
                    jp_f['properties']['contiguousCodestreamBox'][
                        'cod']['sop']
                    relabled_log['properties'][
                        "contiguousCodestreamBox"]["cod"]["eph"] = jp_f['properties']['contiguousCodestreamBox']['cod']['eph']
                    relabled_log['properties']["contiguousCodestreamBox"]["cod"]["codeBlockWidth"] = jp_f['properties']['contiguousCodestreamBox']['cod']['codeBlockWidth']
                    relabled_log['properties']["contiguousCodestreamBox"]["cod"]["codeBlockHeight"] = jp_f['properties']['contiguousCodestreamBox']['cod']['codeBlockHeight']
                    relabled_log['properties']["contiguousCodestreamBox"]["cod"]["transformation"] = jp_f['properties']['contiguousCodestreamBox']['cod']['transformation']
                    relabled_log['properties']["contiguousCodestreamBox"]["cod"]["layers"] = jp_f['properties']['contiguousCodestreamBox']['cod']['layers']
                    relabled_log['properties']["contiguousCodestreamBox"]["cod"]["levels"] = jp_f['properties']['contiguousCodestreamBox']['cod']['levels']
                except KeyError:
                    logging.warning(
                        f" {jp_f['fileInfo']['filePath']} required Key is not in log")
    return relabled_log
