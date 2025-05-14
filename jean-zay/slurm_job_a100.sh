#!/bin/bash

#SBATCH --job-name=vllmTest # Nom du jobe
#SBATCH --output=vllmTest_a100_%j.log   # name of output file
#SBATCH --error=vllmTest_a100_%j.error  # name of error file (here, common with the output file)

#SBATCH -C a100                # Choix de partition (here gpu_p5 partition 80GB A100 GPU)
#SBATCH --gres=gpu:1                 # number of GPUs per node (max 8 with gpu_p2, gpu_p5)
#SBATCH --nodes=1                    # number of nodes
#SBATCH --ntasks-per-node=3          # number of MPI tasks per node (= number of GPUs per node)
#SBATCH --cpus-per-task=8           # number of cores per task for gpu_p5 (1/8 of 8-GPUs A100 node)
#SBATCH --hint=nomultithread         # hyperthreading deactivated

#SBATCH --time=20:00:00             # Déli max

#SBATCH --account=nmf@a100              # Set acccount

#SBATCH --mail-user=jimena.royoletelier@sciencespo.fr # Où envoyer l'e-mail
#SBATCH --mail-type=ALL          # Événements déclencheurs (NONE, BEGIN, END, FAIL, ALL)

# Cleans out modules loaded in interactive and inherited by default
module purge

# Load python enviroment
module load python/3.12.7
conda activate vllm

# Get args
INPUT=$1
OUTPUT=$2
MODEL=$3

# Set env variables
export HF_HUB_OFFLINE=1
export HUGGINGFACE_HUB_CACHE=/lustre/fswork/projects/rech/nmf/umu89ib/.cache/huggingface

# Run command
cmd="python /linkhome/rech/gensoj01/umu89ib/.conda/envs/vllm/lib/python3.12/site-packages/vllm/entrypoints/openai/run_batch.py -i ${INPUT} -o ${OUTPUT} --model=${MODEL} --gpu-memory-utilization=0.9 --max_model_len=21500 --dtype=half"
echo "[RUNNING] ${cmd}"
eval "$cmd"
