#!/bin/bash

#SBATCH --job-name=vllmTest # Nom du jobe
#SBATCH --output=vllmTest_%j.log   # name of output file
#SBATCH --error=vllmTest_%j.error  # name of error file (here, common with the output file)

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

# Example script for running and query a vllm server on a slurm job.
# Before running the job you must launch un interactive terminal a install vllm on a python virtual enviroment
# as explained on the points 1-4 here:
# https://github.com/jimenaRL/llmBenchmarks/blob/main/in2p3/openai_chat_completion_client_for_multimodal.py

# Cleans out modules loaded in interactive and inherited by default
module purge

# load python enviroment
module load python/3.12.7
conda init
conda activate vllm


command1="source /lustre/fswork/projects/rech/nmf/umu89ib/llmBenchmarks/jean-zay/offline/run_batch.sh"
echo "[RUNNING] ${command1}"
eval "$command1"
