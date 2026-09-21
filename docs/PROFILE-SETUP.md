# SIGNAL profile maintenance

The profile uses self-contained SVG images, original typography/layout and vector ASCII portrait data. There are no fonts, images, scripts, widgets, or statistics services loaded from third-party servers. The initial ASCII/contribution concept was inspired by the supplied Avi Vashishta guide; SIGNAL is an independently designed upgrade.

## Publish and update

Merge the accompanying pull request into main to apply this design. The Actions workflow runs when rendering scripts/configuration change, around 06:17 UTC (11:47 IST) daily, and via Actions > Update profile art > Run workflow. GitHub can delay schedules or disable them on inactive repositories. Fetching needs no personal token; the workflow commits with the automatic GITHUB_TOKEN and contents: write. Failed parsing preserves the previous committed assets.

## Design and content

- hero.svg shows the identity, role, animated ASCII portrait, scan line and orbit paths.
- systems.svg presents the frontend, backend and AI/data stack with moving connector signals.
- contrib-heatmap.svg contains actual public contribution counts and window-limited streaks.
- link-*.svg are local clickable link labels, wrapped in README anchors.

Edit profile.json for the role. The hero name, editorial copy, colors, stack and project labels live in scripts/make_showcase.py. The original info-card files remain available for reverting to the first design but are not used by this README.

```sh
python scripts/make_showcase.py
python scripts/render_heatmap_svg.py
```

Motion uses CSS inside SVGs. Entrances play once; orbital, scan and signal details loop slowly. Set STATIC=1 to generate motionless output. The reduced-motion media query disables all animations and hides scan/signal effects. Content remains visible if animation is unsupported. Browser, GitHub image cache and OS settings can affect playback. Detailed labels scale down with the SVG on small screens; README images include descriptive alternative text.

## Portrait

The original photograph and resume are not stored in the repository. data/portrait.json contains only the cropped ASCII character grid used by the renderer. To change it:

```sh
python -m pip install -r scripts/requirements-portrait.txt
python scripts/prepare_portrait.py /path/to/photo.jpeg
python scripts/make_showcase.py
```

The default crop and red-background mask are tuned to the supplied illustrated portrait. Use --background blue for a blue backdrop or --background none for an already isolated image. Use --crop LEFT TOP RIGHT BOTTOM with fractions between 0 and 1 to change framing. Daily rendering uses only the Python standard library; image packages are only needed to replace portrait data.

## Calendar

```sh
python -m unittest discover -s scripts -p 'test_*.py'
python scripts/fetch_contributions.py
python scripts/render_heatmap_svg.py
```

The undocumented public GitHub HTML calendar may change. Counts come from tooltips, not color levels. Current streak permits an unfinished zero-contribution day; longest streak covers only the displayed rolling window. Private activity appears only when exposed in the public calendar. The displayed UTC sync date helps identify cached images.
