# LetterWave Quest

Turn words into music! LetterWave Quest is a lightweight Python audio game/app that reads any uppercase word, "draws" each letter as a waveform over one 4-beat measure at your chosen BPM, stitches them into a tune, plays it back, and lets you save it as a .wav file.

## Features
- Word-to-Waveform: letters rendered into images; each vertical slice drives audio amplitude.
- Tempo Control: user picks BPM; each letter plays for exactly one 4/4 measure.
- Real-time Playback: console UI to type a word, hear it immediately, and optionally save to disk.
 - Pure Python: uses numpy, Pillow, wave, and sounddevice.

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
python -m letterwave
```