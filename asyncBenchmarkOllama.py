import csv
import hashlib
import asyncio
import aiohttp
from string import Template
from argparse import ArgumentParser

ap = ArgumentParser()
ap.add_argument('--model', type=str)
ap.add_argument('--promtsFile', type=str, default="")
args = ap.parse_args()
model = args.model
promtsFile = args.promtsFile

URL = "http://localhost:11434/api/generate"
HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}
DATA = '{"model": "${model}", "prompt": "${prompt}", "stream": false, "keep_alive": "25m"}'

if not promtsFile:
    prompts = ["Why sky is blue?", "1+3?"]
else:
    with open(promtsFile) as csvfile:
        reader = csv.DictReader(csvfile)
        prompts = [row['prompt'] for row in reader]

async def getPrompt():
    for prompt in prompts:
        yield prompt

async def do_post(session, url, model, prompt):
    async with session.post(url, data=Template(DATA).substitute(model=model, prompt=prompt), headers=HEADERS) as response:
        data = await response.text()
        print(f">>>>> Requesting prompt {prompt}")
        hashvalue = hashlib.sha1(prompt.encode()).hexdigest()[:6]
        filename = f'{model}_prompt_{hashvalue}.txt'
        with open(filename, 'w') as file:
            file.write(data)

async def run_all():
    async with aiohttp.ClientSession() as session:
        post_tasks = []
        # prepare the coroutines that post
        async for prompt in getPrompt():
            post_tasks.append(do_post(session, url=URL, model=model, prompt=prompt))
        # now execute them all at once
        await asyncio.gather(*post_tasks)

asyncio.run(run_all())
