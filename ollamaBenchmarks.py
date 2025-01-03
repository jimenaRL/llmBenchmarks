import csv
import json
import requests
from tqdm import tqdm
from string import Template
from argparse import ArgumentParser

ap = ArgumentParser()
ap.add_argument('--model', type=str)
args = ap.parse_args()
model = args.model


URL = "http://localhost:11434/api/generate"
HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}
DATA = '{"model": "${model}", "prompt": "${prompt}", "stream": false, "keep_alive": "25m"}'

prompts = [
  "Why sky is blue?",
  "1+3?",
  "What type of organism is commonly used in preparation of foods such as cheese and yogurt?",
  "What phenomenon makes global winds blow northeast to southwest or the reverse in the northern hemisphere and northwest to southeast or the reverse in the southern hemisphere?",
  "Changes from a less-ordered state to a more-ordered state (such as a liquid to a solid) are always what?",
  "What is the least dangerous radioactive decay?",
  "Is France a polarized country?",
  "Which medialab is the best one?"
]

stats = []
for prompt in tqdm(prompts):

  data = Template(DATA).substitute(model=model, prompt=prompt)
  res = requests.post(url=URL, headers=HEADERS, data=data)
  contents = json.loads(res.content)
  stats.append({
    'prompt': prompt,
    'answer': contents["response"],
    'total_duration_ns': contents['total_duration'],
    'load_duration_ns': contents['load_duration'],
    'total_duration_s': "{:1.4f}".format(1e-09 * contents['total_duration']),
    'load_duration_s': "{:1.4f}".format(1e-09 * contents['load_duration']),
    'prompt_tokens_per_s': "{:1.9f}".format(1e-09 * contents['prompt_eval_duration'] / contents['prompt_eval_count']),
    'answer_tokens_per_s': "{:1.9f}".format(1e-09 * contents['eval_duration'] / contents['eval_count']),
  })

fieldnames = [
  'prompt',
  'answer',
  'total_duration_ns',
  'load_duration_ns',
  'total_duration_s',
  'load_duration_s',
  'prompt_tokens_per_s',
  'answer_tokens_per_s',
]

with open(f'{model}_cpu.csv', 'w', newline='') as csvfile:
  writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
  writer.writeheader()
  writer.writerows(stats)
