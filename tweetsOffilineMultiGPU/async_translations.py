import os
import csv
import time
import asyncio
from argparse import ArgumentParser

from openai import OpenAI

ap = ArgumentParser()
ap.add_argument('--limit', type=int, default=-1)
ap.add_argument('--nbgpus', type=int, default=1)

args = ap.parse_args()
limit = args.limit
nbgpus = args.nbgpus

results_file = "/sps/humanum/user/jroyolet/dev/llmBenchmarks/tweetsOffilineMultiGPU/translations/mistralai_Mistral-7B-Instruct-v0.2/translations.csv"

# Load tweets
file = "/sps/humanum/user/jroyolet/dev/llmBenchmarks/tweetsOffilineMultiGPU/cleaned_text2annotate_2022-03-27_2022-04-25.csv"
with open(file, 'r') as f:
    reader = csv.reader(f)
    tweets = [l[0] for l in reader][:limit]

# Run vllm server
vllm_serve_command = f'vllm serve "mistralai/Mistral-7B-Instruct-v0.2" --disable-log-stats --disable-log-requests --tensor-parallel-size {nbgpus} &'
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
        print(f"Model not ready: {e}")
        time.sleep(30)
print(f"Model is ready: {model} !")


async def doCompletetion(tweet):
    res = client.responses.create(
        model="mistralai/Mistral-7B-Instruct-v0.2",
        instructions="Please translate the following text to english.",
        input=tweet)
    return tweet, res.output_text

async def tweetsIterator():
    for tweet in tweets:
        yield tweet

async def run_all():
    # Asynchronously call the function for each prompt
    tasks = [
        doCompletetion(tweet)
        async for tweet in tweetsIterator()
    ]
    # Gather and run the tasks concurrently
    results = await asyncio.gather(*tasks)
    return results

# Run all courutines
start = time.time()
results = asyncio.run(run_all())
end = time.time()
print(f"Took {end - start} seconds.")

# save to file
headers = ["fr", f"en"]
with open(results_file, 'w') as f:
    writer =  csv.writer(f)
    writer.writerow(headers)
    writer.writerows(results)
print(f"LLM answers (={len(results)}) saved to {results_file}")
