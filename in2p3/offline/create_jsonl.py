import csv
import json
from string import Template

template_dict = {
    "custom_id": "request-${id}",
    "method": "POST", "url": "/v1/chat/completions",
    "body": {
      "model": "llava-hf/llava-1.5-7b-hf",
      "messages": [
        {
          "role": "system",
          "content": "You are a helpful assistant."
        },
        {
          "role": "user",
          'content': [
            {'type': 'text', 'text': '${prompt}'},
            {'type': 'text', 'text': '${content_text}'},
            {'type': 'image_url', 'image_url': {'url': '${image_url}'}}
            ]
        }
      ],
      "max_completion_tokens": 1000}
}

prompt = "Please indicate whether the Twitter account "
prompt += "(which has the following bio and photo)"
prompt += "belongs to a human person or not."
prompt += "Be concise ans anwers only with yes, no or ambigous."

# load data
with open("data.csv", 'r') as f:
    data = [row for row in csv.reader(f)]

headers = data[0]
data = data[1:]

# remove breaklines from data
for d in data:
    d[2] = d[2].replace("\n", " ")

# customize lines with input data
lines = [
    Template(json.dumps(template_dict)).substitute(
        prompt=prompt,
        id=d[0],
        image_url=d[1],
        content_text=d[2])
    for d in data
]

# checks lines are ok
for line in lines:
    try:
        json.loads(line, strict=True)
    except Exception as e:
        print(f"Unnable to load line as json dict: {line}")
        print(e)

# write lines to jsonl file
with open('test_for_llava.jsonl', 'w') as of:
    for line in lines:
        of.write(line+"\n")


