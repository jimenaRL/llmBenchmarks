from vllm import LLM, SamplingParams
llm = LLM(model="HuggingFaceH4/zephyr-7b-beta", gpu_memory_utilization=1, max_model_len=21500, dtype='half')
sampling_params = SamplingParams(
    temperature=0.7,
    top_p=0.95,
    top_k=50,
    max_tokens=16,
    repetition_penalty=1.2,
)



    messages=[{
        "role": "system",
        "content": "You are a helpful assistant."
    }, {
        "role": "user",
        "content": "Who won the world series in 2020?"
    }, {
        "role":
        "assistant",
        "content":
        "The Los Angeles Dodgers won the World Series in 2020."
    }, {
        "role": "user",
        "content": "Where was it played?"
    }]


outputs = llm.chat(messages=messages, sampling_params=sampling_params, use_tqdm=True)

res = output.outputs[0].text