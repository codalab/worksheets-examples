CMD='cl run'

# Docker image
# CMD="$CMD --request-docker-image "

# Dependencies
CMD="$CMD :src :dataset"

# Main command
CMD="$CMD 'python src/train_nli.py \
           --word_emb_path datasets/GloVe/glove.840B.300d.txt \
           --train_frac 0.1'"

# Run configuration
CMD="$CMD --request-gpus 1"

echo $CMD
exec $CMD