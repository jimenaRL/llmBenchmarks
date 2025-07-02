import os
import csv
import time
import json
import asyncio
from time import sleep
from openai import OpenAI
from string import Template
from argparse import ArgumentParser
import subprocess as sp
from subprocess import Popen, PIPE

# DEFAULTLLMPARAMS = '{"model": "HuggingFaceH4/zephyr-7b-beta", "gpu_memory_utilization": 0.9, "max_model_len": 21500, "dtype": "half"}'
DEFAULTLLM = "HuggingFaceH4/zephyr-7b-beta"
DEFAULTDTYPE = "half"
DEFAULTDECODING = "xgrammar"
DEFAULTSAMPLINGPARAMS = '{"temperature": 0.7, "top_p": 0.95, "top_k": 50, "max_tokens": 16, "repetition_penalty": 1.2}'

ap = ArgumentParser(prog="Make openia async requests.")
ap.add_argument('--llm', required=False, type=str, default=DEFAULTLLM)
ap.add_argument('--dtype', required=False, type=str, default=DEFAULTDTYPE)
ap.add_argument('--guided_decoding_backend', required=False, type=str, default=DEFAULTDECODING)
ap.add_argument('--sampling_params', required=False, type=str, default=DEFAULTSAMPLINGPARAMS)
ap.add_argument('--guided_choice', required=True, type=str)
ap.add_argument('--system_prompt', required=True, type=str)
ap.add_argument('--user_prompt', required=True, type=str)
ap.add_argument('--tweets_file', required=True, type=str)
ap.add_argument('--tweets_column', required=True, type=str)
ap.add_argument('--results_file', required=True, type=str)

args = ap.parse_args()
llm = args.llm
dtype = args.dtype
decoding = args.guided_decoding_backend
sampling_params = json.loads(args.sampling_params)
guided_choice = args.guided_choice.split(',')
tweets_file = args.tweets_file
tweets_column = args.tweets_column
system_prompt = args.system_prompt
user_prompt = args.user_prompt
results_file = args.results_file

parameters = vars(args)
parameters = json.dumps(parameters, sort_keys=True, indent=4)
print(f"PARAMETERS:\n{parameters[2:-2]}")

# 1/ Load tweets
if not os.path.exists(tweets_file):
    raise ValueError(f"Unnable to find tweets file at {tweets_file}")
with open(tweets_file, newline='') as f:
    csvFile = csv.DictReader(f)
    tweets = [l[tweets_column] for l in csvFile]
print(f"Load {len(tweets)} tweets from column {tweets_column} on {tweets_file}.")

# 2/ Launch vllm server
vllm_serve_command  = f"vllm serve {llm} --guided-decoding-backend={decoding} --disable-log-stats --dtype={dtype}"
os.system(vllm_serve_command+" &")
print(f"Launched vllm server with command:\n\t{vllm_serve_command}")

# 4/ Wait for vllm server to be available and retrive model
openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000/v1"
client = OpenAI(
    base_url=openai_api_base,
    api_key=openai_api_key)

model = None
while not model:
    try:
        model = client.models.list().data[0].id
    except Exception as e:
        print(f"Model not ready: {e}")
        sleep(30)
print(f"Model is ready: {model} !")


# 3/ Create async functions to request vllm server trought openAI API
async def doCompletetion(model, messages, extra_body, tweet):
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        extra_body=extra_body)
    return idx, completion.choices[0].message.content

async def messageIterator():
    for tweet in enumerate(tweets):
        yield tweet, [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content":  Template(user_prompt).substitute(tweet=tweet)
                    }
                ]

label_extra_body = sampling_params.update({"guided_choice": guided_choice})

async def run_all():
    # Asynchronously call the function for each prompt
    tasks = [
        doCompletetion(model, messages, label_extra_body, tweet)
        async for tweet, messages in messageIterator()
    ]
    # Gather and run the tasks concurrently
    results = await asyncio.gather(*tasks)
    return results

# 6/ Run all courutines
start = time.time()
results = asyncio.run(run_all())
end = time.time()
print(f"Took {end - start} seconds.")

headers = ["tweet", f"choice"]
with open(results_file, 'w') as f:
    writer =  csv.writer(f)
    writer.writerow(headers)
    writer.writerows(results)
print(f"LLM answers (={len(results)}) saved to {results_file}.")


# 7/ Kill vllm server
cmd_tokill = {'vllm', 'python3'}
p = Popen(['ps'], stdout=PIPE)
ps_out = p.communicate()[0].decode().split('\n')
pids_tokill = [l.split(' ')[0] for l in ps_out if l.split(' ')[-1] in cmd_tokill]

for pid in pids_tokill:
    pipe = sp.Popen(f'kill {pid}', shell=True, stdout=sp.PIPE, stderr=sp.PIPE )
    res = pipe.communicate()
    assert pipe.returncode == 0
