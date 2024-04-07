import numpy as np
import math
import os
import json
import pandas as pd
from tqdm import tqdm
import time
import pickle
from argparse import ArgumentParser
import threading
import re

argumentParser = ArgumentParser()
argumentParser.add_argument(
    "--vacabulary_path", default="../拼音汉字表/一二级汉字表.txt"
)
argumentParser.add_argument(
    "--word_times_path", default="../two_grammer/word_times.json"
)
argumentParser.add_argument(
    "--first_word_times_path", default="../two_grammer/first_word_times.json"
)
argumentParser.add_argument("--w2n_path", default="../two_grammer/w2n.json")
argumentParser.add_argument("--n2w_path", default="../two_grammer/n2w.json")
argumentParser.add_argument("--train_dataset_path", default="../语料库/sina_news_gbk")
argumentParser.add_argument("--encoding", default="gbk")
argumentParser.add_argument("--key", default="html")
argumentParser.add_argument(
    "--output_path_times", default="../two_grammer/two_grammer_times.pkl"
)
args = argumentParser.parse_args()


def cal_first_word_times():
    trainDatasets = os.listdir(args.train_dataset_path)
    trainDatasets = [i for i in trainDatasets if i != "README.txt" and i != ".DS_Store"]
    pattern = r"[，。：；、]"
    vacabulary_dict = {}
    with open(args.first_word_times_path, "w", encoding="utf-8") as json_file:
        json_file.write("")
    with open(args.vacabulary_path, "r") as f:
        for line in f:
            for c in line:
                vacabulary_dict[c] = 0
    for trainDataset in tqdm(trainDatasets):
        trian_dataset_path = args.train_dataset_path
        print(trian_dataset_path)
        with open(
            os.path.join(trian_dataset_path, trainDataset), "r", encoding=args.encoding
        ) as f:
            for line in tqdm(f):
                data = json.loads(line)
                data = data[args.key]
                data = re.split(pattern, data)
                for part in data:
                    try:
                        vacabulary_dict[part[0]] += 1
                    except:
                        continue
    with open(args.first_word_times_path, "w", encoding="utf-8") as json_file:
        json_file.write(json.dumps(vacabulary_dict, indent=4, ensure_ascii=False))


def cal_word_times():
    vacabulary_dict = {}
    with open(args.word_times_path, "w", encoding="utf-8") as json_file:
        json_file.write("")
    with open(args.vacabulary_path, "r") as f:
        for line in f:
            for c in line:
                vacabulary_dict[c] = 0
    trainDatasets = os.listdir(args.train_dataset_path)
    trainDatasets = [i for i in trainDatasets if i != "README.txt" and i != ".DS_Store"]
    for trainDataset in tqdm(trainDatasets):
        trian_dataset_path = args.train_dataset_path
        print(trian_dataset_path)
        with open(
            os.path.join(trian_dataset_path, trainDataset), "r", encoding=args.encoding
        ) as f:
            for line in tqdm(f):
                data = json.loads(line)
                data = data[args.key]
                for c in data:
                    try:
                        vacabulary_dict[c] += 1
                    except:
                        continue
    record = json.dumps(vacabulary_dict, indent=4, ensure_ascii=False)
    with open(args.word_times_path, "w", encoding="utf-8") as json_file:
        json_file.write(record)


def cal_n2w():
    with open(args.word_times_path, "r", encoding="utf-8") as f:
        data = dict(json.load(f))
    reverse = {}
    for i, key in enumerate(data.keys()):
        reverse[i] = key
    with open(args.n2w_path, "w", encoding="utf-8") as file:
        file.write(json.dumps(reverse, ensure_ascii=False))


def cal_w2n():
    with open(args.word_times_path, "r", encoding="utf-8") as f:
        all = dict(json.load(f))
        map = {}
        for i, key in enumerate(all.keys()):
            map[key] = i
        with open(args.w2n_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(map, ensure_ascii=False))


def update_sheet(train_path, trainDatasets, record, map, content: str, encodeing):
    k = 0
    for trainDataset in tqdm(trainDatasets):
        with open(os.path.join(train_path, trainDataset), "r", encoding=encodeing) as f:
            for line in tqdm(f):
                try:
                    data = json.loads(line)
                    data = data[content]
                    for i, word in enumerate(data):
                        if i == len(data) - 1:
                            break
                        try:
                            record[word][map[f"{data[i+1]}"]] += 1
                        except KeyError:
                            continue
                except:
                    k += 1
                    continue
    # print(f"k is : {k}")

    return record


def train_two_grammer_times():
    record = {}
    map = get_word_to_number(args.w2n_path)
    with open(args.word_times_path, "r", encoding="utf-8") as f:
        all = dict(json.load(f))
        length = len(all)
        for key in all.keys():
            record[key] = [0] * length
    trainDatasets = get_dataSets(args.train_dataset_path)

    record = update_sheet(
        args.train_dataset_path,
        trainDatasets,
        record,
        map,
        args.key,
        encodeing=args.encoding,
    )
    record = pd.DataFrame(record)
    record.to_pickle(args.output_path_times)


def get_dataSets(path):
    trainDatasets = os.listdir(path)
    trainDatasets = [i for i in trainDatasets if i != "README.txt" and i != ".DS_Store"]
    return trainDatasets


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


if __name__ == "__main__":
    print("get_word_times")
    cal_word_times()
    cal_w2n()
    cal_n2w()
    cal_first_word_times()
    print("get_two_grammer")
    train_two_grammer_times()
