#!/bin/bash

if command -v pyenv &>/dev/null; then
  pyenv install 3.11
else
  brew install python@3.11
fi

python3.11 -m pip install -r requirements.txt

sudo cp commit /usr/local/bin
sudo cp commit_message_generator.py /usr/local/bin

sudo chmod +x /usr/local/bin/commit
sudo chmod +x /usr/local/bin/commit_message_generator.py
