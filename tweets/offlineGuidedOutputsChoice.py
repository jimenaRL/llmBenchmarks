import os
import csv
import json
import time
from string import Template
from argparse import ArgumentParser

from vllm import LLM, SamplingParams
from vllm.sampling_params import GuidedDecodingParams

DEFAULTLLM = "HuggingFaceH4/zephyr-7b-beta"
DEFAULTPARAMS = '{"temperature": 0.7, "top_p": 0.95, "top_k": 50, "max_tokens": 16, "repetition_penalty": 1.2}'
DEFAULTDECODING = "xgrammar"

ap = ArgumentParser(prog="Make openia async requests.")
ap.add_argument('--llm', required=False, type=str, default=DEFAULTLLM)
ap.add_argument('--sampling_params', required=False, type=str, default=DEFAULTPARAMS)
ap.add_argument('--guided_choice', required=True, type=str)
ap.add_argument('--guided_decoding_backend', required=False, type=str, default=DEFAULTDECODING)
ap.add_argument('--system_prompt', required=True, type=str)
ap.add_argument('--user_prompt', required=True, type=str)
ap.add_argument('--tweets_file', required=True, type=str)
ap.add_argument('--tweets_column', required=True, type=str)
ap.add_argument('--results_file', required=True, type=str)

args = ap.parse_args()
llm = args.llm
sampling_params = json.loads(args.sampling_params)
guided_choice = ','.split(args.guided_choice)
guided_decoding_backend = args.guided_decoding_backend
tweets_file = args.tweets_file
tweets_column = args.tweets_column
system_prompt = args.system_prompt
user_prompt = args.user_prompt
results_file = args.results_file

parameters = vars(args)
parameters = json.dumps(parameters, sort_keys=True, indent=4)
print(f"PARAMETERS:\n{parameters[2:-2]}")

if not os.path.exists(tweets_file):
    raise ValueError(f"Unnable to find tweets file at {tweets_file}")
with open(tweets_file, newline='') as f:
    csvFile = csv.DictReader(f)
    tweets = [l[tweets_column] for l in csvFile]
print(f"Load {len(tweets)} tweets from column {tweets_column} on {tweets_file}.")

llm = LLM(model=llm, guided_decoding_backend=guided_decoding_backend)
sampling_params.update({"guided_decoding": GuidedDecodingParams(choice=guided_choice)})
sampling_params = SamplingParams(**sampling_params)

def messageIterator():
    for tweet in tweets:
        yield [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content":  Template(user_prompt).substitute(tweet=tweet)
                    }
                ]

messages = [m for m in messageIterator()]
print(messages)

outputs = llm.chat(
    messages=messages,
    sampling_params=sampling_params,
    use_tqdm=True
)

results = []
for n, (tweet, o) in enumerate(zip(tweets, outputs)):
    results.append([idx, tweet, o.outputs[0].text])

headers = ["id", "tweet", "choice"]
with open(results_file, 'w') as f:
    writer =  csv.writer(f)
    writer.writerow(headers)
    writer.writerows(results)
print(f"LLM answers (={len(results)}) saved to {results_file}.")

