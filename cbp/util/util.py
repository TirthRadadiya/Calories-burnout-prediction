import yaml
from cbp.exception import HousingException
import os,sys

def read_yaml_file(file_path:str)-> dict:
    """
    Reads a YAML file and returns the contents as a dictionary.
    file_path: str
    """
    try:
        with open(file_path, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise HousingException(e,sys) from e
    
def get_obtain_obj(dataset):
    """
    Takes the dataset and return the different features of it.
        - All the columns with the related datatypes
        - All the numerical and categorical column
        - Domain value of categorical column
    dataset: dataframe
    """
    columns = dataset.columns
    column_dtypes = dict(dataset.dtypes)
    numerical_col = []
    categorical_col = []
    for i in column_dtypes:
        column_dtypes[i] = str(column_dtypes[i])
        if "float" in column_dtypes[i] or "int" in column_dtypes[i]:
            numerical_col.append(i)
        elif "object" in column_dtypes[i]:
            column_dtypes[i] = "category"
            categorical_col.append(i)
    domain_value = {}
    for value in categorical_col:
        domain_value[value] = list(dataset[value].unique())
    obtained_obj = {"columns":column_dtypes,"numerical_column":numerical_col,"categorical_column":categorical_col,"domain_value":domain_value}
    return obtained_obj