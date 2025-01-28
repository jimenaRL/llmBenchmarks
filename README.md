# LLM serving using inference optimized frameworks

- [vllm](https://github.com/vllm-project/vllm/)
- [tgi](https://github.com/huggingface/text-generation-inference/)

Scripts usage example: 

```
time python asyncChatBenchmark.py \    
    --framework={vllm or tgi} \
    --port {port} \
    --model=HuggingFaceH4/zephyr-7b-beta \
    --parameters='{"temperature": 0.7, "max_tokens": 16, "top_k": 50, "top_p": 0.95, "repetition_penalty": 1.2}' \
    --messages_file=twitterBios.csv \
    --system_content="You are an expert in sports. Please classify the following Twitter profile bio as 'sport-fan' or 'not-sport-fan'. This is the bio:"
```

To use the [async chat script](https://github.com/jimenaRL/llmBenchmarks/blob/main/asyncChatBenchmark.py) with vllm or tgi frameworks on gépéhu, you must first launch a chat completion server. Here are some examples using zephyr model on CPU, 1 or 2 NVIDIA RTX A4500 graphics cards.

### vllm CPU

```
docker run -d --name myVLLMChatCompleteionServerCPU \                 
    -v /home/{username}/storage:/root/.cache/huggingface \
    -p {port}:8000 \
    vllm-cpu-env \
    --model HuggingFaceH4/zephyr-7b-beta
```

### vllm 1 GPU

```
vllm serve HuggingFaceH4/zephyr-7b-beta \
    --port {port} \
    --gpu_memory_utilization 1 \
    --max_model_len 21500
```
or

```
docker run -d --name myVLLMChatCompleteionServer1GPU --runtime nvidia --gpus '"device=0"' \
    -v /home/{username}/storage:/root/.cache/huggingface \
    -p {port}:8000 \           
    --env "PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True" \
    --ipc=host \                                         
    vllm/vllm-openai:latest \              
    --model HuggingFaceH4/zephyr-7b-beta \
    --gpu_memory_utilization 1 \
    --max_model_len 21500
``` 

### tgi 1 GPU


```
docker run -d --name myTGIChatCompleteionServer1GPU --gpus '"device=1"' \
    --shm-size 1g \
    -p {port}:80 \
    -v /home/{username}/storage:/data \
    ghcr.io/huggingface/text-generation-inference:3.0.0 \
    --model-id HuggingFaceH4/zephyr-7b-beta
```

### tgi 2 GPU

```
docker run -d --name myTGIChatCompleteionServer2GPUs --gpus all \
    --shm-size 1g \
    -p {port}:80 \
    -v /home/{username}/storage/hf_cache:/data \
    ghcr.io/huggingface/text-generation-inference:3.0.0 \
    --model-id HuggingFaceH4/zephyr-7b-beta \
    --num-shard=2
```
