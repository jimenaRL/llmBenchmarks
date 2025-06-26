import os
import csv
import time
import asyncio
from time import sleep
from openai import OpenAI
from string import Template
from argparse import ArgumentParser
import subprocess as sp
from subprocess import Popen, PIPE

ap = ArgumentParser(prog="Create python commands or slurm jobs for openia async requests.")
ap.add_argument('--tweets_file', required=True, type=str)
ap.add_argument('--language', required=True, type=str, choices=["english", "french"])
ap.add_argument('--experiment', required=True, type=int, choices=[1, 2])
args = ap.parse_args()
tweets_file = args.tweets_file
language = args.language
experiment = args.experiment

results_file = f"results_promts_{language}_{experiment}_{tweets_file.split('.csv')[0]}.csv"

guided_choice = {
    "french": {
        1: ["Macron", "Mélenchon", "Le Pen", "Aucun"],
        2: ["Macron", "Mélenchon", "Le Pen", "Autre"],
    },
    "english": {
        1: ["Macron", "Mélenchon", "Le Pen", "None"],
        2: ["Macron", "Mélenchon", "Le Pen", "Other"],
    }
}

instructions = {
    "french": {
        1: "Tu vas classifier des messages des médias sociaux selon s’ils expriment l’intention de voter pour un candidat ou s’ils appellent à voter pour un candidat à l’élection présidentielle de 2022 en France. Dis moi si le message suivant exprime l'intention de voter pour ou appelle à voter pour Macron, Mélenchon ou Le Pen, en répondant uniquement par le nom de famille du candidat, ou par “Aucun”, si le message ne montre soutien pour aucun de ces trois candidats. Voici le message: ${tweet}",
        2 : "Tu vas classifier des messages des médias sociaux selon s’ils expriment du soutien pour un candidat à l’élection présidentielle de 2022 en France. Dis moi si le message suivant exprime du soutien pour Macron, Mélenchon ou Le Pen, en répondant uniquement par le nom de famille du candidat, ou par le mot “Autre”, si le message n’exprime pas d’intention vote ou appelleà voter pour l’un de ces trois candidats. Voici le message: ${tweet}"
    },
    "english": {
        1: "You'll classify social media posts based on whether they express the intention to vote for a candidate or if they call for a vote for a candidate in the 2022 presidential election in France. Tell me if the following message expresses the intention to vote for or calls for a vote for Macron, Mélenchon or Le Pen, replying only with the candidate's last name, or with 'None', if the message does not show support for any of these three candidates. Here is the message:: ${tweet}",
        2: " You'll classify social media posts based on whether they express support for a candidate in the 2022 presidential election in France. Tell me if the following message expresses support for Macron, Mélenchon or Le Pen, by replying only with the candidate's last name, or with the word 'Other', if the message does not express an intention to vote or calls for a vote for one of these three candidates. Here is the message: ${tweet}"
    },
}


with open(tweets_file, newline='') as f:
    csvFile = csv.DictReader(f)
    tweets = [l for l in csvFile]
print(f"Load {len(tweets)} tweets.")

# 0/ Launch vllm server
cmd = "vllm serve HuggingFaceH4/zephyr-7b-beta --guided-decoding-backend=xgrammar --disable-log-stats --dtype=half &"
os.system(cmd)
print(f"Launched command:\n\t{cmd}")

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


# 5/ Create async functions to request vllm server trought openAI api
async def doCompletetion(model, messages, extra_body):
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        extra_body=extra_body)
    content = completion.choices[0].message.content
    return content

async def asyncMessageIterator(instructions, language):
    for tweet in tweets:
        yield [
                    {
                        "role": "system",
                        "content": "Tu es un expert en politique française."
                    },
                    {
                        "role": "user",
                        "content":  Template(instructions).substitute(tweet=tweet[language])
                    }
                ]

label_extra_body = {
    "guided_choice": guided_choice[language][experiment],
    "temperature": 0.7,
    "max_tokens": 16,
    "top_k": 50,
    "top_p": 0.95,
    "repetition_penalty": 1.2,
    }

async def run_all(instructions, messages):
    # Asynchronously call the function for each prompt
    tasks = [
        doCompletetion(model, messages, label_extra_body)
        async for messages in asyncMessageIterator(instructions)
    ]
    # Gather and run the tasks concurrently
    results = await asyncio.gather(*tasks)
    return results

# 6/ Run all courutines
start = time.time()
results = asyncio.run(run_all(instructions[language][experiment]))
end = time.time()

with open(results_file, 'w') as f:
    writer =  csv.writer(f)
    writer.writerow(headers)
    writer.writerows(zip(tweets, results))
print(f"LLM answers (={len(results)}) saved to {results_file}.")
print(f"Took {end - start} seconds.")


# 7/ Kill vllm server
cmd_tokill = {'vllm', 'python3'}
p = Popen(['ps'], stdout=PIPE)
ps_out = p.communicate()[0].decode().split('\n')
pids_tokill = [l.split(' ')[0] for l in ps_out if l.split(' ')[-1] in cmd_tokill]

for pid in pids_tokill:
    pipe = sp.Popen(f'kill {pid}', shell=True, stdout=sp.PIPE, stderr=sp.PIPE )
    res = pipe.communicate()
    assert pipe.returncode == 0
