from src.pipeline.training_pipeline import TrainPipeline
from src.exception import PlantException
import sys
import os

if __name__ =="__main__":
    try:
    
        train_pipeline = TrainPipeline()
        train_pipeline.run_pipeline()

    except Exception as e:
        raise PlantException(e, sys)
