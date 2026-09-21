from datetime import date, timedelta
import json
from art import ROOT, start, text, reveal, save


def main():
    data = json.loads((ROOT / 'data/contributions.json').read_text())
    days, stats = data['days'], data['stats']
    parts = start(860, 258, 'ashifrza contribution calendar',
                  f"{stats['total']} contributions from {days[0]['date']} to {days[-1]['date']}. Updated daily.")
    parts += [text(24, 30, 'ashifrza / contributions', 13, '#e6edf3'),
              text(836, 30, f"updated {data['as_of']} UTC", 10, '#8b949e', 'text-anchor="end"')]
    first = date.fromisoformat(days[0]['date'])
    origin = first - timedelta(days=(first.weekday() + 1) % 7)
    weeks = ((date.fromisoformat(days[-1]['date']) - origin).days // 7) + 1
    step = min(14.5, 772 / weeks)
    palette = ['#161b22', '#0e4429', '#006d32', '#26a641', '#39d353']
    previous_month = None
    for day in days:
        day_date = date.fromisoformat(day['date'])
        offset = (day_date - origin).days
        col, row = divmod(offset, 7)
        x, y = 57 + col * step, 64 + row * 15
        if day_date.month != previous_month and day_date.day == 1:
            if col < weeks - 2:
                parts.append(text(x, 53, day_date.strftime('%b'), 9, '#8b949e'))
            previous_month = day_date.month
        parts.append(f'<g{reveal((col + row) * .023)}><rect x="{x:.2f}" y="{y}" width="{step-3:.2f}" height="12" rx="2" fill="{palette[day["level"]]}"><title>{day["date"]}: {day["count"]} contributions</title></rect></g>')
    for row, label in [(1, 'Mon'), (3, 'Wed'), (5, 'Fri')]:
        parts.append(text(24, 74 + row * 15, label, 9, '#8b949e'))
    parts.append(text(57, 185, f"{days[0]['date']} to {days[-1]['date']}", 9, '#8b949e'))
    parts.append(text(678, 185, 'Less', 9, '#8b949e'))
    for index, color in enumerate(palette):
        parts.append(f'<rect x="{710 + index * 15}" y="176" width="11" height="11" rx="2" fill="{color}"/>')
    parts.append(text(790, 185, 'More', 9, '#8b949e'))
    parts.append('<path d="M24 201H836" stroke="#21262d"/>')
    parts += [text(24, 228, f"{stats['total']:,} contributions", 14, '#39d353'),
              text(294, 228, f"current streak  {stats['current_streak']}d", 11),
              text(550, 228, f"longest streak  {stats['longest_streak']}d", 11),
              text(24, 246, 'Rolling calendar. Streaks measured within the displayed period.', 8, '#8b949e')]
    save(parts, 'contrib-heatmap.svg')


if __name__ == '__main__':
    main()
