#!/usr/bin/env python3
"""Build the BotKudos static site.

Reads stories.json (the only file you normally edit) and produces:

  index.html                 the main browse page (stories embedded as data,
                             first 12 cards pre-rendered as static HTML so
                             crawlers and no-JS clients see real headlines)
  kudos/<slug>/index.html  one static page per story, for search engines
  sitemap.xml                every public URL, so crawlers find each story
  robots.txt                 crawler rules + sitemap pointer
  feed.xml                   RSS 2.0 feed of every story, newest first

Story URLs look like: https://botkudos.com/kudos/<slug>/
The slug is derived deterministically from the story title, so a URL stays
stable as long as the title does not change. Avoid renaming titles casually:
it changes the story's URL.

Run: python3 build.py
"""
import base64
import html
import json
import re
from datetime import date, datetime, timezone
from email.utils import format_datetime
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).parent
SITE = "https://botkudos.com"
TODAY = date.today().isoformat()

PER_PAGE = 12
VISUAL_BREAK_AFTER = 8
VISUAL_BREAKS = [
    "media-generation-visual-break-1-0-879ca26a-0aab-4f88-b35f-739571202ef1.webp",
    "media-generation-visual-break-2-0-36bfcaa3-711a-4cc2-ab16-ac27c75b4f2b.webp",
    "media-generation-visual-break-3-0-313d0b29-5f93-4be3-abf2-60602d9d79f2.webp",
    "media-generation-visual-break-4-0-9dad0aba-1852-430e-ae95-9835a5ba7242.webp",
]
SITE_SHARE_TEXT = ("Bot Kudos - Tech wins, quiet heroics, and innovation "
                   "doing good in the world, collected while the logs are still warm.")

ICON_SHARE = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
              'stroke-width="2" aria-hidden="true"><path d="M12 3v12"/>'
              '<path d="M7 8l5-5 5 5"/><path d="M5 12v8h14v-8"/></svg>')
ICON_X = "M18.9 2H22l-6.8 7.8L23.2 22h-6.3l-4.9-6.4L6.4 22H3.3l7.3-8.3L1.6 2H8l4.4 5.9L18.9 2zm-1.1 18h1.7L7.1 3.9H5.3L17.8 20z"
ICON_FACEBOOK = ("M13.5 22v-8h2.7l.4-3.2h-3.1V8.7c0-.9.3-1.6 1.6-1.6h1.7V4.2c-.3 0-1.3-.1-2.4-.1"
                 "-2.4 0-4 1.4-4 4.1v2.6H7.7V14h2.7v8h3.1z")
ICON_WHATSAPP = ("M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.4 13.9c-.2.7-1.3 1.3-1.8 1.4"
                 "-.5.1-1 .2-3.4-.7-2.9-1.2-4.7-4.1-4.9-4.3-.1-.2-1.1-1.5-1.1-2.9s.7-2 1-2.3c.2-.3.5-.3.7-.3h.5"
                 "c.2 0 .4 0 .6.5s.8 1.9.8 2c.1.1.1.3 0 .5-.3.6-.6.8-.4 1.1.7 1.2 1.6 2 2.8 2.6.3.2.5.1.7-.1l.8-.9"
                 "c.2-.3.4-.2.7-.1l2 1c.3.1.5.2.6.4 0 .1 0 .7-.2 1.1z")
ICON_TELEGRAM = "M2 21l21-9L2 3v7l15 2-15 2v7z"
ICON_COPY = ("M16 1H4a2 2 0 0 0-2 2v14h2V3h12V1zm3 4H8a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h11a2 2 0 0 0-2-2V7a2 2 0 "
             "0 0-2-2zm0 16H8V7h11v14z")

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]

KUDOS_LEVELS = {1: "Nice", 2: "Bravo", 3: "Legend"}


def kudos_badge_html(story):
    try:
        level = int(story.get("kudos_level"))
    except (TypeError, ValueError):
        return ""
    label = KUDOS_LEVELS.get(level)
    if not label:
        return ""
    return (f'<span class="kudos-level kl{level}">'
            f'Kudos level: {html.escape(label)}</span>')


def slugify(title, used):
    s = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:60].rstrip("-")
    s = s or "kudos"
    base, i = s, 2
    while s in used:
        s = f"{base}-{i}"
        i += 1
    used.add(s)
    return s


def pub_label(pub_date):
    parts = (pub_date or "").split("-")
    if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
        return f"{MONTHS[int(parts[1]) - 1]} {parts[0]}"
    if len(parts) == 1 and parts[0].isdigit():
        return parts[0]
    return pub_date or ""


def lastmod(pub_date):
    parts = (pub_date or "").split("-")
    if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
        return f"{parts[0]}-{parts[1]}-01"
    if len(parts) == 1 and parts[0].isdigit():
        return f"{parts[0]}-01-01"
    return TODAY


def meta_desc(summary):
    d = re.sub(r"\s+", " ", summary or "").strip()
    return d if len(d) <= 160 else d[:157].rsplit(" ", 1)[0] + "..."


def rss_pubdate(pub_date):
    parts = (pub_date or "").split("-")
    try:
        dt = datetime(int(parts[0]),
                      int(parts[1]) if len(parts) > 1 else 1,
                      1, tzinfo=timezone.utc)
    except (ValueError, IndexError):
        dt = datetime.now(timezone.utc)
    return format_datetime(dt)


def rss_cdata(text):
    return (text or "").replace("]]>", "]]&gt;")


def plat_icon(path):
    return (f'<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
            f'<path d="{path}"/></svg>')


def share_hrefs(title, url, text=None):
    share_text = text if text is not None else f"{title} - via Bot Kudos"
    full = f"{share_text} {url}"
    q = lambda s: quote(s, safe="")
    return {
        "x": f"https://twitter.com/intent/tweet?text={q(share_text)}&url={q(url)}",
        "facebook": f"https://www.facebook.com/sharer/sharer.php?u={q(url)}",
        "whatsapp": f"https://wa.me/?text={q(full)}",
        "telegram": f"https://t.me/share/url?url={q(url)}&text={q(share_text)}",
        "copy": full,
    }


def share_pop_items(title, url, text=None):
    hrefs = share_hrefs(title, url, text)
    e = lambda v: html.escape(v, quote=True)
    items = [
        (hrefs["x"], ICON_X, "Post on X"),
        (hrefs["facebook"], ICON_FACEBOOK, "Facebook"),
        (hrefs["whatsapp"], ICON_WHATSAPP, "WhatsApp"),
        (hrefs["telegram"], ICON_TELEGRAM, "Telegram"),
    ]
    out = "".join(
        f'<a href="{e(href)}" target="_blank" rel="noopener">'
        f'{plat_icon(path)}<span>{label}</span></a>'
        for href, path, label in items
    )
    out += (f'<button type="button" data-copy="{e(hrefs["copy"])}">'
            f'{plat_icon(ICON_COPY)}<span>Copy link</span></button>')
    return out


def card_html(story, index, chunk_len, chunk_index):
    """Static version of the JS storyCards() markup, for the pre-rendered grid."""
    title = story.get("title", "Untitled kudos")
    url = story.get("url", SITE + "/")
    e = lambda v: html.escape(v, quote=True)
    card = (
        '<article class="card">\n'
        '  <div class="card-body">\n'
        f'    <h2>{e(title)}</h2>\n'
        '    <div class="story-meta">\n'
        f'      <time class="story-date" datetime="{e(story.get("pub_date", ""))}">'
        f'{e(pub_label(story.get("pub_date")))}</time>\n'
        '      <span class="meta-dot" aria-hidden="true">·</span>\n'
        f'      <span class="category" data-category="{e(story.get("category", ""))}">'
        f'{e(story.get("category", ""))}</span>\n'
        f'      {kudos_badge_html(story)}\n'
        '    </div>\n'
        f'    <p class="summary">{e(story.get("summary", ""))}</p>\n'
        '    <div class="card-foot">\n'
        f'      <a class="source-link" href="{e(story.get("source_url", SITE))}" '
        f'target="_blank" rel="noopener noreferrer" '
        f'aria-label="Read original story from {e(story.get("source_name", "Source"))}">\n'
        f'        {e(story.get("source_name", "Source"))} <span aria-hidden="true">↗</span>\n'
        '      </a>\n'
        '      <div class="share-wrap">\n'
        f'        <button class="share-btn" type="button" data-share-btn '
        f'data-share-title="{e(title)}" data-share-url="{e(url)}" '
        f'aria-haspopup="true" aria-expanded="false" aria-label="Share: {e(title)}">\n'
        f'          {ICON_SHARE}<span>Share</span>\n'
        '        </button>\n'
        f'        <div class="share-pop" hidden>{share_pop_items(title, url)}</div>\n'
        '      </div>\n'
        '    </div>\n'
        '  </div>\n'
        '</article>'
    )
    if index == VISUAL_BREAK_AFTER - 1 and chunk_len > VISUAL_BREAK_AFTER:
        img = VISUAL_BREAKS[chunk_index % len(VISUAL_BREAKS)]
        card += (
            '\n<div class="visual-break" aria-hidden="true">\n'
            f'  <img src="assets/generated/{img}" alt="" loading="lazy" />\n'
            '</div>'
        )
    return card


def build_story_page(story, slug, prev_link, next_link, template):
    title = story.get("title", "Untitled kudos")
    summary = story.get("summary", "")
    canonical = f"{SITE}/kudos/{slug}/"
    desc = meta_desc(summary)
    paras = [p for p in re.split(r"\n\s*\n", summary.strip()) if p.strip()]
    summary_html = "".join(f"<p>{html.escape(p)}</p>" for p in paras) or "<p></p>"
    tags_html = "".join(f"<span>{html.escape(t)}</span>" for t in story.get("tags", []))
    ld = {
        "@context": "https://schema.org",
        "@type": "NewsArticle",
        "headline": title,
        "description": desc,
        "datePublished": lastmod(story.get("pub_date")),
        "author": {"@type": "Organization", "name": "Bot Kudos", "url": SITE},
        "publisher": {"@type": "Organization", "name": "Bot Kudos", "url": SITE},
        "mainEntityOfPage": canonical,
    }
    page = template
    page = page.replace("__TITLE__", html.escape(title))
    page = page.replace("__META_DESC__", html.escape(desc, quote=True))
    page = page.replace("__CANONICAL__", canonical)
    page = page.replace("__CATEGORY__", html.escape(story.get("category", "AI Fails")))
    page = page.replace("__KUDOS_LEVEL__", kudos_badge_html(story))
    page = page.replace("__DATE__", html.escape(pub_label(story.get("pub_date"))))
    page = page.replace("__SUMMARY_HTML__", summary_html)
    page = page.replace("__SOURCE_NAME__", html.escape(story.get("source_name", "Source")))
    page = page.replace("__SOURCE_URL__", html.escape(story.get("source_url", SITE), quote=True))
    page = page.replace("__TAGS_HTML__", tags_html)
    page = page.replace("__JSON_LD__", json.dumps(ld, ensure_ascii=False))
    page = page.replace("__PREV_LINK__", prev_link)
    page = page.replace("__NEXT_LINK__", next_link)
    return page


def main():
    stories = json.loads((ROOT / "stories.json").read_text(encoding="utf-8"))
    template = (ROOT / "template.html").read_text(encoding="utf-8")
    story_tpl = (ROOT / "story_template.html").read_text(encoding="utf-8")

    # Slugs first: story pages, sitemap, share URLs, and static cards all need them.
    used = set()
    slugs = []
    for s in stories:
        if s.get("slug"):
            slug = s["slug"]
            used.add(slug)
        else:
            slug = slugify(s.get("title", ""), used)
        slugs.append(slug)
    for story, slug in zip(stories, slugs):
        story["url"] = f"{SITE}/kudos/{slug}/"

    # Main page: embed stories as data, exactly as before.
    blob = base64.b64encode(
        json.dumps(stories, indent=1, ensure_ascii=False).encode("utf-8")
    ).decode("ascii")
    assert template.count("__STORIES_B64__") == 1, "template placeholder missing"
    assert template.count("__STATIC_CARDS__") == 1, "static cards placeholder missing"
    assert template.count("__SITE_SHARE_POP__") == 1, "site share placeholder missing"
    page = template.replace("__STORIES_B64__", blob)
    first_chunk = stories[:PER_PAGE]
    static_cards = "".join(
        card_html(story, i, len(first_chunk), 0)
        for i, story in enumerate(first_chunk)
    )
    page = page.replace("__STATIC_CARDS__", static_cards)
    page = page.replace("__SITE_SHARE_POP__",
                        share_pop_items("Bot Kudos", SITE + "/", SITE_SHARE_TEXT))
    (ROOT / "index.html").write_text(page, encoding="utf-8")

    # Per-story static pages.
    urls = []
    for i, story in enumerate(stories):
        slug = slugs[i]
        prev_link = (f'<a href="/kudos/{slugs[i - 1]}/">&larr; Newer kudos</a>'
                     if i > 0 else "")
        next_link = (f'<a href="/kudos/{slugs[i + 1]}/">Older kudos &rarr;</a>'
                     if i < len(stories) - 1 else "")
        out = ROOT / "kudos" / slug / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(
            build_story_page(story, slug, prev_link, next_link, story_tpl),
            encoding="utf-8")
        urls.append((f"{SITE}/kudos/{slug}/", lastmod(story.get("pub_date"))))

    # Sitemap.
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
             f"  <url><loc>{SITE}/</loc><lastmod>{TODAY}</lastmod>"
             "<changefreq>daily</changefreq></url>"]
    for loc, lm in urls:
        lines.append(f"  <url><loc>{loc}</loc><lastmod>{lm}</lastmod></url>")
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # robots.txt.
    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n",
        encoding="utf-8")

    # RSS feed: every story, newest first.
    feed = ['<?xml version="1.0" encoding="UTF-8"?>',
            '<rss version="2.0">',
            "<channel>",
            "<title>Bot Kudos</title>",
            f"<link>{SITE}/</link>",
            "<description>Tech wins, quiet heroics, and innovation doing good "
            "in the world, collected while the logs are still warm.</description>",
            "<language>en-us</language>",
            f"<lastBuildDate>{format_datetime(datetime.now(timezone.utc))}"
            "</lastBuildDate>"]
    for story in stories:
        try:
            level_num = int(story.get("kudos_level"))
        except (TypeError, ValueError):
            level_num = None
        level = KUDOS_LEVELS.get(level_num, "")
        feed.append("<item>")
        feed.append(f"<title>{html.escape(story.get('title', ''), quote=False)}</title>")
        feed.append(f"<link>{story['url']}</link>")
        feed.append(f"<guid>{story['url']}</guid>")
        feed.append(f"<pubDate>{rss_pubdate(story.get('pub_date'))}</pubDate>")
        feed.append(f"<category>{html.escape(story.get('category', ''), quote=False)}</category>")
        feed.append(f"<description><![CDATA[{rss_cdata(story.get('summary', ''))} "
                    f"(Kudos level {story.get('kudos_level')}: {level}.)]]></description>")
        feed.append("</item>")
    feed += ["</channel>", "</rss>"]
    (ROOT / "feed.xml").write_text("\n".join(feed) + "\n", encoding="utf-8")

    print(f"built index.html with {len(stories)} stories, "
          f"{len(urls)} story pages, sitemap.xml, robots.txt, feed.xml")


if __name__ == "__main__":
    main()
