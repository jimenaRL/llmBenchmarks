import os
import csv
import time
import asyncio
import numpy as np
from argparse import ArgumentParser

from openai import OpenAI

ap = ArgumentParser()
ap.add_argument('--limit', type=int, default=-1)
ap.add_argument('--nbgpus', type=int, default=1)
ap.add_argument('--batch_size', type=int, default=10000)
ap.add_argument('--batch_idx_start', type=int, default=0)

args = ap.parse_args()
limit = args.limit
nbgpus = args.nbgpus
batch_size = args.batch_size
batch_idx_start = args.batch_idx_start

results_folder = "/sps/humanum/user/jroyolet/dev/llmBenchmarks/tweetsOffilineMultiGPU/translations/mistralai_Mistral-7B-Instruct-v0.2"

# Load tweets
file = "/sps/humanum/user/jroyolet/dev/llmBenchmarks/tweetsOffilineMultiGPU/cleaned_text2annotate_2022-03-27_2022-04-25.csv"
with open(file, 'r') as f:
    reader = csv.reader(f)
    tweets = [[n, l[0]] for n, l in enumerate(reader)][:limit]

# Run vllm server
vllm_serve_command = f'vllm serve "mistralai/Mistral-7B-Instruct-v0.2" --disable-log-requests --disable-log-stats --tensor-parallel-size {nbgpus} &'
print(f"[RUNNING] {vllm_serve_command}")
os.system(vllm_serve_command)

# Wait for vllm server to be available and retrive model
client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="EMPTY"
)
model = None
while not model:
    try:
        model = client.models.list().data[0].id
    except Exception as e:
        print(f"Model not ready: {e}. Waiting 30 more seconds...")
        time.sleep(30)
print(f"Model is ready: {model} !")


async def doCompletetion(tweet):
    res = client.responses.create(
        model="mistralai/Mistral-7B-Instruct-v0.2",
        instructions="Please translate the following text from french to english.",
        input=tweet[1])
    return tweet[0], tweet[1], res.output_text

async def tweetsIterator(start, end):
    for tweet in tweets[start:end]:
        yield tweet

async def run_all(start, end):
    # Asynchronously call the function for each prompt
    tasks = [
        doCompletetion(tweet)
        async for tweet in tweetsIterator(start, end)
    ]
    # Gather and run the tasks concurrently
    results = await asyncio.gather(*tasks)
    return results

data_length = len(tweets)
batchl = [
    [i * batch_size, (i + 1) * batch_size]
    for i in range(np.int32(data_length / batch_size + 1))
]
batchl[-1][1] = min(data_length,  batchl[-1][1])

headers = ["idx","fr", "en"]

for batch_idx, b in enumerate(batchl):

        if batch_idx < batch_idx_start:
            continue

        file = os.path.join(results_folder, f"translations_{batch_idx}.csv")
        lockfile = file + ".lock"

        # If batch already computed continue or lock is granted, continue
        if os.path.exists(file):
            print(f"Already computed file at {file}. Continuing.")
            continue

        if os.path.exists(lockfile):
            print(f"Found active lock for file at {file}. Continuing.")
            continue

        # If not, create lock and start batch computation
        with open(lockfile, 'w') as f:
            csv.writer(f).writerow(headers)
        print(f"Computing batch at index {batch_idx}...")

        # Run all courutines
        start = time.time()
        results = asyncio.run(run_all(start=b[0], end=b[1]))
        end = time.time()
        print(f"Took {end - start} seconds.")

        # save to file
        with open(file, 'w') as f:
            writer =  csv.writer(f)
            writer.writerow(headers)
            writer.writerows(results)
        print(f"LLM answers (={len(results)}) saved to {file}")

        # and release lock
        os.system(f"rm {lockfile}")
