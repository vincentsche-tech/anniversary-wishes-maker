#!/usr/bin/env python3
"""
Wire the new /anniversary-card-messages.html page into the site:

1. Insert an internal link into the "More Anniversary Wishes" grid of every
   content page that has one, plus the index grid. The site's existing pattern
   is that each page's grid lists the sibling content pages, so the new page
   gets the same treatment (and is reachable from anywhere).
2. Append the new URL to sitemap.xml.

Both steps are idempotent (skip if the link / URL already present) and support
--dry.

Note: per the GSC red line, adding a page does NOT mean resubmitting the
sitemap — it is a dynamic sitemap and Google picks it up on the next read.
"""
import re, os, sys

ROOT = "."
NEW_SLUG = "anniversary-card-messages.html"
NEW_CARD = (
    '\n      <a class="scene-card" href="/%s">'
    '<b>💌 Card Messages</b><span>Short lines to write in a card.</span></a>' % NEW_SLUG
)
# grid that sits directly under the "More Anniversary Wishes" heading
GRID_RE = re.compile(
    r'(<h2>More Anniversary Wishes</h2>\s*<div class="grid"[^>]*>\s*<a class="scene-card".*?</a>)',
    re.S,
)
INDEX_GRID_RE = re.compile(r'(<div class="grid"[^>]*>\s*<a class="scene-card".*?</a>)', re.S)


def link_targets():
    """Content pages that own a 'More Anniversary Wishes' grid, plus index.html."""
    out = []
    for fn in sorted(f for f in os.listdir(ROOT) if f.endswith('.html')):
        if fn == NEW_SLUG:
            continue
        c = open(os.path.join(ROOT, fn), encoding='utf-8').read()
        if 'More Anniversary Wishes' in c or (fn == 'index.html' and 'scene-card' in c):
            out.append(fn)
    return out


def add_link(fn, dry):
    path = os.path.join(ROOT, fn)
    c = open(path, encoding='utf-8').read()
    if 'href="/%s"' % NEW_SLUG in c:
        print(f"SKIP (already linked): {fn}")
        return False
    m = GRID_RE.search(c)
    if not m and fn == 'index.html':
        m = INDEX_GRID_RE.search(c)
    if not m:
        print(f"WARN no grid anchor in {fn} — skipping")
        return False
    new = c[:m.end(1)] + NEW_CARD + c[m.end(1):]
    if dry:
        print(f"[dry] would add link in {fn}")
        return False
    open(path, 'w', encoding='utf-8').write(new)
    print(f"LINKED: {fn}")
    return True


def add_sitemap(dry):
    path = os.path.join(ROOT, 'sitemap.xml')
    c = open(path, encoding='utf-8').read()
    if NEW_SLUG in c:
        print("SKIP (already in sitemap)")
        return False
    entry = (
        '<url><loc>https://www.anniversarywishesmaker.com/%s</loc>'
        '<lastmod>2026-08-28</lastmod><changefreq>monthly</changefreq>'
        '<priority>0.7</priority></url>\n' % NEW_SLUG
    )
    new = c.replace('</urlset>', entry + '</urlset>', 1)
    if dry:
        print("[dry] would add sitemap entry")
        return False
    open(path, 'w', encoding='utf-8').write(new)
    print("SITEMAP: entry added")
    return True


if __name__ == '__main__':
    dry = '--dry' in sys.argv
    changed = 0
    for fn in link_targets():
        if add_link(fn, dry):
            changed += 1
    if add_sitemap(dry):
        changed += 1
    print(f"\nDone. {'[dry-run] ' if dry else ''}Files changed: {changed}")
