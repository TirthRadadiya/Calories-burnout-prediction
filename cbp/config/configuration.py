from cbp.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig
from util.util import read_yaml_file
import os,sys
from cbp.exception import HousingException
from cbp.logger import logging

class Configuration:

    def __init__(self,
        config_file_path:str = config_file_path
        current_time_stamp:str = current_time_stamp,
        ROOT_DIR:str -> ROOT_DIR)->None:
        try:
            self.config = read_yaml_file(config_file_path)
            self.trainig_pipeline_config = self.get_trainig_pipeline_config(ROOT_DIR)
            self.time_stamp = current_time_stamp
        except Exception as e:
            raise HousingException(e,sys) from e

    def get_data_ingestion_config(self)->DataIngestionConfig::
        try:
            data_ingestion_config = self.config['data_ingestion']
            artifact_dir = self.trainig_pipeline_config.artifact_dir
            data_ingestion_artifact_dir = os.path.join(artifact_dir,
            "data_ingestion",
            self.time_stamp
            )

            dataset_download_url = data_ingestion_config['dataset_download_url']

            raw_data_dir = os.path.join(data_ingestion_artifact_dir,data_ingestion_config["raw_data_dir"])

            tgz_download_dir = os.path.join(data_ingestion_artifact_dir,data_ingestion_config["tgz_download_dir"]))

            ingested_data_dir = os.path.join(data_ingestion_artifact_dir,data_ingestion_config["ingested_dir"]

            ingested_train_dir = os.path.join(ingested_data_dir,data_ingestion_config["ingested_train_dir"])

            ingested_test_dir = os.path.join(ingested_data_dir,data_ingestion_config["ingested_test_dir"])

            data_ingestion_config = DataIngestionConfig(
                dataset_download_url=dataset_download_url,
                raw_data_dir=raw_data_dir,
                tgz_download_dir=tgz_download_dir,
                ingested_train_dir=ingested_train_dir,
                ingested_test_dir=ingested_test_dir,
            )
            logger.info(f"Data Ingestion Config: {data_ingestion_config}")

            return data_ingestion_config
        except Exception as e:
            raise HousingException(e,sys) from e

    def get_trainig_pipeline_config(self,ROOT_DIR) -> TrainingPipelineConfig:
        try:
            trainig_pipeline_config = self.config["training_pipeline_config"]
            artifact_dir = os.path.join(ROOT_DIR,
            trainig_pipeline_config["pipeline_name"],
            trainig_pipeline_config["artifact_dir"]
            )
            trainig_pipeline_config = TrainingPipelineConfig(artifact_dir=artifact_dir)
            logging.info(f"Training Pipeline Config: {trainig_pipeline_config}")
            return trainig_pipeline_config
        except Exception as e:
            raise HousingException(e,sys) from e
