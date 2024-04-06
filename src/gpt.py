import openai
import os

input_path = "测试语料/std_input.txt"
ouput_path = "gpt_test.txt"
openai_key = os.getenv("OPENAI_API_KEY")
print(openai_key)
results = []
with open(input_path, "r") as f:
    k = 0
    for line in f:
        k += 1
        completion = openai.ChatCompletion.create(
            model="gpt-4-1106",
            messages=[
                {
                    "role": "user",
                    "content": f"请把下列拼音翻译为汉字 '{line}' ,输出时只输出答案,不能加任何空格和标点",
                }
            ],
        )
        try:
            print(completion.choices[0].message.content)
            # results.append(completion.choices[0].message.content)
            with open(ouput_path, "a") as fout:
                fout.write(f"{completion.choices[0].message.content}\n")
        except:
            print(f"{k}: {completion.choices[0].message}")
            results.append(completion.choices[0].message)
            with open("except.txt", "a") as fout:
                fout.write(f"{k:} {completion.choices[0].message}\n")
