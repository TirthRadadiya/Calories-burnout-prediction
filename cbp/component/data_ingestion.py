import os
from cbp.config.configuration import Configuration

class DataIngestion:
    def __init__(self):
        self.dataset_download_url = dataset_download_url
        self.raw_data_dir = "raw_data"
        self.ingested_dir = "ingested_data"
        self.ingested_train_dir = "train"
        self.ingested_test_dir = "test"

    def initiate_data_ingestion(self):
        dataset_download_url = "https://raw.githubusercontent.com/ageron/handson-ml/master/datasets/housing/housing.tgz"
        tgz_download_dir = "cbp/artifact"
        