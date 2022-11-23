from cbp.entity.config_entity import DataIngestionConfig
import os
from cbp.exception import HousingException
from cbp.logger import logging
import sys

class Configuration():

    def __init__(self):
        self.artifact_dir = "/cbp/artifact"
        self.time_stamp = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"

    def get_data_ingestion_config(self):
        try:
            data_ingestion_dir = os.path.join(self.artifact_dir,self.time_stamp,"/data_ingestion")
            tgz_download_dir = os.path.join(data_ingestion_dir,"/tgz_file")
            raw_data_dir = os.path.join(data_ingestion_dir,"/raw_data")
            ingested_data_dir = os.path.join(data_ingestion_dir,"/ingested_data")
            ingested_train_dir = os.path.join(ingested_data_dir,"/train")
            ingested_test_dir = os.path.join(ingested_data_dir,"/test")

            data_ingestion_config = DataIngestionConfig(
                tgz_download_dir=tgz_download_dir,
                raw_data_dir=raw_data_dir,
                ingested_train_dir=ingested_train_dir,
                ingested_test_dir=ingested_test_dir
            )

            return data_ingestion_config
        except Exception as e:
            raise HousingException(e,sys) from e