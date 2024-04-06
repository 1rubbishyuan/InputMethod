from argparse import ArgumentParser
from results.detect import *

argumentparse = ArgumentParser()
argumentparse.add_argument("--output_path", required=True)
argumentparse.add_argument("--std_output_path", default="测试语料/std_output.txt")
args = argumentparse.parse_args()


if __name__ == "__main__":
    detect(args.output_path, args.std_output_path)
    first_word_detect(args.output_path, args.std_output_path)
    # a = [1, 2, 3]
    # for k in a:
    #     k = k + 1
    # print(a)
