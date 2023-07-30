import os 
import sys 
from six.moves import urllib
import zipfile 
from src.exception import PlantException
from src.logger import logging
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from huggingface_hub import hf_hub_download
from tqdm import tqdm


class DataIngestion:
    def __init__(
        self, data_ingestion_config: DataIngestionConfig = DataIngestionConfig()
    ):
        try:
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise PlantException(e, sys)

    def download_dataset(self):
        # The path to the downloaded file in the cache.
        print(f"Commencing the dataset download from the hub...")
        logging.info(f"Commencing the dataset download from the hub...")

        filepath = hf_hub_download(repo_id=self.data_ingestion_config.huggingface_repo_id, 
                                    filename=self.data_ingestion_config.huggingface_file_name, 
                                    repo_type="dataset")

        # Create the destination directory if it doesn't exist.
        os.makedirs(self.data_ingestion_config.feature_store_file_path, exist_ok=True)

        # Save the file to the specified location.
        destination_path = os.path.join(self.data_ingestion_config.feature_store_file_path, self.data_ingestion_config.huggingface_file_name)
        with open(destination_path, "wb") as f_dest, open(filepath, "rb") as f_src:
            f_dest.write(f_src.read())
        
        return destination_path

    def extract_and_move_zip(self, zip_file_path):
        logging.info(f"Zip file extraction has begun.")
        destination_dir=self.data_ingestion_config.dataset_location
        
        # Extract the zip file.
        with zipfile.ZipFile(zip_file_path, "r") as zip_file:
            zip_file.extractall(destination_dir)
        
        logging.info(f"Zip file extraction has complete.")

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        logging.info("Entered the initiate_data_ingestion method of the Data_Ingestion class.")
        try:
            zip_file_path = self.download_dataset()
            self.extract_and_move_zip(zip_file_path=zip_file_path)

            data_ingestion_artifact = DataIngestionArtifact(dataset_path=self.data_ingestion_config.dataset_location,
                                                            feature_store_path=zip_file_path)
            logging.info("Data Ingestion Artifacts Genereated")

            return data_ingestion_artifact
        
        except Exception as e:
            raise PlantException(e, sys)