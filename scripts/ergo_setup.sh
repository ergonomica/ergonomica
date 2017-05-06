#!/bin/bash

echo "[ergo_setup.sh]: Welcome to the Ergonomica config setup wizard."

echo "[ergo_setup.sh]: Creating ~/.ergo directory..."
mkdir ~/.ergo

echo "[ergo_setup.sh]: Creating blank ~/.ergo/.ergo_profile and ~/.ergo/.ergo_history files..."
touch ~/.ergo/.ergo_profile
touch ~/.ergo/.ergo_history

echo "[ergo_setup.sh]: Creating packages directory in ~/.ergo..."
mkdir ~/.ergo/packages

read -p "[ergo_setup.sh]: Do you want to install the Ergonomica Package Manager (epm)? (Y\n)" -n 1 -r
if ! [[ $REPLY =~ ^[Nn]$ ]]
then
    echo "[ergo_setup.sh]: Installing epm..."
    curl -L "https://raw.githubusercontent.com/ergonomica/package-epm/master/epm.py" > ~/.ergo/packages/epm.py
    echo "[ergo_setup.sh]: epm successfully installed."
fi

echo "[ergo_setup.sh]: Setup complete."
