"""Convert json and yaml files in dictionaries."""
import json

import yaml


def convert_file_into_dict(file_path: str) -> dict:
    """Convert file (json or yaml) into dictionary.

    Args:
        file_path: The path to a file.

    Returns:
        The dictionary.
    """
    extension = file_path.split('.')[-1]
    with open(file_path) as import_file:
        if extension == 'json':
            return json.load(import_file)
        elif extension in {'yaml', 'yml'}:
            return yaml.safe_load(import_file)
