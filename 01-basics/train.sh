# This is an example script to start a CodaLab run. There are often several
# things to configure, including the docker image, compute resources, bundle
# dependencies (code and data), and custom arguments to pass to the command.
# Factoring all this into a script makes it easier to run and track different
# configurations.

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
CMD="$CMD --word_emb_path word-vectors.txt"
CMD="$CMD --train_frac 0.1"
CMD="$CMD --n_epochs 3"

# Run it!
FINAL_COMMAND="$CODALAB_ARGS '$CMD'"
echo $FINAL_COMMAND
exec bash -c "$FINAL_COMMAND"
