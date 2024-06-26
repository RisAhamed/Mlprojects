import sys
import os
import numpy as np
import pandas as pd
from dataclasses import dataclass
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from src.utils import save_object
from src.exception import CustomException
from src.logger import logging


@dataclass
class DataTransformationConfoig:
    preprocessor_obj_file_path = os.path.join("artifacts","preprocessor.pkl")

class DataTranformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfoig()

    def get_data_transformer_object(self):
        try:
            categorical_columns= ['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch',
       'test_preparation_course']
            numerical_columns = ['reading_score', 'writing_score']
            numerical_pipeline = Pipeline(
                steps = [
                    ("imputer ",SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler(with_mean=False))
                ]
        )
            categorical_pipeline = Pipeline(
                steps  =[
                    ("imputer",SimpleImputer(strategy ="most_frequent")),
                    ("oneHotEncoder",OneHotEncoder()),
                    ("Scaler", StandardScaler(with_mean=False)) ]            )
            logging.info("Numeric Columns encoding Completed")
            logging.info("Categorical Columns encoding completed")
            preprocessor = ColumnTransformer(
                [
                    ("numeric_pipeline",numerical_pipeline,numerical_columns),
                    ("Categorical_pipeline",categorical_pipeline,categorical_columns)
                ]
            )
            return preprocessor

        except Exception as e: 
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("reading the Test and Train data")
            logging.info("Obtaining preprocessing Object")

            preprocessing_obj = self.get_data_transformer_object()
            target_column_name = "math_score"
            numerical_columns = ['reading_score', 'writing_score']

            input_feature_train_df = train_df.drop(columns = [target_column_name],axis =1,inplace =False)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns = [target_column_name],axis =1,inplace =False)
            target_feature_test_df = test_df[target_column_name]

            logging.info(
                f"Applying preprocessing object on trainning Data frame and Testing Data Frame"
            )
            input_feature_train_Arr =preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_Arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[
                input_feature_train_Arr,np.array(target_feature_train_df)
            ]

            test_arr = np.c_[
                input_feature_test_Arr,np.array(target_feature_test_df)
            ]

            logging.info(f"saved preprocessing Object")

            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessing_obj
            )
            return (
                train_arr,test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
 
            pass
        except Exception as e:
            raise CustomException(e,sys)