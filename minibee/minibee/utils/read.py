import numpy as np
import re
import os
from . import access
from ...log import logger
from yaml import safe_load as yaml_load
from json import load as json_load

def yaml(path):
    logger.debug(f"Opening YAML file at {path}.")
    with open(path, 'r') as ifile:
        res = yaml_load(ifile)
    return res


def json(path):
    logger.debug(f"Opening JSON file at {path}.")
    with open(path, 'r') as ifile:
        res = json_load(ifile)
    return res

def convert_dict_list_to_array(data):
    """Converts all dictionary values to numpy arrays.

    Args:
        data (dict): dictionary to convert

    Returns:
        dict: dictionary with values converted into arrays

    """

    for k, v in data.items():
        data[k] = np.array(list(v))
    return data