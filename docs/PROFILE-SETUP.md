# Developer dashboard maintenance

This README is a GitHub-native developer dashboard, not a replacement for ashifrza.in. It uses animated SVG panels, repository links, an expandable About section, local technology logos and a game launcher. No portrait is displayed.

## Data and content

scripts/fetch_github.py reads public GitHub REST endpoints for repositories, stars, forks, followers and repository language bytes. It paginates the repository list. Language totals exclude forks and the profile repository; they are source-code shares, not proficiency ratings. A failed fetch leaves the previous complete snapshot intact. The standard-library scripts need no personal access token; Actions supplies its automatic token to avoid the anonymous API limit.

scripts/fetch_contributions.py reads GitHub's public contribution calendar. It validates every day and count before replacing the last good snapshot. Streaks are limited to the displayed calendar, with the current unfinished day allowed to have zero contributions.

About/experience content is drawn from the supplied resume. HireEdge and openness to roles come from the public GitHub bio at the time of this redesign. These editorial statements are maintained in scripts/build_dashboard.py and README.md; the numeric repository data refreshes daily.

The Profile views badge is the external Komarev badge-load counter. It is not GitHub's official analytics, a count of unique people, or an all-time reconstructed total. Proxies, caches, bots and repeated loads can affect it. All other profile art and logos are local files.

## Edit and regenerate

```sh
python scripts/fetch_github.py
python scripts/fetch_contributions.py
python scripts/build_dashboard.py
python scripts/render_activity.py
python -m unittest discover -s scripts -p 'test_*.py'
node scripts/test-game.mjs
```

The main-branch workflow refreshes around 06:17 UTC daily and can be run manually. GitHub may delay schedules or disable them for inactive public repositories. SVGs show their snapshot date. STATIC=1 disables generated animations; reduced-motion preferences also disable SVG animation. README SVGs cannot run JavaScript, accept game controls or load interactive 3D scenes.

## Commit Dash

The playable game lives in game/ and is published separately on the repository's gh-pages branch at https://ashifrza.github.io/ASHIFRZA/. Only the game is hosted; it contains no portfolio pages. Controls: arrow keys or A/D, left/right buttons, or a horizontal swipe. Space pauses/resumes, Escape toggles pause, and losing focus pauses the game. Runs last 45 seconds with three health points. Five consecutive pickups enable double points. Best scores stay in localStorage; no analytics or leaderboard server is used by the game.

Run locally with any static HTTP server; ES modules do not run reliably from file:// URLs:

```sh
python -m http.server 8000 --directory game
```

After editing the game, publish those files to the gh-pages branch. The publish-arcade workflow automates this when game files are merged to main. GitHub Pages must use the gh-pages branch, root folder. The profile's daily data workflow does not modify the game.

## Assets

Technology logos are from Devicon (https://github.com/devicons/devicon), distributed with its MIT license in assets/logos/LICENSE. Technology names and marks belong to their respective owners. Portrait assets and their generators have been removed from this version; earlier versions remain in Git history.
