## 文件结构
默认情况下文件目录如下(提交的代码包中不含语料和预处理后的pkl和json，即不含中间文件，请按照README来进行目录构建和代码运行)
```
├── input.txt (默认输入)
├── output.txt (默认输出)
├── README.md
├── requirements.txt(运行gpt.py和optuna调参时才需要)
├── src
    ├──
    ├── benchmark.py
    ├── main.py
    ├── gpt.py
    ├── params (存储optuna调参的结果)
    │   ├── params.txt
    ├── results
    │   ├── __init__.py
    │   ├── detect.py
    │   ├── three_grammer
    │   │   ├── results.txt  
    │   └── two_grammer
    │       ├── results.txt
    ├── three_grammer (三元的中间文件目录,我提交的此文件夹为空,train后会有内容)
    │   ├── n2w.json
    │   ├── three_grammer_times.pkl
    │   ├── w2n.json
    │   └── word_times.json
    ├── train
    │   ├── __init__.py
    │   ├── train_three_grammer.py
    │   └── train_two_grammer.py
    ├── two_grammer  (二元的中间文件目录,我提交的此文件夹为空,train后会有内容)
    │   ├── n2w.json
    │   ├── two_grammer_times.pkl
    │   ├── w2n.json
    │   └── word_times.json
    ├── utils
    │   ├── __init__.py
    │   └── utils.py
    ├── 拼音汉字表 (汉字拼音表,我提交的此文件夹为空,记得添加内容)
    │   ├── README.txt
    │   ├── 一二级汉字表.txt
    │   └── 拼音汉字表.txt
    ├── 测试语料 (建议将测试语料放在这里,我提交的此文件夹为空,记得添加内容)
    │   ├── std_input.txt
    │   └── std_output.txt
    ├── 语料库 (训练使用的语料库，可以在此目录下增加其他语料库，我提交的此文件夹为空,记得添加内容)
    │   ├── SMP2020 (语料库1，默认不使用)
    │   │   ├── README.txt
    │   │   └── usual_train_new.txt
    │   └── sina_news_gbk (语料库2，默认只使用该语料库)
    │       ├── 2016-04.txt
    │       ├── 2016-05.txt
    │       ├── 2016-06.txt
    │       ├── 2016-07.txt
    │       ├── 2016-08.txt
    │       ├── 2016-09.txt
    │       ├── 2016-10.txt
    │       ├── 2016-11.txt
    │       └── README.txt
```
## 程序运行
#### 训练
首先需要使用train目录下的train_two_grammer和train_three_grammer来统计二元和三元字的词频并存储,首先cd到train目录下，然后需要输入`python train_two_grammer {参数}`以及`pyhton train_three_grammer {参数}`来运行,参数如下,其中update项为必填项，其含义为是否在已经训练好的模型基础上继续训
```
usage: train_two_grammer.py [-h] [--vacabulary_path VACABULARY_PATH] [--word_times_path WORD_TIMES_PATH]
                            [--first_word_times_path FIRST_WORD_TIMES_PATH] [--w2n_path W2N_PATH] [--n2w_path N2W_PATH]
                            [--train_dataset_path TRAIN_DATASET_PATH] [--encoding ENCODING] [--key KEY]
                            [--output_path_times OUTPUT_PATH_TIMES]
```
`vacabulary_path`是词典的路径
`word_times_path`单字词频的存储位置,应为json,
`w2n_path`是字到number的映射存储位置
`n2w_path`是number到字的映射存储位置
`first_word_times_path`是首字的频数存储位置
`output_path_times`统计好的词频文件放置位置
`train_dataset_path`训练集路径
`encoding`训练集所需的encoding,默认为gbk
`key`训练集中有用内容的键值,默认为html
#### 运行
使用`python main.py {参数}`来运行,参数如下
```
usage: main.py [-h] [--word_times_path WORD_TIMES_PATH] [--w2n_path W2N_PATH] [--n2w_path N2W_PATH]
               [--first_word_times_path FIRST_WORD_TIMES_PATH] [--first_word FIRST_WORD]
               [--two_grammer_model_path TWO_GRAMMER_MODEL_PATH] [--three_grammer_model_path THREE_GRAMMER_MODEL_PATH]
               [--output_path OUTPUT_PATH] [--std_output_path STD_OUTPUT_PATH] [--input_path INPUT_PATH]
               [--read_mode READ_MODE] [--model_mode MODEL_MODE] [--lambda1 LAMBDA1] [--lambda2 LAMBDA2] [--lambda3 LAMBDA3]
               [--adjust ADJUST]
```
`word_times_path`即存储好的单字词频的文件路径,应为json,
`w2n_path`是字到number的映射
`n2w_path`是number到字的映射
`first_word_times_path`是首字的频数
`first_word`代表是否把首字的概率设置为首字的频数,默认为0,即不设置，1为设置
`two_grammer_model_path`是要加载的二元词频文件(即二元模型文件,train中存储为pkl)
`three_grammer_model_path`同上理
`output_path`为把输出存储到哪个文件,若mode为cmd则无效
`input_path`为输入的读取文件，若mode为cmd则无效
`read_mode`，若为file则从文件中读取,若为cmd则从命令行读取,默认为file
`model_mode` 可以输入two_grammer活three_grammer，默认为前者
`lambda1,lambda2,lambda3`分别代表3,2,1元语法的占比,
`adjust`为1时则会进行optuna调参，可以设置调参的范围和步长
*注：以上参数都有设置好的默认值，默认情况下会直接加载train的默认设置中得到的二元模型，可以更改model_model来跑三元模型，注意output_path的设置，以免覆盖掉您之前跑的结果*

## 评价
上述运行结束后会进行一次评价，如果想对某一个输出的文件进行单独评价可如下运行`python benchmark.py --output_path {要测试的文件} --std_output_path {标准答案}`,评价的内容为字准确率和句准确率以及首字准确率