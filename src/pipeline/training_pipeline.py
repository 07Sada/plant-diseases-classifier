import sys 
import os 
from src.exception import PlantException 
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.entity.config_entity import DataIngestionConfig
from src.entity.config_entity import DataValidationConfig
from src.entity.config_entity import ModelTrainerConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.entity.artifact_entity import DataValidationArtifact
from src.entity.artifact_entity import ModelTrainerArtifact
from src.components.model_trainer import ModelTrainer
from src.logger import logging

class TrainPipeline:

    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.model_trainer_config = ModelTrainerConfig()

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info("Entered the start_data_ingestion method of TrainPipeline class")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)

            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

            logging.info("Exited the start_data_ingestion method of TrainPipeline class")

            return data_ingestion_artifact

        except Exception as e:
            raise PlantException(e, sys)

    def start_model_trainer(self) -> ModelTrainerArtifact:
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            model_trainer = ModelTrainer(model_trainer_config=self.model_trainer_config,
                                        data_ingestion_artifact=data_ingestion_artifact)
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            return model_trainer_artifact

        except Exception as e:
            raise PlantException(e, sys)

    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        logging.info("Entered the start_data_validation method of TrainPipeline class")
        try:

            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                            data_validation_config=self.data_validation_config,)

            data_validation_artifact = data_validation.initiate_data_validation()
            
            logging.info("Performed the data validation operation")
            logging.info("Exited the start_data_validation method of TrainPipeline class")
            
            return data_validation_artifact

        except Exception as e:
            raise PlantException(e, sys)


    def run_pipeline(self) -> None:
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)

            if data_validation_artifact.validation_status == True:
                model_trainer_artifact = self.start_model_trainer()

            else:
                raise Exception("Your data is not in correct format")

        except Exception as e:
            raise PlantException(e, sys)
