bios = [
    "C'est la patience",
    "photo, musique, vin, moto, voyages",
    "Rieur",
    "The world is divided into two categories, those who have a level of conscience developed and the others 🇷 #TeamPatriote #JambonBeurre #Macrondehors",
    "Syndicat National de l'Enseignement Technique Agricole Public. Membre de la Fédération Syndicale Unitaire. #FSU #EnseignementAgricole",
    "Enseignante, féministe, et autres gros mots du genre en -iste.",
    "« Elle est à vous, votre culture, et je vous l'ai composée avec amour, comme un bouquet »",
    "Ecole Boule, disque Vogue, Publicis Conseil . Sous le nom d'Olivier Sorel Produit et interprète un spectacle pour faire vivre l'oeuvre de Gilbert Bécaud",
    "MP, Chair of the Foreign Affairs Committee of @Jekaba11 ||| Saeimas deputāts, Ārlietu komisijas priekšsēdētājs, @VL_TBLNNK valdes loceklis, zemessargs",
    "Prône l’union sacré contre les Wokes",
    "Plus rien ne m’étonne jusqu’ici tout va bien",
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
