from datetime import date, timedelta
import unittest
from fetch_contributions import parse_calendar, statistics


class CalendarTests(unittest.TestCase):
    def test_tooltips_counts_and_future_cells(self):
        start = date(2025, 1, 1)
        html = ''.join(f'<td id="d{i}" data-date="{start + timedelta(days=i)}" data-level="{1 if i == 0 else 0}"></td><tool-tip for="d{i}">{"1,234 contributions" if i == 0 else "No contributions"} on a day.</tool-tip>' for i in range(366))
        days = parse_calendar(html, date(2025, 12, 31))
        self.assertEqual(len(days), 365)
        self.assertEqual(statistics(days)['total'], 1234)
        with self.assertRaises(ValueError):
            parse_calendar(html.replace('1,234 contributions', 'Unavailable'), date(2025, 12, 31))

    def test_missing_or_empty_calendar_fails(self):
        with self.assertRaises(ValueError):
            parse_calendar('<html>rate limited</html>', date.today())

    def test_streak_allows_unfinished_today(self):
        def days(counts):
            return [{'date': f'2025-12-{i+1:02}', 'count': count} for i, count in enumerate(counts)]
        self.assertEqual(statistics(days([1, 2, 3, 0]))['current_streak'], 3)
        self.assertEqual(statistics(days([1, 2, 0, 0]))['current_streak'], 0)
        self.assertEqual(statistics(days([1, 2, 0, 3]))['longest_streak'], 2)
        self.assertEqual(statistics(days([0, 0, 0]))['current_streak'], 0)


if __name__ == '__main__':
    unittest.main()
