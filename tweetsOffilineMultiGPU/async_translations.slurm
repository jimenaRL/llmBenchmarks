#!/bin/sh

# SLURM options:

#SBATCH --job-name=asynctranstions # Nom du job
#SBATCH --output=/sps/humanum/user/jroyolet/dev/llmBenchmarks/tweetsOffilineMultiGPU/translations/mistralai_Mistral-7B-Instruct-v0.2/%j.log # log file path

#SBATCH --partition=gpu               # Choix de partition
#SBATCH --gres=gpu:h100:2

#SBATCH --ntasks=1                    # Exécuter une seule tâche
#SBATCH --mem=128G                    # Mémoire en MB par défaut
#SBATCH --time=6-23:59             #  Max temps execution en format « jours-heures:minutes »

#SBATCH --mail-user=jimena.royoletelier@sciencespo.fr # Où envoyer l'e-mail
#SBATCH --mail-type=ALL          # Événements déclencheurs (NONE, BEGIN, END, FAIL, ALL)

module load Programming_Languages/python/3.11.4
source /sps/humanum/user/jroyolet/environments/vllm-0.10.1/bin/activate

echo ""
echo $(which gcc)
echo $(gcc --version)

echo ""
echo $(python --version)
echo $(which python)
echo $(pip --version)

echo ""
nvidia-smi

LIMIT=$1

# Get args
cmd=f"python async_translations.py --limit={LIMIT}"

echo "[RUNNING] ${cmd}"
eval "$cmd"
