# Check https://docs.vllm.ai/en/stable/getting_started/examples/openai.html
# and https://github.com/vllm-project/vllm/blob/main/vllm/entrypoints/openai/run_batch.py

INPUT=$1
OUTPUT=$2

python /linkhome/rech/gensoj01/umu89ib/.conda/envs/vllm/lib/python3.12/site-packages/vllm/entrypoints/openai/run_batch.py \
    -i ${INPUT} \
    -o ${OUTPUT} \
    --model=HuggingFaceH4/zephyr-7b-beta \
    --gpu-memory-utilization=0.9 \
    --max_model_len=21500 \
    --dtype=half
