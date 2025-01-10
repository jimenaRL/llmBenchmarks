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
ap.add_argument('--user_content', type=str, required=False, default="")
ap.add_argument('-v', '--verbose',  action='store_true')
args = ap.parse_args()
framework = args.framework
model = args.model
parameters = args.parameters
port = args.port
user_content = args.user_content
system_content = args.system_content
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
    URL = f"http://localhost:{PORT}/generate_stream"
    HEADERS = {'Content-Type': 'application/json'}
    DATA = {"inputs": "${prompt}", "parameters": parameters}
    DATA = json.dumps(DATA)
elif framework == 'ollama':
    if port:
        PORT = port
    else:
        PORT = 11434
    URL = f"http://localhost:{PORT}/api/generate"
    HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}
    DATA = {"model": model, "prompt": "${prompt}", "keep_alive": "25m"}
    DATA.update(parameters)
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

TESTPROMPT = "1+3?"
if not promptsFile:
    prompts = [TESTPROMPT]
else:
    with open(promptsFile) as csvfile:
        reader = csv.DictReader(csvfile)
        prompts = [row['prompt'] for row in reader]

# add pre prompt
if prePrompt:
    prompts = [prePrompt+p for p in prompts]

async def getPrompts():
    for prompt in prompts:
        yield prompt

async def do_post(session, url, prompt):
    postData = Template(DATA).substitute(prompt=prompt)
    async with session.post(url, data=postData, headers=HEADERS) as response:
        data = await response.text()
        if verbose:
            print(f"[QUERY]: {postData}")
            print(f"[REPONSE]: {data}")
        hashvalue = hashlib.sha1(prompt.encode()).hexdigest()[:8]
        filename = f'{framework}_{modelname}_{hashvalue}.txt'
        with open(filename, 'w') as file:
            file.write(data)

async def run_all():
    async with aiohttp.ClientSession() as session:
        post_tasks = []
        # prepare the coroutines that post
        async for prompt in getPrompts():
            post_tasks.append(do_post(session, url=URL, prompt=prompt))
        # now execute them all at once
        await asyncio.gather(*post_tasks)

asyncio.run(run_all())
