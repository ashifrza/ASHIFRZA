"""Fetch GitHub's public contribution calendar. No third-party packages or PAT."""
import argparse
from datetime import date, datetime, timedelta, timezone
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import time
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


class CalendarParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cells = {}
        self.tips = {}
        self.tip_id = None
        self.tip_text = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('data-date') and a.get('data-level') is not None:
            self.cells[a['id']] = {'date': a['data-date'], 'level': int(a['data-level'])}
        if tag == 'tool-tip':
            self.tip_id = a.get('for')
            self.tip_text = []

    def handle_data(self, text):
        if self.tip_id:
            self.tip_text.append(text)

    def handle_endtag(self, tag):
        if tag == 'tool-tip' and self.tip_id:
            self.tips[self.tip_id] = ''.join(self.tip_text).strip()
            self.tip_id = None


def parse_calendar(html, today):
    parser = CalendarParser()
    parser.feed(html)
    days = []
    for cell_id, cell in parser.cells.items():
        if date.fromisoformat(cell['date']) > today:
            continue
        tip = parser.tips.get(cell_id, '')
        match = re.match(r'([\d,]+) contributions?\b', tip)
        if tip.startswith('No contributions'):
            count = 0
        elif match:
            count = int(match.group(1).replace(',', ''))
        else:
            raise ValueError(f'Unrecognized contribution tooltip: {tip!r}')
        if cell['level'] not in range(5):
            raise ValueError('Unexpected GitHub color level')
        days.append({**cell, 'count': count})
    days.sort(key=lambda d: d['date'])
    if not 365 <= len(days) <= 371:
        raise ValueError(f'Expected a full year of daily cells, received {len(days)}')
    dates = [date.fromisoformat(d['date']) for d in days]
    if dates[-1] != today or any(b - a != timedelta(days=1) for a, b in zip(dates, dates[1:])):
        raise ValueError('Calendar is stale, duplicated, or has missing dates')
    return days


def statistics(days):
    longest = run = 0
    monthly = {}
    for day in days:
        run = run + 1 if day['count'] else 0
        longest = max(longest, run)
        month = day['date'][:7]
        monthly[month] = monthly.get(month, 0) + day['count']
    # An unfinished zero-contribution day does not break yesterday's streak.
    current = 0
    ended = days[:-1] if days and not days[-1]['count'] else days
    for day in reversed(ended):
        if not day['count']:
            break
        current += 1
    return {'total': sum(d['count'] for d in days), 'current_streak': current,
            'longest_streak': longest, 'best_day': max(days, key=lambda d: d['count']),
            'monthly_totals': monthly}


def main():
    args = argparse.ArgumentParser()
    args.add_argument('--html', type=Path, help='Read a saved GitHub response for offline verification')
    opts = args.parse_args()
    username = json.loads((ROOT / 'profile.json').read_text())['username']
    if not re.fullmatch(r'[A-Za-z0-9-]{1,39}', username):
        raise ValueError('Invalid username')
    url = f'https://github.com/users/{username}/contributions'
    if opts.html:
        html = opts.html.read_text(encoding='utf-8')
    else:
        for attempt in range(3):
            try:
                request = Request(url, headers={'User-Agent': 'github-profile-calendar', 'Accept-Language': 'en-US'})
                with urlopen(request, timeout=30) as response:
                    html = response.read().decode('utf-8')
                break
            except OSError:
                if attempt == 2:
                    raise
                time.sleep(2 ** attempt)
    today = datetime.now(timezone.utc).date()
    days = parse_calendar(html, today)
    payload = {'username': username, 'as_of': today.isoformat(), 'source': url,
               'days': days, 'stats': statistics(days)}
    output = ROOT / 'data/contributions.json'
    output.parent.mkdir(exist_ok=True)
    temporary = output.with_suffix('.tmp')
    temporary.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')
    temporary.replace(output)
    print(f"Fetched {len(days)} days; {payload['stats']['total']} contributions")


if __name__ == '__main__':
    main()
