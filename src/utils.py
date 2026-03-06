import yaml
from typing import Dict

def read_yaml(path:str='src/config.yaml') -> Dict[str,str|int]:
    """
    This function loads yaml files

    Parameters
    ----------
    path : str
        Path to the config file
    
    Retruns
    -------
    config : Dict[str,str|int]
        This is a dictionary with the differnt variables in the yaml file
    """
    with open(path) as file:
        config = yaml.safe_load(file)
    return config
