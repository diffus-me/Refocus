from pydantic import BaseSettings


class Settings(BaseSettings):
    api_image_dir: str = "./api-outputs"
    s3_prefix: str = "http://localhost:7865/file=./api-outputs"
    hostname: str = ""
    binary_dir: str = "./"
    models_dir: str = "./"
    preset_dir: str = "./presets"
    models_db_path: str = "./models/models_db.json"

    feature_permissions_url: str = ""
    workdir_jfs_target: str = ""
    workdir_name: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
