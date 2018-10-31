CMD='cl run'

# If you want to change the docker image....
# CMD="$CMD --request-docker-image "

# Add dependencies
CMD="$CMD :src :dataset"

# The command you actually run
CMD="$CMD 'python src/main.py --input dataset --eta 0234'"

echo $CMD
exec $CMD