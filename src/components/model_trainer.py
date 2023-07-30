import os 
import sys 
import shutil 
from ultralytics import YOLO 
from src.logger import logging 
from src.exception import PlantException
from src.entity.config_entity import ModelTrainerConfig
from src.entity.artifact_entity import ModelTrainerArtifact
from src.entity.artifact_entity import DataIngestionArtifact

class ModelTrainer:
    
    try:
        def __init__(self, model_trainer_config:ModelTrainerConfig, data_ingestion_artifact:DataIngestionArtifact):
            self.model_trainer_config = model_trainer_config
            self.data_ingestion_artifact = data_ingestion_artifact

        def initiate_model_trainer(self) -> ModelTrainerArtifact:
            logging.info(f"Removing and existing runs directory from previous training")
            os.system("rm -rf runs")

            model_config_file_name = self.model_trainer_config.weight_name.split('.')[0]
            print(model_config_file_name)

            os.system(f"yolo task=classify mode=train model=yolov8n-cls.pt data={daset_path} epochs=1 imgsz=128")
            
            os.system(f"yolo task=classify mode=train model={self.model_trainer_config.weight_name} \
                data={self.data_ingestion_artifact.dataset_path} epochs={self.model_trainer_config.no_epochs} \
                    imgsz=128 batch={self.model_trainer_config.batch_size} patience={self.model_trainer_config.patience}")

            os.system("cp runs/classify/train/weights/best.pt custom_model_weights/")
            os.makedirs(self.model_trainer_config.model_trainer_dir, exist_ok=True)

            
            os.system(f"cp runs/detect/train/weights/best.pt {self.model_trainer_config.model_trainer_dir}/")

            model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path="custom_model_weights/best.pt",)

            logging.info("Exited initiate_model_trainer method of ModelTrainer class")
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")

            return model_trainer_artifact

    except Exception as e:
            raise PlantException(e, sys)