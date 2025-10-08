import os
from glob import glob
import  pandas as pd

# BASEPATH = "/sps/humanum/user/jroyolet/dev/llmBenchmarks/tweetsOffilineMultiGPU"
BASEPATH = "/home/jimena/work/dev/llmBenchmarks/tweetsOffilineMultiGPU"
VERSION = "v2"
OUTPUTSFOLDER = os.path.join(BASEPATH, "models_outputs", VERSION)
RESULTSFOLDER = os.path.join(BASEPATH, "joint_results", VERSION)
os.makedirs(RESULTSFOLDER, exist_ok=True)

MODELS = {
    "v1": [
        "zephyr-7b-beta",
        "gpt-oss-20b",
        "Mistral-Small-3.1-24B-Instruct-2503",
        "Magistral-Small-2506",
        "Mistral-Small-24B-Instruct-2501",
        "max_model_len_8000_Qwen3-30B-A3B-Instruct-2507",
        "gpt-oss-120b",
        "Llama-3.3-70B-Instruct",
        "max_model_len_7000_Llama-3.3-70B-Instruct",
        "DeepSeek-R1-Distill-Llama-70B",
        "Mistral-Large-Instruct-2411"
    ],

    "v2": [
        "zephyr-7b-beta",
        "max_model_len_8000_Qwen3-30B-A3B-Instruct-2507",
        "gpt-oss-120b",
        "max_model_len_7000_Llama-3.3-70B-Instruct",
        "Mistral-Large-Instruct-2411",
    ],
}

ANNOTATIONS = {

    "multiple": [
        "voteintention/multiple/all",
        "support/multiple/all",
        "criticism/multiple/all"
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

DEFAULTANSWER = {
    "multiple": "None",
    "binary" : "NO"
}



SETTINGS = ANNOTATIONS.keys()

def parseAnwers(whole_answer, model, setting):

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

    if "gpt-oss" in model:
        whole_answer = whole_answer.split("assistantfinal")[-1]

    if setting == "binary":
        whole_answer = whole_answer.upper()

    annotation = DEFAULTANSWER[setting]
    for choice in CHOICES[setting]:
        if whole_answer[:len(choice)] == choice:
            annotation = choice

    return annotation

def extract_data(model, annotation, setting, df=None, columns=[]):

    assert model in MODELS[VERSION]
    assert setting in SETTINGS

    folders = glob(os.path.join(OUTPUTSFOLDER, f"*{model}*"))
    assert len(folders) == 1
    folder = folders[0]

    # get free answers
    colname = "FREE-" + model
    path_free = os.path.join(folder, "free", annotation, "llm_answer_0.csv")
    df_free = pd.read_csv(path_free) \
        .fillna("None") \
        .rename(columns={"answer": colname})

    df_free[colname] = df_free[colname].apply(lambda a: parseAnwers(a, model, setting))

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

    df_guided[colname] = df_guided[colname].apply(lambda a: parseAnwers(a, model, setting))


    df = df.merge(df_guided, on=['idx', 'tweet'])

    columns.extend(["FREE-" + model, "GUIDED-" + model])

    return df, columns

for setting in SETTINGS:

    for annotation in ANNOTATIONS[setting]:

        df = None
        columns = ["idx", "tweet"]

        for model in MODELS[VERSION]:
            df, columns = extract_data(model, annotation, setting, df, columns)

        models_cols_free = [c for c in df.columns[2:] if 'FREE' in c]
        models_cols_guided = [c for c in df.columns[2:] if 'GUIDED' in c]
        df = df.assign(freeMayorityVote=df[models_cols_free].mode(axis=1)[0])
        df = df.assign(guidedMayorityVote=df[models_cols_guided].mode(axis=1)[0])
        df = df.rename(columns={
            'freeMayorityVote':"FREE-mayorityVote",
            'guidedMayorityVote':"GUIDED-mayorityVote",
            })
        columns.append("FREE-mayorityVote")
        columns.append("GUIDED-mayorityVote")

        path = os.path.join(RESULTSFOLDER, f"{annotation.replace('/', '_')}.csv")

        df[columns].to_csv(path, index=False)

        print(f"Results for annotation {annotation} results saved at {path}")
        os.system(f"xan shuffle {path} | xan slice -l 5 | xan v")
