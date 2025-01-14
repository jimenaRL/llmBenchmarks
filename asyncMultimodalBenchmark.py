"""An example showing how to use vLLM to serve VLMs.

Launch the vLLM server first in a separated terminal with the following command:
vllm serve llava-hf/llava-1.5-7b-hf --chat-template template_llava.jinja
"""

import csv
import json
import base64
import requests
import hashlib
import asyncio
import aiohttp
from string import Template
from argparse import ArgumentParser

ap = ArgumentParser()
ap.add_argument('--images_urls_file', type=str, required=False, default="")
ap.add_argument('--port', type=int, required=False, default=8000)
ap.add_argument('--max_tokens', type=int, required=False, default=64)
ap.add_argument('--text', type=str, required=False, default="I'd like you to look at an image and describe it for me")
ap.add_argument('-v', '--verbose',  action='store_true')
args = ap.parse_args()
images_urls_file = args.images_urls_file
port = args.port
max_tokens = args.max_tokens
text = args.text
verbose = args.verbose

TESTIMAGEURL = "https://www.oceano.org/wp-content/uploads/2019/06/06_M%C3%A9duse-Pelagia-noctiluca_M_Dagnino-scaled.jpg"
if images_urls_file:
    with open(images_urls_file) as csvfile:
        reader = csv.DictReader(csvfile)
        images_urls = [row['image_url'] for row in reader]
else:
        images_urls = [TESTIMAGEURL]

URL = f"http://localhost:{port}/v1/chat/completions"
HEADERS = {'Content-Type': 'application/json'}
DATA = {
    "model": "llava-hf/llava-1.5-7b-hf",
    "max_tokens": max_tokens,
    "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": text
            },
            {
              "type": "image_url",
              "image_url": {
                "url": "${image_url}"
              }
            }
          ]
        }
    ],
}
DATA = json.dumps(DATA)

async def getImagesUrls():
    for image_url in images_urls:
        yield image_url

async def do_post(session, url, image_url):
    postData = Template(DATA).substitute(image_url=image_url)
    async with session.post(url, data=postData, headers=HEADERS) as response:
        data = await response.text()
        if verbose:
            print(f"[QUERY]: {postData}")
            print(f"[REPONSE]: {data}")
        hashvalue = hashlib.sha1((image_url+text).encode()).hexdigest()[:8]
        filename = f'{hashvalue}.txt'
        with open(filename, 'w') as file:
            file.write(data)

async def run_all():
    async with aiohttp.ClientSession() as session:
        post_tasks = []
        # prepare the coroutines that post
        async for image_url in getImagesUrls():
            post_tasks.append(do_post(session, url=URL, image_url=image_url))
        # now execute them all at once
        await asyncio.gather(*post_tasks)

asyncio.run(run_all())














