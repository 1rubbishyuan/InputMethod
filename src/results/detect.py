from argparse import ArgumentParser


def detect(output_path, std_output_path):
    output = []
    with open(output_path, "r", encoding="utf-8") as f:
        for line in f:
            output.append(line.strip("\n"))
    right = []
    with open(std_output_path, "r", encoding="utf-8") as f:
        for line in f:
            right.append(line.strip("\n"))
    word = 0
    word_right = 0
    sentence = 0
    sentence_right = 0
    for i in range(len(output)):
        tmp = 0
        tmp_right = 0
        for j, c in enumerate(output[i]):
            tmp += 1
            try:
                if c == right[i][j]:
                    tmp_right += 1
            except:
                pass
            word += tmp
            word_right += tmp_right
        if tmp == tmp_right:
            sentence_right += 1
        sentence += 1
    print(f"word right: {word_right/word}")
    print(f"sentence right: {sentence_right/sentence}")
    return sentence_right / sentence


def first_word_detect(output_path, std_output_path):
    output = []
    with open(output_path, "r", encoding="utf-8") as f:
        for line in f:
            output.append(line.strip("\n"))
    right = []
    with open(std_output_path, "r", encoding="utf-8") as f:
        for line in f:
            right.append(line.strip("\n"))
    firstword = 0
    firstword_right = 0
    for i in range(len(right)):
        firstword += 1
        if output[i][0] == right[i][0]:
            firstword_right += 1
    print(f"first_word_right: {firstword_right/firstword}")
    return firstword_right / firstword
