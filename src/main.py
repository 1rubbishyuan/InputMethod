import time
import pandas as pd
import numpy as np
import pickle
import os
import optuna
from utils.utils import (
    get_word_to_number,
    get_number_to_word,
    get_word_times,
    get_first_word_times,
)
from results.detect import detect, first_word_detect
from argparse import ArgumentParser
from tqdm import tqdm

# from results.detect import detect

argumentParser = ArgumentParser()
argumentParser.add_argument("--word_times_path", default="two_grammer/word_times.json")
argumentParser.add_argument("--w2n_path", default="two_grammer/w2n.json")
argumentParser.add_argument("--n2w_path", default="two_grammer/n2w.json")
argumentParser.add_argument(
    "--first_word_times_path", default="two_grammer/first_word_times.json"
)
argumentParser.add_argument("--first_word", default=0)
argumentParser.add_argument(
    "--two_grammer_model_path", default="two_grammer/two_grammer_times.pkl"
)
argumentParser.add_argument(
    "--three_grammer_model_path", default="three_grammer/three_grammer_times.pkl"
)
argumentParser.add_argument("--output_path", default="../output.txt")
argumentParser.add_argument("--std_output_path", default="测试语料/std_output.txt")
argumentParser.add_argument("--input_path", default="../input.txt")
argumentParser.add_argument(
    "--read_mode", default="file"
)  # 如果是cmd 就说明从命令行输入
argumentParser.add_argument("--model_mode", default="two_grammer")
argumentParser.add_argument("--lambda1", default=20)
argumentParser.add_argument("--lambda2", default=1)
argumentParser.add_argument("--lambda3", default=0)
argumentParser.add_argument("--adjust", default=0)
args = argumentParser.parse_args()


def get_map():
    map = {}
    with open("拼音汉字表/拼音汉字表.txt", "r", encoding="gbk") as f:
        for line in f:
            word_list = line.split(" ")
            map[word_list[0]] = [i.strip("\n") for i in word_list[1:]]
    return map


def two_grammer_vertible(
    first_word_times, line, vacabulary, lambda1, lambda2, two_grammer, wtn, map
):
    word_list = [i.strip("\n") for i in line.split(" ")]
    word_list = [map[i] for i in word_list]
    sum = np.sum(list(vacabulary.values()))
    final_list = []
    first_list = []
    if args.first_word == "1":
        sum = np.sum(list(first_word_times.values()))
        for i, word in enumerate(word_list[0]):
            first_list.append([0, word, first_word_times[word] / sum])
    else:
        for i, word in enumerate(word_list[0]):
            first_list.append([0, word, vacabulary[word] / sum])
    final_list.append(first_list)
    for i in range(len(word_list)):
        if i == 0:
            continue
        tmp_list = []
        for j, word in enumerate(word_list[i]):
            least = 0
            least_index = 0
            for k, last in enumerate(final_list[i - 1]):
                mid = 0
                try:
                    mid = (two_grammer[wtn[word], wtn[last[1]]]) / (vacabulary[last[1]])
                except:
                    mid = 0
                now = last[2] * (lambda1 * mid + lambda2 * (vacabulary[word]) / sum)
                if now > least:
                    least = now
                    least_index = k
            tmp_list.append([least_index, word, least])
        final_list.append(tmp_list)
    final_reference_list = [last[2] for last in final_list[-1]]
    final_least_index = np.argmax(final_reference_list)

    chase = final_least_index
    ans = []
    for i in range(len(final_list) - 1, -1, -1):
        ans.append(final_list[i][chase][1])
        chase = final_list[i][chase][0]
    ans.reverse()
    return ans


def two_grammer_inputMethod(inputFile):
    lambda1 = int(args.lambda2)
    lambda2 = int(args.lambda3)
    wtn = get_word_to_number(args.w2n_path)
    two_grammer: pd.DataFrame = pd.read_pickle(args.two_grammer_model_path)
    two_grammer = two_grammer.to_numpy()
    map = get_map()
    vacabulary = get_word_times(args.word_times_path)
    sum = np.sum(list(vacabulary.values()))
    first_word_times = get_first_word_times(args.first_word_times_path)
    start_time = time.time()
    if args.read_mode == "file":
        with open(args.output_path, "w", encoding="utf-8") as f:
            f.write("")
        with open(inputFile, "r") as f:
            for line in f:
                ans = two_grammer_vertible(
                    first_word_times,
                    line,
                    vacabulary,
                    lambda1,
                    lambda2,
                    two_grammer,
                    wtn,
                    map,
                )
                with open(args.output_path, "a", encoding="utf-8") as f:
                    f.write(f"{''.join(ans)}\n")
        end_time = time.time()
        print("程序运行时间：", end_time - start_time, "秒")
    elif args.read_mode == "cmd":
        while True:
            line = input()
            if line == "quit":
                break
            ans = two_grammer_vertible(
                line, vacabulary, lambda1, lambda2, two_grammer, wtn, map
            )
            print(f"{''.join(ans)}")


def three_grammer_vertible(
    first_word_times,
    line,
    word_times,
    lambda1,
    lambda2,
    lambda3,
    three_grammer,
    two_grammer,
    wtn,
    map,
):
    word_list = [i.strip("\n") for i in line.split(" ")]
    word_list = [map[i] for i in word_list]
    sum = np.sum(list(word_times.values()))
    final_list = []
    first_list = []
    if args.first_word == "1":
        sum = np.sum(list(first_word_times.values()))
        for i, word in enumerate(word_list[0]):
            first_list.append([0, word, first_word_times[word] / sum])
    else:
        for i, word in enumerate(word_list[0]):
            first_list.append([0, word, word_times[word] / sum])
    final_list.append(first_list)
    second_list = []
    for i, word in enumerate(word_list[1]):
        least = 0
        least_index = 0
        for k, last in enumerate(final_list[0]):
            mid2 = 0
            try:
                mid2 = (two_grammer[wtn[word], wtn[last[1]]]) / (word_times[last[1]])
                # if two_grammer[wtn[word], wtn[last[1]]] > 30:
                # print(
                #     f"{lambda1}:{lambda2}:{lambda3} {mid2} / {last[1]}{word}: {two_grammer[wtn[word], wtn[last[1]]]} / {word_times[last[1]]} :{last[2] * (lambda2 * mid2 + lambda3 * (word_times[word]) / sum)}"
                # )
            except:
                mid2 = 0
            now = last[2] * (lambda2 * mid2 + lambda3 * (word_times[word]) / sum)
            if now > least:
                least = now
                least_index = k
        second_list.append([least_index, word, least])
    final_list.append(second_list)
    # print(second_list)
    for i in range(len(word_list)):
        if i == 0:
            continue
        if i == 1:
            continue
        tmp_list = []
        for j, word in enumerate(word_list[i]):
            least = 0
            least_index = 0
            for k, last in enumerate(final_list[i - 1]):
                for m, llast in enumerate(final_list[i - 2]):
                    mid1 = 0
                    try:
                        mid1 = (
                            three_grammer[f"{llast[1]}{last[1]}{word}"]
                            * three_grammer[f"{llast[1]}{last[1]}{word}"]
                            / (two_grammer[wtn[last[1]], wtn[llast[1]]])
                        )
                    except:
                        mid1 = 0
                    mid2 = 0
                    try:
                        mid2 = (
                            (two_grammer[wtn[word], wtn[last[1]]])
                            * (two_grammer[wtn[word], wtn[last[1]]])
                            / (word_times[last[1]])
                        )
                    except:
                        mid2 = 0
                    now = last[2] * (
                        lambda1 * mid1
                        + lambda2 * mid2
                        + lambda3 * (word_times[word]) / sum
                    )
                    if now > least:
                        # print(
                        #     f"{llast[1]}{last[1]}{word} : {m} {k} : {final_list[i-1][k][1],final_list[i - 2][m][1]}"
                        # )
                        least = now
                        least_index = k
                        # final_list[i - 1][k][0] = m
            tmp_list.append([least_index, word, least])
        final_list.append(tmp_list)
    final_reference_list = [last[2] for last in final_list[-1]]
    final_least_index = np.argmax(final_reference_list)

    chase = final_least_index
    ans = []
    # print(final_list[-1])
    for i in range(len(final_list) - 1, -1, -1):
        # print(chase)
        # print(final_list[i])
        ans.append(final_list[i][chase][1])
        chase = final_list[i][chase][0]
    ans.reverse()
    return ans


def three_grammer_inputMethod(inputFile):
    lambda1 = int(args.lambda1)
    lambda2 = int(args.lambda2)
    lambda3 = int(args.lambda3)
    wtn = get_word_to_number(args.w2n_path)
    map = get_map()
    first_word_times = get_first_word_times(args.first_word_times_path)
    word_times = get_word_times(args.word_times_path)
    two_grammer: pd.DataFrame = pd.read_pickle(args.two_grammer_model_path)
    two_grammer = two_grammer.to_numpy()
    with open(args.three_grammer_model_path, "rb") as f:
        three_grammer = pickle.load(f)
    print("start")
    start_time = time.time()
    if args.read_mode == "file":
        with open(args.output_path, "w", encoding="utf-8") as f:
            f.write("")
        with open(inputFile, "r") as f:
            for line in tqdm(f):
                ans = three_grammer_vertible(
                    first_word_times,
                    line,
                    word_times,
                    lambda1,
                    lambda2,
                    lambda3,
                    three_grammer,
                    two_grammer,
                    wtn,
                    map,
                )
                with open(args.output_path, "a", encoding="utf-8") as f:
                    f.write(f"{''.join(ans)}\n")
        end_time = time.time()
        print("程序运行时间：", end_time - start_time, "秒")
    elif args.read_mode == "cmd":
        while True:
            line = input()
            if line == "quit":
                break
            lambda1 = input("lambda1:")
            lambda1 = int(lambda1)
            lambda2 = input("lambda1:")
            lambda2 = int(lambda2)
            ans = three_grammer_vertible(
                line,
                word_times,
                lambda1,
                lambda2,
                lambda3,
                three_grammer,
                two_grammer,
                wtn,
                map,
            )
            print(f"{''.join(ans)}")


def three_grammer_inputMethod_adjust(inputFile, lambda1, lambda2, lambda3):
    lambda1 = lambda1
    lambda2 = lambda2
    lambda3 = lambda3
    wtn = get_word_to_number(args.w2n_path)
    map = get_map()
    word_times = get_word_times(args.word_times_path)
    start_time = time.time()
    two_grammer: pd.DataFrame = pd.read_pickle(args.two_grammer_model_path)
    two_grammer = two_grammer.to_numpy()
    with open(args.three_grammer_model_path, "rb") as f:
        three_grammer = pickle.load(f)
    print("start")
    if args.read_mode == "file":
        with open(args.output_path, "w", encoding="utf-8") as f:
            f.write("")
        with open(inputFile, "r") as f:
            for line in tqdm(f):
                ans = three_grammer_vertible(
                    line,
                    word_times,
                    lambda1,
                    lambda2,
                    lambda3,
                    three_grammer,
                    two_grammer,
                    wtn,
                    map,
                )
                with open(args.output_path, "a", encoding="utf-8") as f:
                    f.write(f"{''.join(ans)}\n")
        end_time = time.time()
        print("程序运行时间：", end_time - start_time, "秒")


def objective(trial):
    param = {
        "lambda1": trial.suggest_int("lambda1", 300000, 800000, step=50000),
        "lambda2": trial.suggest_int("lambda2", 100, 1000, step=50),
        "lambda3": trial.suggest_int("lambda3", 0, 50, step=2),
    }
    three_grammer_inputMethod_adjust(
        args.input_path, param["lambda1"], param["lambda2"], param["lambda3"]
    )
    loss = 1 - detect(args.output_path, args.std_output_path)
    with open(os.path.join("params", "params.txt"), "a") as f:
        f.write(
            f"{param['lambda1']}:{param['lambda2']}:{param['lambda3']}-----{1-loss}\n"
        )
    print(loss)
    return loss


if __name__ == "__main__":
    if args.adjust == "1":
        study = optuna.create_study(direction="minimize")
        study.optimize(objective, 100)
        params = study.best_params
        print(f"the best params are:\n {params}")
        with open(os.path.join("params", "best_param.txt"), "w") as fout:
            fout.write(params)
    else:
        if args.model_mode == "two_grammer":
            two_grammer_inputMethod(args.input_path)
        elif args.model_mode == "three_grammer":
            three_grammer_inputMethod(args.input_path)
        if args.read_mode == "file":
            detect(args.output_path, args.std_output_path)
            first_word_detect(args.output_path, args.std_output_path)
