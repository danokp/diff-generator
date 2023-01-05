"""Functions fot files comparison."""
import json


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


def generate_diff(import_file1: str, import_file2: str) -> str:
    """Compare two json-files and return the result of comparison.

    Args:
        import_file1: The first file to compare.
        import_file2: The second file to compare.

    Returns:
        The result of comparison.
    """
    with open(import_file1) as file1:
        file1_dict = json.load(file1)
    with open(import_file2) as file2:
        file2_dict = json.load(file2)
    diff_result_list = []
    for key, value1 in file1_dict.items():
        if key in file2_dict:
            poped_value2 = file2_dict.pop(key)
            if value1 == poped_value2:
                diff_result_list.append((key, value1, ''))
            else:
                diff_result_list.append((key, value1, '-'))
                diff_result_list.append((key, poped_value2, '+'))
        else:
            diff_result_list.append((key, value1, '-'))
    for key2, value2 in file2_dict.items():
        diff_result_list.append((key2, value2, '+'))
    diff_result = '\n'.join(
        f'{_fill(tupl[2], size=4)}{tupl[0]}: {tupl[1]}'   # noqa: WPS221
        for tupl in sorted(diff_result_list, key=lambda x: x[0])
    )
    return f'{{\n{diff_result}\n}}'
