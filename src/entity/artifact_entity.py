from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    dataset_path:str
    feature_store_path:str

@dataclass
class DataValidationArtifact:
    validation_status: bool

@dataclass
class ModelTrainerArtifact:
    trained_model_file_path: str