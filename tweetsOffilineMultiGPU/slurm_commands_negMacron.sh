export MODELPARAMS="'{\"model\": \"HuggingFaceH4/zephyr-7b-beta\", \"guided_decoding_backend\": \"xgrammar\", \"seed\": 19, \"gpu_memory_utilization\": 0.9}'"
export SAMPLINGPARAMS="'{\"temperature\": 0.7, \"top_p\": 0.95, \"top_k\": 50, \"max_tokens\": 16, \"repetition_penalty\": 1.2, \"seed\": 19}'"
export CHOICES=""
export OUTFOLDER=1xH100_zephyr-7b-beta_NOGUIDED
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:1 \
    --export=ALL \
    negMacron.slurm


export MODELPARAMS="'{\"model\": \"HuggingFaceH4/zephyr-7b-beta\", \"guided_decoding_backend\": \"xgrammar\", \"seed\": 19, \"gpu_memory_utilization\": 0.9}'"
export SAMPLINGPARAMS="'{\"temperature\": 0.7, \"top_p\": 0.95, \"top_k\": 50, \"max_tokens\": 16, \"repetition_penalty\": 1.2, \"seed\": 19}'"
export CHOICES="'YES,NO'"
export OUTFOLDER=1xH100_zephyr-7b-beta
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:1 \
    --export=ALL \
    negMacron.slurm



export MODELPARAMS="'{\"model\": \"openai/gpt-oss-20b\", \"guided_decoding_backend\": \"xgrammar\", \"seed\": 19}'"
export SAMPLINGPARAMS="'{\"seed\": 19, \"max_tokens\": 256}'"
export CHOICES="'YES,NO'"
export OUTFOLDER=1xH100_gpt-oss-20b
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:1 \
    --export=ALL \
    negMacron.slurm


export MODELPARAMS="'{\"model\": \"openai/gpt-oss-120b\", \"guided_decoding_backend\": \"xgrammar\", \"seed\": 19}'"
export SAMPLINGPARAMS="'{\"seed\": 19, \"max_tokens\": 256}'"
export CHOICES="'YES,NO'"
export OUTFOLDER=1xH100_gpt-oss-120b
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:1 \
    --export=ALL \
    negMacron.slurm
