from gendiff.gendiff_func import generate_diff
import os


def write_answer_from_file(path):
    with open(path) as file:
        return ''.join(file.readlines())

DIR_PATH = os.path.join(os.path.dirname(__file__), 'fixtures')
path_json_file1 = os.path.join(DIR_PATH, 'file1.json')
path_json_file2 = os.path.join(DIR_PATH, 'file2.json')
answer_file1_file2 = write_answer_from_file(DIR_PATH+'/answer_json_file1_file2.txt')
answer_help_option = write_answer_from_file(DIR_PATH+'/answer_help_option.txt')
path_yaml_file1 = os.path.join(DIR_PATH, 'file1.yaml')
path_yaml_file2 = os.path.join(DIR_PATH, 'file2.yaml')



def test_gendiff_json():
    assert generate_diff(path_json_file1, path_json_file2) == answer_file1_file2


def test_gendiff_yaml():
    assert generate_diff(path_yaml_file1, path_yaml_file2) == answer_file1_file2


# def test_gendiff_options():
#     assert == answer_help_option