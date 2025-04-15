"""An example showing how to use vLLM to serve text+image models
and run online serving with OpenAI client on a single interactive terminal
on the IN2P3 computation center.

1. Acces a GPU interactive terminal on IN2P3 computation platform:

$ srun -p gpu_interactive -t 0-03:00 --mem 16G --gres=gpu:h100:1 --pty bash -i

2. Check that GPU card is available and running

$ nvidia-smi

3. Create a python virtual enviroment and activate it

$ python3 -m venv ./environments/vllmEnv
$ source environments/vllmEnv/bin/activate

The creation must be done only one time but the activattion
must be donne at each conection to the interactive terminal.

4. Install vLLM with pip 

$ pip install vllm==0.8.2

The 0.8.2 version has support for the CUDA version (12.4) installed.

6. Launch the vllm server with llava-1.5 model

$ vllm serve llava-hf/llava-1.5-7b-hf --chat-template template_llava.jinja --disable-log-stats &

Pay attention to the "&" at the end of the command,
this allows you to continue using the same interactive terminal on IN2P3
while the vLLM server is running in the background on a separate process.

Since the vllm server will run on the same terminal as the python script consuming it,
we disable the statistics logs to have a cleaner terminal.

Note also that we use the chat template for llava model accesible at the
[vllm git repository](https://github.com/vllm-project/vllm/tree/main/examples).

7. Wait for about 5-10 minutes until the server is ready and stable, and then launch this python script:

$ python openai_chat_completion_client_for_multimodal.py -v \
--prompt="Please indicate whether the Twitter account (which has the following bio and photo) belongs to a human person or not. Be concise ans anwers only with yes, no or undeterminate." \
--content_text="Président de la République française." \
--image_url=https://pbs.twimg.com/profile_images/1550535324501164032/0lTW_4tj_400x400.jpg
"""

import csv
import base64

import requests
from openai import OpenAI

from argparse import ArgumentParser

DEFAULT_IMAGE_URL = "https://pbs.twimg.com/profile_images/1570498434532089858/VeyQlH3U_400x400.jpg"
DEFAULT_CONTENT_TEXT = "This is Chimamanda Ngozi Adichie’s official Twitter."
DEFAULT_PROMPT = """
    Please state if the twitter account to which the followings bio and picture belongs to a human person or not.
    Be concise ans anwers only with yes, no or undeterminate."""

# Modify OpenAI's API key and API base to use vLLM's API server.
OPENAI_API_KEY = "EMPTY"
OPENAI_API_BASE = "http://localhost:8000/v1"

client = OpenAI(
     # defaults to os.environ.get("OPENAI_API_KEY")
     api_key=OPENAI_API_KEY,
     base_url=OPENAI_API_BASE,
)

models = client.models.list()
model = models.data[0].id

def encode_base64_content_from_url(content_url: str) -> str:
    """Encode a content retrieved from a remote url to base64 format."""

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    with requests.get(content_url, headers=headers) as response:
        response.raise_for_status()
        result = base64.b64encode(response.content).decode('utf-8')

    return result

def run(id, prompt, image_url, content_text, encode_image, verbose) -> None:

    # Use base64 encoded image in the payload
    if encode_image:
        image_base64 = encode_base64_content_from_url(image_url)
        messages = [{
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt
                },
                {
                    "type": "text",
                    "text": content_text
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_base64}"
                    },
                },
            ],
        }]

    # Use image url in the payload
    else:
        messages = [{
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "text",
                        "text": content_text
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url
                        },
                    },
                ],
            }]

    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model,
        max_completion_tokens=64)
    result = chat_completion.choices[0].message.content

    if verbose:
        log = "Chat completion output from "
        if encode_image:
            log += "base64 encoded"
        else:
            log += "url"
        print(f"{log} image: {result}")

    with open(f"{id}.txt", "w") as f:
        f.write(f"{content_text}: {result}\n")


def main(args) -> None:
    if args.csv_file is None:
        run("reponse",
            args.prompt,
            args.image_url,
            args.content_text,
            args.encode_image,
            args.verbose)
    else:
        with open(args.csv_file, mode ='r') as file:
          csvFile = csv.DictReader(file)
          for i, d in enumerate(csvFile):
                run(i,
                    args.prompt,
                    d['image_url'],
                    d['content_text'],
                    args.encode_image,
                    args.verbose)

if __name__ == "__main__":
    parser = ArgumentParser(
        description='Demo on using OpenAI client for online serving with '
        'text+image language models served with vLLM.')
    parser.add_argument('--image_url',
                        '-i',
                        type=str,
                        default=DEFAULT_IMAGE_URL,
                        help='Image url for multimodal data.')
    parser.add_argument('--prompt',
                        '-p',
                        type=str,
                        default=DEFAULT_PROMPT,
                        help='The prompt.')
    parser.add_argument('--content_text',
                        '-t',
                        type=str,
                        default=DEFAULT_CONTENT_TEXT,
                        help='Content text for multimodal data.')
    parser.add_argument('--csv_file',
                        '-f',
                        type=str,
                        help='CSV file with image_url and content_text columns.')
    parser.add_argument('--encode_image', '-e',  action='store_true')
    parser.add_argument('--verbose', '-v',  action='store_true')

    args = parser.parse_args()
    print(args)
    main(args)
