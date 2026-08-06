#!/bin/bash

echo ">> INSTALLING REQUIREMENTS..."
cd /MusicPlayer

pip3 install -U -r requirements.txt

echo ">> STARTING MUSIC PLAYER USERBOT..."

python3 main.py
