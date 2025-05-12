import re
import csv
import json
from string import Template
from argparse import ArgumentParser

ap = ArgumentParser()
ap.add_argument('--request_template', type=str, required=False, default="patternRequest_llava.json")
ap.add_argument('--bios_path', type=str, required=False, default="biosExample.csv")
ap.add_argument('--output_file', type=str, required=False, default="batchRequestExample.jsonl")
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
    ids_bios = [r for r in reader]

# Create a batch of request in the form of a jsonl file
# by substituting each bio and id into the request pattern.
# We use use json.dumps to scape all possible conflictual characters
requests =  [
    Template(pattern).substitute(id=ib[0], userbio=json.dumps(ib[1])[1:-1])
    for ib in ids_bios
]
dumped_requests = map(json.dumps, requests)
with open(outputJsonl, "w") as f:
    f.writelines('\n'.join(requests))

assert len(ids_bios) == len(requests)

print(f"Jsonl output file wrote to {outputJsonl} with {len(requests)} lines.")
