from gendiff.generate_diff import generate_diff
import os
import pytest


def write_answer_from_file(path):
    with open(path) as file:
        return ''.join(file.readlines())


def make_path_to_file(file_name):
    return os.path.join(DIR_PATH, file_name)


DIR_PATH = os.path.join(os.path.dirname(__file__), 'fixtures')

json_file1 = 'file1.json'
json_file2 = 'file2.json'
empty_file = 'empty.json'
json_file1_rec = 'file1_rec.json'
json_file2_rec = 'file2_rec.json'
yaml_file1 = 'file1.yaml'
yaml_file2 = 'file2.yaml'
yaml_file1_rec = 'file1_rec.yaml'
yaml_file2_rec = 'file2_rec.yaml'

answer_stylish_file1_file2_rec = 'answer_stylish_file1_file2_rec.txt'
answer_plain_file1_file2_rec = 'answer_plain_file1_file2_rec.txt'
answer_json_file1_file2_rec = 'answer_json_file1_file2_rec.txt'
answer_file1_file2 = 'answer_json_file1_file2.txt'
answer_empty = 'answer_empty.txt'


@pytest.mark.parametrize('first_file, second_file, answer, format', [
    (empty_file, empty_file, answer_empty, 'stylish'),
    (yaml_file1, yaml_file2, answer_file1_file2, 'stylish'),
    (json_file1, json_file2, answer_file1_file2, 'stylish'),
    (yaml_file1_rec, yaml_file2_rec, answer_stylish_file1_file2_rec, 'stylish'),
    (json_file1_rec, json_file2_rec, answer_stylish_file1_file2_rec, 'stylish'),
    (yaml_file1_rec, json_file2_rec, answer_stylish_file1_file2_rec, 'stylish'),
    (yaml_file1_rec, yaml_file2_rec, answer_plain_file1_file2_rec, 'plain'),
    (json_file1_rec, json_file2_rec, answer_plain_file1_file2_rec, 'plain'),
    (json_file1_rec, json_file2_rec, answer_json_file1_file2_rec, 'json'),
    (yaml_file1_rec, yaml_file2_rec, answer_json_file1_file2_rec, 'json'),
])
def test_gendiff(first_file, second_file, answer, format):
    assert generate_diff(
        make_path_to_file(first_file), make_path_to_file(second_file), format
    ) == write_answer_from_file(make_path_to_file(answer))


@pytest.mark.parametrize('first_file, second_file, answer', [
    (empty_file, empty_file, answer_empty),
    (yaml_file1, yaml_file2, answer_file1_file2),
    (json_file1, json_file2, answer_file1_file2),
    (yaml_file1_rec, yaml_file2_rec, answer_stylish_file1_file2_rec),
    (json_file1_rec, json_file2_rec, answer_stylish_file1_file2_rec),
])
def test_gendiff_no_format(first_file, second_file, answer):
    assert generate_diff(
        make_path_to_file(first_file), make_path_to_file(second_file)
    ) == write_answer_from_file(make_path_to_file(answer))


@pytest.mark.parametrize('first_file, second_file, answer, format', [
    (yaml_file1_rec, yaml_file2_rec, answer_stylish_file1_file2_rec, 'stylis'),
    (yaml_file1_rec, yaml_file2_rec, answer_plain_file1_file2_rec, 'plai'),
    (yaml_file1_rec, yaml_file2_rec, answer_json_file1_file2_rec, 'jsoN'),
])
def test_gendiff_exception(first_file, second_file, answer, format):
    with pytest.raises(Exception):
        generate_diff(
            make_path_to_file(first_file),
            make_path_to_file(second_file),
            format
        )
