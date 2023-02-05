"""Compare two files and return difference in needed format."""
from gendiff.data_comparison import generate_diff_dict
from gendiff.format_output.json import json
from gendiff.format_output.plain import plain
from gendiff.format_output.stylish import stylish
from gendiff.parse import convert_file_into_dict


def generate_diff(
    file1_path: str,
    file2_path: str,
    diff_format: str = 'stylish',
) -> str:
    """Generate difference between file1 and file2.

    Args:
        file1_path: The path for the first file.
        file2_path: The path for the second file.
        diff_format: The format of difference representaton.

    Returns:
        Comparison result string.

    Raises:
        ValueError: If 'diff_format' not in {'stylish', 'plain', 'json'}
    """
    format_dict = {
        'stylish': stylish,
        'plain': plain,
        'json': json,
    }
    diff_dict = generate_diff_dict(
        convert_file_into_dict(file1_path),
        convert_file_into_dict(file2_path),
        {},
    )
    formatter = format_dict.get(diff_format)
    if formatter is None:
        raise ValueError(
            f'Choose one of the available formats: '
            f'{list(format_dict.keys())}.',
        )
    return formatter(diff_dict)
