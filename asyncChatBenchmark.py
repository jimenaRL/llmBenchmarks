"""
Usage example:

time python asyncChatBenchmark.py \
    --framework={vllm or tgi} \
    --port {port} \
    --model=HuggingFaceH4/zephyr-7b-beta \
    --parameters='{"temperature": 0.7, "max_tokens": 16, "top_k": 50, "top_p": 0.95, "repetition_penalty": 1.2}' \
    --messages_file=twitterBios.csv \
    --system_content="You are an expert in sports. Please classify the following Twitter profile bio as 'sport-fan' or 'not-sport-fan'. This is the bio:"

To use this script with vllm or tgi frameworks on gépéhu, you must first launch a chat completion server.
Here are some examples using zephyr model on CPU, 1 GPU or 2 GPUs.

[vllm CPU]

docker run -d --name myVLLMChatCompleteionServerCPU \
    -v /home/{username}/storage:/root/.cache/huggingface \
    -p {port}:8000 \
    vllm-cpu-env \
    --model HuggingFaceH4/zephyr-7b-beta

[vllm 1 GPU]

vllm serve HuggingFaceH4/zephyr-7b-beta \
    --port {port} \
    --gpu_memory_utilization 1 \
    --max_model_len 21500

or

docker run -d --name myVLLMChatCompleteionServer1GPU --runtime nvidia --gpus '"device=0"' \
    -v /home/{username}/storage:/root/.cache/huggingface \
    -p {port}:8000 \
    --env "PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True" \
    --ipc=host \
    vllm/vllm-openai:latest \
    --model HuggingFaceH4/zephyr-7b-beta \
    --gpu_memory_utilization 1 \
    --max_model_len 21500

[tgi 1 GPU]

docker run -d --name myTGIChatCompleteionServer1GPU --gpus '"device=1"' \
    --shm-size 1g \
    -p {port}:80 \
    -v /home/{username}/storage:/data \
    ghcr.io/huggingface/text-generation-inference:3.0.0 \
    --model-id HuggingFaceH4/zephyr-7b-beta

[tgi 2 GPU]

docker run -d --name myTGIChatCompleteionServer2GPUs --gpus all \
    --shm-size 1g \
    -p {port}:80 \
    -v /home/{username}/storage/hf_cache:/data \
    ghcr.io/huggingface/text-generation-inference:3.0.0 \
    --model-id HuggingFaceH4/zephyr-7b-beta \
    --num-shard=2

"""

import os
import csv
import json
import hashlib
import asyncio
import aiohttp
from string import Template
from argparse import ArgumentParser

ap = ArgumentParser()
ap.add_argument('--framework', type=str, choices=["tgi", "vllm", "ollama"], required=True)
ap.add_argument('--model', type=str, required=False, default="")
ap.add_argument('--parameters', type=str, required=False, default="")
ap.add_argument('--port', type=str, required=False)
ap.add_argument('--system_content', type=str, required=False, default="")
ap.add_argument('--output_folder', type=str, required=False, default="outputs")
ap.add_argument('--user_content', type=str, required=False, default="")
ap.add_argument('--messages_file', type=str, required=False, default="")
ap.add_argument('-v', '--verbose',  action='store_true')
args = ap.parse_args()
framework = args.framework
model = args.model
parameters = args.parameters
port = args.port
user_content = args.user_content
output_folder = args.output_folder
system_content = args.system_content
messages_file = args.messages_file
verbose = args.verbose


if parameters:
    parameters = json.loads(parameters)
else:
    parameters = {}

if framework == 'tgi':
    if port:
        PORT = port
    else:
        PORT = 8080
    URL = f"http://localhost:{PORT}/v1/chat/completions"
    HEADERS = {'Content-Type': 'application/json'}
    DATA = {
        "model": "tgi",
        "messages": [
            {"role": "system", "content": "${system_content}"},
            {"role": "user", "content": "${user_content}"}
        ],
        "stream": False
    }
    DATA.update(parameters)
    DATA = json.dumps(DATA)
elif framework == 'ollama':
    if port:
        PORT = port
    else:
        PORT = 11434
    URL = f"http://localhost:{PORT}/api/chat"
    HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}
    DATA = {
        "model": model,
        "stream": False,
        "keep_alive": "25m",
        "messages": [
            {"role": "system", "content": "${system_content}"},
            {"role": "user", "content": "${user_content}"}
        ]
    }
    DATA["options"] = parameters
    DATA = json.dumps(DATA)
else: # framework == 'vllm'
    if port:
        PORT = port
    else:
        PORT = 8000
    URL = f"http://localhost:{PORT}/v1/chat/completions"
    HEADERS = {'Content-Type': 'application/json'}
    DATA = {
        "model": model,
        "messages": [
            {"role": "system", "content": "${system_content}"},
            {"role": "user", "content": "${user_content}"}
        ]
    }
    DATA.update(parameters)
    DATA = json.dumps(DATA)

modelname = model.split('/')[-1]

if messages_file and not system_content:
    with open(messages_file) as csvfile:
        reader = csv.DictReader(csvfile)
        messages = [[row['system'], row['user']] for row in reader]
elif messages_file and system_content:
    with open(messages_file) as csvfile:
        reader = csv.DictReader(csvfile)
        messages = [[system_content, row['user']] for row in reader]
elif system_content & user_content:
        system_contents = [system_content]
        user_contents = [user_content]
else:
    raise ValueError(
        "Must specify `messages_file` or `system_content` and `user_content`.")

async def getMessages():
    for message in messages:
        yield message[0], message[1]

async def do_post(session, url, system_content, user_content):
    postData = Template(DATA).substitute(system_content=system_content, user_content=user_content)
    async with session.post(url, data=postData, headers=HEADERS) as response:
        data = await response.text()
        if verbose:
            print(f"[QUERY]: {postData}")
            print(f"[REPONSE]: {data}")
        hashvalue = hashlib.sha1((system_content+user_content).encode()).hexdigest()[:8]
        filename = os.path.join(output_folder, f'{framework}_{modelname}_{hashvalue}.txt')
        with open(filename, 'w') as file:
            file.write(data)

async def run_all():
    async with aiohttp.ClientSession() as session:
        post_tasks = []
        # prepare the coroutines that post
        async for system_content, user_content in getMessages():
            post_tasks.append(do_post(session, url=URL, system_content=system_content, user_content=user_content))
        # now execute them all at once
        await asyncio.gather(*post_tasks)

asyncio.run(run_all())
