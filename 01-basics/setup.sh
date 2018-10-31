printf "Setting up virtual environment...\n"
virtualenv -p python3.6 venv
source venv/bin/activate
pip install -U pip setuptools
pip install -r requirements.txt

printf "Downloading datasets...\n"
cd infersent/dataset/
bash get_datasets.sh