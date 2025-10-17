#!/bin/sh

#SBATCH --partition=gpu               # Choix de partition

#SBATCH --ntasks=1                    # Exécuter une seule tâche
#SBATCH --mem=32G                    # Mémoire en MB par défaut
#SBATCH --time=6-23:59             # Déli max

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

export BASEPATH=/sps/humanum/user/jroyolet/dev/llmBenchmarks/tweetsOffilineMultiGPU

echo ""
echo "BASEPATH:"
echo "${BASEPATH}"

echo ""
echo "MODELPARAMS:"
echo "${MODELPARAMS}"

echo ""
echo "SAMPLINGPARAMS:"
echo "${SAMPLINGPARAMS}"

echo ""
echo "CHOICES:"
echo "${CHOICES}"

echo ""
echo "OUTFOLDER:"
echo "${OUTFOLDER}"

echo ""

cmd="python ${BASEPATH}/tweets.py \
       --model_params=${MODELPARAMS} \
       --sampling_params=${SAMPLINGPARAMS} \
       --tweets_file=${BASEPATH}/200_sampled_xan_seed_123_fr_en.csv \
       --tweets_column=cleaned_text2annotate \
       --system_prompt='Tu es un expert en politique française.' \
       --user_prompt='S'il te plaît classifie ce message sur les réseaux sociaux (publié dans les semaines précédant l'élection présidentielle française de 2022) selon qu'il exprime explicitement l'intention de vote de son auteur ou appelle à voter pour Macron, Mélenchon ou Le Pen lors de cette élection, ou qu'il n'exprime aucun de ces votes. Ta réponse doit se baser uniquement sur les informations contenues dans le message. N'assume pas qu'un message contenant uniquement des opinions positives sur un candidat exprime explicitement l'intention de voter pour ce candidat. N'assume pas qu'un message correspondant aux opinions ou aux positions politiques d'un candidat exprime nécessairement l'intention de voter pour ce candidat. Ne confonds pas un retweets, le discours indirect ou une citation avec l'opinion de l'auteur du message. Soit concis et répond uniquement en indiquant le nom de famille du candidat ou la mention « Aucun ». Voici le message: \${tweet}' \
       --guided_choice=${CHOICES} \
       --outfolder=${OUTFOLDER}/voteintention/multiple/all"
echo "[RUNNING] ${cmd}"
eval "$cmd"


