#!/bin/sh

# SLURM options:

#SBATCH --job-name=4xH100_DeepSeek-R1-Distill-Llama-70B # Nom du job
#SBATCH --output=/sps/humanum/user/jroyolet/dev/llmBenchmarks/tweetsOffilineMultiGPU/4xH100_DeepSeek-R1-Distill-Llama-70B/%j.log   # Standard output et error log

#SBATCH --partition=gpu               # Choix de partition
#SBATCH --gres=gpu:h100:4

#SBATCH --ntasks=1                    # Exécuter une seule tâche
#SBATCH --mem=16G                    # Mémoire en MB par défaut
#SBATCH --time=6-23:59             # Déli max

#SBATCH --mail-user=jimena.royoletelier@sciencespo.fr # Où envoyer l'e-mail
#SBATCH --mail-type=ALL          # Événements déclencheurs (NONE, BEGIN, END, FAIL, ALL)


module load Programming_Languages/python/3.11.4
source /sps/humanum/user/jroyolet/environments/vllm-0.10.1/bin/activate

echo $(which gcc)
echo $(gcc --version)

echo $(python --version)
echo $(which python)
echo $(pip --version)

nvidia-smi

# Deepseek recommends to avoid adding a system prompt; all instructions should be contained within the user prompt.

export BASEPATH=/sps/humanum/user/jroyolet/dev/llmBenchmarks/tweetsOffilineMultiGPU
export IDX=4xH100_DeepSeek-R1-Distill-Llama-70B

cmd="python ${BASEPATH}/tweets.py \
        --model_params='{\"model\": \"deepseek-ai/DeepSeek-R1-Distill-Llama-70B\", \"guided_decoding_backend\": \"xgrammar\", \"seed\": 119, \"tensor_parallel_size\": 4}' \
        --sampling_params='{\"temperature\": 0.6, \"top_p\": 0.95}' \
        --tweets_file=${BASEPATH}/200_sampled_xan_seed_123_fr_en.csv \
        --tweets_column=english \
        --system_prompt='' \
        --user_prompt='You are an expert in French politics. Please classify the following social media message (that were posted in the weeks leading up to the 2022 presidential election in France) according to whether it express support or positive attitudes towards Le Pen in this election. You must use only the information contained in the message. Be concise and answer only YES or NO. Here is the message: ${tweet}' \
        --guided_choice=YES,NO \
        --logfile=${BASEPATH}/${IDX}/out.log \
        --outfolder=${BASEPATH}/${IDX}"

echo "[RUNNING] ${cmd}"
eval "$cmd"
