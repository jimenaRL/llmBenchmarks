export MODELPARAMS="'{\"model\": \"HuggingFaceH4/zephyr-7b-beta\", \"guided_decoding_backend\": \"xgrammar\", \"seed\": 19, \"gpu_memory_utilization\": 0.9}'"
export SAMPLINGPARAMS="'{\"temperature\": 0.7, \"top_p\": 0.95, \"top_k\": 50, \"max_tokens\": 16, \"repetition_penalty\": 1.2, \"seed\": 19}'"
export CHOICES=""
export OUTFOLDER=outputs/v1/1xH100_zephyr-7b-beta/free
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:1 \
    --export=ALL \
    binaryChoicesPromptsEnglish_v1.slurm


export MODELPARAMS="'{\"model\": \"HuggingFaceH4/zephyr-7b-beta\", \"guided_decoding_backend\": \"xgrammar\", \"seed\": 19, \"gpu_memory_utilization\": 0.9}'"
export SAMPLINGPARAMS="'{\"temperature\": 0.7, \"top_p\": 0.95, \"top_k\": 50, \"max_tokens\": 16, \"repetition_penalty\": 1.2, \"seed\": 19}'"
export CHOICES="'YES,NO'"
export OUTFOLDER=outputs/v1/1xH100_zephyr-7b-beta/guided
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:1 \
    --export=ALL \
    binaryChoicesPromptsEnglish_v1.slurm


export MODELPARAMS="'{\"model\": \"HuggingFaceH4/zephyr-7b-beta\", \"guided_decoding_backend\": \"xgrammar\", \"seed\": 19, \"gpu_memory_utilization\": 0.9}'"
export SAMPLINGPARAMS="'{\"temperature\": 0.7, \"top_p\": 0.95, \"top_k\": 50, \"max_tokens\": 16, \"repetition_penalty\": 1.2, \"seed\": 19}'"
export CHOICES=""
export OUTFOLDER=outputs/v1/1xH100_zephyr-7b-beta/free
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:1 \
    --export=ALL \
    multipleChoicesPromptsEnglish_v1.slurm


export MODELPARAMS="'{\"model\": \"HuggingFaceH4/zephyr-7b-beta\", \"guided_decoding_backend\": \"xgrammar\", \"seed\": 19, \"gpu_memory_utilization\": 0.9}'"
export SAMPLINGPARAMS="'{\"temperature\": 0.7, \"top_p\": 0.95, \"top_k\": 50, \"max_tokens\": 16, \"repetition_penalty\": 1.2, \"seed\": 19}'"
export CHOICES="'Macron,Mélenchon,Le Pen,None'"
export OUTFOLDER=outputs/v1/1xH100_zephyr-7b-beta/guided
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:1 \
    --export=ALL \
    multipleChoicesPromptsEnglish_v1.slurm


--------------------------------------------------------------------------------

export MODELPARAMS="'{\"model\": \"openai/gpt-oss-20b\", \"guided_decoding_backend\": \"xgrammar\", \"seed\": 19}'"
export SAMPLINGPARAMS="'{\"seed\": 19, \"max_tokens\": 256}'"
export CHOICES="'YES,NO'"
export OUTFOLDER=outputs/v1/1xH100_gpt-oss-20b/guided
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:1 \
    --export=ALL \
    binaryChoicesPromptsEnglish_v1.slurm


export MODELPARAMS="'{\"model\": \"openai/gpt-oss-20b\", \"guided_decoding_backend\": \"xgrammar\", \"seed\": 19}'"
export SAMPLINGPARAMS="'{\"seed\": 19, \"max_tokens\": 256}'"
export CHOICES="'Macron,Mélenchon,Le Pen,None'"
export OUTFOLDER=outputs/v1/1xH100_gpt-oss-20b/guided
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:1 \
    --export=ALL \
    multipleChoicesPromptsEnglish_v1.slurm


export MODELPARAMS="'{\"model\": \"openai/gpt-oss-20b\", \"guided_decoding_backend\": \"xgrammar\", \"seed\": 19}'"
export SAMPLINGPARAMS="'{\"seed\": 19, \"max_tokens\": 256}'"
export CHOICES="''"
export OUTFOLDER=outputs/v1/1xH100_gpt-oss-20b/free
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:1 \
    --export=ALL \
    binaryChoicesPromptsEnglish_v1.slurm


export MODELPARAMS="'{\"model\": \"openai/gpt-oss-20b\", \"guided_decoding_backend\": \"xgrammar\", \"seed\": 19}'"
export SAMPLINGPARAMS="'{\"seed\": 19, \"max_tokens\": 256}'"
export CHOICES="''"
export OUTFOLDER=outputs/v1/1xH100_gpt-oss-20b/free
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:1 \
    --export=ALL \
    multipleChoicesPromptsEnglish_v1.slurm


--------------------------------------------------------------------------------

export MODELPARAMS="'{\"model\": \"openai/gpt-oss-120b\", \"guided_decoding_backend\": \"xgrammar\", \"seed\": 19}'"
export SAMPLINGPARAMS="'{\"seed\": 19, \"max_tokens\": 256}'"
export CHOICES="'YES,NO'"
export OUTFOLDER=outputs/v1/1xH100_gpt-oss-120b/guided
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:1 \
    --export=ALL \
    binaryChoicesPromptsEnglish_v1.slurm


export MODELPARAMS="'{\"model\": \"openai/gpt-oss-120b\", \"guided_decoding_backend\": \"xgrammar\", \"seed\": 19}'"
export SAMPLINGPARAMS="'{\"seed\": 19, \"max_tokens\": 256}'"
export CHOICES="'Macron,Mélenchon,Le Pen,None'"
export OUTFOLDER=outputs/v1/1xH100_gpt-oss-120b/guided
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:1 \
    --export=ALL \
    multipleChoicesPromptsEnglish_v1.slurm


export MODELPARAMS="'{\"model\": \"openai/gpt-oss-120b\", \"guided_decoding_backend\": \"xgrammar\", \"seed\": 19}'"
export SAMPLINGPARAMS="'{\"seed\": 19, \"max_tokens\": 256}'"
export CHOICES="''"
export OUTFOLDER=outputs/v1/1xH100_gpt-oss-120b/free
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:1 \
    --export=ALL \
    binaryChoicesPromptsEnglish_v1.slurm


export MODELPARAMS="'{\"model\": \"openai/gpt-oss-120b\", \"guided_decoding_backend\": \"xgrammar\", \"seed\": 19}'"
export SAMPLINGPARAMS="'{\"seed\": 19, \"max_tokens\": 256}'"
export CHOICES="''"
export OUTFOLDER=outputs/v1/1xH100_gpt-oss-120b/free
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:1 \
    --export=ALL \
    multipleChoicesPromptsEnglish_v1.slurm

--------------------------------------------------------------------------------

export MODELPARAMS="'{\"model\": \"deepseek-ai/DeepSeek-R1-Distill-Llama-70B\", \"guided_decoding_backend\": \"xgrammar\", \"seed\": 119, \"tensor_parallel_size\": 2, \"max_model_len\": 9000}'"
export SAMPLINGPARAMS="'{\"temperature\": 0.6, \"top_p\": 0.95, \"seed\": 19, \"max_tokens\": 256}'"
export CHOICES="'YES,NO'"
export OUTFOLDER=outputs/v1/2xH100_max_model_len_9000_DeepSeek-R1-Distill-Llama-70B/guided
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:2 \
    --export=ALL \
    binaryChoicesPromptsEnglish_v1.slurm


export MODELPARAMS="'{\"model\": \"deepseek-ai/DeepSeek-R1-Distill-Llama-70B\", \"guided_decoding_backend\": \"xgrammar\", \"seed\": 119, \"tensor_parallel_size\": 2, \"max_model_len\": 9000}'"
export SAMPLINGPARAMS="'{\"temperature\": 0.6, \"top_p\": 0.95, \"seed\": 19, \"max_tokens\": 256}'"
export CHOICES="'Macron,Mélenchon,Le Pen,None'"
export OUTFOLDER=outputs/v1/2xH100_max_model_len_9000_DeepSeek-R1-Distill-Llama-70B/guided
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:2 \
    --export=ALL \
    multipleChoicesPromptsEnglish_v1.slurm


export MODELPARAMS="'{\"model\": \"deepseek-ai/DeepSeek-R1-Distill-Llama-70B\", \"guided_decoding_backend\": \"xgrammar\", \"seed\": 119, \"tensor_parallel_size\": 2, \"max_model_len\": 9000}'"
export SAMPLINGPARAMS="'{\"temperature\": 0.6, \"top_p\": 0.95, \"seed\": 19, \"max_tokens\": 256}'"
export CHOICES="''"
export OUTFOLDER=outputs/v1/2xH100_max_model_len_9000_DeepSeek-R1-Distill-Llama-70B/free
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:2 \
    --export=ALL \
    binaryChoicesPromptsEnglish_v1.slurm


export MODELPARAMS="'{\"model\": \"deepseek-ai/DeepSeek-R1-Distill-Llama-70B\", \"guided_decoding_backend\": \"xgrammar\", \"seed\": 119, \"tensor_parallel_size\": 2, \"max_model_len\": 9000}'"
export SAMPLINGPARAMS="'{\"temperature\": 0.6, \"top_p\": 0.95, \"seed\": 19, \"max_tokens\": 256}'"
export CHOICES="''"
export OUTFOLDER=outputs/v1/2xH100_max_model_len_9000_DeepSeek-R1-Distill-Llama-70B/free
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:2 \
    --export=ALL \
    multipleChoicesPromptsEnglish_v1.slurm


-------------------------------------------------------------------------------

export MODELPARAMS="'{\"model\": \"Qwen/Qwen3-30B-A3B-Instruct-2507\", \"guided_decoding_backend\": \"xgrammar\", \"seed\": 119, \"max_model_len\": 8000, \"tensor_parallel_size\": 1}'"
export SAMPLINGPARAMS="'{\"temperature\": 0.7, \"min_p\": 0, \"top_p\": 0.8, \"top_k\": 20, \"seed\": 19, \"max_tokens\": 256}'"
export CHOICES="'YES,NO'"
export OUTFOLDER=outputs/v1/1xH100_max_model_len_8000_Qwen3-30B-A3B-Instruct-2507/guided
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:1 \
    --export=ALL \
    binaryChoicesPromptsEnglish_v1.slurm

export MODELPARAMS="'{\"model\": \"Qwen/Qwen3-30B-A3B-Instruct-2507\", \"guided_decoding_backend\": \"xgrammar\", \"seed\": 119, \"max_model_len\": 8000, \"tensor_parallel_size\": 1}'"
export SAMPLINGPARAMS="'{\"temperature\": 0.7, \"min_p\": 0, \"top_p\": 0.8, \"top_k\": 20, \"seed\": 19, \"max_tokens\": 256}'"
export CHOICES="'Macron,Mélenchon,Le Pen,None'"
export OUTFOLDER=outputs/v1/1xH100_max_model_len_8000_Qwen3-30B-A3B-Instruct-2507/guided
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:1 \
    --export=ALL \
    multipleChoicesPromptsEnglish_v1.slurm


export MODELPARAMS="'{\"model\": \"Qwen/Qwen3-30B-A3B-Instruct-2507\", \"guided_decoding_backend\": \"xgrammar\", \"seed\": 119, \"max_model_len\": 8000, \"tensor_parallel_size\": 1}'"
export SAMPLINGPARAMS="'{\"temperature\": 0.7, \"min_p\": 0, \"top_p\": 0.8, \"top_k\": 20, \"seed\": 19, \"max_tokens\": 256}'"
export CHOICES="''"
export OUTFOLDER=outputs/v1/1xH100_max_model_len_8000_Qwen3-30B-A3B-Instruct-2507/free
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:1 \
    --export=ALL \
    binaryChoicesPromptsEnglish_v1.slurm


export MODELPARAMS="'{\"model\": \"Qwen/Qwen3-30B-A3B-Instruct-2507\", \"guided_decoding_backend\": \"xgrammar\", \"seed\": 119, \"max_model_len\": 8000, \"tensor_parallel_size\": 1}'"
export SAMPLINGPARAMS="'{\"temperature\": 0.7, \"min_p\": 0, \"top_p\": 0.8, \"top_k\": 20, \"seed\": 19, \"max_tokens\": 256}'"
export CHOICES="''"
export OUTFOLDER=outputs/v1/1xH100_max_model_len_8000_Qwen3-30B-A3B-Instruct-2507/free
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:1 \
    --export=ALL \
    multipleChoicesPromptsEnglish_v1.slurm

-------------------------------------------------------------------------------


export MODELPARAMS="'{\"model\": \"mistralai/Mistral-Small-24B-Instruct-2501\", \"tokenizer_mode\": \"mistral\", \"config_format\": \"mistral\", \"load_format\": \"mistral\", \"guided_decoding_backend\": \"xgrammar\", \"seed\": 119, \"tensor_parallel_size\": 1}'"
export SAMPLINGPARAMS="'{\"temperature\": 0.15, \"seed\": 19, \"max_tokens\": 256}'"
export CHOICES="'YES,NO'"
export OUTFOLDER=outputs/v1/1xH100_Mistral-Small-24B-Instruct-2501/guided
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:1 \
    --export=ALL \
    binaryChoicesPromptsEnglish_v1.slurm

export MODELPARAMS="'{\"model\": \"mistralai/Mistral-Small-24B-Instruct-2501\", \"tokenizer_mode\": \"mistral\", \"config_format\": \"mistral\", \"load_format\": \"mistral\", \"guided_decoding_backend\": \"xgrammar\", \"seed\": 119, \"tensor_parallel_size\": 1}'"
export SAMPLINGPARAMS="'{\"temperature\": 0.15, \"seed\": 19, \"max_tokens\": 256}'"
export CHOICES="'Macron,Mélenchon,Le Pen,None'"
export OUTFOLDER=outputs/v1/1xH100_Mistral-Small-24B-Instruct-2501/guided
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:1 \
    --export=ALL \
    multipleChoicesPromptsEnglish_v1.slurm


export MODELPARAMS="'{\"model\": \"mistralai/Mistral-Small-24B-Instruct-2501\", \"tokenizer_mode\": \"mistral\", \"config_format\": \"mistral\", \"load_format\": \"mistral\", \"guided_decoding_backend\": \"xgrammar\", \"seed\": 119, \"tensor_parallel_size\": 1}'"
export SAMPLINGPARAMS="'{\"temperature\": 0.15, \"seed\": 19, \"max_tokens\": 256}'"
export CHOICES="''"
export OUTFOLDER=outputs/v1/1xH100_Mistral-Small-24B-Instruct-2501/free
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:1 \
    --export=ALL \
    binaryChoicesPromptsEnglish_v1.slurm


export MODELPARAMS="'{\"model\": \"mistralai/Mistral-Small-24B-Instruct-2501\", \"tokenizer_mode\": \"mistral\", \"config_format\": \"mistral\", \"load_format\": \"mistral\", \"guided_decoding_backend\": \"xgrammar\", \"seed\": 119, \"tensor_parallel_size\": 1}'"
export SAMPLINGPARAMS="'{\"temperature\": 0.15, \"seed\": 19, \"max_tokens\": 256}'"
export CHOICES="''"
export OUTFOLDER=outputs/v1/1xH100_Mistral-Small-24B-Instruct-2501/free
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:1 \
    --export=ALL \
    multipleChoicesPromptsEnglish_v1.slurm


--------------------------------------------------------------------------------

export MODELPARAMS="'{\"model\": \"mistralai/Mistral-Small-3.1-24B-Instruct-2503\", \"tokenizer_mode\": \"mistral\", \"config_format\": \"mistral\", \"load_format\": \"mistral\", \"guided_decoding_backend\": \"xgrammar\", \"seed\": 119, \"tensor_parallel_size\": 1}'"
export SAMPLINGPARAMS="'{\"temperature\": 0.15, \"seed\": 19, \"max_tokens\": 256}'"
export CHOICES="'YES,NO'"
export OUTFOLDER=outputs/v1/1xH100_Mistral-Small-3.1-24B-Instruct-2503/guided
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:1 \
    --export=ALL \
    binaryChoicesPromptsEnglish_v1.slurm

export MODELPARAMS="'{\"model\": \"mistralai/Mistral-Small-3.1-24B-Instruct-2503\", \"tokenizer_mode\": \"mistral\", \"config_format\": \"mistral\", \"load_format\": \"mistral\", \"guided_decoding_backend\": \"xgrammar\", \"seed\": 119, \"tensor_parallel_size\": 1}'"
export SAMPLINGPARAMS="'{\"temperature\": 0.15, \"seed\": 19, \"max_tokens\": 256}'"
export CHOICES="'Macron,Mélenchon,Le Pen,None'"
export OUTFOLDER=outputs/v1/1xH100_Mistral-Small-3.1-24B-Instruct-2503/guided
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:1 \
    --export=ALL \
    multipleChoicesPromptsEnglish_v1.slurm


export MODELPARAMS="'{\"model\": \"mistralai/Mistral-Small-3.1-24B-Instruct-2503\", \"tokenizer_mode\": \"mistral\", \"config_format\": \"mistral\", \"load_format\": \"mistral\", \"guided_decoding_backend\": \"xgrammar\", \"seed\": 119, \"tensor_parallel_size\": 1}'"
export SAMPLINGPARAMS="'{\"temperature\": 0.15, \"seed\": 19, \"max_tokens\": 256}'"
export CHOICES="''"
export OUTFOLDER=outputs/v1/1xH100_Mistral-Small-3.1-24B-Instruct-2503/free
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:1 \
    --export=ALL \
    binaryChoicesPromptsEnglish_v1.slurm


export MODELPARAMS="'{\"model\": \"mistralai/Mistral-Small-3.1-24B-Instruct-2503\", \"tokenizer_mode\": \"mistral\", \"config_format\": \"mistral\", \"load_format\": \"mistral\", \"guided_decoding_backend\": \"xgrammar\", \"seed\": 119, \"tensor_parallel_size\": 1}'"
export SAMPLINGPARAMS="'{\"temperature\": 0.15, \"seed\": 19, \"max_tokens\": 256}'"
export CHOICES="''"
export OUTFOLDER=outputs/v1/1xH100_Mistral-Small-3.1-24B-Instruct-2503/free
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:1 \
    --export=ALL \
    multipleChoicesPromptsEnglish_v1.slurm


-------------------------------------------------------------------------------

export MODELPARAMS="'{\"model\": \"meta-llama/Llama-3.3-70B-Instruct\", \"guided_decoding_backend\": \"xgrammar\", \"max_model_len\": 7000, \"seed\": 119, \"tensor_parallel_size\": 2}'"
export SAMPLINGPARAMS="'{\"seed\": 19, \"max_tokens\": 256}'"
export CHOICES="'YES,NO'"
export OUTFOLDER=outputs/v1/2xH100_max_model_len_7000_Llama-3.3-70B-Instruct/guided
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:2 \
    --export=ALL \
    binaryChoicesPromptsEnglish_v1.slurm

export MODELPARAMS="'{\"model\": \"meta-llama/Llama-3.3-70B-Instruct\", \"guided_decoding_backend\": \"xgrammar\", \"max_model_len\": 7000, \"seed\": 119, \"tensor_parallel_size\": 2}'"
export SAMPLINGPARAMS="'{\"seed\": 19, \"max_tokens\": 256}'"
export CHOICES="'Macron,Mélenchon,Le Pen,None'"
export OUTFOLDER=outputs/v1/2xH100_max_model_len_7000_Llama-3.3-70B-Instruct/guided
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:2 \
    --export=ALL \
    multipleChoicesPromptsEnglish_v1.slurm


export MODELPARAMS="'{\"model\": \"meta-llama/Llama-3.3-70B-Instruct\", \"guided_decoding_backend\": \"xgrammar\", \"max_model_len\": 7000, \"seed\": 119, \"tensor_parallel_size\": 2}'"
export SAMPLINGPARAMS="'{\"seed\": 19, \"max_tokens\": 256}'"
export CHOICES="''"
export OUTFOLDER=outputs/v1/2xH100_max_model_len_7000_Llama-3.3-70B-Instruct/free
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:2 \
    --export=ALL \
    binaryChoicesPromptsEnglish_v1.slurm


export MODELPARAMS="'{\"model\": \"meta-llama/Llama-3.3-70B-Instruct\", \"guided_decoding_backend\": \"xgrammar\", \"max_model_len\": 7000, \"seed\": 119, \"tensor_parallel_size\": 2}'"
export SAMPLINGPARAMS="'{\"seed\": 19, \"max_tokens\": 256}'"
export CHOICES="''"
export OUTFOLDER=outputs/v1/2xH100_max_model_len_7000_Llama-3.3-70B-Instruct/free
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:2 \
    --export=ALL \
    multipleChoicesPromptsEnglish_v1.slurm


-------------------------------------------------------------------------------
export MODELPARAMS="'{\"model\": \"mistralai/Mistral-Large-Instruct-2411\", \"tokenizer_mode\": \"mistral\", \"config_format\": \"mistral\", \"load_format\": \"mistral\", \"guided_decoding_backend\": \"xgrammar\", \"seed\": 119, \"tensor_parallel_size\": 4}'"
export SAMPLINGPARAMS="'{\"temperature\": 0.15, \"seed\": 19, \"max_tokens\": 256}'"
export CHOICES="'YES,NO'"
export OUTFOLDER=outputs/v1/4xH100_Mistral-Large-Instruct-2411/guided
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:4 \
    --export=ALL \
    binaryChoicesPromptsEnglish_v1.slurm

export MODELPARAMS="'{\"model\": \"mistralai/Mistral-Large-Instruct-2411\", \"tokenizer_mode\": \"mistral\", \"config_format\": \"mistral\", \"load_format\": \"mistral\", \"guided_decoding_backend\": \"xgrammar\", \"seed\": 119, \"tensor_parallel_size\": 4}'"
export SAMPLINGPARAMS="'{\"temperature\": 0.15, \"seed\": 19, \"max_tokens\": 256}'"
export CHOICES="'Macron,Mélenchon,Le Pen,None'"
export OUTFOLDER=outputs/v1/4xH100_Mistral-Large-Instruct-2411/guided
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:4 \
    --export=ALL \
    multipleChoicesPromptsEnglish_v1.slurm


export MODELPARAMS="'{\"model\": \"mistralai/Mistral-Large-Instruct-2411\", \"tokenizer_mode\": \"mistral\", \"config_format\": \"mistral\", \"load_format\": \"mistral\", \"guided_decoding_backend\": \"xgrammar\", \"seed\": 119, \"tensor_parallel_size\": 4}'"
export SAMPLINGPARAMS="'{\"temperature\": 0.15, \"seed\": 19, \"max_tokens\": 256}'"
export CHOICES="''"
export OUTFOLDER=outputs/v1/4xH100_Mistral-Large-Instruct-2411/free
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:4 \
    --export=ALL \
    binaryChoicesPromptsEnglish_v1.slurm


export MODELPARAMS="'{\"model\": \"mistralai/Mistral-Large-Instruct-2411\", \"tokenizer_mode\": \"mistral\", \"config_format\": \"mistral\", \"load_format\": \"mistral\", \"guided_decoding_backend\": \"xgrammar\", \"seed\": 119, \"tensor_parallel_size\": 4}'"
export SAMPLINGPARAMS="'{\"temperature\": 0.15, \"seed\": 19, \"max_tokens\": 256}'"
export CHOICES="''"
export OUTFOLDER=outputs/v1/4xH100_Mistral-Large-Instruct-2411/free
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:4 \
    --export=ALL \
    multipleChoicesPromptsEnglish_v1.slurm



-------------------------------------------------------------------------------

