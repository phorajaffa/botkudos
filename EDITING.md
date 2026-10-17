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
    "title": "Headline goes here",
    "summary": "One or two punchy sentences. Deadpan, never mean.",
    "source_name": "Reuters",
    "source_url": "https://example.com/the-article",
    "image_url": "",
    "tags": ["robot", "fail"],
    "category": "Robots"
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

- `category` must be exactly one of: Chatbots, Self-Driving, Robots,
  Algorithms, Bot Swarms, Scams & Fraud.
- `pub_date` is year-month: `2026-09`.
- No em dashes anywhere. No "this is not X, this is Y" phrasing.
- Skip data breaches unless a bot, agent, or AI system caused them.
- Keep `image_url` as `""` (the site uses its own generated illustrations).

## If the site looks broken after your edit

You probably left a trailing comma or a missing quote. GitHub shows a red X
on invalid JSON. Press Ctrl+Z, or ask Zuckie to fix it.

## Story URLs (for search engines)

Every story automatically gets its own page, like
`botkudos.com/kudos/chatgpt-invented-court-case/`. The address comes from
the title, so avoid renaming a title after publishing: it changes the URL.
You never need to touch these pages; they rebuild on every commit.

## Notes

- New stories from the daily news sweep are not added automatically yet.
  That pipeline is next; for now, add finds by hand.
- A story you delete here stays deleted. Nothing re-adds it on its own.
