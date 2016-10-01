#!/usr/bash

installer_version=1

if [[ `cat version.txt` == "$installer_version" ]]; then
    echo "Latest version already installed."
fi

apt-get update
apt-get install -yf python3-dev git pip

git clone https://github.com/beshaya/minespace && \
cd minespace && \
git pull && \
pip install -r requirements.txt && \
gsutil cp gs://tnfc-minespace/config.py ./ &&\
cd ../ &&\
echo "$installer_version" > version.txt && \
echo "Installation complete."    

