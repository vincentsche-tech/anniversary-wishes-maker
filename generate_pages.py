#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Anniversary 站内容页生成：从 wordbank.json 渲染 10 个页面"""
import json, os

BASE = '/sandbox/workspace/anniversary-site'
DOMAIN = 'https://anniversarywishesmaker.com'
GA_TAG = 'G-XXXXXXXXXX'  # TODO: 替换为新 GA4 Measurement ID

wb = json.load(open(f'{BASE}/wordbank.json', encoding='utf-8'))

GA4 = f'''<script async src="https://www.googletagmanager.com/gtag/js?id={GA_TAG}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{GA_TAG}');
</script>'''

TONE_META = {
    'romantic': ('🥰 Romantic', 'Heartfelt messages for the one you love.'),
    'funny': ('😂 Funny', "Playful wishes that'll make them smile."),
    'short': ('📝 Short & Sweet', 'Quick, meaningful messages for cards and texts.'),
    'religious': ('🙏 Religious', 'Faith-centered wishes for couples who share their faith.'),
}

PAGES = [
    {
        'slug': 'anniversary-wishes-for-husband',
        'h1': 'Anniversary Wishes for Husband',
        'title': 'Anniversary Wishes for Husband – 30+ Romantic & Funny Messages',
        'desc': 'Find the perfect anniversary wish for your husband — romantic, funny, short, and religious messages he will love.',
        'data': 'husband',
        'intro': 'Your husband deserves to know how much he means to you. These wishes range from deeply romantic to playfully funny — pick the one that sounds like you, then add a personal memory.',
        'faq': [
            ('What should I write to my husband for our anniversary?',
             'Start with what he means to you: "Happy anniversary to my husband, my best friend, and my favorite person." Add one specific memory from your years together — that personal touch makes it unforgettable.'),
            ('Should I write a funny or romantic anniversary message for my husband?',
             'It depends on his sense of humor! If he loves jokes, a funny message like "thanks for not running away" lands perfectly. If he is sentimental, go romantic. Many couples mix both.'),
            ('How do I make my anniversary message special?',
             'Name the milestone ("5 years!"), mention an inside joke or memory, and say something specific about why you love him. Specific beats generic every time.'),
        ],
    },
    {
        'slug': 'anniversary-wishes-for-wife',
        'h1': 'Anniversary Wishes for Wife',
        'title': 'Anniversary Wishes for Wife – 30+ Romantic & Sweet Messages',
        'desc': 'Find the perfect anniversary wish for your wife — romantic, funny, short, and religious messages that show how much you love her.',
        'data': 'wife',
        'intro': 'Your wife is your partner, your home, your best friend. These wishes celebrate her and the life you have built together. Choose the one that sounds like you, then add your own touch.',
        'faq': [
            ('What is a romantic anniversary message for my wife?',
             '"To my wife, my partner, my home: happy anniversary. Loving you is the greatest privilege of my life." Add a memory — the day you met, your wedding, a favorite trip — to make it yours.'),
            ('What should I write in an anniversary card for my wife?',
             'Open with how much she means to you, mention one specific thing you love about her, name the milestone, and close with love. Handwritten is always a bonus.'),
            ('How can I make my wife feel special on our anniversary?',
             'Pair a heartfelt message with a small gesture — her favorite flowers, a playlist of your songs, or recreating your first date. The message and the gesture together are magic.'),
        ],
    },
    {
        'slug': 'anniversary-wishes-for-couple',
        'h1': 'Anniversary Wishes for a Couple',
        'title': 'Anniversary Wishes for a Couple – 30+ Heartfelt Messages',
        'desc': 'Celebrate a couple you love with these anniversary wishes — romantic, funny, short, and religious messages for friends and family.',
        'data': 'couple',
        'intro': 'When friends or family celebrate an anniversary, a warm message shows you see and honor their love. These wishes work for any couple you care about.',
        'faq': [
            ('What do you write to a couple on their anniversary?',
             '"Happy anniversary to a couple whose love inspires everyone around them." Add something specific — a quality you admire about them as a couple, or a memory you share.'),
            ('What should I write in an anniversary card for friends?',
             'Keep it warm and personal: congratulate them, mention something you admire about their relationship, and wish them many more years of happiness together.'),
            ('Is it okay to send a funny anniversary message to a couple?',
             'Yes, if you know they will laugh! Funny wishes work great for close friends. Just make sure it celebrates them — the joke should be warm, not at anyone\'s expense.'),
        ],
    },
    {
        'slug': 'anniversary-wishes-for-parents',
        'h1': 'Anniversary Wishes for Parents',
        'title': 'Anniversary Wishes for Parents – 30+ Heartfelt Messages',
        'desc': 'Celebrate Mom and Dad\'s anniversary with these heartfelt wishes — messages that honor their love and the family they built.',
        'data': 'parents',
        'intro': 'Your parents\' anniversary is a celebration of the love that built your family. These wishes honor their journey and the example they have set for you.',
        'faq': [
            ('What should I write to my parents on their anniversary?',
             'Thank them for their example: "Happy anniversary to the couple who taught me what love looks like." Mention something specific you appreciate about their marriage.'),
            ('How do I write a meaningful anniversary message for Mom and Dad?',
             'Acknowledge their milestone, thank them for building your family, and share a memory of them together. Specific gratitude is the most meaningful gift.'),
            ('What if I live far from my parents on their anniversary?',
             'A heartfelt text, video message, or mailed card all work. The distance matters less than the sincerity — make sure they know you are thinking of them.'),
        ],
    },
    {
        'slug': 'anniversary-wishes-for-friend',
        'h1': 'Anniversary Wishes for Friends',
        'title': 'Anniversary Wishes for Friends – 30+ Heartfelt Messages',
        'desc': 'Celebrate your friends\' anniversary with these wishes — romantic, funny, and short messages for the couples you love.',
        'data': 'friend',
        'intro': 'Friends are the family we choose — and celebrating their anniversary is celebrating their love story. These wishes are warm, fun, and perfect for any friendship.',
        'faq': [
            ('What do I write to friends on their anniversary?',
             '"Happy anniversary to two of my favorite people!" Add a warm wish for their love and a personal note — a memory or something you admire about them as a couple.'),
            ('Should I send a funny or heartfelt anniversary message to friends?',
             'Both work! Funny wishes are great for close friends. If you want to be safe, a warm and sincere message never misses.'),
        ],
    },
    {
        'slug': '1st-anniversary-wishes',
        'h1': '1st Anniversary Wishes',
        'title': '1st Anniversary Wishes – 30+ Sweet Messages for Year One',
        'desc': 'Celebrate the first anniversary with these sweet wishes — romantic, funny, short, and religious messages for the first year of forever.',
        'data': '1st',
        'intro': 'The first anniversary is special — the first year of forever, full of new memories. These wishes celebrate that beautiful beginning. (Traditional gift: paper, for the story you are starting to write.)',
        'faq': [
            ('What should I write for a 1st anniversary?',
             '"One year down, forever to go. Happy 1st anniversary, my love!" Add a memory from your first year of marriage — the first home, the first trip, the little routines.'),
            ('What is the traditional 1st anniversary gift?',
             'Paper is the traditional 1st anniversary gift — symbolizing the blank pages of your new story together. A handwritten letter fits perfectly.'),
        ],
    },
    {
        'slug': '25th-anniversary-wishes',
        'h1': '25th Anniversary Wishes (Silver)',
        'title': '25th Anniversary Wishes – 30+ Messages for the Silver Anniversary',
        'desc': 'Celebrate 25 years of marriage with these silver anniversary wishes — romantic, funny, short, and religious messages for a true milestone.',
        'data': '25th',
        'intro': 'Twenty-five years of marriage is a silver milestone — a quarter century of love, partnership, and shared memories. These wishes honor that remarkable journey.',
        'faq': [
            ('What should I write for a 25th anniversary?',
             'Name the milestone: "Happy 25th anniversary! A quarter century of love." Acknowledge the achievement and the love that made it possible.'),
            ('What is the traditional 25th anniversary gift?',
             'Silver — hence "silver anniversary." Silver jewelry, a silver frame with a photo of the couple, or a silver keepsake all work beautifully.'),
        ],
    },
    {
        'slug': '50th-anniversary-wishes',
        'h1': '50th Anniversary Wishes (Golden)',
        'title': '50th Anniversary Wishes – 30+ Messages for the Golden Anniversary',
        'desc': 'Celebrate 50 years of marriage with these golden anniversary wishes — romantic, funny, short, and religious messages for a once-in-a-lifetime milestone.',
        'data': '50th',
        'intro': 'Fifty years of marriage is a golden milestone — half a century of love, commitment, and memories. These wishes honor a truly extraordinary journey.',
        'faq': [
            ('What should I write for a 50th anniversary?',
             '"Happy 50th anniversary! Half a century of love, and your story is more beautiful than any fairy tale." Honor the achievement — 50 years together is extraordinary.'),
            ('What is the traditional 50th anniversary gift?',
             'Gold — hence "golden anniversary." Gold jewelry, a gold watch, or a gold-framed photo of the couple are classic choices.'),
        ],
    },
    {
        'slug': 'work-anniversary-wishes',
        'h1': 'Work Anniversary Wishes',
        'title': 'Work Anniversary Wishes – 30+ Professional & Friendly Messages',
        'desc': 'Find the perfect work anniversary wish — professional, friendly, and funny messages to celebrate a colleague\'s milestone.',
        'data': 'work',
        'intro': 'Work anniversaries matter — they celebrate dedication, growth, and contribution. These wishes work for colleagues, team members, bosses, and employees.',
        'faq': [
            ('What should I write in a work anniversary message?',
             'Acknowledge their years of service, mention a specific contribution, and wish them continued success: "Happy work anniversary! Your dedication inspires the whole team."'),
            ('Should a work anniversary message be formal or casual?',
             'It depends on your relationship. For colleagues and teammates, warm and friendly works. For bosses or in formal settings, keep it professional but sincere.'),
            ('What is a good funny work anniversary message?',
             '"Happy work anniversary! Thanks for showing up, showing out, and not showing up late too often." Funny messages work great for close colleagues.'),
        ],
    },

    {
        'slug': '5th-anniversary-wishes',
        'h1': '5th Anniversary Wishes',
        'title': '5th Anniversary Wishes – 30+ Sweet Messages for Five Years',
        'desc': 'Celebrate five years of marriage with these 5th anniversary wishes — romantic, funny, short, and religious messages.',
        'data': '5th',
        'intro': 'Five years of marriage is a beautiful milestone — the foundation is built, the adventure continues. These wishes celebrate half a decade of love.',
        'faq': [
            ('What should I write for a 5th anniversary?',
             '"Five years of building a life together, and I would choose you again every single time." Add a memory from your five years — your first home, a trip, a shared achievement.'),
            ('What is the traditional 5th anniversary gift?',
             'Wood is the traditional 5th anniversary gift — symbolizing the strength and roots of your relationship. Personalized wooden items are popular choices.'),
        ],
    },
    {
        'slug': '10th-anniversary-wishes',
        'h1': '10th Anniversary Wishes',
        'title': '10th Anniversary Wishes – 30+ Messages for a Decade of Love',
        'desc': 'Celebrate ten years of marriage with these 10th anniversary wishes — romantic, funny, short, and religious messages for a decade of love.',
        'data': '10th',
        'intro': 'Ten years of marriage is a true milestone — a decade of love, growth, and shared history. These wishes honor that beautiful journey.',
        'faq': [
            ('What should I write for a 10th anniversary?',
             '"Happy 10th anniversary! A decade of love, laughter, and growing together." Acknowledge the decade and the growth you have shared.'),
            ('What is the traditional 10th anniversary gift?',
             'Tin or aluminum is the traditional 10th anniversary gift — symbolizing flexibility and durability. Modern alternatives include diamond jewelry.'),
        ],
    },
    {
        'slug': 'wedding-anniversary-wishes',
        'h1': 'Wedding Anniversary Wishes',
        'title': 'Wedding Anniversary Wishes – 40+ Heartfelt Messages',
        'desc': 'The best wedding anniversary wishes for any couple — romantic, funny, short, and religious messages to celebrate their love story.',
        'data': 'couple',
        'intro': 'A wedding anniversary celebrates the day a couple promised forever. These wishes work for spouses, parents, friends, and family — for any milestone from year one to year fifty.',
        'faq': [
            ('What is a good wedding anniversary wish?',
             '"May your love continue to bloom with each passing year." Or keep it simple and sincere: "Happy anniversary! Here\'s to a lifetime of love."'),
            ('What is the difference between wedding anniversary and happy anniversary?',
             'They mean the same thing — "happy anniversary" is the common greeting, "wedding anniversary" names the occasion. Use them interchangeably.'),
            ('How do I wish a couple a happy wedding anniversary?',
             'Congratulate them, mention something you admire about their relationship, and wish them continued happiness. A personal memory makes it special.'),
        ],
    },
]

PAGE_TPL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{domain}/{slug}.html">
<meta name="theme-color" content="#b8860b">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E%F0%9F%A5%82%3C/text%3E%3C/svg%3E">
{ga4}
<style>
  :root{{--bg:#fdf9f2;--card:#fff;--ink:#3a362f;--muted:#8d8578;--accent:#b8860b;--accent-dark:#9a7209;--soft:#faf3e3;--line:#eee5d2;--radius:14px;--shadow:0 4px 20px rgba(58,54,47,.06);}}
  *{{margin:0;padding:0;box-sizing:border-box;}}
  body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;background:var(--bg);color:var(--ink);line-height:1.7;}}
  h1,h2,h3{{font-family:Georgia,"Times New Roman",serif;font-weight:700;letter-spacing:-.2px;}}
  header{{background:#fff;border-bottom:1px solid var(--line);padding:16px 0;}}
  header .inner{{max-width:960px;margin:0 auto;padding:0 20px;display:flex;align-items:center;gap:14px;flex-wrap:wrap;}}
  .logo{{background:var(--accent);color:#fff;font-family:Georgia,serif;font-size:15px;font-weight:700;padding:7px 14px;border-radius:8px;text-decoration:none;}}
  nav.topnav{{margin-left:auto;display:flex;gap:16px;flex-wrap:wrap;}}
  nav.topnav a{{color:var(--muted);font-size:14px;text-decoration:none;}}
  nav.topnav a:hover{{color:var(--accent);}}
  main{{max-width:960px;margin:0 auto;padding:36px 20px 64px;}}
  .hero{{text-align:center;margin-bottom:28px;}}
  .hero h1{{font-size:31px;line-height:1.25;}}
  .hero p{{color:var(--muted);margin-top:12px;font-size:16px;max-width:640px;margin-left:auto;margin-right:auto;}}
  .card{{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);padding:28px;margin-bottom:24px;}}
  .card h2{{font-size:20px;margin-bottom:12px;}}
  .card h3{{font-size:17px;margin:20px 0 10px;}}
  .advice-box{{background:var(--soft);border-left:4px solid var(--accent);border-radius:0 10px 10px 0;padding:18px 20px;margin:16px 0;}}
  .advice-box h3{{font-size:16px;margin:0 0 8px;}}
  .advice-box ul{{margin-left:20px;}}
  .advice-box li{{margin-bottom:6px;font-size:14.5px;}}
  .msg-item{{display:flex;align-items:flex-start;gap:10px;background:var(--soft);border:1px solid var(--line);border-radius:12px;padding:14px 16px;margin-bottom:10px;}}
  .msg-text{{flex:1;font-size:15px;line-height:1.6;}}
  .msg-copy{{background:var(--accent);color:#fff;border:none;border-radius:8px;padding:6px 12px;font-size:12.5px;font-weight:600;cursor:pointer;white-space:nowrap;flex-shrink:0;}}
  .msg-copy.copied{{background:#c9a227;}}
  .grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:14px;}}
  .scene-card{{display:block;background:#fff;border:1px solid var(--line);border-radius:12px;padding:18px 20px;text-decoration:none;color:var(--ink);transition:all .15s;}}
  .scene-card:hover{{border-color:var(--accent);box-shadow:var(--shadow);}}
  .scene-card b{{font-size:15px;display:block;margin-bottom:4px;color:var(--accent-dark);}}
  .scene-card span{{font-size:13.5px;color:var(--muted);}}
  .faq-item{{margin-bottom:18px;}}
  .faq-item b{{display:block;margin-bottom:4px;font-size:15px;}}
  .faq-item p{{font-size:14.5px;color:#6b6356;}}
  footer{{text-align:center;color:var(--muted);font-size:13px;padding:28px 0 48px;border-top:1px solid var(--line);}}
  footer a{{color:var(--accent);text-decoration:none;}}
  .toast{{position:fixed;bottom:24px;left:50%;transform:translateX(-50%) translateY(80px);background:var(--ink);color:#fff;padding:10px 22px;border-radius:999px;font-size:14px;opacity:0;transition:all .3s;pointer-events:none;z-index:99;}}
  .toast.show{{opacity:1;transform:translateX(-50%) translateY(0);}}
  @media(max-width:600px){{.hero h1{{font-size:25px;}}}}
</style>
</head>
<body>
<header>
  <div class="inner">
    <a class="logo" href="/">🥂 Anniversary Wishes</a>
    <nav class="topnav">
      <a href="/">Generator</a>
      <a href="/anniversary-wishes-for-husband.html">For Husband</a>
      <a href="/anniversary-wishes-for-wife.html">For Wife</a>
      <a href="/anniversary-wishes-for-couple.html">For Couple</a>
      <a href="/work-anniversary-wishes.html">Work</a>
      <a href="/about.html">About</a>
    </nav>
  </div>
</header>

<main>
  <div class="hero">
    <h1>{h1}</h1>
    <p>{intro}</p>
  </div>

  <div class="card">
    <h2>💌 Ready-to-Use Anniversary Wishes</h2>
    <p style="font-size:14.5px;color:#6b6356;margin-bottom:16px;">Click any message to copy it, then add your own personal touch.</p>
{tone_sections}
    <p style="margin-top:16px;font-size:14.5px;">Need something different? Use the <a href="/" style="color:var(--accent);">free anniversary wishes generator</a> — choose who it's for and a style, and get fresh wishes in seconds.</p>
  </div>

  <div class="card">
    <h2>How to Make These Wishes Yours</h2>
    <div class="advice-box">
      <h3>✅ The Personal Touch</h3>
      <ul>
        <li>Add a specific memory — the day you met, your first trip, a favorite tradition</li>
        <li>Name the milestone: "5 years!" or "A quarter century!"</li>
        <li>Mention one quality you genuinely admire in them</li>
        <li>Keep it in your own voice — sincerity beats perfection</li>
      </ul>
    </div>
  </div>

  <div class="card">
    <h2>More Anniversary Wishes</h2>
    <div class="grid">
      <a class="scene-card" href="/anniversary-wishes-for-husband.html"><b>For Husband</b><span>Romantic and funny wishes for your man.</span></a>
      <a class="scene-card" href="/anniversary-wishes-for-wife.html"><b>For Wife</b><span>Sweet messages for your wife.</span></a>
      <a class="scene-card" href="/anniversary-wishes-for-couple.html"><b>For a Couple</b><span>Wishes for friends and family couples.</span></a>
      <a class="scene-card" href="/anniversary-wishes-for-parents.html"><b>For Parents</b><span>Celebrate Mom and Dad's love.</span></a>
      <a class="scene-card" href="/1st-anniversary-wishes.html"><b>1st Anniversary</b><span>Messages for year one of forever.</span></a>
      <a class="scene-card" href="/25th-anniversary-wishes.html"><b>25th (Silver)</b><span>A quarter century of love.</span></a>
      <a class="scene-card" href="/50th-anniversary-wishes.html"><b>50th (Golden)</b><span>Half a century together.</span></a>
      <a class="scene-card" href="/work-anniversary-wishes.html"><b>Work Anniversary</b><span>Professional milestones done right.</span></a>
    </div>
  </div>

  <div class="card">
    <h2>Frequently Asked Questions</h2>
{faq}
  </div>
</main>

<footer>
  Copyright <span id="year"></span> © <a href="/">Anniversary Wishes</a>. Made with love for all the anniversaries.<br>
  <a href="/about.html">About</a> · <a href="/contact.html">Contact</a> · <a href="/privacy-policy.html">Privacy</a> · <a href="/terms.html">Terms</a>
</footer>

<div class="toast" id="toast"></div>

<script>
document.querySelectorAll('.msg-copy').forEach(function(btn){{
  btn.addEventListener('click',function(){{
    var text=btn.parentElement.querySelector('.msg-text').textContent;
    function done(){{
      btn.textContent='✓ Copied';btn.classList.add('copied');
      showToast('Copied! Add your personal touch 💛');
      setTimeout(function(){{btn.textContent='Copy';btn.classList.remove('copied');}},1800);
      gtag('event','wish_copied',{{}});
    }}
    if(navigator.clipboard&&window.isSecureContext){{navigator.clipboard.writeText(text).then(done);}}
    else{{var ta=document.createElement('textarea');ta.value=text;ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);ta.select();try{{document.execCommand('copy');done();}}catch(e){{}}document.body.removeChild(ta);}}
  }});
}});
let toastTimer;
function showToast(msg){{var t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');clearTimeout(toastTimer);toastTimer=setTimeout(function(){{t.classList.remove('show');}},2200);}}
document.getElementById('year').textContent=new Date().getFullYear();
</script>
</body>
</html>
"""


def get_messages(data_key):
    """从词库取消息：recipients 或 milestones"""
    if data_key in wb.get('recipients', {}):
        return wb['recipients'][data_key]['messages']
    if data_key in wb.get('milestones', {}):
        return wb['milestones'][data_key]['messages']
    # 兼容 couple 用于 wedding-anniversary
    return wb['recipients'][data_key]['messages']


def build_tone_sections(msgs):
    out = []
    for tone, (label, sub) in TONE_META.items():
        items_list = msgs.get(tone, [])
        if not items_list:
            continue
        items = ''.join(
            f'      <div class="msg-item"><div class="msg-text">{m}</div><button class="msg-copy">Copy</button></div>\n'
            for m in items_list
        )
        out.append(f'    <h3>{label}</h3>\n    <p style="font-size:13.5px;color:var(--muted);margin-bottom:10px;">{sub}</p>\n{items}')
    return '\n'.join(out)


def build_faq(faq_list):
    return '\n'.join(
        f'    <div class="faq-item"><b>{q}</b><p>{a}</p></div>'
        for q, a in faq_list
    )


def main():
    for page in PAGES:
        msgs = get_messages(page['data'])
        tone_sections = build_tone_sections(msgs)
        faq = build_faq(page['faq'])
        html = PAGE_TPL.format(
            title=page['title'], desc=page['desc'], domain=DOMAIN,
            slug=page['slug'], ga4=GA4, h1=page['h1'], intro=page['intro'],
            tone_sections=tone_sections, faq=faq,
        )
        path = f"{BASE}/{page['slug']}.html"
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        total = sum(len(msgs.get(t, [])) for t in TONE_META)
        print(f'✅ {page["slug"]}.html ({total} msgs)')


if __name__ == '__main__':
    main()
