# Profile maintenance

This profile follows the terminal / ASCII / contribution-calendar concept described in the supplied guide by Avi Vashishta (https://github.com/AVIVASHISHTA29). Its scripts are independently implemented for Ashif Rza.

## Publish

Merge the accompanying pull request into main. The README in ashifrza/ASHIFRZA is the profile README. The workflow runs on merge when its scripts/configuration change, every day around 06:17 UTC (11:47 IST), and manually from Actions > Update profile art > Run workflow. GitHub may delay scheduled jobs and can disable schedules on inactive public repositories.

No personal access token or repository secret is needed. Fetching uses GitHub's public HTML; committing uses GitHub Actions' automatic GITHUB_TOKEN with contents: write. Repository rules or disabled Actions may require owner configuration. The public calendar format is undocumented and may change. Parsing failures stop the job and preserve the previous committed artwork instead of publishing fabricated zeroes.

## Edit the info card

Edit profile.json, then run:

```sh
python scripts/make_info_card.py
```

The rows come from the provided resume. The role and account name follow the user's explicit request. The original resume and photograph are not published. Edit or shorten rows if content would exceed the fixed card width.

## Update the portrait

Only portrait generation needs extra packages:

```sh
python -m pip install -r scripts/requirements-portrait.txt
python scripts/make_ascii_svg.py /path/to/photo.jpeg
```

The default mask is tuned to the supplied blue background. For another background, isolate the portrait onto white first and use --keep-background. The resulting SVG is self-contained vector text; it does not embed the original photograph. All three cards support STATIC=1 for motionless generation and a reduced-motion preference. Animation plays once. Without animation support, the complete card remains visible.

## Refresh contributions locally

Python 3.12 or later is recommended. The daily scripts use only the standard library.

```sh
python -m unittest discover -s scripts -p 'test_*.py'
python scripts/fetch_contributions.py
python scripts/render_heatmap_svg.py
```

Counts are parsed from GitHub's tooltips, not inferred from color intensity. The calendar uses GitHub's rolling public window, with UTC fetch dates. Current streak allows today's count to be zero while yesterday's streak remains active. Longest streak is limited to the displayed window, not all-time. Private activity depends on what the account exposes publicly. The SVG includes its data date because GitHub's image cache can delay visible refreshes.
