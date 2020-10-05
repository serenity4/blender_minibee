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

def read_json(source):
    """Reads json from source file.

    Args:
        source (str): source file path

    Returns:
        dict: dictionary containing JSON data

    """

    with open(source, 'r') as ifile:
        data = json.load(ifile)

    return data
