"""An example showing how to use ollame to serve mutimodal LLMs.

Launch the vLLM server first in a separated terminal with the following command:
docker run -d --runtime nvidia --gpus all -v ollama:/root/.ollama -p {port}:11434 --name ollama ollama/ollama
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
ap.add_argument('--model', type=str, required=False, default="llama3.2-vision")
ap.add_argument('--port', type=int, required=False, default=8000)
ap.add_argument('--text', type=str, required=False, default="I'd like you to look at an image and describe it for me")
ap.add_argument('-v', '--verbose',  action='store_true')
args = ap.parse_args()
images_urls_file = args.images_urls_file
port = args.port
model = args.model
text = args.text
verbose = args.verbose

TESTIMAGEURL = "https://www.oceano.org/wp-content/uploads/2019/06/06_M%C3%A9duse-Pelagia-noctiluca_M_Dagnino-scaled.jpg"
if images_urls_file:
    with open(images_urls_file) as csvfile:
        reader = csv.DictReader(csvfile)
        images_urls = [row['image_url'] for row in reader]
else:
        images_urls = [TESTIMAGEURL]

URL = f"http://localhost:{port}/api/chat"
HEADERS = {'Content-Type': 'application/json'}
DATA = {
    "model": model,
    "stream": False,
    "messages": [
        {
            "role": "user",
            "content": text,
            "images": ["${image64}"]
        }
    ]
}
DATA = json.dumps(DATA)

# Use base64 encoded image in the payload
def encode_image_base64_from_url(image_url: str) -> str:
    """Encode an image retrieved from a remote url to base64 format."""

    with requests.get(image_url) as response:
        response.raise_for_status()
        result = base64.b64encode(response.content).decode('utf-8')

    return result

async def getImages64EncodedFromUrls():
    for image_url in images_urls:
        yield encode_image_base64_from_url(image_url)

async def do_post(session, url, image64):
    postData = Template(DATA).substitute(image64=image64)
    async with session.post(url, data=postData, headers=HEADERS) as response:
        data = await response.text()
        if verbose:
            print(f"[QUERY]: {postData}")
            print(f"[REPONSE]: {data}")
        hashvalue = hashlib.sha1((image64+text).encode()).hexdigest()[:8]
        filename = f'{hashvalue}.txt'
        with open(filename, 'w') as file:
            file.write(data)

async def run_all():
    async with aiohttp.ClientSession() as session:
        post_tasks = []
        # prepare the coroutines that post
        async for image64 in getImages64EncodedFromUrls():
            post_tasks.append(do_post(session, url=URL, image64=image64))
        # now execute them all at once
        await asyncio.gather(*post_tasks)

asyncio.run(run_all())














