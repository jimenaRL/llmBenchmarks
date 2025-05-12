# Check https://docs.vllm.ai/en/stable/getting_started/examples/openai.html
# and https://github.com/vllm-project/vllm/blob/main/vllm/entrypoints/openai/run_batch.py

INPUT=$1
OUTPUT=$2

python /linkhome/rech/gensoj01/umu89ib/.conda/envs/vllm/lib/python3.12/site-packages/vllm/entrypoints/openai/run_batch.py \
    -i ${INPUT} \
    -o ${OUTPUT} \
    --model llava-hf/llava-1.5-7b-hf
