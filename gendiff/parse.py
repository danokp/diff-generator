"""Convert json and yaml files in dictionaries."""
import json

import yaml


def read_json_file(file_path: str) -> dict:
    """Read json file.

    Args:
        file_path: The path to a file.

    Returns:
        The dictionary.
    """
    with open(file_path) as import_file:
        return json.load(import_file)


def read_yaml_file(file_path: str) -> dict:
    """Read yaml(yml) file.

    Args:
        file_path: The path to a file.

    Returns:
        The dictionary.
    """
    with open(file_path) as import_file:
        return yaml.safe_load(import_file)


def convert_file_into_dict(file_path: str) -> dict:
    """Convert file (json or yaml) into dictionary.

    Args:
        file_path: The path to a file.

    Returns:
        The dictionary.

    Raises:
        ValueError: If file type not in json, yaml or yml.
    """
    extension = file_path.split('.')[-1]
    if extension == 'json':
        return read_json_file(file_path)
    elif extension in {'yaml', 'yml'}:
        return read_yaml_file(file_path)
    raise ValueError('Only json, yaml or yml formats are available.')
