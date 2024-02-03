import os
from datetime import datetime
from logger import logging
from exception import CustomException
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

@dataclass
class DataIngestionconfig:
    train_filename = 'train.csv'
    test_filename = 'test.csv'
    raw_filename = 'raw.csv'
    artifacts_dir = 'artifacts'

    raw_data_path = os.path.join(artifacts_dir, raw_filename)
    train_data_path = os.path.join(artifacts_dir, train_filename)
    test_data_path = os.path.join(artifacts_dir, test_filename)

    raw_data_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

class CustomException(Exception):
    def __init__(self, error_detail):
        self.error_detail = error_detail
        super().__init__(f"CustomException: {error_detail}")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionconfig()

    def initiate_data_ingestion(self):
        logging.info('Data Ingestion method starts')

        try:
            df = pd.read_csv(os.path.join('notebook', 'data', 'gemstone.csv'))

            logging.info('Dataset read as pandas Dataframe')

            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)

            # Append timestamp to raw data file
            raw_data_path_with_timestamp = f"{self.ingestion_config.raw_data_path}_{self.ingestion_config.raw_data_timestamp}.csv"
            df.to_csv(raw_data_path_with_timestamp, index=False)

            logging.info("Train test split")
            train_set, test_set = train_test_split(df, test_size=0.30, random_state=42)

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)
            os.makedirs(os.path.dirname(self.ingestion_config.test_data_path), exist_ok=True)

            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info('Ingestion of data is completed')

            return self.ingestion_config.train_data_path, self.ingestion_config.test_data_path

        except Exception as e:
            error_detail = f'Error occurred in Data Ingestion: {str(e)}'
            logging.error(error_detail)
            raise CustomException(error_detail)

# Example usage outside DataIngestion class
try:
    data_ingestion = DataIngestion()
    train_data_path, test_data_path = data_ingestion.initiate_data_ingestion()
    # Continue with the rest of your training pipeline
except CustomException as ce:
    logging.error(f'CustomException: {ce.error_detail}')
except Exception as e:
    logging.error(f'Unexpected error: {str(e)}')


