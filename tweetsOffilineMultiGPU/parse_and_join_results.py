import os
from glob import glob
import  pandas as pd

# BASEPATH = "/sps/humanum/user/jroyolet/dev/llmBenchmarks/tweetsOffilineMultiGPU"
BASEPATH = "/home/jimena/work/dev/llmBenchmarks/tweetsOffilineMultiGPU"

MODELS = [
    "zephyr-7b-beta",
    "gpt-oss-20b",
    "Mistral-Small-3.1-24B-Instruct-2503",
    "Magistral-Small-2506",
    "Mistral-Small-24B-Instruct-2501",
    "max_model_len_8000_Qwen3-30B-A3B-Instruct-2507",
    "gpt-oss-120b",
    "Llama-3.3-70B-Instruct",
    "DeepSeek-R1-Distill-Llama-70B",
    "Mistral-Large-Instruct-2411"
]

ANNOTATIONS = {

    "multiple": [
        "voteintention/multiple/all",
        "support/multiple/all",
        # "criticism/multiple/all"
    ],

    "binary" : [
        "criticism/binary/lepen",
        "criticism/binary/macron",
        "criticism/binary/melenchon",
        "support/binary/lepen",
        "support/binary/macron",
        "support/binary/melenchon",
        "voteintention/binary/lepen",
        "voteintention/binary/macron",
        "voteintention/binary/melenchon",
    ]
}

CHOICES = {
    "multiple": ["Macron", "Mélenchon", "Le Pen", "None"],
    "binary" : ["YES", "NO"]
}

SETTINGS = ANNOTATIONS.keys()

def parseAnwers(whole_answer, setting):

    whole_answer = whole_answer \
        .strip() \
        .split('\n')[0] \
        .replace("(", "") \
        .replace(")", "") \
        .replace(":", "") \
        .replace("'", "") \
        .replace('"', "") \
        .replace(".", "") \
        .replace("·", "") \
        .replace(",", "")

    if setting == "binary":
        whole_answer = whole_answer.upper()


    annotation = whole_answer
    for choice in CHOICES[setting]:
        if whole_answer[:len(choice)] == choice:
            annotation = choice

    return annotation

def extract_data(model, annotation, setting, df=None, columns=[]):

    assert model in MODELS
    assert setting in SETTINGS

    folders = glob(os.path.join(BASEPATH, "outputs/v1", f"*{model}*"))
    assert len(folders) == 1
    folder = folders[0]
    # print(f"Reading results for model {model} at {folder}")

    # get free answers
    colname = "FREE-" + model
    path_free = os.path.join(folder, "free", annotation, "llm_answer_0.csv")
    df_free = pd.read_csv(path_free) \
        .fillna("None") \
        .rename(columns={"answer": colname})

    if df is not None:
        df = df.merge(df_free, on=['idx', 'tweet'])
    else:
        df = df_free

    # get guided answers
    colname = "GUIDED-" + model
    path_guided = os.path.join(folder, "guided", annotation, "llm_answer_0.csv")
    df_guided = pd.read_csv(path_guided) \
        .fillna("None") \
        .rename(columns={"answer": colname})
    df_guided[colname] = df_guided[colname].apply(lambda a: parseAnwers(a, setting))

    if "gpt-oss" in model:
        df_guided[colname] = df_guided[colname] \
            .apply(lambda s: s.split("assistantfinal")[-1])

    df = df.merge(df_guided, on=['idx', 'tweet'])

    columns.extend(["FREE-" + model, "GUIDED-" + model])

    return df, columns

for setting in ANNOTATIONS:

    for annotation in ANNOTATIONS[setting]:

        df = None
        columns = ["idx", "tweet"]

        for model in MODELS:
            try:
                df, columns = extract_data(model, annotation, setting, df, columns)
            except Exception as exc:
                print(exc)
                print("Continuing...")

        path = f"{annotation.replace('/', '_')}.csv"

        df[columns].to_csv(path, index=False)
        print(f"Results for annotation {annotation} results saved at {path}")
        os.system(f"xan shuffle {path} | xan slice -l 5 | xan v")
