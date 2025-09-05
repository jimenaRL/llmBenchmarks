import os
from glob import glob
import  pandas as pd

# BASEPATH = "/sps/humanum/user/jroyolet/dev/llmBenchmarks/tweetsOffilineMultiGPU"
BASEPATH = "/home/jimena/work/dev/llmBenchmarks/tweetsOffilineMultiGPU"

models = [
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


def extract_data(model, annotation, df=None, columns=[]):

    folders = glob(os.path.join(BASEPATH, f"*{model}*"))
    assert len(folders) == 1
    folder = folders [0]

    path_free = os.path.join(folder, "free", annotation, "llm_answer_0.csv")
    df_free = pd.read_csv(path_free)
    df_free = df_free.rename(columns={"answer": "FREE-" + model})

    if df is not None:
        df = df.merge(df_free, on=['idx', 'tweet'])
    else:
        df = df_free

    path_guided = os.path.join(folder, "guided", annotation, "llm_answer_0.csv")
    df_guided = pd.read_csv(path_guided)
    if "gpt-oss" in model:
        df_guided["answer"] = df_guided["answer"].apply(lambda s: s.split("assistantfinal")[-1])
    df_guided = df_guided.rename(columns={"answer": "GUIDED-" + model})

    df = df.merge(df_guided, on=['idx', 'tweet'])

    columns.extend(["FREE-" + model, "GUIDED-" + model])

    return df, columns

annotations = [
    "voteintention/multiple/all",
    "support/multiple/all",
    "criticism/multiple/all"
]

annotations = [
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

for annotation in annotations:

    df = None
    columns = ["idx", "tweet"]

    for model in models:
        try:
            df, columns = extract_data(model, annotation, df, columns)
        except Exception as exc:
            print(exc)
            print("Continuing...")

    df = df.fillna("None")

    path = f"{annotation.replace('/', '_')}.csv"

    df[columns].to_csv(path, index=False)
    print(f"Results for annotation {annotation} results saved at {path}.")

