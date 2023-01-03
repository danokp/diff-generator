#!/usr/bin/env python3
import argparse
import json


def main():
    inputs = parse_args()
    diff_result = generate_diff(
        inputs.first_file,
        inputs.second_file
    )
    print(diff_result)

def parse_args():
    parser = argparse.ArgumentParser(
        prog='gendiff',
        description='Compares two configuration files and shows a difference.')
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format',
                        help='set format of output')
    args = parser.parse_args()
    return args


def _fill(name, size, sep=' '):
    return name.rjust(size-1, sep).ljust(size, sep)


def generate_diff(import_file_1, import_file_2):
    file_1_dict = json.load(open(import_file_1))
    file_2_dict = json.load(open(import_file_2))
    diff_result_list = []
    for k, v in file_1_dict.items():
        if k in file_2_dict:
            v_2 = file_2_dict.pop(k)
            if v == v_2:
                diff_result_list.append((k, v, ''))
            else:
                diff_result_list.append((k, v, '-'))
                diff_result_list.append((k, v_2, '+'))
        else:
            diff_result_list.append((k, v, '-'))
    for k, v in file_2_dict.items():
        diff_result_list.append((k, v, '+'))
    diff_result = '{\n' + '\n'.join(
        map(
            lambda tupl: f'{_fill(tupl[2], size=4)}{tupl[0]}: {tupl[1]}',
            sorted(diff_result_list,
                   key=lambda x: x[0])
        )
    ) + '\n}'
    return diff_result


if __name__ == '__main__':
    main()
