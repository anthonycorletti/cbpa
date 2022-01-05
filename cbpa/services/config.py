import yaml

from cbpa.schemas.config import Config


class ConfigService:
    def __init__(self) -> None:
        pass

    def load_config(self, filepath: str) -> Config:
        with open(filepath, "r") as f:
            content = yaml.safe_load(f)
        return Config(**content)
