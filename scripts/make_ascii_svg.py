"""Convert a local portrait into vector ASCII; the original photograph stays local.

For this supplied blue-background portrait, a chroma mask removes the background.
For other photographs use a pre-isolated image and --keep-background.
"""
import argparse
import numpy as np
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
from art import STATIC, start, text, save


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('photo')
    parser.add_argument('--keep-background', action='store_true')
    opts = parser.parse_args()
    photo = ImageOps.exif_transpose(Image.open(opts.photo)).convert('RGB')
    pixels = np.asarray(photo).astype(float)
    mask = np.ones(pixels.shape[:2], dtype=bool)
    if not opts.keep_background:
        r, g, b = pixels[:, :, 0], pixels[:, :, 1], pixels[:, :, 2]
        mask = ~((b > r * 1.25 + 20) & (b > g * 1.12) & (g > r * 1.2))
    pixels[~mask] = 255
    gray = Image.fromarray(pixels.astype('uint8')).convert('L')
    gray = ImageOps.autocontrast(gray, cutoff=1)
    gray = ImageEnhance.Contrast(gray).enhance(1.18)
    gray = gray.filter(ImageFilter.UnsharpMask(radius=3, percent=140, threshold=3))
    grid = np.asarray(gray.resize((100, 56), Image.Resampling.LANCZOS))
    ramp = ' .`:-=+*cs#%@'
    rows = [''.join(ramp[min(len(ramp)-1, int((255-int(v)) / 256 * len(ramp)))] for v in row) for row in grid]
    parts = start(370, 408, 'ASHIF RZA animated ASCII portrait', 'Monochrome ASCII portrait drawn from Ashif\'s photograph, revealing one row at a time.')
    parts += [text(18, 30, './portrait --ascii', 11, '#8b949e'), '<path d="M0 47H370" stroke="#21262d"/>']
    for index, row in enumerate(rows):
        y = 64 + index * 5.75
        if not STATIC:
            # The underlying rectangle is full width for renderers without SMIL.
            parts.append(f'<defs><clipPath id="row{index}"><rect x="14" y="{y-5.75}" width="342" height="6.5"><animate attributeName="width" values="0;0;342" keyTimes="0;{(index*.037)/(index*.037+.12):.5f};1" dur="{index*.037+.12:.3f}s" fill="freeze"/></rect></clipPath></defs>')
        clip = '' if STATIC else f'class="wipe" clip-path="url(#row{index})"'
        parts.append(f'<g {clip}>' + text(14, y, row, 5.6, '#c9d1d9', 'xml:space="preserve" textLength="342" lengthAdjust="spacingAndGlyphs"') + '</g>')
    save(parts, 'ashif-ascii.svg')


if __name__ == '__main__':
    main()
