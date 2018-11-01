# TODO: add brief description

### CodaLab arguments
CODALAB_ARGS="cl run"

# Docker image (default: codalab/default-cpu)
CODALAB_ARGS="$CODALAB_ARGS --request-docker-image codalab/default-gpu"
CODALAB_ARGS="$CODALAB_ARGS --request-gpus 1"

# Bundle dependencies
CODALAB_ARGS="$CODALAB_ARGS :src"                              # Code
CODALAB_ARGS="$CODALAB_ARGS :SNLI"                             # Dataset
CODALAB_ARGS="$CODALAB_ARGS word-vectors.txt:glove.840B.300d"  # Word vectors

### Command to execute
CMD="python src/train_nli.py"
CMD="$CMD --nlipath SNLI"
CMD="$CMD --train_frac 0.1"
#CMD="$CMD --word_emb_path word-vectors.txt"

# Run it!
FINAL_COMMAND="$CODALAB_ARGS '$CMD'"
echo $FINAL_COMMAND
exec bash -c "$FINAL_COMMAND"
