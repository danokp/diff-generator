"""Compares two files."""
import argparse

from gendiff.gendiff_func import generate_diff


def main():
    inputs = parse_args()
    return generate_diff(
        inputs.first_file,
        inputs.second_file,
    )


def parse_args():
    """Return the files to compare.

    Create command-line options (-h (--help), -f (--format))
    and arguments (first_file, second_file).

    Returns:
        Namespace with files to compare and their format.
    """
    parser = argparse.ArgumentParser(
        prog='gendiff',
        description='Compares two configuration files and shows a difference.',
    )
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument(
        '-f',
        '--format',
        help='set format of output',
    )
    return parser.parse_args()


if __name__ == '__main__':
    main()
