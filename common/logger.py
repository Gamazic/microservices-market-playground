import logging.config
import yaml


def load_yaml_logging_config(path):
    with open(path, "r") as stream:
        config = yaml.safe_load(stream)
    logging.config.dictConfig(config)
