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
       --user_prompt='You are an expert in French politics. Please classify the following social media message (that was posted in the weeks leading up to the 2022 presidential election in France) according to whether it express explicit criticism or negative attitudes towards Macron in this election. You should base your answer solely on the information contained in the message. Don't assume that a message containing criticism or negative attitudes towards the party to which Macron belongs, or which is against Macron's opinions or political positions, constitutes explicit criticism or negative attitude towards Macron. Be concise and answer only YES or NO. Here is the message: \${tweet}' \
       --guided_choice=${CHOICES} \
       --outfolder=${OUTFOLDER}/criticism/binary/macron"
echo "[RUNNING] ${cmd}"
eval "$cmd"


cmd="python ${BASEPATH}/tweets.py \
       --model_params=${MODELPARAMS} \
       --sampling_params=${SAMPLINGPARAMS} \
       --tweets_file=${BASEPATH}/200_sampled_xan_seed_123_fr_en.csv \
       --tweets_column=english \
       --system_prompt='' \
       --user_prompt='You are an expert in French politics. Please classify the following social media message (that was posted in the weeks leading up to the 2022 presidential election in France) according to whether it express explicit criticism or negative attitudes towards Le Pen in this election. You should base your answer solely on the information contained in the message. Don't assume that a message containing criticism or negative attitudes towards the party to which Le Pen belongs, or which is against Le Pen's opinions or political positions, constitutes explicit criticism or negative attitude towards Le Pen. Be concise and answer only YES or NO. Here is the message: \${tweet}' \
       --guided_choice=${CHOICES} \
       --outfolder=${OUTFOLDER}/criticism/binary/lepen"
echo "[RUNNING] ${cmd}"
eval "$cmd"


cmd="python ${BASEPATH}/tweets.py \
       --model_params=${MODELPARAMS} \
       --sampling_params=${SAMPLINGPARAMS} \
       --tweets_file=${BASEPATH}/200_sampled_xan_seed_123_fr_en.csv \
       --tweets_column=english \
       --system_prompt='' \
       --user_prompt='You are an expert in French politics. Please classify the following social media message (that was posted in the weeks leading up to the 2022 presidential election in France) according to whether it express explicit criticism or negative attitudes towards Mélenchon in this election. You should base your answer solely on the information contained in the message. Don't assume that a message containing criticism or negative attitudes towards the party to which Mélenchon belongs, or which is against Mélenchon's opinions or political positions, constitutes explicit criticism or negative attitude towards Mélenchon. Be concise and answer only YES or NO. Here is the message: \${tweet}' \
       --guided_choice=${CHOICES} \
       --outfolder=${OUTFOLDER}/criticism/binary/melenchon"
echo "[RUNNING] ${cmd}"
eval "$cmd"




cmd="python ${BASEPATH}/tweets.py \
       --model_params=${MODELPARAMS} \
       --sampling_params=${SAMPLINGPARAMS} \
       --tweets_file=${BASEPATH}/200_sampled_xan_seed_123_fr_en.csv \
       --tweets_column=english \
       --system_prompt='' \
       --user_prompt='You are an expert in French politics. Please classify the following social media message (that was posted in the weeks leading up to the 2022 presidential election in France) according to whether it express explicit support or positive attitudes towards Macron in this election. You should base your answer solely on the information contained in the message. Don't assume that a message containing support or positive attitudes towards the party to which Macron belongs, or which is aligned with Macron's opinions or political positions, constitutes explicit support or positive attitudes towards Macron. Be concise and answer only YES or NO. Here is the message: \${tweet}' \
       --guided_choice=${CHOICES} \
       --outfolder=${OUTFOLDER}/support/binary/macron"
echo "[RUNNING] ${cmd}"
eval "$cmd"


cmd="python ${BASEPATH}/tweets.py \
       --model_params=${MODELPARAMS} \
       --sampling_params=${SAMPLINGPARAMS} \
       --tweets_file=${BASEPATH}/200_sampled_xan_seed_123_fr_en.csv \
       --tweets_column=english \
       --system_prompt='' \
       --user_prompt='You are an expert in French politics. Please classify the following social media message (that was posted in the weeks leading up to the 2022 presidential election in France) according to whether it express explicit support or positive attitudes towards Le Pen in this election. You should base your answer solely on the information contained in the message. Don't assume that a message containing support or positive attitudes towards the party to which Le Pen belongs, or which is aligned with Le Pen's opinions or political positions, constitutes explicit support or positive attitudes towards Le Pen. Be concise and answer only YES or NO. Here is the message: \${tweet}' \
       --guided_choice=${CHOICES} \
       --guided_choice=${CHOICES} \
       --outfolder=${OUTFOLDER}/support/binary/lepen"
echo "[RUNNING] ${cmd}"
eval "$cmd"


cmd="python ${BASEPATH}/tweets.py \
       --model_params=${MODELPARAMS} \
       --sampling_params=${SAMPLINGPARAMS} \
       --tweets_file=${BASEPATH}/200_sampled_xan_seed_123_fr_en.csv \
       --tweets_column=english \
       --system_prompt='' \
       --user_prompt='You are an expert in French politics. Please classify the following social media message (that was posted in the weeks leading up to the 2022 presidential election in France) according to whether it express explicit support or positive attitudes towards Mélenchon in this election. You should base your answer solely on the information contained in the message. Don't assume that a message containing support or positive attitudes towards the party to which Mélenchon belongs, or which is aligned with Mélenchon's opinions or political positions, constitutes explicit support or positive attitudes towards Mélenchon. Be concise and answer only YES or NO. Here is the message: \${tweet}' \
       --guided_choice=${CHOICES} \
       --guided_choice=${CHOICES} \
       --outfolder=${OUTFOLDER}/support/binary/melenchon"
echo "[RUNNING] ${cmd}"
eval "$cmd"


cmd="python ${BASEPATH}/tweets.py \
       --model_params=${MODELPARAMS} \
       --sampling_params=${SAMPLINGPARAMS} \
       --tweets_file=${BASEPATH}/200_sampled_xan_seed_123_fr_en.csv \
       --tweets_column=english \
       --system_prompt='' \
       --user_prompt='You are an expert in French politics. Please classify the following social media message (that was posted in the weeks leading up to the 2022 presidential election in France) according to whether it explicitly express the intention to vote for Macron in this election. You should base your answer solely on the information contained in the message. Do not assume that a message containing only positive opinions about Macron explicitly expresses an intention to vote for Macron. Do not assume that a message that corresponds to Macron's political opinions or positions necessarily expresses the explicit intention to vote for Macron. Be concise and answer only YES or NO. Here is the message: \${tweet}' \
       --guided_choice=${CHOICES} \
       --outfolder=${OUTFOLDER}/voteintention/binary/macron"
echo "[RUNNING] ${cmd}"
eval "$cmd"


cmd="python ${BASEPATH}/tweets.py \
       --model_params=${MODELPARAMS} \
       --sampling_params=${SAMPLINGPARAMS} \
       --tweets_file=${BASEPATH}/200_sampled_xan_seed_123_fr_en.csv \
       --tweets_column=english \
       --system_prompt='' \
       --user_prompt='You are an expert in French politics. Please classify the following social media message (that was posted in the weeks leading up to the 2022 presidential election in France) according to whether it explicitly express the intention to vote for Le Pen in this election. You should base your answer solely on the information contained in the message. Do not assume that a message containing only positive opinions about Le Pen explicitly expresses an intention to vote for Le Pen. Do not assume that a message that corresponds to Le Pen's political opinions or positions necessarily expresses the explicit intention to vote for Le Pen. Be concise and answer only YES or NO. Here is the message: \${tweet}' \
       --guided_choice=${CHOICES} \
       --outfolder=${OUTFOLDER}/voteintention/binary/lepen"
echo "[RUNNING] ${cmd}"
eval "$cmd"


cmd="python ${BASEPATH}/tweets.py \
       --model_params=${MODELPARAMS} \
       --sampling_params=${SAMPLINGPARAMS} \
       --tweets_file=${BASEPATH}/200_sampled_xan_seed_123_fr_en.csv \
       --tweets_column=english \
       --system_prompt='' \
       --user_prompt='You are an expert in French politics. Please classify the following social media message (that was posted in the weeks leading up to the 2022 presidential election in France) according to whether it explicitly express the intention to vote for Mélenchon in this election. You should base your answer solely on the information contained in the message. Do not assume that a message containing only positive opinions about Mélenchon explicitly expresses an intention to vote for Mélenchon. Do not assume that a message that corresponds to Mélenchon's political opinions or positions necessarily expresses the explicit intention to vote for Mélenchon. Be concise and answer only YES or NO. Here is the message: \${tweet}' \
       --guided_choice=${CHOICES} \
       --outfolder=${OUTFOLDER}/voteintention/binary/melenchon"
echo "[RUNNING] ${cmd}"
eval "$cmd"
