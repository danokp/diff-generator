import os
import sys


from gendiff.cli import parse_args
from tests.test_gendiff import test_formats, test_files # noqa F401


def test_parse_args(test_formats, test_files):
    first_file, second_file = test_files
    format = test_formats[0]
    sys.argv = [
        'gendiff',
        first_file,
        second_file,
        '-f',
        format,
    ]
    args = parse_args()
    assert args.first_file == first_file
    assert args.second_file == second_file
    assert args.format == format


def test_cli_launch():
    a = os.system('poetry run gendiff -h')
    assert a == 0
