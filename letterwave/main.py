"""
Main UI and application logic for LetterWave Quest.
"""
import sys
import os

from .renderer import Renderer
from .audioio import assemble_sequence, save_wav
from .player import play

SAMPLE_RATE = 44100

def bpm_to_seconds(bpm):
    return 4 * 60.0 / bpm

def main():
    default_bpm = 120
    font_path = None
    img_size = (200, 200)
    renderer = None
    print("LetterWave Quest")
    while True:
        print("\nMenu:")
        print("1) New Composition")
        print("2) Options")
        print("3) Exit")
        choice = input("Select option: ").strip()
        if choice == '1':
            word = input("Enter word (A-Z only): ").strip().upper()
            if not word.isalpha():
                print("Invalid input; letters only.")
                continue
            bpm_str = input(f"Enter BPM (default {default_bpm}): ").strip()
            bpm = default_bpm
            if bpm_str:
                try:
                    bpm_val = int(bpm_str)
                    if 40 <= bpm_val <= 300:
                        bpm = bpm_val
                    else:
                        print("BPM out of range (40-300). Using default.")
                except ValueError:
                    print("Invalid BPM; using default.")
            duration = bpm_to_seconds(bpm)
            num_samples = int(SAMPLE_RATE * duration)
            if renderer is None:
                renderer = Renderer(font_path, img_size)
            segments = []
            for ch in word:
                segments.append(renderer.render_wave(ch, num_samples))
            waveform = assemble_sequence(segments)
            play(waveform, SAMPLE_RATE)
            ans = input("Save WAV? (y/n): ").strip().lower()
            if ans == 'y':
                fname = input("Filename (without extension): ").strip()
                if fname:
                    save_wav(fname + '.wav', waveform, SAMPLE_RATE)
                    print(f"Saved to {fname}.wav")
                else:
                    print("No filename given; skipping save.")
        elif choice == '2':
            print("\nOptions:")
            print(f"1) Set default BPM (current {default_bpm})")
            print(f"2) Set font path (current {font_path or 'system default'})")
            print("3) Back")
            opt = input("Select option: ").strip()
            if opt == '1':
                bpm_str = input("Enter default BPM (40-300): ").strip()
                try:
                    bpm_val = int(bpm_str)
                    if 40 <= bpm_val <= 300:
                        default_bpm = bpm_val
                        print(f"Default BPM set to {default_bpm}")
                    else:
                        print("BPM out of range")
                except ValueError:
                    print("Invalid BPM")
            elif opt == '2':
                path = input("Enter font path (or blank to use system default): ").strip()
                if path and not os.path.isfile(path):
                    print("File not found")
                else:
                    font_path = path or None
                    renderer = None
                    print(f"Font path set to {font_path or 'system default'}")
            elif opt == '3':
                continue
            else:
                print("Invalid option")
        elif choice == '3':
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid option")

if __name__ == '__main__':
    main()