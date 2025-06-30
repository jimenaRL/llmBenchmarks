import os
import csv
import json
import time
from string import Template
from argparse import ArgumentParser

from vllm import LLM, SamplingParams
from vllm.sampling_params import GuidedDecodingParams

DEFAULTLLM="HuggingFaceH4/zephyr-7b-beta"
DEFAULTPARAMS= '{"temperature": 0.7, "top_p": 0.95, "top_k": 50, "max_tokens": 16, "repetition_penalty": 1.2}'

ap = ArgumentParser(prog="Make openia async requests.")
ap.add_argument('--llm', required=False, type=str, default=DEFAULTLLM)
ap.add_argument('--sampling_params', required=False, type=str, default=DEFAULTPARAMS)
ap.add_argument('--guided_choice', required=True, type=str)
ap.add_argument('--system_prompt', required=True, type=str)
ap.add_argument('--user_prompt', required=True, type=str)
ap.add_argument('--tweets_file', required=True, type=str)
ap.add_argument('--results_file', required=True, type=str)

args = ap.parse_args()
llm = args.llm
sampling_params = json.loads(args.sampling_params)
guided_choice = ','.split(args.guided_choice)
tweets_file = args.tweets_file
system_prompt = args.system_prompt
user_prompt = args.user_prompt
results_file = args.results_file

if not os.path.exists(tweets_file):
    raise ValueError(f"Unnable to find tweets fiel at {tweets_file}")
with open(tweets_file, newline='') as f:
    csvFile = csv.DictReader(f)
    tweets = [l for l in csvFile]
print(f"Load {len(tweets)} tweets from {tweets_file}.")

llm = LLM(model=llm)
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

prompts = [m for m in messageIterator()]

outputs = llm.generate(
    prompts=prompts,
    sampling_params=sampling_params,
)

# results = output.outputs[0].text
# content = completion.choices[0].message.content



# headers = ["id", f"choice"]
# with open(results_file, 'w') as f:
#     writer =  csv.writer(f)
#     writer.writerow(headers)
#     writer.writerows(enumerate(results))
# print(f"LLM answers (={len(results)}) saved to {results_file}.")

