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
       --user_prompt='You are an expert in French politics. Please classify the following social media message (that was posted in the weeks leading up to the 2022 presidential election in France) according to whether it express the intention to vote for the intention to vote for or calls for a vote for Macron, Mélenchon or Le Pen. You must use only the information contained in the message. Be concise and answer only only with the last name of the candidate, or with None, if the message does not show support for any of these three candidates. Here is the message: \${tweet}' \
       --guided_choice='Macron,Mélenchon,Le Pen,None' \
       --outfolder=${OUTFOLDER}/voteintention/all"
echo "[RUNNING] ${cmd}"
eval "$cmd"


cmd="python ${BASEPATH}/tweets.py \
       --model_params=${MODELPARAMS} \
       --sampling_params=${SAMPLINGPARAMS} \
       --tweets_file=${BASEPATH}/200_sampled_xan_seed_123_fr_en.csv \
       --tweets_column=english \
       --system_prompt='' \
       --user_prompt='You are an expert in French politics. Please classify the following social media message (that was posted in the weeks leading up to the 2022 presidential election in France) according to whether it express support for Macron, Mélenchon or Le Pen, by replying only with last name of the candidate, or with the word Other, if the message does not express an intention to vote or calls for a vote for one of these three candidates. You must use only the information contained in the message. Be concise. Here is the message: \${tweet}' \
       --guided_choice='Macron,Mélenchon,Le Pen,Other' \
       --outfolder=${OUTFOLDER}/support/all"
echo "[RUNNING] ${cmd}"
eval "$cmd"

cmd="python ${BASEPATH}/tweets.py \
       --model_params=${MODELPARAMS} \
       --sampling_params=${SAMPLINGPARAMS} \
       --tweets_file=${BASEPATH}/200_sampled_xan_seed_123_fr_en.csv \
       --tweets_column=english \
       --system_prompt='' \
       --user_prompt='You are an expert in French politics. Please classify the following social media message (that was posted in the weeks leading up to the 2022 presidential election in France) according to whether it express criticism or negative attitudes towards Macron in this election. You must use only the information contained in the message. Be concise and answer only YES or NO. Here is the message: \${tweet}' \
       --guided_choice=${CHOICES} \
       --outfolder=${OUTFOLDER}/criticism/macron"
echo "[RUNNING] ${cmd}"
eval "$cmd"


cmd="python ${BASEPATH}/tweets.py \
       --model_params=${MODELPARAMS} \
       --sampling_params=${SAMPLINGPARAMS} \
       --tweets_file=${BASEPATH}/200_sampled_xan_seed_123_fr_en.csv \
       --tweets_column=english \
       --system_prompt='' \
       --user_prompt='You are an expert in French politics. Please classify the following social media message (that was posted in the weeks leading up to the 2022 presidential election in France) according to whether it express criticism or negative attitudes towards Le Pen in this election. You must use only the information contained in the message. Be concise and answer only YES or NO. Here is the message: \${tweet}' \
       --guided_choice=${CHOICES} \
       --outfolder=${OUTFOLDER}/criticism/lepen"
echo "[RUNNING] ${cmd}"
eval "$cmd"


cmd="python ${BASEPATH}/tweets.py \
       --model_params=${MODELPARAMS} \
       --sampling_params=${SAMPLINGPARAMS} \
       --tweets_file=${BASEPATH}/200_sampled_xan_seed_123_fr_en.csv \
       --tweets_column=english \
       --system_prompt='' \
       --user_prompt='You are an expert in French politics. Please classify the following social media message (that was posted in the weeks leading up to the 2022 presidential election in France) according to whether it express criticism or negative attitudes towards Mélenchon in this election. You must use only the information contained in the message. Be concise and answer only YES or NO. Here is the message: \${tweet}' \
       --guided_choice=${CHOICES} \
       --outfolder=${OUTFOLDER}/criticism/melenchon"
echo "[RUNNING] ${cmd}"
eval "$cmd"




cmd="python ${BASEPATH}/tweets.py \
       --model_params=${MODELPARAMS} \
       --sampling_params=${SAMPLINGPARAMS} \
       --tweets_file=${BASEPATH}/200_sampled_xan_seed_123_fr_en.csv \
       --tweets_column=english \
       --system_prompt='' \
       --user_prompt='You are an expert in French politics. Please classify the following social media message (that was posted in the weeks leading up to the 2022 presidential election in France) according to whether it express support or positive attitudes towards Macron in this election. You must use only the information contained in the message. Be concise and answer only YES or NO. Here is the message: \${tweet}' \
       --guided_choice=${CHOICES} \
       --outfolder=${OUTFOLDER}/support/macron"
echo "[RUNNING] ${cmd}"
eval "$cmd"


cmd="python ${BASEPATH}/tweets.py \
       --model_params=${MODELPARAMS} \
       --sampling_params=${SAMPLINGPARAMS} \
       --tweets_file=${BASEPATH}/200_sampled_xan_seed_123_fr_en.csv \
       --tweets_column=english \
       --system_prompt='' \
       --user_prompt='You are an expert in French politics. Please classify the following social media message (that was posted in the weeks leading up to the 2022 presidential election in France) according to whether it express support or positive attitudes towards Le Pen in this election. You must use only the information contained in the message. Be concise and answer only YES or NO. Here is the message: \${tweet}' \
       --guided_choice=${CHOICES} \
       --outfolder=${OUTFOLDER}/support/lepen"
echo "[RUNNING] ${cmd}"
eval "$cmd"


cmd="python ${BASEPATH}/tweets.py \
       --model_params=${MODELPARAMS} \
       --sampling_params=${SAMPLINGPARAMS} \
       --tweets_file=${BASEPATH}/200_sampled_xan_seed_123_fr_en.csv \
       --tweets_column=english \
       --system_prompt='' \
       --user_prompt='You are an expert in French politics. Please classify the following social media message (that was posted in the weeks leading up to the 2022 presidential election in France) according to whether it express support or positive attitudes towards Mélenchon in this election. You must use only the information contained in the message. Be concise and answer only YES or NO. Here is the message: \${tweet}' \
       --guided_choice=${CHOICES} \
       --outfolder=${OUTFOLDER}/support/melenchon"
echo "[RUNNING] ${cmd}"
eval "$cmd"


cmd="python ${BASEPATH}/tweets.py \
       --model_params=${MODELPARAMS} \
       --sampling_params=${SAMPLINGPARAMS} \
       --tweets_file=${BASEPATH}/200_sampled_xan_seed_123_fr_en.csv \
       --tweets_column=english \
       --system_prompt='' \
       --user_prompt='You are an expert in French politics. Please classify the following social media message (that was posted in the weeks leading up to the 2022 presidential election in France) according to whether it express the intention to vote for Macron in this election. You must use only the information contained in the message. Be concise and answer only YES or NO. Here is the message: \${tweet}' \
       --guided_choice=${CHOICES} \
       --outfolder=${OUTFOLDER}/voteintention/macron"
echo "[RUNNING] ${cmd}"
eval "$cmd"


cmd="python ${BASEPATH}/tweets.py \
       --model_params=${MODELPARAMS} \
       --sampling_params=${SAMPLINGPARAMS} \
       --tweets_file=${BASEPATH}/200_sampled_xan_seed_123_fr_en.csv \
       --tweets_column=english \
       --system_prompt='' \
       --user_prompt='You are an expert in French politics. Please classify the following social media message (that was posted in the weeks leading up to the 2022 presidential election in France) according to whether it express the intention to vote for Le Pen in this election. You must use only the information contained in the message. Be concise and answer only YES or NO. Here is the message: \${tweet}' \
       --guided_choice=${CHOICES} \
       --outfolder=${OUTFOLDER}/voteintention/lepen"
echo "[RUNNING] ${cmd}"
eval "$cmd"


cmd="python ${BASEPATH}/tweets.py \
       --model_params=${MODELPARAMS} \
       --sampling_params=${SAMPLINGPARAMS} \
       --tweets_file=${BASEPATH}/200_sampled_xan_seed_123_fr_en.csv \
       --tweets_column=english \
       --system_prompt='' \
       --user_prompt='You are an expert in French politics. Please classify the following social media message (that was posted in the weeks leading up to the 2022 presidential election in France) according to whether it express the intention to vote for Mélenchon in this election. You must use only the information contained in the message. Be concise and answer only YES or NO. Here is the message: \${tweet}' \
       --guided_choice=${CHOICES} \
       --outfolder=${OUTFOLDER}/voteintention/melenchon"
echo "[RUNNING] ${cmd}"
eval "$cmd"
