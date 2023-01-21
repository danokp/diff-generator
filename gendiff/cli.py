"""Make positional and optional arguments."""
import argparse


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
        choices=['stylish', 'plain', 'json'],
        default='stylish',
    )
    return parser.parse_args()
