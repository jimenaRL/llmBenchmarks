import os
import sys
import csv
import json
import sqlite3
import logging
import numpy as np

from string import Template
from argparse import ArgumentParser

from vllm import LLM, SamplingParams
from vllm.sampling_params import GuidedDecodingParams

DEFAULTOUTFOLDER = "/home/jimena.royoletelier/storage/toErase"
DEFAULTBATCHSIZE = 5000
DEFAULTMODELPARAMS = '{"model": "HuggingFaceH4/zephyr-7b-beta", "guided_decoding_backend": "xgrammar", "seed": 19, "dtype": "half", "max_model_len": 21500, "gpu_memory_utilization": 0.9, "tensor_parallel_size": 1}'
DEFAULTSAMPLEPARAMS = '{"temperature": 0.7, "top_p": 0.95, "top_k": 50, "max_tokens": 16, "repetition_penalty": 1.2, "seed": 19}'


def writeCsv(file, rows, headers, logger, verbose=True):
    if not isinstance(headers, list):
        raise ValueError(
            f"Headers must be a list. Found {type(headers)} for '{headers}'.")
    with open(file, 'w') as f:
        writer = csv.writer(f)
        if headers:
            writer.writerow(headers)
        writer.writerows(rows)
    if verbose:
        logger.info(f"Csv file saved at {file}")


def make_logger(logfile):
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.DEBUG,
        format=f"%(asctime)s %(message)s",
        handlers=[
            logging.FileHandler(logfile, 'w', 'utf-8'),
            logging.StreamHandler(sys.stdout)])
    return logger


def getData(dbpath, label, logger):

    table = f'llm_answer_{label}'

    # 1/ Retrive the english translations
    logger.info(f"Retreiving bios from {dbpath}.")
    QUERY = "SELECT pseudo_id,english_translation FROM english_translations"
    with sqlite3.connect(dbpath) as con:
        cur = con.cursor()
        cur.execute(QUERY)
        data = cur.fetchall()

    # 2/ Remove already translated entries
    QUERY = f"""
            SELECT EXISTS (
                SELECT
                    name
                FROM
                    sqlite_master
                WHERE
                    type='table' AND
                    name='{table}'
            )"""
    with sqlite3.connect(dbpath) as con:
        cur = con.cursor()
        cur.execute(QUERY)
        res = cur.fetchall()
    table_exists = res[0][0] == 1

    if table_exists:
        QUERY = f"SELECT pseudo_id FROM {table}"
        with sqlite3.connect(dbpath) as con:
            cur = con.cursor()
            cur.execute(QUERY)
            res = cur.fetchall()
        computed_pids = [r[0] for r in res]
        logger.info(
            f"Found {len(computed_pids)} already computed entries in {table}.")
        data = [d for d in data if d[0] not in computed_pids]

    logger.info(f"Found {len(data)} entries to be computed in {table}.")

    return data


def make_prompts(system_prompt, user_prompt, tweets):
    return [
        [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": Template(user_prompt).substitute(tweet=tweet)
            }
        ] for tweet in tweets]


def compute_llm_asnwers(data, model, sampling_params, system_prompt, user_prompt, output_folder, logger):

    logger.info(
        f"Computing llm answers {len(data)} bios.")

    outcolumns = [
        "idx",
        "tweet",
        'answer'
    ]

    data_length = len(data)
    batchl = [
        [i * batch_size, (i + 1) * batch_size]
        for i in range(np.int32(data_length / batch_size + 1))
    ]
    batchl[-1][1] = min(data_length,  batchl[-1][1])

    tweets_idx = range(len(data))

    for batch_idx, b in enumerate(batchl):

        if len(tweets) == 0:
            continue

        prompts = make_prompts(system_prompt, user_prompt, data[b[0]: b[1]])

        outputs = model.chat(
            messages=prompts,
            sampling_params=sampling_params,
            use_tqdm=True)

        parsed_outputs = [o.outputs[0].text for o in outputs]

        rows = zip(tweets_idx[b[0]: b[1]], data[b[0]: b[1]], parsed_outputs)

        file = os.path.join(output_folder, f"llm_answer_{batch_idx}.csv")

        writeCsv(file, rows, outcolumns, logger)

    return data


if __name__ == "__main__":

    """
    Example of script calling using 2 V100 gpu cards.
    Deepseek recommends to avoid adding a system prompt; all instructions should be contained within the user prompt.

     python tweets.py \
        --model_params='{"model": "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B", "guided_decoding_backend": "xgrammar", "seed": 19, "dtype": "half", "gpu_memory_utilization": 0.9, "tensor_parallel_size": 2}' \
        --sampling_params='{"temperature": 0.6, "top_p": 0.95}' \
        --tweets_file=200_sampled_xan_seed_123_fr_en.csv \
        --tweets_column=english \
        --system_prompt='' \
        --user_prompt='You are an expert in French politics. Please classify the following social media message (that were posted in the weeks leading up to the 2022 presidential election in France) according to whether it express support or positive attitudes towards Le Pen in this election. You must use only the information contained in the message. Be concise and answer only YES or NO. Here is the message: ${tweet}' \
        --guided_choice=YES,NO \
        --logfile=/sps/humanum/user/jroyolet/dev/llmBenchmarks/tweetsOffilineMultiGPU/logs/2Xv100DeepSeek-R1-Distill-Qwen-32B.log \
        --outfolder=/sps/humanum/user/jroyolet/dev/llmBenchmarks/tweetsOffilineMultiGPU/2Xv100DeepSeek-R1-Distill-Qwen-32B/
    """

    ap = ArgumentParser()
    ap.add_argument('--model_params', type=str, default=DEFAULTMODELPARAMS)
    ap.add_argument('--sampling_params', type=str, default=DEFAULTSAMPLEPARAMS)
    ap.add_argument('--batch_size', type=int, default=DEFAULTBATCHSIZE)

    ap.add_argument('--system_prompt', required=True, type=str)
    ap.add_argument('--user_prompt', required=True, type=str)
    ap.add_argument('--guided_choice', required=False, type=str, default='')

    ap.add_argument('--tweets_file', required=True, type=str)
    ap.add_argument('--tweets_column', required=True, type=str)

    ap.add_argument('--logfile', type=str, default=None)
    ap.add_argument('--outfolder', type=str, default=DEFAULTOUTFOLDER)

    args = ap.parse_args()

    model_params = json.loads(args.model_params)
    sampling_params = json.loads(args.sampling_params)
    batch_size = args.batch_size

    system_prompt = args.system_prompt
    user_prompt = args.user_prompt
    guided_choice = args.guided_choice.split(',') if args.guided_choice else None
    tweets_file = args.tweets_file
    tweets_column = args.tweets_column

    outfolder = args.outfolder
    logfile = args.logfile if args.logfile is not None else os.path.join(outfolder, "out.log")

    os.makedirs(outfolder, exist_ok=True)

    # 1/ Make logger and log parameters
    logger = make_logger(logfile)

    parameters = vars(args)
    dumped_parameters = json.dumps(parameters, sort_keys=True, indent=4)
    logger.info("---------------------------------------------------------")
    logger.info(f"PARAMETERS:\n{dumped_parameters[2:-2]}")

    # 2/ Load data (tweets) to be used in prompts
    if not os.path.exists(tweets_file):
        raise ValueError(f"Unnable to find tweets file at {tweets_file}")
    with open(tweets_file, newline='') as f:
        csvFile = csv.DictReader(f)
        tweets = [l[tweets_column] for l in csvFile]
    print(f"Load {len(tweets)} tweets from column {tweets_column} on {tweets_file}.")

    # 3/ Set sampling params
    if guided_choice:
        guided_decoding_params = GuidedDecodingParams(choice=guided_choice)
        sp = SamplingParams(
            **sampling_params,
            guided_decoding=guided_decoding_params)
    else:
        sp = SamplingParams(**sampling_params)
    logger.info(f"LLM model was loaded. Sampling params are {sp}.")

    # 4/ Load model
    model = LLM(**model_params)

    # 5/ Compute answers
    compute_llm_asnwers(
        tweets, model, sp,
        system_prompt, user_prompt,
        outfolder, logger)
