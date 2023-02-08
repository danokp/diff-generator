import os
import pytest


from gendiff.generate_diff import generate_diff


DIR_PATH = os.path.join(os.path.dirname(__file__), 'fixtures')
TEST_FILES = {
    'json': ['file1_rec.json', 'file2_rec.json'],
    'yaml': ['file1_rec.yaml', 'file2_rec.yaml'],
}
TEST_FORMATS = {
    'stylish': 'answer_stylish_file1_file2_rec.txt',
    'plain': 'answer_plain_file1_file2_rec.txt',
    'json': 'answer_json_file1_file2_rec.txt',
}
TEST_WRONG_FORMATS = ['stylis', 'plai', 'jsoN']


def write_answer_from_file(path):
    with open(path) as file:
        return ''.join(file.readlines())


def make_path_to_file(file_name):
    return os.path.join(DIR_PATH, file_name)


@pytest.fixture(params=TEST_FILES)
def test_files(request):
    return TEST_FILES[request.param]


@pytest.fixture(params=TEST_FORMATS)
def test_formats(request):
    return request.param, TEST_FORMATS[request.param]


@pytest.fixture(params=TEST_WRONG_FORMATS)
def test_wrong_formats(request):
    return request.param


def test_gendiff(test_files, test_formats):
    first_file, second_file = test_files
    format, answer = test_formats
    assert generate_diff(
        make_path_to_file(first_file), make_path_to_file(second_file), format
    ) == write_answer_from_file(make_path_to_file(answer))


def test_gendiff_empty():
    test_gendiff(['empty.json', 'empty.json'], ['stylish', 'answer_empty.txt'])


def test_gendiff_exception(test_files, test_wrong_formats):
    first_file, second_file = test_files
    with pytest.raises(ValueError) as exception:
        generate_diff(
            make_path_to_file(first_file),
            make_path_to_file(second_file),
            test_wrong_formats
        )
    assert str(exception.value) == "Choose one of the available formats: " \
                                   "['stylish', 'plain', 'json']."


def test_parse_exception():
    first_file = 'wrong_file_format.txt'
    second_file = 'wrong_file_format.txt'
    with pytest.raises(ValueError) as exception:
        generate_diff(
            make_path_to_file(first_file),
            make_path_to_file(second_file),
        )
    assert str(exception.value) == 'Only json, yaml or yml formats are available.'
