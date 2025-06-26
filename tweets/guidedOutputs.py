import csv
from vllm import LLM, SamplingParams
from vllm.sampling_params import GuidedDecodingParams

choices = [
    "Macron",
    "Mélenchon",
    "Le Pen",
    "Aucun"
]
llm = LLM(
    model="HuggingFaceH4/zephyr-7b-beta",
    gpu_memory_utilization=1,
    max_model_len=21500,
    dtype='half')
guided_decoding_params = GuidedDecodingParams(choice=choices)
sampling_params = SamplingParams(
    temperature=0.7,
    top_p=0.95,
    top_k=50,
    max_tokens=16,
    repetition_penalty=1.2,
    guided_decoding=guided_decoding_params)


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


def make_promt(tweet, instructions):
    return [
            {
                "role": "system",
                "content": "Tu es un expert en politique française"
            },
            {
                "role": "user",
                "content":  Template(instructions).substitute(tweet=tweet)
            }
        ]

def getOutputs(tweets, instructions):
    return llm.chat(
        messages=[make_promt(tweet, instructions) for tweet in tweets],
        sampling_params=sampling_params,
        use_tqdm=True)

headers = ['tweet', 'choice']

results_file_1 = "results_promts_1.csv"
with open(results_file_1, 'w') as f:
    results = zip(tweets, getOutputs(tweets, instructions_1))
    writer =  csv.writer(f)
    writer.writerow(headers)
    writer.writerows(results)
    print(f"LLM answers (={len(results)}) saved to {results_file_1}")

