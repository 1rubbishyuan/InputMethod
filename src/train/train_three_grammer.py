import numpy as np
import math
import os
import json
import pandas as pd
from tqdm import tqdm
import time
import pickle
from argparse import ArgumentParser
import re

# import threading

argumentParser = ArgumentParser()
argumentParser.add_argument(
    "--vacabulary_path", default="../拼音汉字表/一二级汉字表.txt"
)
argumentParser.add_argument(
    "--word_times_path", default="../three_grammer/word_times.json"
)
argumentParser.add_argument(
    "--first_word_times_path", default="../three_grammer/first_word_times.json"
)
argumentParser.add_argument("--w2n_path", default="../three_grammer/w2n.json")
argumentParser.add_argument("--n2w_path", default="../three_grammer/n2w.json")
argumentParser.add_argument("--train_dataset_path", default="../语料库/sina_news_gbk")
argumentParser.add_argument("--encoding", default="gbk")
argumentParser.add_argument("--key", default="html")
argumentParser.add_argument(
    "--output_path_times", default="../three_grammer/three_grammer_times.pkl"
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
    with open(args.vacabulary_path, "r") as f:
        for line in f:
            for c in line:
                vacabulary_dict[c] = 0
    trainDatasets = os.listdir(args.train_dataset_path)
    trainDatasets = [i for i in trainDatasets if i != "README.txt" and i != ".DS_Store"]
    for trainDataset in tqdm(trainDatasets):
        trian_dataset_path = args.train_dataset_path
        # print(trian_dataset_path)
        with open(
            os.path.join(trian_dataset_path, trainDataset), "r", encoding=args.encoding
        ) as f:
            for line in tqdm(f):
                # print(line)
                try:
                    data = json.loads(line)
                    data = data[args.key]
                    for c in data:
                        try:
                            vacabulary_dict[c] += 1
                        except:
                            continue
                except:
                    # print(line)
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


def update_sheet(train_path, trainDatasets, record, w2n, content: str, encoding: str):
    # k = 0

    def collect(trainDataset):
        with open(os.path.join(train_path, trainDataset), "r", encoding=encoding) as f:
            for line in tqdm(f):
                try:
                    data = json.loads(line)
                    data = data[content]
                    for i, word in enumerate(data):
                        if i == len(data) - 3:
                            break
                        try:
                            record[f"{word}{data[i+1]}{data[i+2]}"] += 1
                        except KeyError:
                            record[f"{word}{data[i+1]}{data[i+2]}"] = 1
                except:
                    # k += 1
                    continue

    for trainDataset in tqdm(trainDatasets):
        collect(trainDataset)
        # t = threading.Thread(target=collect, args=(trainDataset,))
        # threads.append(t)
        # t.start()
    # for t in threads:
    #     t.join()

    return record


def train_three_grammer_times():
    # if args.update == 1:
    #     with open(args.output_path_times, "rb") as f:
    #         record = pickle.load(f)
    #     trainDatasets = get_dataSets(args.train_dataset_path)
    #     w2n = get_word_to_number(args.w2n_path)
    #     record = update_sheet(
    #         args.train_dataset_path,
    #         trainDatasets,
    #         record,
    #         w2n,
    #         "content",
    #         encoding="utf-8",
    #     )
    #     with open(args.output_path_times, "wb") as f:
    #         pickle.dump(record, f)
    # else:
    w2n = get_word_to_number(args.w2n_path)
    # n2w = get_number_to_word()
    # word_times = get_word_times()
    trainDatasets = get_dataSets(args.train_dataset_path)
    record = {}
    record = update_sheet(
        args.train_dataset_path,
        trainDatasets,
        record,
        w2n,
        args.key,
        encoding=args.encoding,
    )
    with open(args.output_path_times, "wb") as f:
        pickle.dump(record, f)


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
    print("get_three_grammer")
    train_three_grammer_times()
