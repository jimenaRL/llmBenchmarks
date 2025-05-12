import re
import csv
import json
from string import Template

requestTemplate = "requestPattern.json"
biosPath = "biosExample.csv"
outputJsonl = "requestBatch.jsonl"

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
# by substituting each bio into the request pattern
requests =  [Template(pattern).substitute(id=i, userbio=b) for i, b in enumerate(bios)]
dumped_requests = map(json.dumps, requests)
with open(outputJsonl, "w") as f:
    f.writelines('\n'.join(dumped_requests))

# Validate the created jsonl file
with open(outputJsonl, "r") as f:
    reloaded_requests = list(map(json.loads, f.readlines()))

assert len(bios) == len(reloaded_requests)
