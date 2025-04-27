"""
Audio I/O module: assemble sequences and save as WAV.
"""
import numpy as np
import wave

def assemble_sequence(segments):
    """
    Concatenate a list of waveform segments into one array.
    :param segments: List of numpy.ndarray of float32.
    :return: numpy.ndarray of float32.
    """
    if not segments:
        return np.array([], dtype=np.float32)
    return np.concatenate(segments)

def normalize(waveform):
    """
    Normalize waveform to maximum absolute amplitude of 1.0.
    :param waveform: numpy.ndarray.
    :return: numpy.ndarray.
    """
    maxval = np.max(np.abs(waveform))
    if maxval == 0:
        return waveform
    return waveform / maxval

def to_pcm16(waveform):
    """
    Convert float32 waveform in [-1.0,1.0] to PCM16 bytes.
    :param waveform: numpy.ndarray of float32.
    :return: bytes.
    """
    norm = normalize(waveform)
    pcm = (norm * 32767).astype(np.int16)
    return pcm.tobytes()

def save_wav(filename, waveform, sample_rate=44100, channels=1):
    """
    Save waveform to a WAV file.
    :param filename: Output path ending in .wav.
    :param waveform: numpy.ndarray of float32.
    :param sample_rate: Sample rate in Hz.
    :param channels: Number of audio channels.
    """
    pcm_bytes = to_pcm16(waveform)
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(pcm_bytes)
