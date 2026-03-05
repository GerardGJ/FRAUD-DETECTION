import yaml
import os
from typing import Dict

def read_yaml(path:str='src/config.yaml') -> Dict[str,str]:
    print(os.getcwd())
    with open(path) as file:
        config = yaml.safe_load(file)
    return config
