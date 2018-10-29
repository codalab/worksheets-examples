echo "Setting up virtual environment..."

virtualenv -p python3.6 venv
source venv/bin/activate
pip install -U pip setuptools
pip install -r requirements.txt


printf "Downloading dataset... "

# Download & show spinner
python ./download.py 2>/dev/null &
pid=$!
spin='-\|/'
i=0
while kill -0 $pid 2>/dev/null
do
  i=$(( (i+1) %4 ))
  printf "\b${spin:$i:1}"
  sleep .1
done

# Prepare data directory
unzip data.zip -d data/
rm data.zip

printf "\bdone.\n"


# Make experiments directory
mkdir experiments/