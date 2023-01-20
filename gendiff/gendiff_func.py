"""Compare two files and return difference in needed format."""
from gendiff.data_coparison import generate_diff_dict
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
    """
    format_dict = {
        'stylish': stylish,
        'plain': plain,
    }
    diff_dict = generate_diff_dict(
        convert_file_into_dict(file1_path),
        convert_file_into_dict(file2_path),
        {},
    )
    return format_dict[diff_format](diff_dict)
