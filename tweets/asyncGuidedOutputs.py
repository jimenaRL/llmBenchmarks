import csv
from vllm import LLM, SamplingParams
from vllm.sampling_params import GuidedDecodingParams

guided_choice = [
    "Macron",
    "Mélenchon",
    "Le Pen",
    "Aucun"
]

instructions_1 = """Tu vas classifier des messages des médias sociaux selon s’ils expriment l’intention de voter pour un candidat
ou s’ils appellent à voter pour un candidat à l’élection présidentielle de 2022 en France.
Dis moi si le message suivant exprime l'intention de voter pour ou appelle à voter pour Macron, Mélenchon ou Le Pen,
en répondant uniquement par le nom de famille du candidat, ou par “Aucun”, si le message ne montre soutien pour aucun de ces trois candidats.
Voici le message: ${tweet}
"""

instructions_2 = """Tu vas classifier des messages des médias sociaux selon s’ils expriment du soutien pour un candidat
à l’élection présidentielle de 2022 en France.
Dis moi si le message suivant exprime du soutien pour Macron, Mélenchon ou Le Pen, en répondant uniquement
par le nom de famille du candidat, ou par le mot “Autre”, si le message n’exprime pas d’intention vote ou appelle
à voter pour l’un de ces trois candidats.
Voici le message: ${tweet}
"""

with open('sample_xan_seed_761.csv', newline='') as f:
    tweets = [r[:-1] for r in f.readlines()][1:]
print(f"Load {len(tweets)} tweets.")

# 0/ Launch vllm server
cmd = "vllm serve HuggingFaceH4/zephyr-7b-beta --guided-decoding-backend=xgrammar --disable-log-stats --dtype=half &"
os.system(cmd)
print(f"Launched command:\n\t{cmd}")

# 4/ Wait for vllm server to be available and retrive model
openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000/v1"
client = OpenAI(
    base_url=openai_api_base,
    api_key=openai_api_key)

model = None
while not model:
    try:
        model = client.models.list().data[0].id
    except Exception as e:
        print(f"Model not ready: {e}")
        sleep(30)
print(f"Model is ready: {model} !")


# 5/ Create async functions to request vllm server trought openAI api
async def doCompletetion(model, messages, extra_body):
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        extra_body=extra_body)
    content = completion.choices[0].message.content
    return content

async def asyncMessageIterator(instructions):
    for tweet in tweets:
        yield [
                    {
                        "role": "system",
                        "content": "Tu es un expert en politique française."
                    },
                    {
                        "role": "user",
                        "content":  Template(instructions).substitute(tweet=tweet)
                    }
                ]


label_extra_body = {
    "guided_choice": guided_choice,
    "temperature": 0.7,
    "max_tokens": 16,
    "top_k": 50,
    "top_p": 0.95,
    "repetition_penalty": 1.2,
    }

async def run_all(instructions):
    # Asynchronously call the function for each prompt
    tasks = [
        doCompletetion(model, messages, label_extra_body)
        async for messages in asyncMessageIterator(instructions)
    ]
    # Gather and run the tasks concurrently
    results = await asyncio.gather(*tasks)
    return results

# 6/ Run all courutines
headers = ['tweet', 'choice']

results_1 = asyncio.run(run_all(instructions_1))
results_file_1 = "results_promts_1.csv"
with open(results_file_1, 'w') as f:
    writer =  csv.writer(f)
    writer.writerow(headers)
    writer.writerows(results_1)
    print(f"LLM answers (={len(results_1)}) saved to {results_file_1}")

results_2 = asyncio.run(run_all(instructions_2))
results_file_2 = "results_promts_2.csv"
with open(results_file_2, 'w') as f:
    writer =  csv.writer(f)
    writer.writerow(headers)
    writer.writerows(results_2)
    print(f"LLM answers (={len(results_2)}) saved to {results_file_2}")



