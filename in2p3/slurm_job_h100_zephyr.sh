#!/bin/sh

# SLURM options:

#SBATCH --job-name=vllmZephyrH100 # Nom du job
#SBATCH --output=logs/%j.log   # Standard output et error log

#SBATCH --partition=gpu               # Choix de partition
#SBATCH --gres=gpu:h100:1

#SBATCH --ntasks=1                    # Exécuter une seule tâche
#SBATCH --mem=16G                    # Mémoire en MB par défaut
#SBATCH --time=6-23:59             # Déli max

#SBATCH --mail-user=jimena.royoletelier@sciencespo.fr # Où envoyer l'e-mail
#SBATCH --mail-type=ALL          # Événements déclencheurs (NONE, BEGIN, END, FAIL, ALL)

source /sps/humanum/user/jroyolet/environments/vllm0.8.4/bin/activate

# Get args
INPUT=$1
OUTPUT=$2

# Run command
cmd="python /sps/humanum/user/jroyolet/environments/vllm0.8.4/lib64/python3.9/site-packages/vllm/entrypoints/openai/run_batch.py \
    -i ${INPUT} \
    -o ${OUTPUT} \
    --model=HuggingFaceH4/zephyr-7b-beta \
    --gpu-memory-utilization=0.9 \
    --max_model_len=21500 \
    --dtype=half \
    --guided-decoding-backend=xgrammar \
    --disable-log-stats \"

echo "[RUNNING] ${cmd}"
eval "$cmd"
