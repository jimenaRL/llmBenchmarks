#!/bin/sh

# SLURM options:

#SBATCH --job-name=vllm_server_llava_test # Nom du jobe
#SBATCH --output=logs/%j.log   # Standard output et error log

#SBATCH --partition=gpu               # Choix de partition
#SBATCH --gres=gpu:v100:1

#SBATCH --ntasks=1                    # Exécuter une seule tâche
#SBATCH --mem=16G                    # Mémoire en MB par défaut
#SBATCH --time=6-23:59             # Déli max

#SBATCH --mail-user=myemail@notgmail.fr  # Où envoyer l'e-mail
#SBATCH --mail-type=ALL          # Événements déclencheurs (NONE, BEGIN, END, FAIL, ALL)

# Example script for running and query a vllm server on a slurm job.
# Before running the job you must launch un interactive terminal a install vllm on a python virtual enviroment
# as explained on the points 1-4 here:
# https://github.com/jimenaRL/llmBenchmarks/blob/main/in2p3/openai_chat_completion_client_for_multimodal.py

source /sps/humanum/user/jroyolet/dev/environments/vllmEnv/bin/activate

MODEL="llava-hf/llava-1.5-7b-hf"
CHAT_TEMPLATE="/sps/humanum/user/jroyolet/dev/llmBenchmarks/in2p3/template_llava.jinja"
SCRIPT="/sps/humanum/user/jroyolet/dev/llmBenchmarks/in2p3/openai_chat_completion_client_for_multimodal.py -v"

command1="vllm serve ${MODEL} --chat-template ${CHAT_TEMPLATE} --disable-log-stats &"
echo "[RUNNING] ${command1}"
eval "$command1"

command2="sleep 600"
echo "[RUNNING] ${command2}"
eval "$command2"

command3="python ${SCRIPT}"
echo "[RUNNING] ${command3}"
eval "$command3"
