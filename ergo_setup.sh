#!/bin/bash

mkdir ~/.ergo && touch ~/.ergo/.ergo_profile && touch ~/.ergo/.ergo_history && mkdir ~/.ergo/packages

read -r -p "Would you like to enable showing autocompletion? (creates a file ~/.initrc) [y/N] " response
case $response in
    [yY][eE][sS]|[yY]) 
        echo set show-all-if-ambiguous on >>  ~/.inputrc
        ;;
    *)
        ;;
esac
