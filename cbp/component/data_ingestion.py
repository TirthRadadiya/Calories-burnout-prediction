from cbp.entity.config_entity import DataIngestionConfig
from cbp.entity.artifact_entity import DataIngestionArtifact
import os,sys
from cbp.exception import HousingException
from cbp.logger import logging
from six.moves import urllib
import tarfile
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit

class DataIngestion:

    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            logging.info(f"{'='*20}Data Ingestion log started.{'='*20} ")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise HousingException(e,sys) from e


    def download_data(self):
        try:
            dataset_download_url = self.data_ingestion_config.dataset_download_url

            tgz_download_dir = self.data_ingestion_config.tgz_download_dir
            
            if os.path.exists(tgz_download_dir):
                os.remove(tgz_download_dir)

            os.makedirs(tgz_download_dir,exist_ok=True)

            dataset_filename = os.path.basename(dataset_download_url)

            tgz_file_path = os.path.join(tgz_download_dir, dataset_filename)
            logging.info(f"Downloading data from {dataset_download_url} to {tgz_download_dir}")
            urllib.request.urlretrieve(dataset_download_url, tgz_file_path)
            logging.info(f"File :[{tgz_file_path}] has been downloaded successfully.")
            return tgz_file_path
        except Exception as e:
            raise HousingException(e,sys) from e

    def extract_tgz_file(self,tgz_file_path:str):
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)

            os.makedirs(raw_data_dir,exist_ok=True)

            logging.info(f"Extracting tgz file : [{tgz_file_path}] into dir :[{raw_data_dir}]")
            with tarfile.open(tgz_file_path) as housing_tgz_file_obj:
                housing_tgz_file_obj.extractall(path=raw_data_dir)
            logging.info("Extraction completed")
            
        except Exception as e:
            raise HousingException(e,sys) from e

    def split_data_as_train_test(self) -> DataIngestionArtifact:
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            file_name = os.listdir(raw_data_dir)[0]

            file_path = os.path.join(raw_data_dir,file_name)
            logging.info(f"Reading csv file: [{file_path}]")

            dataframe = pd.read_csv(file_path)

            dataframe["income_cat"] = pd.cut(
                dataframe["median_income"],
                bins=[0.0, 1.5, 3.0, 4.5, 6.0, np.inf],
                labels=[1,2,3,4,5]
            )

            logging.info(f"Splitting data into train and test")
            strat_train_set = None
            strat_test_set = None

            split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

            for train_index,test_index in split.split(dataframe, dataframe["income_cat"]):
                strat_train_set = dataframe.loc[train_index].drop(["income_cat"],axis=1)
                strat_test_set = dataframe.loc[test_index].drop(["income_cat"],axis=1)

            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir,file_name)

            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir,file_name)
            
            if strat_train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok=True)
                logging.info(f"Exporting training datset to file: [{train_file_path}]")
                strat_train_set.to_csv(train_file_path,index=False)

            if strat_test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir, exist_ok= True)
                logging.info(f"Exporting test dataset to file: [{test_file_path}]")
                strat_test_set.to_csv(test_file_path,index=False)
            

            data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_file_path,
                                test_file_path=test_file_path,
                                is_ingested=True,
                                message=f"Data ingestion completed successfully."
                                )

            logging.info(f"Data Ingestion artifact:[{data_ingestion_artifact}]")
            return data_ingestion_artifact

        except Exception as e:
            raise HousingException(e,sys) from e

    def initiate_data_ingestion(self):
        try:
            tgz_file_path = self.download_data()
            self.extract_tgz_file(tgz_file_path)
            return self.split_data_as_train_test()
        except Exception as e:
            raise HousingException(e,sys) from e