#!/bin/sh

# SLURM options:

#SBATCH --job-name=offlineGuidedOutputsChoice # Nom du job
#SBATCH --output=/sps/humanum/user/jroyolet/logs/%j.log # log file path

#SBATCH --partition=gpu               # Choix de partition
#SBATCH --gres=gpu:v100:1

#SBATCH --ntasks=1                    # Exécuter une seule tâche
#SBATCH --mem=16G                    # Mémoire en MB par défaut
#SBATCH --time=6-23:59             #  Max temps execution en format « jours-heures:minutes »

#SBATCH --mail-user=jimena.royoletelier@sciencespo.fr # Où envoyer l'e-mail
#SBATCH --mail-type=ALL          # Événements déclencheurs (NONE, BEGIN, END, FAIL, ALL)

source /sps/humanum/user/jroyolet/environments/vllm0.8.4/bin/activate

# Get args
COMMAND=$1

echo "[PARTITION] v100 [RUNNING] ${COMMAND}"
eval "$COMMAND"


