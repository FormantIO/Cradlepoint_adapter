#!/usr/bin/env bash
set -e

# Skip apt dependencies to avoid sudo

# install the formant python module
pip3 install setuptools
pip3 install wheel
pip3 install -r requirements.txt

touch setup.lock
