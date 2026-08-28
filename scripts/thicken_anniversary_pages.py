#!/usr/bin/env python3
"""
P1: thicken high-impression anniversary pages to 800+ words.

Two content archetypes, because the pages are not interchangeable:
  - 'year' pages (1st/10th/25th/30th/50th): milestone + TRADITIONAL GIFT angle
    (paper / tin / silver / pearl / gold).
  - 'relation' pages (for-friend): no gift-year logic exists for a friend, so the
    middle section becomes "what to skip when writing to a friend" instead.

Each page gets 3 page-aware `.card guide` sections inserted BEFORE the
"More Anniversary Wishes" nav card, keeping reading order:
  wishes -> how-to -> meaning -> NEW GUIDE -> more-links -> FAQ

All copy is page-aware so pages never read as near-duplicates of each other.
Idempotent: skips if `card guide` already present. Supports --dry (prints
before -> after word counts so shortfalls are caught before writing).
"""
import re, os, sys, html

ROOT = "."
GUIDE_CSS = """
  .card.guide p{margin-bottom:12px;line-height:1.75;}
  .card.guide ul{margin-left:20px;margin-bottom:12px;}
  .card.guide li{margin-bottom:6px;}"""

# fn -> (archetype, data dict)
# Already thickened 2026-08-28: 25th / 1st / 50th (kept here as the site record;
# idempotence skips them because they already contain `card guide`).
PAGE_DATA = {
    '25th-anniversary-wishes.html': ('year', {
        'ordinal': '25th', 'milestone': 'a quarter century', 'gift': 'silver',
        'gift_detail': 'A silver frame holding a photo from the wedding day is a classic that always lands.',
    }),
    '1st-anniversary-wishes.html': ('year', {
        'ordinal': '1st', 'milestone': 'your first year', 'gift': 'paper',
        'gift_detail': 'A handwritten letter on good paper, or a framed photo from year one, both fit the theme.',
    }),
    '50th-anniversary-wishes.html': ('year', {
        'ordinal': '50th', 'milestone': 'half a century', 'gift': 'gold',
        'gift_detail': 'Gold jewelry, a gold-framed photo, or a golden keepsake box all mark the moment well.',
    }),
    '10th-anniversary-wishes.html': ('year', {
        'ordinal': '10th', 'milestone': 'ten years', 'gift': 'tin',
        'gift_detail': 'A tin picture frame, a set of aluminium coasters, or anything built to last another decade fits the theme.',
    }),
    '30th-anniversary-wishes.html': ('year', {
        'ordinal': '30th', 'milestone': 'thirty years', 'gift': 'pearl',
        'gift_detail': 'Pearl jewelry, a pearl-inlaid frame, or a keepsake box all carry the symbolism well.',
    }),
    'anniversary-wishes-for-friend.html': ('relation', {
        'relation': 'friend',
    }),
}


def year_sections(d):
    o, m, g, gd = d['ordinal'], d['milestone'], d['gift'], d['gift_detail']
    return [
        (
            f"How to Choose the Right {o} Anniversary Message",
            [
                "Picking the right words starts with who you are writing to. For your spouse, lean romantic and specific — name the year and say what it taught you. For parents or a couple you know well, warm and admiring works better than playful.",
                f"{m.capitalize()} together is a real milestone, so let the message sound like you. Shorten any wish on this page until it fits your own voice — one sincere sentence in your words beats a polished paragraph in someone else's.",
            ],
        ),
        (
            f"Pairing Your {o} Wish With the Traditional {g.capitalize()} Gift",
            [
                f"The traditional {o} anniversary gift is {g}, and a short wish turns it into a keepsake. Slip a note into the gift box, write one line inside the card, or read it aloud just before handing the gift over.",
                f"{gd} A gift already carries meaning, so keep the words short — two or three lines is plenty when the present says the rest.",
            ],
        ),
        (
            f"How to Deliver Your {o} Anniversary Wish",
            [
                "Delivery matters as much as wording. A handwritten card suits a milestone like this and tends to get kept for years. A text works when you want it read the moment it lands, especially if you are apart that day.",
                "A social post lets friends and family join the celebration — pair a short caption with one good photo. If you can say it in person, do that first, then follow up in writing so the words outlive the day.",
            ],
        ),
    ]


def relation_sections(d):
    return [
        (
            "How to Choose the Right Anniversary Wish for a Friend",
            [
                "Writing to a friend is different from writing to a partner — the tone stays warm but light. Match the message to how close you are: a long shared history can carry an inside joke, while a newer friendship reads better with something simple and warm.",
                "If you know the couple well, mention them both by name and reference the year. If you mostly know one of them, keep it about their happiness rather than details you were not there for.",
            ],
        ),
        (
            "What to Skip When Writing to a Friend",
            [
                "Two things trip people up. The first is going too romantic — language that suits a spouse can feel odd coming from a friend, so save the deep declarations for your own partner.",
                "The second is going too generic. A message that could be sent to anyone reads like filler. One specific detail — the year, a shared memory, the way they are together — is what makes a friend's anniversary wish actually land.",
            ],
        ),
        (
            "How to Deliver Your Wish to a Friend",
            [
                "A text or a message in the group chat works well for friends and gets read right away, which is usually what you want on the day itself.",
                "If you want something they will keep, a short card or a note tucked inside a gift does that better. Posting publicly is fine too — just keep the caption warm and avoid sharing details they might not want online.",
            ],
        ),
    ]


def guide_sections(archetype, data):
    return year_sections(data) if archetype == 'year' else relation_sections(data)


def build_guide_html(archetype, data):
    parts = []
    for h2, paras in guide_sections(archetype, data):
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
    archetype, data = PAGE_DATA[fn]

    # Anchor: insert immediately BEFORE the card containing "More Anniversary Wishes"
    try:
        idx = c.index('More Anniversary Wishes')
        start = c.rindex('<div class="card">', 0, idx)
    except ValueError:
        print(f"WARN anchor not found in {fn} — skipping")
        return False

    before = word_count(c)
    guide_html = build_guide_html(archetype, data)
    new = c[:start] + guide_html + c[start:]
    if '.card.guide' not in new:
        new = new.replace('</style>', GUIDE_CSS + '\n</style>', 1)
    after = word_count(new)
    flag = "" if after >= 800 else "  <-- UNDER 800"

    if dry:
        print(f"[dry] {fn}: {before} -> {after} words (+{after - before}){flag}")
        return False
    open(path, 'w', encoding='utf-8').write(new)
    print(f"THICKENED {fn}: {before} -> {after} words (+{after - before}){flag}")
    return True


if __name__ == '__main__':
    dry = '--dry' in sys.argv
    changed = 0
    for fn in PAGE_DATA:
        if process(fn, dry):
            changed += 1
    print(f"\nDone. {'[dry-run] ' if dry else ''}Pages changed: {changed}/{len(PAGE_DATA)}")
