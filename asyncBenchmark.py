import csv
import json
import hashlib
import asyncio
import aiohttp
from string import Template
from argparse import ArgumentParser

ap = ArgumentParser()
ap.add_argument('--framework', type=str, choices=["ollama", "vllm"], required=True)
ap.add_argument('--model', type=str, required=True)
ap.add_argument('--params', type=str, required=False, default="")
ap.add_argument('--port', type=str, default="")
ap.add_argument('--promptsFile', type=str, default="")
ap.add_argument('--prePrompt', type=str, default="")
ap.add_argument('-v', '--verbose',  action='store_true')
args = ap.parse_args()
framework = args.framework
model = args.model
params=args.params
port = args.port
prePrompt = args.prePrompt
promptsFile = args.promptsFile
verbose = args.verbose

modelname = model.split('/')[-1]

if framework == 'ollama':
    if port:
        PORT = port
    else:
        PORT = 11434
    URL = f"http://localhost:{PORT}/api/generate"
    HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}
    DATA = '{"model": "${model}", "prompt": "${prompt}", "stream": false, "keep_alive": "25m"}'
else: # framework == 'vllm'
    if port:
        PORT = port
    else:
        PORT = 8000
    URL = f"http://localhost:{PORT}/v1/completions"
    HEADERS = {'Content-Type': 'application/json'}
    DATA = '{"model": "${model}", "prompt": "${prompt}"}'

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

async def do_post(session, url, model, prompt):
    postData = Template(DATA).substitute(model=model, prompt=prompt)
    if params:
        dataDict = json.loads(postData)
        dataDict.update(json.loads(params))
        postData = json.dumps(dataDict)
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
            post_tasks.append(do_post(session, url=URL, model=model, prompt=prompt))
        # now execute them all at once
        await asyncio.gather(*post_tasks)

asyncio.run(run_all())