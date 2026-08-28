#!/usr/bin/env python3
"""
P1: thicken the 3 highest-impression anniversary pages from ~650 to 850+ words.

Targets (GSC 28d impressions):
  - 25th (18 imp, pos 56.9)  -> silver anniversary
  - 1st  (15 imp, pos 53.6)  -> paper anniversary
  - 50th (13 imp, pos 35.9)  -> golden anniversary

Each page gets 3 page-aware `.card guide` sections (~250 words total) inserted
BEFORE the "More Anniversary Wishes" nav card, so the reading order stays:
  wishes -> how-to -> meaning -> NEW GUIDE -> more-links -> FAQ

Content is page-aware (silver / paper / gold, quarter century / first year /
half century) so the three pages are not near-duplicates of each other.

Idempotent: skips if `card guide` already present. Supports --dry.
"""
import re, os, sys, html

ROOT = "."
GUIDE_CSS = """
  .card.guide p{margin-bottom:12px;line-height:1.75;}
  .card.guide ul{margin-left:20px;margin-bottom:12px;}
  .card.guide li{margin-bottom:6px;}"""

# page -> (ordinal, milestone phrase, traditional gift, gift-detail sentence)
PAGE_DATA = {
    '25th-anniversary-wishes.html': (
        '25th', 'a quarter century', 'silver',
        'A silver frame holding a photo from the wedding day is a classic that always lands.',
    ),
    '1st-anniversary-wishes.html': (
        '1st', 'your first year', 'paper',
        'A handwritten letter on good paper, or a framed photo from year one, both fit the theme.',
    ),
    '50th-anniversary-wishes.html': (
        '50th', 'half a century', 'gold',
        'Gold jewelry, a gold-framed photo, or a golden keepsake box all mark the moment well.',
    ),
}


def guide_sections(ordinal, milestone, gift, gift_detail):
    """Return list of (h2, [paragraphs]) — page-aware long-form content."""
    return [
        (
            f"How to Choose the Right {ordinal} Anniversary Message",
            [
                f"Picking the right words starts with the relationship. For your spouse, lean romantic and specific — name the year and say what it taught you. For parents or a couple you know well, warm and admiring works best. For friends, keep it light and celebratory.",
                f"{milestone.capitalize()} together is a real milestone, so let the message sound like you. Shorten any wish on this page until it fits your own voice — a sincere sentence in your words beats a beautiful paragraph in someone else's.",
            ],
        ),
        (
            f"Pairing Your {ordinal} Wish With the Traditional {gift.capitalize()} Gift",
            [
                f"The traditional {ordinal} anniversary gift is {gift}, and one short wish turns it into a keepsake. Slip a note into the gift box, write a line inside the card, or read it aloud just before handing the gift over.",
                f"{gift_detail} Even a single sincere sentence carries weight when the gift itself already says the rest.",
            ],
        ),
        (
            f"How to Deliver Your {ordinal} Anniversary Wish",
            [
                f"Delivery matters as much as wording. A handwritten card suits a milestone like this and tends to get kept for years. A text works when you want it read the moment it lands.",
                f"A social post lets friends and family join the celebration — pair it with a short caption and one good photo. If you can say it in person, do that first, then follow up in writing so the words survive the day.",
            ],
        ),
    ]


def build_guide_html(ordinal, milestone, gift, gift_detail):
    parts = []
    for h2, paras in guide_sections(ordinal, milestone, gift, gift_detail):
        inner = "\n".join(f"    <p>{p}</p>" for p in paras)
        parts.append(f'  <div class="card guide">\n    <h2>{h2}</h2>\n{inner}\n  </div>\n')
    return "\n".join(parts)


def word_count(c):
    body = re.sub(r'<script.*?</script>', '', c, flags=re.S)
    body = re.sub(r'<style.*?</style>', '', body, flags=re.S)
    txt = html.unescape(re.sub(r'<[^>]+>', ' ', body))
    return len(re.sub(r'\s+', ' ', txt).strip().split())


def process(fn, dry):
    path = os.path.join(ROOT, fn)
    if not os.path.exists(path):
        print(f"MISSING: {fn}")
        return False
    c = open(path, encoding='utf-8').read()
    if 'card guide' in c:
        print(f"SKIP (already thickened): {fn}")
        return False
    ordinal, milestone, gift, gift_detail = PAGE_DATA[fn]

    # Anchor: insert immediately BEFORE the card containing "More Anniversary Wishes"
    try:
        idx = c.index('More Anniversary Wishes')
        start = c.rindex('<div class="card">', 0, idx)
    except ValueError:
        print(f"WARN anchor not found in {fn} — skipping")
        return False

    before = word_count(c)
    guide_html = build_guide_html(ordinal, milestone, gift, gift_detail)
    new = c[:start] + guide_html + c[start:]
    if '.card.guide' not in new:
        new = new.replace('</style>', GUIDE_CSS + '\n</style>', 1)
    after = word_count(new)

    if dry:
        print(f"[dry] {fn}: {before} -> {after} words (+{after - before})")
        return False
    open(path, 'w', encoding='utf-8').write(new)
    print(f"THICKENED {fn}: {before} -> {after} words (+{after - before})")
    return True


if __name__ == '__main__':
    dry = '--dry' in sys.argv
    changed = 0
    for fn in PAGE_DATA:
        if process(fn, dry):
            changed += 1
    print(f"\nDone. {'[dry-run] ' if dry else ''}Pages changed: {changed}/{len(PAGE_DATA)}")
