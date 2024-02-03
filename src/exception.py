import sys
import logging

def error_message_detail(error, error_detail_info=None):
    exc_info = sys.exc_info() if error_detail_info is None else error_detail_info
    _, _, exc_tb = exc_info
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = f"Error occurred in python script name [{file_name}] line number [{exc_tb.tb_lineno}] error message [{error}]"
    return error_message

class CustomException(Exception):
    def __init__(self, error_message, error_detail_info=None):
        super().__init__(error_message)
        self.error_message_detail = error_message_detail(error_message, error_detail_info=error_detail_info)

    def __str__(self):
        return self.error_message_detail

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Logging has started")

    try:
        a = 1 / 0
    except Exception as e:
        logging.exception('Division by zero')
        raise CustomException("Data ingestion failed", error_detail_info=sys.exc_info())
