"""
Player module: playback via sounddevice.
"""
import sys
import threading
try:
    import sounddevice as sd
    _has_sounddevice = True
except ImportError:
    _has_sounddevice = False

def play(waveform, sample_rate=44100, channels=1):
    """
    Play a waveform buffer using sounddevice.
    :param waveform: numpy.ndarray of float32.
    :param sample_rate: Sample rate in Hz.
    :param channels: Number of channels.
    """
    if not _has_sounddevice:
        print("sounddevice not installed; cannot play audio.", file=sys.stderr)
        return

    # Prepare data for playback: shape array according to channels
    data = waveform
    if channels > 1:
        try:
            data = waveform.reshape(-1, channels)
        except Exception:
            print(f"Error reshaping waveform for {channels} channels.", file=sys.stderr)
            return

    # Launch playback in a background thread to avoid blocking main thread
    try:
        def _do_play():
            try:
                sd.play(data, samplerate=sample_rate)
                sd.wait()
            except Exception as e_inner:
                print(f"Audio playback error: {e_inner}", file=sys.stderr)
        thread = threading.Thread(target=_do_play, daemon=True)
        thread.start()
    except Exception as e:
        print(f"Failed to start playback thread: {e}", file=sys.stderr)
