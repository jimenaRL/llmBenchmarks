"""An example showing how to use vLLM to serve text+image models 
and run online serving with OpenAI client on an interactive server on IN2P3 computation center.

1. Acces a GPU interactive server on IN2P3 computation platform:

$ srun -p gpu_interactive -t 0-03:00 --mem 16G --gres=gpu:h100:1 --pty bash -i

2. Check that GPU card is available and running

$ nvidia-smi

3. Create a python virtual enviroment and activate it

$ python3 -m venv ./environments/vllmEnv
$ source environments/vllmEnv/bin/activate

4. Install vLLM with CUDA 12.4

$ pip install vllm==0.8.2


6. Launch the vllm serve with llava-1.5 model

$ vllm serve llava-hf/llava-1.5-7b-hf --chat-template vllm/examples/template_llava.jinja --disable-log-stats & 

Pay attention to the "&" at the end of teh command, this allows to continue to use the same interactive terminal on IN2P3
with the vllm server running on a separate process. 

We also disable stats logs for a cleaner terminal. 

We use the chat template for llava model accesible at the [vllm git repository](https://github.com/vllm-project/vllm/tree/main/examples).
"""
import base64

import requests
from openai import OpenAI

from vllm.utils import FlexibleArgumentParser

DEFAULT_IMAGE_URL = "https://static.actu.fr/uploads/2018/12/09f4ec562f0f019b94f347cbcb10307e.jpg"

# Modify OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000/v1"

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=openai_api_key,
    base_url=openai_api_base,
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

def run(image_url, content_text, encode_image, verbose) -> None:

    # Use base64 encoded image in the payload
    if encode_image:
        image_base64 = encode_base64_content_from_url(image_url)
        messages = [{
            "role": "user",
            "content": [
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

    with open("output.txt", "w") as f:
        f.write(result)


def main(args) -> None:
    run(args.image_url, args.content_text, args.encode_image, args.verbose)

if __name__ == "__main__":
    parser = FlexibleArgumentParser(
        description='Demo on using OpenAI client for online serving with '
        'text+image language models served with vLLM.')
    parser.add_argument('--image-url',
                        '-i',
                        type=str,
                        default=DEFAULT_IMAGE_URL,
                        help='Default image url for multimodal data.')
    parser.add_argument('--content-text',
                        '-t',
                        type=str,
                        default="What's in this image?",
                        help='Default content text for multimodal data.')
    parser.add_argument('--encode_image', '-e',  action='store_true')
    parser.add_argument('--verbose', '-v',  action='store_true')

    args = parser.parse_args()
    print(args)
    main(args)
