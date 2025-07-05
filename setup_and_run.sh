#!/bin/bash


echo "MIDI Note Recorder のセットアップを開始します..."

if [ ! -d "venv" ]; then
    echo "仮想環境を作成中..."
    python3 -m venv venv
fi

echo "仮想環境をアクティベート中..."
source venv/bin/activate

echo "依存関係をインストール中..."
pip install --upgrade pip
pip install -r requirements.txt

echo "MIDI Note Recorder を起動します..."
python midi_recorder.py

deactivate
