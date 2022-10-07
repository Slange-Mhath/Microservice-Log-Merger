import json
import logging


def add_jpylyzer_info_to_db(jp_f_log_path, session, File):
    with open(jp_f_log_path, "r") as jp_log:
        jp_json = json.load(jp_log)
        jp_counter = 0
        # Here needs to go an exception if jp_json has no jpylyzer and then no file key
        for num, jp_f in enumerate(jp_json['jpylyzer']):
            if session.query(File).filter(File.path == jp_f['file']['fileInfo']['filePath']).count() > 0:
                jp_counter += 1
                session.query(File).filter(File.path == jp_f['file']['fileInfo']['filePath']).update(
                    {File.jpylyzer_file_info: json.dumps(
                        relabel_jpylyzer_log(jp_f))},
                    synchronize_session=False)
                if num % 1000 == 0:
                    session.commit()
    session.commit()
    logging.info(" {} Jpylyzer entries uploaded to DB".format(jp_counter))
    print(" {} Jpylyzer entries uploaded to DB".format(jp_counter))


def relabel_jpylyzer_log(jp_f):
    relabled_log = jp_f
    try:
        relabled_log['is_valid'] = jp_f['file']['isValid']
    except KeyError:
        logging.warning(f" {jp_f['file']['fileInfo']['filePath']} has no Key 'isValid'")
    try:
        relabled_log['tool_info'] = jp_f['toolInfo']
    except KeyError:
        logging.warning(f" {jp_f['fileInfo']['filePath']} has no Key toolInfo")
    if jp_f['file']['properties']:
        if 'contiguousCodestreamBox' in jp_f['file']['properties']:
            if 'contiguousCodestreamBox' in jp_f['file']['properties']['contiguousCodestreamBox']:
                if 'contiguousCodestreamBox' in jp_f['file']['properties']['contiguousCodestreamBox']['com']:
                    try:
                        relabled_log['file']['properties']['contiguousCodestreamBox']['com']['lcom'] = \
                        jp_f['file']['properties']['contiguousCodestreamBox']['com']['lcom']
                        relabled_log['file']['properties']['contiguousCodestreamBox']['com']['rcom'] = \
                        jp_f['file']['properties']['contiguousCodestreamBox']['com']['rcom']
                        relabled_log['file']['properties']['contiguousCodestreamBox']['com']['comment'] = \
                        jp_f['file']['properties']['contiguousCodestreamBox']['com']['comment']
                    except KeyError:
                        logging.warning(f" {jp_f['file']['fileInfo']['filePath']} has no Key 'com'")
                if 'contiguousCodestreamBox' in jp_f['file']['properties']['contiguousCodestreamBox']['cod']:
                    try:
                        relabled_log['file']['properties']['contiguousCodestreamBox']['cod']['order'] = jp_f['file']['properties']['contiguousCodestreamBox']['cod']['order']
                        relabled_log['file']['properties']['contiguousCodestreamBox']['cod']['sop'] = jp_f['file']['properties']['contiguousCodestreamBox']['cod']['sop']
                        relabled_log['file']['properties']['contiguousCodestreamBox']['cod']['eph'] = jp_f['file']['properties']['contiguousCodestreamBox']['cod']['eph']
                        relabled_log['file']['properties']['contiguousCodestreamBox']['cod']['codeBlockWidth'] = jp_f['file']['properties']['contiguousCodestreamBox']['cod']['codeBlockWidth']
                        relabled_log['file']['properties']['contiguousCodestreamBox']['cod']['codeBlockHeight'] = jp_f['file']['properties']['contiguousCodestreamBox']['cod']['codeBlockHeight']
                        relabled_log['file']['properties']['contiguousCodestreamBox']['cod']['transformation'] = jp_f['file']['properties']['contiguousCodestreamBox']['cod']['transformation']
                        relabled_log['file']['properties']['contiguousCodestreamBox']['cod']['layers'] = jp_f['file']['properties']['contiguousCodestreamBox']['cod']['layers']
                        relabled_log['file']['properties']['contiguousCodestreamBox']['cod']['levels'] = jp_f['file']['properties']['contiguousCodestreamBox']['cod']['levels']
                    except KeyError:
                        logging.warning(f" {jp_f['file']['fileInfo']['filePath']} has no Key 'cod'")