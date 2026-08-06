#!/bin/bash

set -e

echo ">> INSTALLING REQUIREMENTS..."
cd /MusicPlayer

python3 -m pip install --upgrade pip
python3 -m pip install -U -r requirements.txt

echo ">> TESTING SPOTIPY..."
python3 -c "import spotipy; print('SPOTIPY OK:', spotipy.version)"

echo ">> STARTING MUSIC PLAYER USERBOT..."
python3 main.py
