import yaml
import os
def read_yaml(path:str='src/config.yaml'):
    print(os.getcwd())
    with open(path) as file:
        config = yaml.safe_load(file)
    return config
