import json
import logging


def add_pdf_info_to_db(pdf_analyser_log_path, session, File):
    with open(pdf_analyser_log_path, "r") as pdf_analyser_log:
        pdf_counter = 0
        pdf_log_json = json.load(pdf_analyser_log)
        pdf_analyser_log.close()
        for num, pdf in enumerate(pdf_log_json.items()):
            if session.query(File).filter(
                    File.path == pdf[0]).count() > 0:
                session.query(File).filter(File.path == pdf[0]).update({File.pdf_info: json.dumps(
                           pdf[1])},
                        synchronize_session=False)
                pdf_counter += 1
                if num % 1000 == 0:
                    session.commit()
        session.commit()
        logging.info(
            "{} pdf info uploaded into the DB".format(pdf_counter))
        print("{} pdf info uploaded into the DB".format(pdf_counter))

