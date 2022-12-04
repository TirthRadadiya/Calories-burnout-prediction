from cbp.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig,DataValidationConfig
from cbp.util.util import read_yaml_file
from datetime import datetime
import os,sys
from cbp.exception import HousingException
from cbp.logger import logging

class Configuration:

    def __init__(self,
        ROOT_DIR,
        config_file_path:str = "config/config.yaml",
        current_time_stamp:str = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}" )->None:
            try:
                self.config = read_yaml_file(config_file_path)
                self.trainig_pipeline_config = self.get_trainig_pipeline_config(ROOT_DIR)
                self.time_stamp = current_time_stamp
            except Exception as e:
                raise HousingException(e,sys) from e

    def get_data_ingestion_config(self)->DataIngestionConfig:
        try:
            data_ingestion_info = self.config['data_ingestion_config']
            artifact_dir = self.trainig_pipeline_config.artifact_dir
            data_ingestion_artifact_dir = os.path.join(artifact_dir,
            "data_ingestion",
            self.time_stamp
            )

            dataset_download_url = data_ingestion_info['dataset_download_url']

            raw_data_dir = os.path.join(data_ingestion_artifact_dir,data_ingestion_info["raw_data_dir"])

            tgz_download_dir = os.path.join(data_ingestion_artifact_dir,data_ingestion_info["tgz_download_dir"])

            ingested_data_dir = os.path.join(data_ingestion_artifact_dir,data_ingestion_info["ingested_dir"])

            ingested_train_dir = os.path.join(ingested_data_dir,data_ingestion_info["ingested_train_dir"])

            ingested_test_dir = os.path.join(ingested_data_dir,data_ingestion_info["ingested_test_dir"])

            data_ingestion_config = DataIngestionConfig(
                dataset_download_url=dataset_download_url,
                raw_data_dir=raw_data_dir,
                tgz_download_dir=tgz_download_dir,
                ingested_train_dir=ingested_train_dir,
                ingested_test_dir=ingested_test_dir,
            )
            logging.info(f"Data Ingestion Config: {data_ingestion_config}")

            return data_ingestion_config
        except Exception as e:
            raise HousingException(e,sys) from e

    def get_data_validation_config(self,ROOT_DIR)->DataValidationConfig:
        try:
            data_validation_config = self.config['data_validation_config']
            artifact_dir = self.trainig_pipeline_config.artifact_dir
            data_validation_artifact_dir = os.path.join(artifact_dir,"data_validation",self.time_stamp)


            schema_file_path = os.path.join(ROOT_DIR,data_validation_config["schema_dir"],data_validation_config["schema_file_name"])

            report_file_name = os.path.join(data_validation_artifact_dir,data_validation_config["report_file_name"])
            report_page_file_name = os.path.join(data_validation_artifact_dir,data_validation_config["report_page_file_name"])

            data_validation_config = DataValidationConfig(
                schema_file_path=schema_file_path,
                report_file_path=report_file_name,
                report_page_file_path=report_page_file_name,
            )

            return data_validation_config

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
