import json


class Config(object):
    IMAGE_VIEW_APPLICATION_KEY = "IMAGE_VIEW_APPLICATION"
    IMAGE_VIEW_APPLICATION_DEFAULT_VALUE = "paintdotnet"

    @staticmethod
    def get_image_view_application() -> str:
        return Config.get_config().get(
            Config.IMAGE_VIEW_APPLICATION_KEY,
            Config.IMAGE_VIEW_APPLICATION_DEFAULT_VALUE,
        )
    
    @staticmethod
    def get_config() -> dict:
        return ConfigLoader.config_content

    @staticmethod
    def reload() -> None:
        ConfigLoader.load_config()

    @staticmethod
    def set_config_path(path: str) -> None:
        ConfigLoader.config_path = path
        Config.reload()


class ConfigLoader(object):
    config_path = "config.json"
    config_content = None

    def load_config(self) -> None:
        with open(ConfigLoader.config_path, "r") as config:
            ConfigLoader.config_content = json.load(config)
        print(ConfigLoader.config_content)


