import os
import csv
import json
import numpy as np
import pandas as pd
from sklearn.metrics import precision_recall_fscore_support

BASEPATH = "/home/jimena/work/dev/llmBenchmarks/tweetsOffilineMultiGPU"
GTFILE = os.path.join(BASEPATH, "gt_200_sampled_xan_seed_123_fr_en.csv")
VERSION = "v2"
RESULTSFOLDER = os.path.join(BASEPATH, "joint_results", VERSION)
METRICSFOLDER = os.path.join(BASEPATH, "metrics", VERSION)

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

NBPARAMS = {
    "zephyr-7b-beta": 7,
    "gpt-oss-20b": 20,
    "Mistral-Small-3.1-24B-Instruct-2503": 24,
    "Magistral-Small-2506": 24,
    "Mistral-Small-24B-Instruct-2501": 24,
    "max_model_len_8000_Qwen3-30B-A3B-Instruct-2507": 30,
    "gpt-oss-120b": 120,
    "Llama-3.3-70B-Instruct": 70,
    "max_model_len_7000_Llama-3.3-70B-Instruct": 70,
    "DeepSeek-R1-Distill-Llama-70B": 70,
    "Mistral-Large-Instruct-2411": 123,
    "mayorityVote": -1,
}

KINDS = [
    "FREE",
    "GUIDED",
]

SUPPORTCHOICES = {
    "multiple": ["Macron", "Mélenchon", "Le Pen"],
    "binary" : ["YES"]
}

NBDECIMALS = 2

ANNOTATIONS = [
    "voteintention/multiple/all",
    "support/multiple/all",
    "criticism/multiple/all",
    "criticism/binary/lepen",
    "criticism/binary/macron",
    "criticism/binary/melenchon",
    "support/binary/lepen",
    "support/binary/macron",
    "support/binary/melenchon",
    "voteintention/binary/lepen",
    "voteintention/binary/macron",
    "voteintention/binary/melenchon"
]


for annotation in ANNOTATIONS:

    file = os.path.join(RESULTSFOLDER, f"{annotation.replace('/', '_')}.csv")
    candidate = annotation.split('/')[-1]
    setting = annotation.split('/')[1]
    task = annotation.split('/')[0]
    column = f"{candidate.upper()} {task.upper()}"

    # gt = pd.read_csv(GTFILE, dtype=str)[column].tolist()
    # annotations = pd.read_csv(file)

    with open(GTFILE, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        gt = [r[column] for r in reader]

    with open(file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        annotations = [r for r in reader]

    idxs = range(len(gt))

    metrics = []
    for model in MODELS[VERSION]:

        model_abb = model.split('000_')[-1]

        for kind in KINDS:
            experiment = f"{kind}-{model}"

            ann = [a[experiment] for a in annotations]

            # binary classification
            if setting == "binary":
                res = precision_recall_fscore_support(
                    y_true=gt,
                    y_pred=ann,
                    pos_label='YES',
                    average='binary',
                    zero_division=np.nan)

                res = list(res)
                support =  sum([1 if _ == 'YES' else 0 for _ in gt])

                metrics.append({
                    "model": model_abb,
                    "kind": kind,
                    "params [B]": NBPARAMS[model],
                    "precision": str(res[0])[:NBDECIMALS + 2],
                    "recall": str(res[1])[:NBDECIMALS + 2],
                    "f1_weighted": str(res[2])[:NBDECIMALS + 2],
                    "support": support,
                    "labels": ' | '.join(SUPPORTCHOICES[setting])
                    })

            # multiclass classification
            if setting == "multiple":

                # Calculate metrics for each label, and find their average weighted by support
                # (the number of true instances for each label).
                # This alters ‘macro’ to account for label imbalance;
                # it can result in an F-score that is not between precision and recall.
                # Weighted recall is equal to accuracy.
                # See: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_fscore_support.html

                res = precision_recall_fscore_support(
                    y_true=gt,
                    y_pred=ann,
                    labels=SUPPORTCHOICES['multiple'],
                    average=None,
                    zero_division=np.nan)

                f1_macro = precision_recall_fscore_support(
                    y_true=gt,
                    y_pred=ann,
                    labels=SUPPORTCHOICES['multiple'],
                    average='macro',
                    zero_division=np.nan)[2]

                f1_micro = precision_recall_fscore_support(
                    y_true=gt,
                    y_pred=ann,
                    labels=SUPPORTCHOICES['multiple'],
                    average='micro',
                    zero_division=np.nan)[2]

                f1_weighted = precision_recall_fscore_support(
                    y_true=gt,
                    y_pred=ann,
                    labels=SUPPORTCHOICES['multiple'],
                    average='weighted',
                    zero_division=np.nan)[2]

                metrics.append({
                    "model": model_abb,
                    "kind": kind,
                    "params [B]": NBPARAMS[model],
                    "support": ' | '.join(map(str, res[3])),
                    "labels": ' | '.join(SUPPORTCHOICES[setting]),
                    # "precision": ' | '.join([str(r)[:NBDECIMALS + 2] for r in res[0]]),
                    # "recall": ' | '.join([str(r)[:NBDECIMALS + 2] for r in res[1]]),
                    "f1_binary": ' | '.join([str(r)[:NBDECIMALS + 2] for r in res[2]]),
                    "f1_macro": str(f1_macro)[:NBDECIMALS + 2],
                    "f1_micro":  str(f1_micro)[:NBDECIMALS + 2],
                    "f1_weighted": str(f1_weighted)[:NBDECIMALS + 2],
                    })


    df = pd.DataFrame.from_records(metrics).sort_values(by=["params [B]", "kind"])
    path = os.path.join(METRICSFOLDER, f"{annotation.replace('/', '_')}.csv")
    df.to_csv(path, index=False)
    print(f"Metrics for annotation {annotation} experiment saved at {path}")
    os.system(f"xan v  {path}")

    # df = pd.DataFrame.from_records(metrics).sort_values(by=["f1_weighted"], ascending=False)
    # path = os.path.join(METRICSFOLDER, f"{annotation.replace('/', '_')}.csv")
    # df.to_csv(path, index=False)
    # print(f"Metrics for annotation {annotation} experiment saved at {path}")
    # os.system(f"xan v -l 3 {path}")
