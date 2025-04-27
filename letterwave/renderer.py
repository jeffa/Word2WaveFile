"""
Renderer module: render letters to images and sample as audio waveforms.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

class Renderer:
    def __init__(self, font_path=None, img_size=(200, 200), font_size=180):
        """
        Initialize the renderer.
        :param font_path: Path to a TrueType font file. If None, system default is used.
        :param img_size: Tuple (width, height) for rendered image.
        :param font_size: Font size in points.
        """
        self.img_size = img_size
        if font_path:
            self.font = ImageFont.truetype(font_path, font_size)
        else:
            try:
                # Try common default
                self.font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
            except Exception:
                self.font = ImageFont.load_default()

    def render_letter(self, letter):  # noqa: C901
        """
        Render a single uppercase letter to a grayscale PIL image.
        :param letter: A-Z character.
        :return: PIL.Image in mode 'L'.
        """
        img = Image.new('L', self.img_size, 0)
        draw = ImageDraw.Draw(img)
        w, h = draw.textsize(letter, font=self.font)
        pos = ((self.img_size[0] - w) // 2, (self.img_size[1] - h) // 2)
        draw.text(pos, letter, fill=255, font=self.font)
        return img

    def sample_image(self, img, num_samples, envelope=True):
        """
        Convert a grayscale image into a waveform based on vertical slice brightness.
        :param img: PIL.Image in mode 'L'.
        :param num_samples: Number of audio samples to generate.
        :param envelope: If True, apply simple fade-in/out envelope.
        :return: numpy.ndarray of shape (num_samples,) with float32 values in [-1.0, +1.0].
        """
        W, H = img.size
        pixels = np.array(img)
        # Mean brightness per column
        col_means = pixels.mean(axis=0)
        # Map brightness [0..255] to amplitude [-1..+1]
        amps = (col_means / 127.5) - 1.0
        # Map sample indices to column indices
        idxs = np.floor(np.linspace(0, W - 1, num_samples)).astype(int)
        data = amps[idxs]
        if envelope:
            t = np.linspace(0.0, 1.0, num_samples, endpoint=False)
            env = np.minimum(t, 1.0 - t) * 2.0
            data = data * env
        return data.astype(np.float32)

    def render_wave(self, letter, num_samples, envelope=True):
        """
        Convenience: render letter and sample into waveform.
        :param letter: A-Z character.
        :param num_samples: Number of audio samples.
        :param envelope: Apply fade envelope.
        :return: numpy.ndarray of float32 waveform.
        """
        img = self.render_letter(letter)
        return self.sample_image(img, num_samples, envelope)