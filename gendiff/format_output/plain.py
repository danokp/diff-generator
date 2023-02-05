"""Convert comparison dictionary in plain style."""
from gendiff.data_comparison import (
    VALUE_ADDED,
    VALUE_CHANGED,
    VALUE_REMOVED,
    VALUE_UNCHANGED,
)
from gendiff.format_output.stylish import get_info


def convert_values_in_right_style(value_convert) -> str:
    """Convert values in the right style.

    Args:
        value_convert: A value to be converted.

    Returns:
        The converted value from convert_dict. If it isn't exist, returns value.
    """
    convert_dct = {
        'True': 'true',
        'False': 'false',
        'None': 'null',
    }
    if isinstance(value_convert, str):
        return f"'{value_convert}'"
    elif isinstance(value_convert, dict):
        return '[complex value]'
    return convert_dct.get(str(value_convert), value_convert)


def make_one_diff_line(key_list: list, value, meta: str) -> str:
    diff_line = f"Property '{'.'.join(key_list)}' was "
    if meta == VALUE_CHANGED:
        return (
            f'{diff_line}'
            f'updated. From {convert_values_in_right_style(value[0])} '
            f'to {convert_values_in_right_style(value[1])}'
        )
    elif meta == VALUE_ADDED:
        return (
            f'{diff_line}'
            f'added with value: '
            f'{convert_values_in_right_style(value)}'
        )
    elif meta == VALUE_REMOVED:
        return f'{diff_line}removed'


def plain(diff_dict: dict) -> str:
    def inner(diff_dict: dict, acumulator: list) -> str:
        diff_result = []
        for key in sorted(diff_dict.keys()):
            metadate = get_info(diff_dict[key], 'meta')
            value = get_info(diff_dict[key], 'value')
            if isinstance(value, dict):
                if any(isinstance(v, list) for v in value.values()):
                    diff_result.append(inner(value, acumulator + [key]))
                else:
                    diff_result.append(
                        make_one_diff_line(acumulator + [key], value, metadate),
                    )
            else:
                if metadate == VALUE_UNCHANGED:
                    continue
                else:
                    diff_result.append(
                        make_one_diff_line(acumulator + [key], value, metadate),
                    )
        return '\n'.join(diff_result)
    return inner(diff_dict, [])
