"""Shared SVG helpers. Visible final state remains available without animation."""
from html import escape
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATIC = os.environ.get('STATIC') == '1'
FONT = "'Cascadia Mono','DejaVu Sans Mono',Consolas,monospace"


def start(width, height, title, description):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
            f'<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>',
            '<style>@media(prefers-reduced-motion:reduce){.reveal{animation:none!important}.wipe{clip-path:none!important}.cursor{display:none!important}}',
            '@keyframes enter{from{opacity:0;transform:translateY(-5px)}to{opacity:1;transform:translateY(0)}}',
            '</style>',
            f'<rect x=".5" y=".5" width="{width-1}" height="{height-1}" rx="12" fill="#0d1117" stroke="#30363d"/>']


def text(x, y, value, size=12, color='#c9d1d9', extra=''):
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="{FONT}" font-size="{size}" {extra}>{escape(str(value))}</text>'


def reveal(delay):
    return '' if STATIC else f' class="reveal" style="animation:enter .38s ease-out {delay:.3f}s both"'


def save(parts, name):
    (ROOT / name).write_text('\n'.join(parts + ['</svg>']) + '\n', encoding='utf-8')
