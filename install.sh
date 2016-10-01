#!/usr/bash

installer_version=1

if [[ `cat version.txt` == "$installer_version" ]]; then
    echo "Latest version already installed."
    exit
fi

echo "Installing packages"
apt-get update > /dev/null
apt-get install -yf python3-dev git python-pip virtualenv supervisor > /dev/null

git clone https://github.com/beshaya/minespace /opt/app/
cd /opt/app && git pull && \ 
virtualenv /opt/app/venv -p /usr/bin/python3 &&\
    echo "Installing python modules" && \
    /opt/app/venv/bin/pip install -r /opt/app/requirements.txt > /dev/null&& \
    gsutil cp gs://tnfc-minespace/config.py /opt/app/ &&\
    cd / &&\
    echo "$installer_version" > version.txt && \
    echo "Installation complete."    
