from gendiff.gendiff_func import generate_diff
import os
import pytest


def write_answer_from_file(path):
    with open(path) as file:
        return ''.join(file.readlines())

DIR_PATH = os.path.join(os.path.dirname(__file__), 'fixtures')
path_json_file1 = os.path.join(DIR_PATH, 'file1.json')
path_json_file2 = os.path.join(DIR_PATH, 'file2.json')
path_empty_file = os.path.join(DIR_PATH, 'empty.json')
path_json_file1_rec = os.path.join(DIR_PATH, 'file1_rec.json')
path_json_file2_rec = os.path.join(DIR_PATH, 'file2_rec.json')
path_yaml_file1 = os.path.join(DIR_PATH, 'file1.yaml')
path_yaml_file2 = os.path.join(DIR_PATH, 'file2.yaml')
path_yaml_file1_rec = os.path.join(DIR_PATH, 'file1_rec.yaml')
path_yaml_file2_rec = os.path.join(DIR_PATH, 'file2_rec.yaml')

answer_stylish_file1_file2_rec = write_answer_from_file(DIR_PATH+'/answer_json_file1_file2_rec.txt')
answer_plain_file1_file2_rec = write_answer_from_file(DIR_PATH+'/answer_plain_file1_file2_rec.txt')
answer_file1_file2 = write_answer_from_file(DIR_PATH+'/answer_json_file1_file2.txt')
answer_help_option = write_answer_from_file(DIR_PATH+'/answer_help_option.txt')

@pytest.mark.parametrize('first_file, second_file, answer, format',[
    (path_empty_file, path_empty_file, '{}', 'stylish'),
    (path_yaml_file1, path_yaml_file2, answer_file1_file2, 'stylish'),
    (path_json_file1, path_json_file2, answer_file1_file2, 'stylish'),
    (path_yaml_file1_rec, path_yaml_file2_rec, answer_stylish_file1_file2_rec, 'stylish'),
    (path_json_file1_rec, path_json_file2_rec, answer_stylish_file1_file2_rec, 'stylish'),
    (path_yaml_file1_rec, path_yaml_file2_rec, answer_plain_file1_file2_rec, 'plain'),
    (path_json_file1_rec, path_json_file2_rec, answer_plain_file1_file2_rec, 'plain'),
])
def test_gendiff(first_file, second_file, format, answer):
    assert generate_diff(first_file, second_file, format) == answer



# def test_gendiff_options():
#     assert == answer_help_option