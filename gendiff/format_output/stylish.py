"""Convert comparison dictionary in tree-shaped style."""
from gendiff.data_comparison import (
    VALUE_ADDED,
    VALUE_CHANGED,
    VALUE_REMOVED,
    VALUE_UNCHANGED,
)


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
    if value_convert is False:
        return 'false'
    if value_convert is True:
        return 'true'
    if value_convert is None:
        return 'null'
    return value_convert


def make_one_diff_line(
    key, meta: str, value, lvl: int, indent_size: int, filler: str,
) -> str:
    """Create one difference line.

    Args:
        key: A dictionary key.
        meta: Comparison result.
        value: A dictionary value.
        lvl: Depth of comparison.
        indent_size: The size of indent.
        filler: A symble indent is filled with.

    Returns:
        One difference line.
    """
    diff_meaning_dict = {
        VALUE_UNCHANGED: '',
        VALUE_ADDED: '+',
        VALUE_REMOVED: '-',
    }
    return (
        f'{lvl * indent_size * filler}'
        f'{_fill(diff_meaning_dict[meta], size=indent_size)}'
        f'{key}'
        f': {value}'
    )


def get_info(item, info_type: str):
    """Get value or metadate from diff dictionary.

    Args:
        item: The item to get information from.
        info_type: The information type (metadate or value).

    Returns:
        Value or metadate from diff dictionary
    """
    d = {
        'meta': (1, VALUE_UNCHANGED),
        'value': (0, item),
    }
    index, returned_item = d[info_type]
    return (
        item[index] if isinstance(item, list)
        else returned_item
    )


def stylish(diff_dict: dict) -> str:
    """Stylish difference dictionary.

    Args:
         diff_dict: A difference dictionary.

    Returns:
        Styled string.
    """
    def inner(
        diff_dict: dict,
        lvl: int,
        indent_size: int = 4,
        filler: str = ' ',
    ) -> str:
        diff_result = ['{']
        for key in sorted(diff_dict.keys()):
            metadate = get_info(diff_dict[key], 'meta')
            value = get_info(diff_dict[key], 'value')
            if isinstance(value, dict):
                diff_result.append(
                    make_one_diff_line(
                        key,
                        metadate,
                        inner(value, lvl=lvl + 1),
                        lvl,
                        indent_size,
                        filler,
                    ),
                )
            else:
                if metadate == VALUE_CHANGED:
                    for meta, i in zip((VALUE_REMOVED, VALUE_ADDED), (0, 1)):
                        diff_result.append(
                            make_one_diff_line(
                                key,
                                meta,
                                inner(value[i], lvl=lvl + 1)
                                if isinstance(value[i], dict)
                                else convert_values_in_right_style(value[i]),
                                lvl,
                                indent_size,
                                filler,
                            ),
                        )
                else:
                    diff_result.append(
                        make_one_diff_line(
                            key,
                            metadate,
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
