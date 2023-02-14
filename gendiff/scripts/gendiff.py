"""Compares two files."""
from gendiff.cli import parse_args
from gendiff.diff_generator import generate_diff


def main():
    inputs = parse_args()
    print(
        generate_diff(
            inputs.first_file,
            inputs.second_file,
            inputs.format,
        ),
    )


if __name__ == '__main__':
    main()
