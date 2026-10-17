# botkudos.com

Private repo for the BotKudos site. The live site is served by Cloudflare Pages.

- **`stories.json`** — every story on the site, newest first. This is the file
  you edit. See `EDITING.md` for the cheat sheet.
- **`template.html`** — the page shell. Rarely touched.
- **`build.py`** — bakes `stories.json` into `index.html`. Runs automatically.
- **`assets/generated/`** — the site's illustration images.

Every push to `main` rebuilds the site and deploys it via GitHub Actions.
