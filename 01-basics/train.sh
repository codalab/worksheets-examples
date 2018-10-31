CMD='cl run'

# If you want to change the docker image....
# CMD="$CMD --request-docker-image "

# Add dependencies
CMD="$CMD :src :dataset"

# The command you actually run
CMD="$CMD 'python infersent/train_nli.py \
           --word_emb_path datasets/GloVe/glove.840B.300d.txt \
           --train_frac 0.1'"

echo $CMD
exec $CMD