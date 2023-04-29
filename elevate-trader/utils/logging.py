from logging import config, getLogger
import yaml


def get_logger(logger_name: str = "elevate_trader"):
    "Return the app logger"
    return getLogger(logger_name)

def logger_init():
    "Initialize the logger from logging.yaml config file"
    with open("logging.yaml", "r") as f:
        yaml_content = yaml.safe_load(f.read())
        config.dictConfig(yaml_content)
    
    return get_logger()

