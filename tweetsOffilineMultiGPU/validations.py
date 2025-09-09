import os
import numpy as np
import pandas as pd
from sklearn.metrics import precision_recall_fscore_support

BASEPATH = "/home/jimena/work/dev/llmBenchmarks/tweetsOffilineMultiGPU"
METRICSFOLDER = os.path.join(BASEPATH, "metrics/v1")

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

NBPARAMS = {
    "zephyr-7b-beta": 7,
    "gpt-oss-20b": 20,
    "Mistral-Small-3.1-24B-Instruct-2503": 24,
    "Magistral-Small-2506": 24,
    "Mistral-Small-24B-Instruct-2501": 24,
    "max_model_len_8000_Qwen3-30B-A3B-Instruct-2507": 30,
    "gpt-oss-120b": 120,
    "Llama-3.3-70B-Instruct": 70,
    "DeepSeek-R1-Distill-Llama-70B": 70,
    "Mistral-Large-Instruct-2411": 123
}

ANNOTATIONS = [
    "voteintention/multiple/all",
    "support/multiple/all",
    # "criticism/multiple/all"
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

    file = f"joint_results/{annotation.replace('/', '_')}.csv"
    candidate = annotation.split('/')[-1]
    setting = annotation.split('/')[1]
    task = annotation.split('/')[0]
    column = f"{candidate.upper()} {task.upper()}"

    gt = pd.read_csv("gt_200_sampled_xan_seed_123_fr_en.csv")[column].tolist()
    annotations = pd.read_csv(file)

    idxs = range(len(gt))

    metrics = []
    for model in MODELS:

        experiment = f"GUIDED-{model}"
        if not experiment in annotations:
            continue
        ann = annotations[experiment].tolist()

        # binary classification
        if setting == "binary":
            res = precision_recall_fscore_support(
                y_true=gt,
                y_pred=ann,
                labels=['YES'],
                average='weighted',
                zero_division=np.nan)
            metrics.append({
                "model": model,
                "params": NBPARAMS[model],
                "precision": res[0],
                "recall": res[1],
                "f1": res[2],
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
                y_true=gt, y_pred=ann, average="weighted", zero_division=np.nan)

            metrics.append({
                "model": model,
                "params": NBPARAMS[model],
                "precision": res[0],
                "recall": res[1],
                "f1": res[2],
                })


    df = pd.DataFrame.from_records(metrics).sort_values(by="params")
    path = os.path.join(METRICSFOLDER, f"{annotation.replace('/', '_')}.csv")
    df.to_csv(path, index=False)
    print(f"Metrics for annotation {annotation} experiment saved at {path}")
    os.system(f"xan v {path}")
