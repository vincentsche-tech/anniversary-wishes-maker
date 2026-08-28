#!/usr/bin/env python3
"""
Add FAQPage JSON-LD to anniversary-wishes-maker pages that have a visible FAQ
card but no structured data.

Key correctness rule: Google requires the FAQPage JSON-LD text to match the
visible FAQ text VERBATIM. Every page here already has a hand-written,
page-specific visible FAQ card (e.g. 30th page -> "traditional pearl gift").
So we EXTRACT the existing Q/A from the visible card and emit a matching
JSON-LD — we never overwrite the card or invent generic questions.

- Idempotent: skips pages that already have a FAQPage JSON-LD.
- Fallback: if a page somehow has no visible card, generate a generic one
  (both JSON-LD + card) from faq_data() so the pair still matches.
- Insertion: JSON-LD before </head>. Card (only in fallback) before </main>.
"""
import re, os, json, sys, html

ROOT = "."
TARGETS = [
    '20th-anniversary-wishes.html',
    '30th-anniversary-wishes.html',
    'anniversary-wishes-for-boyfriend.html',
    'anniversary-wishes-for-couple.html',
    'anniversary-wishes-for-friend.html',
    'anniversary-wishes-for-girlfriend.html',
    'anniversary-wishes-for-husband.html',
    'anniversary-wishes-for-parents.html',
    'anniversary-wishes-for-wife.html',
    'funny-anniversary-wishes.html',
    'religious-anniversary-wishes.html',
    'romantic-anniversary-wishes.html',
    'short-anniversary-wishes.html',
    'wedding-anniversary-wishes.html',
    'work-anniversary-wishes.html',
]


def strip_tags(s):
    return re.sub(r'<[^>]+>', '', s)


def clean(s):
    return re.sub(r'\s+', ' ', html.unescape(strip_tags(s))).strip()


def extract_visible_faq(c):
    """Return list of (question, answer) from the visible FAQ card, or None."""
    m = re.search(r'<h2>Frequently Asked Questions</h2>(.*?)</main>', c, re.S)
    if not m:
        return None
    section = m.group(1)
    items = re.findall(
        r'<div class="faq-item"><b>(.*?)</b><p>(.*?)</p></div>', section, re.S
    )
    if not items:
        return None
    return [(clean(q), clean(a)) for q, a in items]


def derive_theme(fn):
    base = fn[:-5]
    if base.endswith('-anniversary-wishes'):
        head = base[:-len('-anniversary-wishes')]
        if head in ('funny', 'romantic', 'short', 'religious'):
            return f"{head} anniversary wishes"
        if head == 'wedding':
            return "wedding anniversary wishes"
        if head == 'work':
            return "work anniversary wishes"
        return f"{head} anniversary wishes"
    if base.startswith('anniversary-wishes-for-'):
        rel = base[len('anniversary-wishes-for-'):]
        rel_map = {
            'friend': 'friends', 'wife': 'your wife', 'husband': 'your husband',
            'couple': 'a couple', 'parents': 'your parents',
            'boyfriend': 'your boyfriend', 'girlfriend': 'your girlfriend',
        }
        return f"anniversary wishes for {rel_map.get(rel, rel)}"
    return "anniversary wishes"


def generic_faq(theme):
    return [
        (f"What should I write in {theme}?",
         "Keep it personal. Name the milestone, say what the year meant, and end with a wish for the year ahead. Short and sincere beats long and generic."),
        (f"How do I make {theme} sound heartfelt?",
         "Use a specific memory and the word \"love.\" Something like \"Another year with you is still my favorite thing\" works far better than a generic \"happy anniversary.\""),
        (f"What are some short {theme} I can copy?",
         "Try \"Happy anniversary — still my favorite person,\" \"Another year, same crush on you,\" or \"Cheers to us.\" Each is under ten words and ready to send."),
        (f"Should I post {theme} on social media?",
         "Yes. A public post with a photo and a short caption doubles as a keepsake and lets family join in. Pair it with a unique hashtag so the memory stays easy to find."),
    ]


def build_json(items):
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in items
        ],
    }
    return json.dumps(data, indent=2, ensure_ascii=False)


def build_card(items):
    parts = ['  <h2>Frequently Asked Questions</h2>']
    for q, a in items:
        parts.append(f'  <div class="faq-item"><b>{q}</b><p>{a}</p></div>')
    return "\n".join(parts)


def process(fn, dry):
    path = os.path.join(ROOT, fn)
    if not os.path.exists(path):
        print(f"MISSING: {fn}")
        return False
    c = open(path, encoding='utf-8').read()
    if '"@type": "FAQPage"' in c:
        print(f"SKIP (has FAQPage JSON-LD): {fn}")
        return False

    existing = extract_visible_faq(c)
    if existing:
        items = existing
        json_block = f'  <script type="application/ld+json">\n{build_json(items)}\n  </script>\n'
        new = c.replace('</head>', json_block + '</head>', 1)
        mode = f"extracted {len(items)} Q/A from visible card"
    else:
        # Fallback: no visible card -> generate both (kept for completeness)
        items = generic_faq(derive_theme(fn))
        json_block = f'  <script type="application/ld+json">\n{build_json(items)}\n  </script>\n'
        card_block = build_card(items)
        new = c.replace('</head>', json_block + '</head>', 1)
        new = new.replace('</main>', card_block + '\n</main>', 1)
        mode = f"generated generic {len(items)} Q/A (no existing card)"

    if dry:
        print(f"[dry] would add FAQPage JSON-LD to {fn} ({mode})")
        return False
    open(path, 'w', encoding='utf-8').write(new)
    print(f"ADDED FAQ JSON-LD: {fn} ({mode})")
    return True


if __name__ == '__main__':
    dry = '--dry' in sys.argv
    changed = 0
    for fn in TARGETS:
        if process(fn, dry):
            changed += 1
    print(f"\nDone. {'[dry-run] ' if dry else ''}Pages changed: {changed}/{len(TARGETS)}")
