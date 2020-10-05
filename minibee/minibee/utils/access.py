from ...log import logger
from typing import Iterable, Dict, Any, Union
import copy
from . import exceptions


def branch_copy(value, deepcopy):
    if deepcopy:
        return copy.deepcopy(value)
    else:
        return value


def get_key(key: str, dictObj: Dict[str, Any], warn: bool = True, deepcopy=False):
    try:
        return branch_copy(dictObj[key], deepcopy)
    except KeyError as e:
        if warn:
            logger.warning(f"Key '{key}' not found.")
        return


def get_attribute(attr: str, namespace, warn: bool = True, deepcopy=False):
    try:
        return branch_copy(getattr(namespace, attr), deepcopy)
    except AttributeError as e:
        if warn:
            breakpoint()
            logger.warning(f"Attribute '{attr}' not found.")
        return


def get_keys(keys: Union[Iterable[str], str], dictObj: Dict[str, Any], deepcopy: bool = False):
    """Gets all the values associated to 'keys' and returns a list.
    Any key that is not found emits a warning log, and the corresponding value is set to None. Relies on the function 'get_key' of the same module.
    Args:
        keys (list or str): List of keys, of string 
        dictObj (dict): Dictionary containing the values to fetch.
    Returns:
        list: List of values. Can containg None elements if the corresponding keys are not present in the dictionary.
    """

    values = []
    if keys == 'all':
        keys = dictObj.keys()
    else:
        if isinstance(keys, str):
            raise TypeError("Invalid type for argument 'keys'. Expected an iterable of strings or the string 'all'.")
    for key in keys:
        values.append(get_key(key, dictObj, deepcopy=deepcopy))
    return values


def get_item(index: int, listObj: Iterable, warn: bool = False):
    try:
        return listObj[index]
    except Exception as e:
        if warn:
            logger.warning(f"Could not access index {index} ({e})")
        return


def get_endpoints(array: Iterable):
    return array[0], array[-1]


def replace_existing_key(dictObj, key, value):
    if get_key(key, dictObj, warn=False) is None:
        exceptions.log_and_raise_error(f"Key {key} does not exist.", ValueError)
    else:
        dictObj[key] = value