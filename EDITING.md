# BotKudos editing cheat sheet

The whole site is driven by one file: **`stories.json`**. Edit it right here
on GitHub (pencil icon), commit, and the live site updates a minute or two later.

## Add a story

1. Open `stories.json`, click the pencil icon.
2. Paste this block at the **top** of the list (newest first), right after the
   opening `[`:

```json
  {
    "pub_date": "2026-09",
    "title": "Headline goes here. It ends with On.",
    "summary": "One or two punchy sentences. Warm and celebratory.",
    "source_name": "Reuters",
    "source_url": "https://example.com/the-article",
    "image_url": "",
    "tags": ["medicine", "vaccine"],
    "category": "Medicine",
    "kudos_level": 2
  },
```

3. Add a comma after the closing `}` if another story follows it.
4. Commit. Done.

## Edit a story

Find its title, change the text, commit. Leave everything else alone.

## Remove a story

Delete its whole `{ ... }` block. If it was the last item, also remove the
comma after the block above it. Commit.

## Rules that keep the site consistent

- `category` must be exactly one of: Medicine, Science, Robots, Climate,
  Education, Accessibility.
- `kudos_level` is 1 (Nice), 2 (Bravo), or 3 (Legend).
- The headline ends with "On." (the mirror of BotGaffe's "Off.").
- `pub_date` is year-month: `2026-09`.
- No em dashes anywhere. No "this is not X, this is Y" phrasing.
- Only positive tech stories: tech wins, quiet heroics, innovation doing good.
  If the story is really about a mishap, it belongs on botgaffe.com instead.
- Every source link must be live and functional before publishing; if a link
  is dead, find an alternate link to the same story. Prefer the original
  reporting over aggregators, and strip tracking parameters from the URL.
- Keep `image_url` as `""` (the site uses its own generated illustrations).

## If the site looks broken after your edit

You probably left a trailing comma or a missing quote. GitHub shows a red X
on invalid JSON. Press Ctrl+Z, or ask Brahmi to fix it.

## Story URLs (for search engines)

Every story automatically gets its own page, like
`botkudos.com/kudos/3d-printed-spine-saves-woman-on/`. The address comes from
the title, so avoid renaming a title after publishing: it changes the URL.
You never need to touch these pages; they rebuild on every commit.

## Notes

- New stories from the daily news sweep are not added automatically yet.
  That pipeline is next; for now, add finds by hand.
- A story you delete here stays deleted. Nothing re-adds it on its own.
