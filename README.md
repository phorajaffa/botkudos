# BotKudos

Tech wins, quiet heroics, and innovation doing good in the world, collected while the logs are still warm.

Sister site of [botgaffe.com](https://botgaffe.com).

- Live: https://botkudos.com (https://botkudos.pages.dev)
- Feed: https://botkudos.com/feed.xml

## Editing

Stories live in `stories.json` — the only file you normally edit. Run `python3 build.py`
to regenerate `index.html`, story pages, `sitemap.xml`, `robots.txt`, and `feed.xml`.
Pushing to `main` auto-deploys to Cloudflare Pages via GitHub Actions.
