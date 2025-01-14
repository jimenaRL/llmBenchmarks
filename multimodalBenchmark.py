"""An example showing how to use vLLM to serve VLMs.

Launch the vLLM server first in a separated terminal with the following command:
vllm serve llava-hf/llava-1.5-7b-hf --chat-template template_llava.jinja
"""

import csv
import base64
import requests
from openai import OpenAI
from argparse import ArgumentParser

ap = ArgumentParser()
ap.add_argument('--images_urls_file', type=str, required=False, default="")
ap.add_argument('--port', type=str, required=False, default='8000')
ap.add_argument('--text', type=str, required=False, default='What’s in this image?')
ap.add_argument('-v', '--verbose',  action='store_true')
args = ap.parse_args()
images_urls_file = args.images_urls_file
port = args.port
text = args.text
verbose = args.verbose

TESTIMAGEURL = "https://www.oceano.org/wp-content/uploads/2019/06/06_M%C3%A9duse-Pelagia-noctiluca_M_Dagnino-scaled.jpg"
if images_urls_file:
    with open(images_urls_file) as csvfile:
        reader = csv.DictReader(csvfile)
        images_urls = [row['image_url'] for row in reader]
else:
        images_urls = [TESTIMAGEURL]

# Modify OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "EMPTY"
openai_api_base = f"http://localhost:{port}/v1"

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=openai_api_key,
    base_url=openai_api_base,
)

models = client.models.list()
model = models.data[0].id

# Use base64 encoded image in the payload
def encode_image_base64_from_url(image_url: str) -> str:
    """Encode an image retrieved from a remote url to base64 format."""

    with requests.get(image_url) as response:
        response.raise_for_status()
        result = base64.b64encode(response.content).decode('utf-8')

    return result


for image_url in images_urls:

    image_base64 = encode_image_base64_from_url(image_url=image_url)
    chat_completion_from_base64 = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": text
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64, {image_base64}"
                    },
                },
            ],
        }],
        model=model,
        max_tokens=64,
    )

    result = chat_completion_from_base64.choices[0].message.content
    print(f"_______________")
    print(f"text: {text}")
    print(f"Image url: {image_url}")
    print(f"Chat completion output: {result}")









