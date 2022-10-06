import json
import logging


def add_jpylyzer_info_to_db(jp_f_log_path, session, File):
    with open(jp_f_log_path, "r") as jp_log:
        jp_json = json.load(jp_log)
        tool_info = jp_json['jpylyzer']['toolInfo']
        jp_counter = 0
        # Here needs to go an exception if jp_json has no jpylyzer and then no file key
        for num, jp_f in enumerate(jp_json['jpylyzer']['file']):
            relabel_jpylyzer_log(jp_f, tool_info)
            if session.query(File).filter(File.path == jp_f['fileInfo']['filePath']).count() > 0:
                jp_counter += 1
                session.query(File).filter(File.path == jp_f['fileInfo']['filePath']).update(
                    {File.jpylyzer_file_info: json.dumps(
                        relabel_jpylyzer_log(jp_f, tool_info))},
                    synchronize_session=False)
                if num % 1000 == 0:
                    session.commit()
    session.commit()
    logging.info(" {} Jpylyzer entries uploaded to DB".format(jp_counter))
    print(" {} Jpylyzer entries uploaded to DB".format(jp_counter))


def relabel_jpylyzer_log(jp_f, tool_info):
    relabled_log = jp_f
    try:
        relabled_log['is_valid'] = jp_f['isValid']
        relabled_log['tool_info'] = tool_info
    except KeyError:
        logging.warning(f" {jp_f['fileInfo']['filePath']} has no Key 'isValid'")
    if jp_f['properties']:
        if 'contiguousCodestreamBox' in jp_f['properties']:
            if 'contiguousCodestreamBox' in jp_f['properties']['contiguousCodestreamBox']:
                if 'contiguousCodestreamBox' in jp_f['properties']['contiguousCodestreamBox']['com']:
                    try:
                        relabled_log['properties']['contiguousCodestreamBox']['com']['lcom'] = \
                        jp_f['properties']['contiguousCodestreamBox']['com']['lcom']
                        relabled_log['properties']['contiguousCodestreamBox']['com']['rcom'] = \
                        jp_f['properties']['contiguousCodestreamBox']['com']['rcom']
                        relabled_log['properties']['contiguousCodestreamBox']['com']['comment'] = \
                        jp_f['properties']['contiguousCodestreamBox']['com']['comment']
                    except KeyError:
                        logging.warning(f" {jp_f['fileInfo']['filePath']} has no Key 'com'")
                if 'contiguousCodestreamBox' in jp_f['properties']['contiguousCodestreamBox']['cod']:
                    try:
                        relabled_log['properties']['contiguousCodestreamBox']['cod']['order'] = jp_f['properties']['contiguousCodestreamBox']['cod']['order']
                        relabled_log['properties']['contiguousCodestreamBox']['cod']['sop'] = jp_f['properties']['contiguousCodestreamBox']['cod']['sop']
                        relabled_log['properties']['contiguousCodestreamBox']['cod']['eph'] = jp_f['properties']['contiguousCodestreamBox']['cod']['eph']
                        relabled_log['properties']['contiguousCodestreamBox']['cod']['codeBlockWidth'] = jp_f['properties']['contiguousCodestreamBox']['cod']['codeBlockWidth']
                        relabled_log['properties']['contiguousCodestreamBox']['cod']['codeBlockHeight'] = jp_f['properties']['contiguousCodestreamBox']['cod']['codeBlockHeight']
                        relabled_log['properties']['contiguousCodestreamBox']['cod']['transformation'] = jp_f['properties']['contiguousCodestreamBox']['cod']['transformation']
                        relabled_log['properties']['contiguousCodestreamBox']['cod']['layers'] = jp_f['properties']['contiguousCodestreamBox']['cod']['layers']
                        relabled_log['properties']['contiguousCodestreamBox']['cod']['levels'] = jp_f['properties']['contiguousCodestreamBox']['cod']['levels']
                    except KeyError:
                        logging.warning(f" {jp_f['fileInfo']['filePath']} has no Key 'cod'")