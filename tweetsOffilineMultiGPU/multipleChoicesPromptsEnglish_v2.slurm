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
       --tweets_column=english \
       --system_prompt='' \
       --user_prompt='You are an expert in French politics. Please classify the following social media message (that was posted in the weeks leading up to the 2022 presidential election in France) according to whether it express criticism or negative attitudes towards Macron, Mélenchon or Le Pen, by replying only with last name of the candidate, or with the word None. You should base your answer solely on the information contained in the message. Don't assume that a message containing criticism or negative attitudes towards the party to which a candidate belongs, or which is againts  a candidate's opinions or political positions, constitutes explicit criticism or negative attitude towards that candidate. Be concise and answer only with last name of the candidate or with the word None. Here is the message: \${tweet}' \
       --guided_choice=${CHOICES} \
       --outfolder=${OUTFOLDER}/criticism/multiple/all"
echo "[RUNNING] ${cmd}"
eval "$cmd"

cmd="python ${BASEPATH}/tweets.py \
       --model_params=${MODELPARAMS} \
       --sampling_params=${SAMPLINGPARAMS} \
       --tweets_file=${BASEPATH}/200_sampled_xan_seed_123_fr_en.csv \
       --tweets_column=english \
       --system_prompt='' \
       --user_prompt='You are an expert in French politics. Please classify the following social media message (that was posted in the weeks leading up to the 2022 presidential election in France) according to whether it express support for Macron, Mélenchon or Le Pen, by replying only with last name of the candidate, or with the word None, if the message does not express an intention to vote or calls for a vote for one of these three candidates. You should base your answer solely on the information contained in the message. Don't assume that a message containing support or positive attitudes towards the party to which a candidate belongs, or which is aligned with a candidate's opinions or political positions, constitutes explicit support or positive attitudes towards that candidate. Be concise and respond only by indicating the candidate's last name or using the word None. Here is the message: \${tweet}' \
       --guided_choice=${CHOICES} \
       --outfolder=${OUTFOLDER}/support/multiple/all"
echo "[RUNNING] ${cmd}"
eval "$cmd"

cmd="python ${BASEPATH}/tweets.py \
       --model_params=${MODELPARAMS} \
       --sampling_params=${SAMPLINGPARAMS} \
       --tweets_file=${BASEPATH}/200_sampled_xan_seed_123_fr_en.csv \
       --tweets_column=english \
       --system_prompt='' \
       --user_prompt='You are an expert in French politics. Please classify the following social media message (that was posted in the weeks leading up to the 2022 presidential election in France) according to whether it explicitly expresses the intention to vote or calls for voting for Macron, Mélenchon or Le Pen in this election, or None of them. You should base your answer solely on the information contained in the message. Do not assume that a message containing only positive opinions about a particular candidate explicitly expresses the intention to vote for that candidate. Do not assume that a message that corresponds to the political opinions or positions of a particular candidate necessarily expresses the explicit intention to vote for that candidate. Be concise and respond only by indicating the candidate's last name or the word None. Here is the message: \${tweet}' \
       --guided_choice=${CHOICES} \
       --outfolder=${OUTFOLDER}/voteintention/multiple/all"
echo "[RUNNING] ${cmd}"
eval "$cmd"


