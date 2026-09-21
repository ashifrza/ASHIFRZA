import json
from art import ROOT, start, text, reveal, save


def main():
    profile = json.loads((ROOT / 'profile.json').read_text())
    parts = start(490, 408, f"{profile['name']} info card", '; '.join(' '.join(row) for row in profile['rows']))
    parts += [text(24, 30, 'ashifrza@github: ~', 11, '#8b949e'), '<path d="M0 47H490" stroke="#21262d"/>',
              text(24, 82, profile['name'], 23, '#e6edf3'),
              text(24, 106, profile['role'], 13, '#39d353'),
              text(24, 127, '---------------------------------------', 12, '#30363d')]
    for index, (key, value) in enumerate(profile['rows']):
        y = 153 + index * 22
        parts += [f'<g{reveal(.3 + index * .11)}>', text(24, y, key, 11, '#39d353'),
                  text(105, y, value, 11), '</g>']
    for index, color in enumerate(['#21262d', '#0e4429', '#006d32', '#26a641', '#39d353', '#c9d1d9', '#e6edf3']):
        parts.append(f'<rect x="{24 + index * 23}" y="375" width="23" height="10" fill="{color}"/>')
    save(parts, 'info-card.svg')


if __name__ == '__main__':
    main()
