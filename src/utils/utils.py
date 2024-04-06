import json


def get_word_times(path):
    vacabulary = {}
    with open(path, "r", encoding="utf-8") as f:
        vacabulary = dict(json.load(f))
    return vacabulary


def get_word_to_number(path):
    map = {}
    with open(path, "r", encoding="utf-8") as f:
        map = dict(json.load(f))
    return map


def get_number_to_word(path):
    reverse = {}
    with open(path, "r", encoding="utf-8") as f:
        reverse = dict(json.load(f))
    return reverse


def gbk_to_utf8(input_file, output_file):
    with open(input_file, "r") as f:
        for line in f:
            with open(output_file, "a") as fout:
                fout.write(line)


def get_first_word_times(path):
    first_word_times = {}
    with open(path, "r", encoding="utf-8") as f:
        first_word_times = dict(json.load(f))
    return first_word_times
