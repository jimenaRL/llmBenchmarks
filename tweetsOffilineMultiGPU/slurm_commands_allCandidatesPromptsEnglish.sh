export MODELPARAMS="'{\"model\": \"HuggingFaceH4/zephyr-7b-beta\", \"guided_decoding_backend\": \"xgrammar\", \"seed\": 19, \"gpu_memory_utilization\": 0.9}'"
export SAMPLINGPARAMS="'{\"temperature\": 0.7, \"top_p\": 0.95, \"top_k\": 50, \"max_tokens\": 16, \"repetition_penalty\": 1.2, \"seed\": 19}'"
export CHOICES=""
export OUTFOLDER=1xH100_zephyr-7b-beta/free
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:1 \
    --export=ALL \
    allCandidatesPromptsEnglish.slurm


export MODELPARAMS="'{\"model\": \"HuggingFaceH4/zephyr-7b-beta\", \"guided_decoding_backend\": \"xgrammar\", \"seed\": 19, \"gpu_memory_utilization\": 0.9}'"
export SAMPLINGPARAMS="'{\"temperature\": 0.7, \"top_p\": 0.95, \"top_k\": 50, \"max_tokens\": 16, \"repetition_penalty\": 1.2, \"seed\": 19}'"
export CHOICES="'YES,NO'"
export OUTFOLDER=1xH100_zephyr-7b-beta/guided
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:1 \
    --export=ALL \
    allCandidatesPromptsEnglish.slurm


export MODELPARAMS="'{\"model\": \"openai/gpt-oss-20b\", \"guided_decoding_backend\": \"xgrammar\", \"seed\": 19}'"
export SAMPLINGPARAMS="'{\"seed\": 19, \"max_tokens\": 256}'"
export CHOICES="'YES,NO'"
export OUTFOLDER=1xH100_gpt-oss-20b/guided
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:1 \
    --export=ALL \
    allCandidatesPromptsEnglish.slurm


export MODELPARAMS="'{\"model\": \"openai/gpt-oss-120b\", \"guided_decoding_backend\": \"xgrammar\", \"seed\": 19}'"
export SAMPLINGPARAMS="'{\"seed\": 19, \"max_tokens\": 256}'"
export CHOICES="'YES,NO'"
export OUTFOLDER=1xH100_gpt-oss-120b/guided
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:1 \
    --export=ALL \
    allCandidatesPromptsEnglish.slurm


export MODELPARAMS="'{\"model\": \"deepseek-ai/DeepSeek-R1-Distill-Llama-70B\", \"guided_decoding_backend\": \"xgrammar\", \"seed\": 119, \"tensor_parallel_size\": 2, \"max_model_len\": 9000}'"
export SAMPLINGPARAMS="'{\"temperature\": 0.6, \"top_p\": 0.95, \"seed\": 19, \"max_tokens\": 256}'"
export CHOICES="'YES,NO'"
export OUTFOLDER=2xH100_max_model_len_9000_DeepSeek-R1-Distill-Llama-70B/guided
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:2 \
    --export=ALL \
    allCandidatesPromptsEnglish.slurm


export MODELPARAMS="'{\"model\": \"deepseek-ai/DeepSeek-R1-Distill-Llama-70B\", \"guided_decoding_backend\": \"xgrammar\", \"seed\": 119, \"tensor_parallel_size\": 2, \"max_model_len\": 9000}'"
export SAMPLINGPARAMS="'{\"temperature\": 0.6, \"top_p\": 0.95, \"seed\": 19, \"max_tokens\": 256}'"
export CHOICES=""
export OUTFOLDER=2xH100_max_model_len_9000_DeepSeek-R1-Distill-Llama-70B/free
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:2 \
    --export=ALL \
    allCandidatesPromptsEnglish.slurm


