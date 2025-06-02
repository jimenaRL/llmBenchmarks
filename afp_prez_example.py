bios = [
    "C'est la virtud",
    "photo, cinéma, bière, moto, voyages",
    "Rigoleur",
    "The world is divided into two categories, those with a developed level of consciousness and those who #TeamPatrie #BeurreJambon #MacronDegage🇷,"
    "Enseignante, féministe, et autres gros mots du genre en -iste.",
    "« C'est la vôtre, votre culture, et je l'ai composée pour vous avec amour, comme un bouquet »",
    "MP, Chair of the Foreign Affairs Committee of @Jekaba11 ||| Saeimas deputāts, Ārlietu komisijas priekšsēdētājs, @VL_TBLNNK valdes loceklis, zemessargs",
    "Plaider pour l'unité sacrée contre le woke",
    "Rien ne me surprend jusqu'à présent, tout va bien",
]


from openai import OpenAI
client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="EMPTY")
model = client.models.list().data[0].id
print(f"Using LLM model {model}")


for bio in bios:
    messages = [
                {
                    "role": "system",
                    "content": "You are an expert in compared politics and political behavior."
                },
                {
                    "role": "user",
                    "content": """Please classify the following Twitter profile bio as “Liberal”, “Not-Liberal” or “Unknown“ according to whether the author of the text (who is from France)
            holds liberal views or beliefs, including but not limited to positive views on abortion, gender equality, and same-sex marriage. Be concise and
            answer only “Liberal”, “Not-Liberal” or “Unknown“: “${userbio}“: """ + bio
                }
            ]
    completion = client.chat.completions.create(model=model,messages=messages)
    print(f"--------------------------------------------------------")
    print(f"[Bio]\n{bio}")
    print(f"[Reponse]\n{completion.choices[0].message.content}")
