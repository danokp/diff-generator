from gendiff.gendiff_func import generate_diff
import os


DIR_PATH = os.path.join(os.path.dirname(__file__), 'fixtures')
path_json_file1 = os.path.join(DIR_PATH, 'file1.json')
path_json_file2 = os.path.join(DIR_PATH, 'file2.json')
with open(DIR_PATH+'/answer_json_file1_file2.txt') as file:
    answer_json_file1_file2 = ''.join(file.readlines())


def test_gendiff():
    assert generate_diff(path_json_file1, path_json_file2) == answer_json_file1_file2
