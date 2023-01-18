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


def generate_diff_list(file1_dict: dict, file2_dict: dict) -> list:
    """Compare two json-files and return the result of comparison.

    Args:
        file1_dict: The first dictionary to compare.
        file2_dict: The second dictionary to compare.

    Returns:
        The result of comparison.
    """
    result = defaultdict(dict)

    def walk_first_dct(result_dict1: dict, file1_dict: dict, file2_dict: dict, lvl: int = 0):
        """Walk through the first dictionary and return differences with the second one.

        Args:
            result_dict1: A dictionary with differences.
            file1_dict: The first dictionary to compare.
            file2_dict: The second dictionary to compare.
            lvl: Depth of comparison.

        Returns:
            The difference dictionary without unique items from the second one.
        """
        for key1, value1 in file1_dict.items():
            if isinstance(value1, dict):
                if key1 in file2_dict:
                    sign, lvl = (
                        (SIGN_VALUE_IN_FILE1_FILE2, lvl)
                        if isinstance(file2_dict[key1], dict)
                        else (SIGN_VALUE_ONLY_IN_FILE1, lvl + 1)
                    )
                    result_dict1[key1][sign] = (
                        walk_first_dct(
                            defaultdict(dict),
                            value1,
                            file2_dict.get(key1, {}),
                            lvl,
                        )
                    )
                else:
                    sign = (
                        SIGN_VALUE_IN_FILE1_FILE2 if lvl > 0
                        else SIGN_VALUE_ONLY_IN_FILE1
                    )
                    result_dict1[key1][sign] = walk_first_dct(
                        defaultdict(dict),
                        value1,
                        file2_dict.get(key1, {}),
                        lvl=lvl + 1,
                    )
            else:
                if key1 in file2_dict:
                    value2pop = file2_dict.pop(key1)
                    if value1 == value2pop:
                        result_dict1[key1][SIGN_VALUE_IN_FILE1_FILE2] = value1
                    else:
                        result_dict1[key1][SIGN_VALUE_ONLY_IN_FILE1] = value1
                        result_dict1[key1][SIGN_VALUE_ONLY_IN_FILE2] = value2pop
                else:
                    sign = (
                        SIGN_VALUE_IN_FILE1_FILE2 if lvl > 0
                        else SIGN_VALUE_ONLY_IN_FILE1
                    )
                    result_dict1[key1][sign] = value1
        return result_dict1

    def walk_second_dct(result_dict2, file2_dict_unique, lvl=0):
        """Walk through the second dictionary and adds unique its items.

        Args:
            result_dict2: A dictionary with differences.
            file2_dict_unique: The second dictionary to compare
            without repeated keys.
            lvl: Depth of comparison.

        Returns:
            All difference dictionary between the first and
            the second dictionary.
        """
        for key2, value2 in file2_dict_unique.items():
            if value2 == {}:
                continue
            sign = (
                SIGN_VALUE_IN_FILE1_FILE2 if lvl > 0
                else SIGN_VALUE_ONLY_IN_FILE2
            )
            if isinstance(value2, dict):
                if key2 in result_dict2:
                    update_dict(
                        result_dict2[key2][SIGN_VALUE_IN_FILE1_FILE2],
                        walk_second_dct(
                            result_dict2[key2][SIGN_VALUE_IN_FILE1_FILE2],
                            value2,
                            lvl=lvl,
                        ),
                    )
                else:
                    result_dict2[key2][sign] = walk_second_dct(
                        defaultdict(dict), value2, lvl=lvl + 1,
                    )
            else:
                result_dict2[key2][sign] = value2
        return result_dict2
    return walk_second_dct(
        walk_first_dct(result, file1_dict, file2_dict), file2_dict,
    )


def generate_diff(file1_path: str, file2_path: str) -> str:
    """Generate difference between file1 and file2.

    Args:
        file1_path: The path for the first file.
        file2_path: The path for the second file.

    Returns:
        Comparison result string.
    """
    return stylish(generate_diff_list(
        convert_file_into_dict(file1_path),
        convert_file_into_dict(file2_path),
    ))
