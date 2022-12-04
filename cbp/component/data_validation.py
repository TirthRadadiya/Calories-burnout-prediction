from cbp.logger import logging
from cbp.exception import HousingException
import os,sys
from cbp.entity.config_entity import DataValidationConfig
from cbp.entity.artifact_entity import DataIngestionArtifact
import pandas as pd
from cbp.util.util import get_obtain_obj,read_yaml_file
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab
import json

import pandas

class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
        except Exception as e:
            raise HousingException(e,sys) from e

    def is_train_test_file_exists(self):
        logging.info("Checking whether the train and test files exist or not")
        try:
            train_file_check = False
            test_file_check = False

            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            train_file_check = os.path.exists(train_file_path)
            test_file_check = os.path.exists(test_file_path)

            exists = train_file_path and test_file_path

            logging.info(f"Is train and test files exist: {exists}")

            if not exists:
                train_file_path = self.data_ingestion_artifact.train_file_path
                test_file_path = self.data_ingestion_artifact.test_file_path
                message=f"Training file: {training_file} or Testing file: {testing_file} is not present"
                raise Exception(message)
            return exists
        except Exception as e:
            raise HousingException(e,sys) from e


    def compare_schema_to_dataset(schema_file_obj,obtained_obj,params):
        #checking the number of columns
        if len(schema_file_obj["columns"]) != len(obtained_obj["columns"]):
            logging.info(f"schema file and {params} data set do not have same number of columns")
            return False

        #checking the name of the columns and checking the data types of the column
        for val in schema_file_obj["columns"].keys():
            if val not in obtained_obj["columns"].keys():
                logging.info(f"{val} not present in {params} data")
                return False
            schema_type = schema_file_obj["columns"][val]
            obtain_type = obtained_obj["columns"][val]
            if schema_type not in obtain_type:
                logging.info(f"{val} is present in {params} data but data types {schema_type} do not match with {obtain_type}")
                return False
            if "float" in schema_type or "int" in schema_type:
                if val not in obtained_obj["numerical_column"]:
                    logging.info(f"{val} is present in {params} data and data types {schema_type} also match with {obtain_type} but {val} is {schema_type} column and still not present in {obtained_obj['numerical_column']}")
                    return False
            if "categorical" in schema_type:
                if val not in obtained_obj["categorical_column"]:
                    logging.info(f"{val} is present in {params} data and data types {schema_type} also match with {obtain_type} but {val} is {schema_type} column and still not present in {obtained_obj['categorical_column']}")
                    return False

        #to check domain value in categorical columns
        cat_col = schema_file_obj["categorical_columns"]
        domain_value = schema_file_obj["domain_value"]
        for value in cat_col:
            for d_value in domain_value[value]:
                if d_value not in obtained_obj["domain_value"][value]:
                    logging.info(f"{d_value} is not described in {obtained_obj['domain_value'][value]} of {val} column of {params} data")
                    return False
        return True

    def validate_dataset_schema(self):
        try:
            logging.info("Starting schema validation of dataset")
            validation_status = False
            train_data_path = self.data_ingestion_artifact.train_file_path
            test_data_path = self.data_ingestion_artifact.test_file_path
            schema_file_obj = read_yaml_file(self.data_validation_config.schema_file_path)

            logging.info("reading test file and train file")
            train_data = pd.read_csv(train_data_path)
            test_data = pd.read_csv(test_path)

            obtained_train_obj = get_obtain_obj(train_data)
            obtained_test_obj = get_obtain_obj(test_data)

            logging.info("validation schema for tarin dataset")
            for_train = compare_schema_to_dataset(schema_file_obj,obtained_train_obj,"train")

            logging.info("validation schema for test dataset")
            for_test = compare_schema_to_dataset(schema_file_obj,obtained_test_obj,"test")

            validation_status = for_test and for_train
        except Exception as e:
            raise HousingException(e,sys) from e

    def get_and_save_data_drift_report(self):
        try:
            profile = Profile(sections=[DataDriftProfileSection()])

            train_df,test_df = self.get_train_and_test_df()

            profile.calculate(train_df,test_df)

            report = json.loads(profile.json())

            report_file_path = self.data_validation_config.report_file_path
            report_dir = os.path.dirname(report_file_path)
            os.makedirs(report_dir,exist_ok=True)

            with open(report_file_path,"w") as report_file:
                json.dump(report, report_file, indent=6)
            return report
        except Exception as e:
            raise HousingException(e,sys) from e

    def save_data_drift_report_page(self):
        try:
            dashboard = Dashboard(tabs=[DataDriftTab()])
            train_df,test_df = self.get_train_and_test_df()
            dashboard.calculate(train_df,test_df)

            report_page_file_path = self.data_validation_config.report_page_file_path
            report_page_dir = os.path.dirname(report_page_file_path)
            os.makedirs(report_page_dir,exist_ok=True)

            dashboard.save(report_page_file_path)
        except Exception as e:
            raise HousingException(e,sys) from e

    def is_data_drift_found(self)->bool:
        try:
            report = self.get_and_save_data_drift_report()
            self.save_data_drift_report_page()
            # return True
        except Exception as e:
            raise HousingException(e,sys) from e
    
    def initiate_data_validation(self):
        try:
            message = []
            is_validated = True
            if self.is_train_test_file_exists():
                message.append("Training and testing file do not exist.")
                is_validated = False
            if self.validate_dataset_schema():
                message.append("Something wrong with the dataset schema.Check logs for proper justification.")
                is_validated = False
            # if  self.is_data_drift_found():
            #     message.append("Data drift has been found in the given dataset. See the reports for proper understanding")
            #     is_validated = False

            message = "Data validation done successfully" if len(message) == 0 else message

            data_validation_artifact = DataValidationArtifact(
                schema_file_path=self.data_validation_config.schema_file_path,
                report_file_path=self.data_validation_config.report_file_path,
                report_page_file_path=self.data_validation_config.report_page_file_path,
                is_validated=is_validated,
                message=message
            )
        except Exception as e:
            raise HousingException(e,sys) from e