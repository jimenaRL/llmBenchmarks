import re
import csv
import json
from string import Template
from argparse import ArgumentParser

ap = ArgumentParser()
ap.add_argument('--request_template', type=str, required=False, default="patternRequest.json")
ap.add_argument('--bios_path', type=str, required=False, default="chargeLoadTest20k.csv")
ap.add_argument('--output_file', type=str, required=False, default="batchRequest20k.jsonl")
args = ap.parse_args()
requestTemplate = args.request_template
biosPath = args.bios_path
outputJsonl = args.output_file

# Validate and load the input request pattern,
# this is equivalent to make pattern = f.read()
with open(requestTemplate, 'r') as f:
    dict_pattern = json.load(f)
    pattern = json.dumps(dict_pattern)

# Load bios
with open(biosPath, 'r') as csvfile:
    reader = csv.reader(csvfile)
    headers = next(reader)
    bios = [c[0] for c in reader]

# Create a batch of request in the form of a jsonl file
# by substituting each bio into the request pattern.
# We use use json.dumps to scape all possible conflictual characters
requests =  [Template(pattern).substitute(id=i, userbio=json.dumps(b)[1:-1]) for i, b in enumerate(bios)]
dumped_requests = map(json.dumps, requests)
with open(outputJsonl, "w") as f:
    f.writelines('\n'.join(requests))

assert len(bios) == len(requests)

print(f"Jsonl output file wrote to {outputJsonl} with {len(requests)} lines.")
