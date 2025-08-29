#!/bin/sh

# SLURM options:

#SBATCH --job-name=1xV100_zephyr-7b-beta # Nom du job
#SBATCH --output=/sps/humanum/user/jroyolet/dev/llmBenchmarks/tweetsOffilineMultiGPU/1xV100_zephyr-7b-beta/%j.log   # Standard output et error log

#SBATCH --partition=gpu               # Choix de partition
#SBATCH --gres=gpu:v100:1

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

# Set and run offline vllm script
python /sps/humanum/user/jroyolet/dev/llmBenchmarks/tweetsOffilineMultiGPU/tweets.py \
  --model_params='{"model": "HuggingFaceH4/zephyr-7b-beta", "guided_decoding_backend": "xgrammar", "seed": 19, "gpu_memory_utilization": 0.9}' \
  --sampling_params='{"temperature": 0.7, "top_p": 0.95, "top_k": 50, "max_tokens": 16, "repetition_penalty": 1.2, "seed": 19}' \
  --tweets_file=/sps/humanum/user/jroyolet/dev/llmBenchmarks/tweetsOffilineMultiGPU/200_sampled_xan_seed_123_fr_en.csv \
  --tweets_column=english \
  --system_prompt='' \
  --user_prompt='You are an expert in French politics. Please classify the following social media message (that were posted in the weeks leading up to the 2022 presidential election in France) according to whether it express support or positive attitudes towards Le Pen in this election. You must use only the information contained in the message. Be concise and answer only YES or NO. Here is the message: ${tweet}' \
  --guided_choice=YES,NO \
  --logfile=/sps/humanum/user/jroyolet/dev/llmBenchmarks/tweetsOffilineMultiGPU/1xV100_zephyr-7b-beta/out.log \
  --outfolder=/sps/humanum/user/jroyolet/dev/llmBenchmarks/tweetsOffilineMultiGPU/1xV100_zephyr-7b-beta
