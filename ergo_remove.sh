#!/bin/bash

echo "[ergo_remove.sh]: Welcome to the ergonomica config removal wizard."

read -p "[ergo_remove.sh]: Are you absolutely sure that you want to delete Ergonomica and all its packages?" -n 1 -r
if ! [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "[ergo_remove.sh]: Removing ~/.ergo and all its contents..."
    rm -rf ~/.ergo
fi

echo "[ergo_remove.sh]: Ergonomica config removal complete."
