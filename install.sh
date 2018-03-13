#!/usr/bin/env bash
apt-get install -y python3
apt-get install -y python3-setuptools
apt-get install -y python3-pip python3-dev

#sudo pip3 install -e ".[test]"
python3 setup.py install

export FLASK_CONFIG=production
export FLASK_APP=run.py