#!/usr/bin/env python3
"""
P0 title CTR tune for anniversary-wishes-maker.

Scope corrected from the original plan using real GSC + GA4 data: the 5 pages
with the highest impressions AND best positions (the ones that actually get
seen in SERPs but get 0 clicks):
  - 30th (pos 8, 4 imp)   <- best position, 0 click
  - wedding (pos 10, 1 imp) <- best position, 0 click
  - 50th (pos 35.9, 13 imp) <- high imp, 2nd-page edge
  - 25th (pos 56.9, 18 imp) <- highest imp on the site
  - 1st (pos 53.6, 15 imp) <- 2nd highest imp

Changes:
  - bump "30+" -> "50+" (stronger number, better CTR)
  - append "& Quotes" synonym to capture the "anniversary quotes" query space
  - keep en-dash, keep title/og:title/twitter:title in sync (verified identical)
  - meta DESCRIPTION is intentionally left untouched (already compliant + on-voice)

Idempotent: skips if the new title is already present.
"""
import os, sys

ROOT = "."
TITLE_FIX = {
    '30th-anniversary-wishes.html': (
        '30th Anniversary Wishes – 30+ Messages for Three Decades',
        '30th Anniversary Wishes – 50+ Heartfelt Messages & Quotes',
    ),
    'wedding-anniversary-wishes.html': (
        'Wedding Anniversary Wishes – 40+ Heartfelt Messages',
        'Wedding Anniversary Wishes – 50+ Heartfelt Messages & Quotes',
    ),
    '50th-anniversary-wishes.html': (
        '50th Anniversary Wishes – 30+ Golden Messages',
        '50th Anniversary Wishes – 50+ Golden Messages & Quotes',
    ),
    '25th-anniversary-wishes.html': (
        '25th Anniversary Wishes – 30+ Silver Messages',
        '25th Anniversary Wishes – 50+ Silver Messages & Quotes',
    ),
    '1st-anniversary-wishes.html': (
        '1st Anniversary Wishes – 30+ Sweet Messages for Year One',
        '1st Anniversary Wishes – 50+ Sweet Messages for Year One',
    ),
}


def process(fn, dry):
    path = os.path.join(ROOT, fn)
    if not os.path.exists(path):
        print(f"MISSING: {fn}")
        return False
    c = open(path, encoding='utf-8').read()
    old, new = TITLE_FIX[fn]
    if new in c:
        print(f"SKIP (already applied): {fn}")
        return False
    if old not in c:
        print(f"WARN old title NOT FOUND in {fn} — skipping")
        return False
    new_c = c
    new_c = new_c.replace(f'<title>{old}</title>', f'<title>{new}</title>', 1)
    new_c = new_c.replace(
        f'<meta property="og:title" content="{old}">',
        f'<meta property="og:title" content="{new}">', 1)
    new_c = new_c.replace(
        f'<meta name="twitter:title" content="{old}">',
        f'<meta name="twitter:title" content="{new}">', 1)
    if dry:
        print(f"[dry] {fn}: {old}  ->  {new}")
        return False
    open(path, 'w', encoding='utf-8').write(new_c)
    print(f"FIXED {fn}: {old}  ->  {new}")
    return True


if __name__ == '__main__':
    dry = '--dry' in sys.argv
    changed = 0
    for fn in TITLE_FIX:
        if process(fn, dry):
            changed += 1
    print(f"\nDone. {'[dry-run] ' if dry else ''}Pages changed: {changed}/{len(TITLE_FIX)}")
