"""Convert json and yaml files in dictionaries."""
import json

import yaml


def convert_json_in_dict(file_opened_to_read) -> dict:
    """Covert json file in dictionary.

    Args:
        file_opened_to_read: A file opened to read.

    Returns:
        The dictionary.
    """
    return json.load(file_opened_to_read)


def convert_yaml_in_dict(file_opened_to_read) -> dict:
    """Convert yaml(yml) file in dictionary.

    Args:
        file_opened_to_read: A file opened to read.

    Returns:
        The dictionary.
    """
    return yaml.safe_load(file_opened_to_read)


def convert_file_into_dict(file_path: str) -> dict:
    """Convert file (json or yaml) into dictionary.

    Args:
        file_path: The path to a file.

    Returns:
        The dictionary.

    Raises:
        ValueError: If file type not in json, yaml or yml.
    """
    convert_func_dict = {
        'json': convert_json_in_dict,
        'yaml': convert_yaml_in_dict,
        'yml': convert_yaml_in_dict,
    }
    extension = file_path.split('.')[-1]
    convert_file_to_dict = convert_func_dict.get(extension)
    if convert_file_to_dict:
        with open(file_path, 'r') as import_file:
            return convert_file_to_dict(import_file)
    raise ValueError('Only json, yaml or yml formats are available.')
