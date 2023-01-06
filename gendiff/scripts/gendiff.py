"""Compares two files."""
from gendiff.gendiff_func import generate_diff
from gendiff.cli import parse_args


def main():
    inputs = parse_args()
    return generate_diff(
        inputs.first_file,
        inputs.second_file,
    )


if __name__ == '__main__':
    main()
