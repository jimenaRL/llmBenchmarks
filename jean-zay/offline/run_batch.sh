# Check https://docs.vllm.ai/en/stable/getting_started/examples/openai.html
# and https://github.com/vllm-project/vllm/blob/main/vllm/entrypoints/openai/run_batch.py

python /linkhome/rech/gensoj01/umu89ib/.conda/envs/vllm/lib/python3.12/site-packages/vllm/entrypoints/openai/run_batch.py \
    -i /lustre/fswork/projects/rech/nmf/umu89ib/llmBenchmarks/jean-zay/offline/test_for_llava.jsonl \
    -o llava_results.jsonl \
    --model llava-hf/llava-1.5-7b-hf
