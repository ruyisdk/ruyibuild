from ruamel.yaml import YAML
import pathlib
import os
import shutil


def read_yaml(yaml_dir):
    '''
    read yaml file and parse it to object
    '''
    if not os.path.exists(yaml_dir):
        raise ValueError(f"yaml_dir can not find in :{yaml_dir}")

    try:
        with open(yaml_dir, 'r', encoding='utf-8') as r_f:
            yaml = YAML()
            data = yaml.load(r_f)
            # print ('yaml_data', data)
            return data
    except Exception as e:
        logger.error(e)
        raise e


def get_config_yaml_dir():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),'conf/config.yaml')
