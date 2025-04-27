"""
Player module: playback via simpleaudio.
"""
import sys
try:
    import simpleaudio as sa
    _has_simpleaudio = True
except ImportError:
    _has_simpleaudio = False

from audioio import to_pcm16

def play(waveform, sample_rate=44100, channels=1):
    """
    Play a waveform buffer.
    :param waveform: numpy.ndarray of float32.
    :param sample_rate: Sample rate in Hz.
    :param channels: Number of channels.
    """
    pcm = to_pcm16(waveform)
    if _has_simpleaudio:
        play_obj = sa.play_buffer(pcm, channels, 2, sample_rate)
        play_obj.wait_done()
    else:
        print("simpleaudio not installed; cannot play audio.")
