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
       --tweets_file=${BASEPATH}/400_balanced_sampled_xan_seed_999_fr_en.csv \
       --tweets_column=english \
       --system_prompt='You are an expert on French politics.' \
       --user_prompt='Please classify the following social media message (published in the weeks leading up to the 2022 French presidential election) according to whether it explicitly expresses the intention of the author to vote or calls for voting for Macron, Mélenchon, or Le Pen in that election, or expresses neither of these votes. Your response should be based solely on the information contained in the message. Do not assume that a message containing only positive opinions about a particular candidate explicitly expresses the intention to vote for that candidate. Do not assume that a message corresponding to the opinions or political positions of a particular candidate necessarily expresses the intention to vote for that candidate. Do not confuse retweets, indirect speech or a quote to another person with the opinion of the author of the message. Be concise and respond only with the last name or the word "None." Here is the message: \${tweet}' \
       --guided_choice=${CHOICES} \
       --outfolder=${OUTFOLDER}/voteintention/multiple/all"
echo "[RUNNING] ${cmd}"
eval "$cmd"


