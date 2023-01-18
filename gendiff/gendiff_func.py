"""Functions for files comparison."""
import json
from collections import defaultdict

import yaml

DIFF_POS = 0
VALUE_POZ = 1
SIGN_VALUE_IN_FILE1_FILE2 = ''
SIGN_VALUE_ONLY_IN_FILE1 = '-'
SIGN_VALUE_ONLY_IN_FILE2 = '+'


def _fill(name: str, size: int, filler: str = ' ') -> str:
    """Convert string into string of the needed length.

    Args:
        name: A string to convert.
        size: The result length of the string.
        (if size <= len(name) nothing will change)
        filler: A filler (default ' ').

    Returns:
        The string filled by filler to the length equal to size.
    """
    return name.rjust(size - 1, filler).ljust(size, filler)


def convert_values_in_right_style(value_convert) -> str:
    """Convert values in the right style.

    Args:
        value_convert: A value to be converted.

    Returns:
        The converted value from convert_dict. If it isn't exist, returns value.
    """
    convert_dct = {
        True: 'true',
        False: 'false',
        None: 'null',
    }
    return convert_dct.get(value_convert, value_convert)


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


def make_one_diff_line(
    key, diff_key: str, value, lvl: int, indent_size: int, filler: str,
) -> str:
    """Create one difference line.

    Args:
        key: A dictionary key.
        diff_key: Comparison result.
        value: A dictionary value.
        lvl: Depth of comparison.
        indent_size: The size of indent.
        filler: A symble indent is filled with.

    Returns:
        One difference line.
    """
    return (
        f'{lvl * indent_size * filler}'
        f'{_fill(diff_key, size=indent_size)}'
        f'{key}'
        f'{":" if value == "" else ": "}'
        f'{value}'
    )


def stylish(diff_dict: dict) -> str:
    """Stylish difference dictionary.

    Args:
         diff_dict: A difference dictionary.

    Returns:
        Styled string.
    """
    def inner(diff_dict, lvl: int, indent_size: int = 4, filler: str = ' '):
        diff_result = ['{']
        for key in sorted(diff_dict.keys()):
            for diff_key in sorted(diff_dict[key].keys(), reverse=True):
                value = diff_dict[key][diff_key]
                if isinstance(value, dict):
                    diff_result.append(
                        make_one_diff_line(
                            key,
                            diff_key,
                            inner(value, lvl=lvl + 1),
                            lvl,
                            indent_size,
                            filler,
                        ),
                    )
                else:
                    diff_result.append(
                        make_one_diff_line(
                            key,
                            diff_key,
                            convert_values_in_right_style(value),
                            lvl,
                            indent_size,
                            filler,
                        ),
                    )
        diff_result.append(f'{lvl * indent_size * filler}}}')
        return '\n'.join(diff_result)
    if diff_dict == {}:
        return '{}'
    return inner(diff_dict, lvl=0)


def update_dict(dict1: dict, dict2: dict):
    """Update dictionary with another without loosing information.

    Args:
        dict1: A dictionary to update.
        dict2: A dictionary dict1 is updated with.
    """
    for key2, value2 in dict2.items():
        if key2 in dict1:
            dict1 = dict1.get(key2) | value2
        else:
            dict1[key2] = value2


def generate_diff_dict(file1_dict: dict, file2_dict: dict) -> dict:
    """Compare two json-files and return the result of comparison.

    Args:
        file1_dict: The first dictionary to compare.
        file2_dict: The second dictionary to compare.

    Returns:
        The result of comparison.
    """
    result = defaultdict(dict)

    def walk_dct(
        result_dict: dict,
        file1_dict: dict,
        file2_dict: dict,
        lvl: int = 0,
    ) -> dict:
        """Walk through the first dictionary and return differences with the second one.

        Args:
            result_dict: A dictionary with differences.
            file1_dict: The first dictionary to compare.
            file2_dict: The second dictionary to compare.
            lvl: Depth of comparison.

        Returns:
            The difference dictionary without unique items from the second one.
        """
        keys_set = set()
        if isinstance(file1_dict, dict):
            keys_set.update(file1_dict.keys())
        if isinstance(file2_dict, dict):
            keys_set.update(file2_dict.keys())
        for key in keys_set:
            if key not in file2_dict:
                value1 = file1_dict[key]
                sign = (
                    SIGN_VALUE_IN_FILE1_FILE2 if lvl > 0
                    else SIGN_VALUE_ONLY_IN_FILE1
                )
                result_dict[key][sign] = (
                    walk_dct(
                        defaultdict(dict),
                        value1,
                        file2_dict.get(key, {}),
                        lvl=lvl + 1,
                    ) if isinstance(value1, dict)
                    else value1
                )
            elif key not in file1_dict:
                value2 = file2_dict[key]
                sign = (
                    SIGN_VALUE_IN_FILE1_FILE2 if lvl > 0
                    else SIGN_VALUE_ONLY_IN_FILE2
                )
                result_dict[key][sign] = (
                    walk_dct(
                        defaultdict(dict),
                        file1_dict.get(key, {}),
                        value2,
                        lvl=lvl + 1,
                    ) if isinstance(value2, dict)
                    else value2
                )
            else:
                value1 = file1_dict[key]
                value2 = file2_dict[key]
                if isinstance(value1, dict):
                    sign, lvl = (
                        (SIGN_VALUE_IN_FILE1_FILE2, lvl)
                        if isinstance(file2_dict[key], dict)
                        else (SIGN_VALUE_ONLY_IN_FILE1, lvl + 1)
                    )
                    result_dict[key][sign] = (
                        walk_dct(
                            defaultdict(dict),
                            file1_dict.get(key, {}),
                            file2_dict.get(key, {}),
                            lvl,
                        )
                    )
                    if not isinstance(file2_dict[key], dict):
                        result_dict[key][SIGN_VALUE_ONLY_IN_FILE2] = value2
                else:
                    if value1 == value2:
                        result_dict[key][SIGN_VALUE_IN_FILE1_FILE2] = value1
                    else:
                        result_dict[key][SIGN_VALUE_ONLY_IN_FILE1] = value1
                        result_dict[key][SIGN_VALUE_ONLY_IN_FILE2] = value2
        return result_dict
    return walk_dct(result, file1_dict, file2_dict)


def generate_diff(file1_path: str, file2_path: str) -> str:
    """Generate difference between file1 and file2.

    Args:
        file1_path: The path for the first file.
        file2_path: The path for the second file.

    Returns:
        Comparison result string.
    """
    return stylish(generate_diff_dict(
        convert_file_into_dict(file1_path),
        convert_file_into_dict(file2_path),
    ))
