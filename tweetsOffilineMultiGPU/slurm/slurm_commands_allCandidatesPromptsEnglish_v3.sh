export MODELPARAMS="'{\"model\": \"meta-llama/Llama-3.3-70B-Instruct\", \"guided_decoding_backend\": \"xgrammar\", \"max_model_len\": 7000, \"seed\": 119, \"tensor_parallel_size\": 2}'"
export SAMPLINGPARAMS="'{\"seed\": 19, \"max_tokens\": 256}'"
export CHOICES="'Macron,Mélenchon,Le Pen,Aucun'"
export OUTFOLDER=/sps/humanum/user/jroyolet/dev/llmBenchmarks/tweetsOffilineMultiGPU/outputs/v3/2xH100_max_model_len_7000_Llama-3.3-70B-Instruct/guided
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:2 \
    --export=ALL \
    /sps/humanum/user/jroyolet/dev/llmBenchmarks/tweetsOffilineMultiGPU/slurm/in2p3/multipleChoicesPromptsEnglish_v3.slurm


export MODELPARAMS="'{\"model\": \"mistralai/Mistral-Large-Instruct-2411\", \"tokenizer_mode\": \"mistral\", \"config_format\": \"mistral\", \"load_format\": \"mistral\", \"guided_decoding_backend\": \"xgrammar\", \"seed\": 119, \"tensor_parallel_size\": 4}'"
export SAMPLINGPARAMS="'{\"temperature\": 0.15, \"seed\": 19, \"max_tokens\": 256}'"
export CHOICES="'Macron,Mélenchon,Le Pen,Aucun'"
export OUTFOLDER=/sps/humanum/user/jroyolet/dev/llmBenchmarks/tweetsOffilineMultiGPU/outputs/v3/4xH100_Mistral-Large-Instruct-2411/guided
sbatch \
    --job-name=${OUTFOLDER} \
    --output=$(pwd)/${OUTFOLDER}/%j.log  \
    --gres=gpu:h100:4 \
    --export=ALL \
    /sps/humanum/user/jroyolet/dev/llmBenchmarks/tweetsOffilineMultiGPU/slurm/in2p3/multipleChoicesPromptsEnglish_v3.slurm
