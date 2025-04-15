# Check https://docs.vllm.ai/en/stable/getting_started/examples/openai.html
# and https://github.com/vllm-project/vllm/blob/main/vllm/entrypoints/openai/run_batch.py

python /sps/humanum/user/jroyolet/dev/vllm/vllm/entrypoints/openai/run_batch.py \
    -i test_for_llava.jsonl \
    -o llava_results.jsonl \
    --model llava-hf/llava-1.5-7b-hf
