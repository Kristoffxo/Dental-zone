# -*- coding: utf-8 -*-
"""Build the blog: index pages and bilingual posts.

English lives at /blog/<slug>, Hindi at /blog/hi/<slug>, cross-linked with
hreflang. Separate URLs rather than a JS toggle on one page — Google indexes
each language properly this way, and it doubles the indexable surface instead
of hiding half of it behind a button.
"""
import io, os, json, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from posts import POSTS

ROOT = "/Users/aryanbasantani/Desktop/dentalzone"
BASE = "https://dentalzoneprayagraj.in"

T = {
 "en": dict(lang="en-IN", blog="Blog", home="Home", other="हिंदी में पढ़ें",
            kicker="From the Clinic", idx_h1="Dental health, explained plainly",
            idx_lede="Straight answers to what patients in Prayagraj actually ask us — no jargon, nothing oversold.",
            idx_title="Dental Health Blog | Dental Zone, Prayagraj",
            idx_meta="Plain-English answers on root canals, implants, braces, children's teeth and oral health, from Dr. Mukesh Basantani's clinic in Lukarganj, Prayagraj.",
            read="Read more", faq="Common questions", back="All posts",
            cta_h="Need to get it looked at?", cta_p="Book a consultation at Lukarganj, or call us directly.",
            book="Book an appointment", call="Call 094506 29270", mins="min read"),
 "hi": dict(lang="hi-IN", blog="ब्लॉग", home="होम", other="Read in English",
            kicker="क्लिनिक से", idx_h1="दांतों की सेहत, आसान भाषा में",
            idx_lede="प्रयागराज के मरीज़ जो सचमुच पूछते हैं, उनके सीधे जवाब — बिना भारी-भरकम शब्दों के, बिना कुछ बढ़ा-चढ़ाकर।",
            idx_title="दांतों की सेहत पर ब्लॉग | डेंटल ज़ोन, प्रयागराज",
            idx_meta="रूट कैनाल, इम्प्लांट, तार, बच्चों के दांत और मुँह की सेहत पर आसान भाषा में जानकारी — डॉ. मुकेश बसंतानी के लूकरगंज, प्रयागराज क्लिनिक से।",
            read="पूरा पढ़ें", faq="अक्सर पूछे जाने वाले सवाल", back="सभी लेख",
            cta_h="दिखाना ज़रूरी लग रहा है?", cta_p="लूकरगंज में अपॉइंटमेंट लीजिए, या सीधे फ़ोन कीजिए।",
            book="अपॉइंटमेंट बुक करें", call="094506 29270 पर कॉल करें", mins="मिनट का पाठ"),
}

MARK = ('<img src="/images/logo-mark.png" alt="Dental Zone" width="361" height="520" decoding="async">')

BOOT = ('<script>(function(){try{var s=localStorage.getItem("dz-theme");'
        'var d=s?s==="dark":window.matchMedia("(prefers-color-scheme: dark)").matches;'
        'document.documentElement.setAttribute("data-theme",d?"dark":"light");}'
        'catch(e){document.documentElement.setAttribute("data-theme","light");}})();</script>')

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
 '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
 '<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800'
 '&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet">')

CSS = """
:root{--bg:#f6f8fc;--ink:#0b1220;--muted:#5f6b81;--line:#e4eaf3;--blue:#1660ff;
--gold:#c8912a;--red:#d92b2b;--dark:#070c18;--white:#fff;
--ease:cubic-bezier(.16,.84,.44,1);--shadow-sm:0 8px 24px rgba(11,18,32,.06);
--shadow-md:0 22px 60px rgba(11,18,32,.09);--shadow-lg:0 40px 100px rgba(11,18,32,.14);
--r:22px;color-scheme:light;}
[data-theme="dark"]{--bg:#080d17;--ink:#e7eef9;--muted:#93a3bb;--line:#1e2839;--blue:#4d8bff;
--red:#ff6b6b;--gold:#e0ad4a;--dark:#05080f;--white:#111827;
--shadow-sm:0 8px 24px rgba(0,0,0,.45);--shadow-md:0 22px 60px rgba(0,0,0,.55);
--shadow-lg:0 40px 100px rgba(0,0,0,.65);color-scheme:dark;}
*{margin:0;padding:0;box-sizing:border-box;}
html{scroll-behavior:smooth;}
body{font-family:'Manrope',system-ui,sans-serif;background:var(--bg);color:var(--ink);
font-size:17px;line-height:1.7;-webkit-font-smoothing:antialiased;overflow-x:hidden;}
body:lang(hi){font-size:17.5px;line-height:1.85;}
a{text-decoration:none;color:inherit;}img{display:block;max-width:100%;}
.container{max-width:820px;margin:0 auto;padding:0 24px;}
.wide{max-width:1120px;}
.display{font-family:'Plus Jakarta Sans',system-ui,sans-serif;font-weight:700;letter-spacing:-1.4px;line-height:1.15;}
:lang(hi) .display{letter-spacing:-.4px;line-height:1.3;}
nav{position:sticky;top:0;z-index:100;background:var(--white);border-bottom:1px solid var(--line);padding:13px 0;}
nav .in{max-width:1120px;margin:0 auto;padding:0 24px;display:flex;align-items:center;justify-content:space-between;gap:16px;}
.lg{display:flex;align-items:center;gap:10px;}
.lg img[src*='logo-mark']{width:auto;height:36px;flex-shrink:0;}
.lg img{height:19px;width:auto;}
.acts{display:flex;align-items:center;gap:9px;}
.lang{padding:8px 15px;border-radius:999px;border:1px solid var(--line);background:var(--bg);
font-weight:700;font-size:13.5px;color:var(--ink);transition:border-color .3s,transform .35s var(--ease);white-space:nowrap;}
.lang:hover{border-color:var(--blue);color:var(--blue);transform:translateY(-1px);}
.cta{background:var(--blue);color:#fff;padding:10px 19px;border-radius:999px;font-weight:700;font-size:13.5px;
box-shadow:0 10px 26px rgba(22,96,255,.28);white-space:nowrap;}
.crumb{padding:20px 0 0;font-size:13px;color:var(--muted);font-weight:600;}
.crumb .s{opacity:.4;margin:0 7px;}
.hd{padding:26px 0 26px;}
.kick{display:inline-block;font-size:11.5px;font-weight:800;letter-spacing:2.4px;text-transform:uppercase;color:var(--blue);margin-bottom:14px;}
.hd h1{font-size:clamp(29px,4.6vw,45px);margin-bottom:16px;}
.hd .lede{font-size:18.5px;line-height:1.8;color:var(--muted);}
.meta{margin-top:16px;font-size:13.5px;color:var(--muted);font-weight:600;}
.meta .s{opacity:.4;margin:0 8px;}
.cover{margin:8px auto 30px;max-width:1120px;padding:0 24px;}
.cover img{width:100%;height:auto;border-radius:var(--r);box-shadow:var(--shadow-md);}
article{padding:6px 0 20px;}
article h2{font-family:'Plus Jakarta Sans',sans-serif;font-weight:700;letter-spacing:-.8px;
font-size:clamp(21px,2.7vw,27px);margin:36px 0 13px;line-height:1.3;}
:lang(hi) article h2{letter-spacing:-.2px;}
article p{margin-bottom:17px;color:#3f4a5f;font-size:17px;line-height:1.9;}
[data-theme="dark"] article p{color:#c2cee0;}
:lang(hi) article p{font-size:17.5px;line-height:2;}
article ul{margin:0 0 20px;padding-left:20px;}
article li{margin-bottom:9px;color:#3f4a5f;font-size:16.5px;line-height:1.85;}
[data-theme="dark"] article li{color:#c2cee0;}
article strong{color:var(--ink);font-weight:700;}
.faqs{margin:38px 0 8px;}
.faqs h2{margin-bottom:16px;}
.qa{background:var(--white);border:1px solid var(--line);border-radius:16px;padding:20px 24px;margin-bottom:12px;box-shadow:var(--shadow-sm);}
.qa h3{font-family:'Plus Jakarta Sans',sans-serif;font-weight:700;font-size:16.5px;margin-bottom:7px;}
.qa p{margin:0;font-size:16px;color:var(--muted);line-height:1.8;}
.end{margin:44px auto 0;max-width:820px;padding:0 24px;}
.end-in{background:linear-gradient(150deg,#070c18,#12294f);color:#fff;border-radius:26px;padding:44px 32px;text-align:center;}
.end-in h2{font-family:'Plus Jakarta Sans',sans-serif;font-weight:700;font-size:clamp(21px,3vw,29px);letter-spacing:-1px;margin-bottom:11px;}
.end-in p{color:#b6c7e0;font-size:15.5px;line-height:1.8;max-width:440px;margin:0 auto 22px;}
.btn{display:inline-flex;align-items:center;gap:9px;padding:14px 26px;border-radius:999px;font-weight:700;font-size:15px;
background:var(--blue);color:#fff;box-shadow:0 14px 34px rgba(22,96,255,.34);transition:transform .4s var(--ease);}
.btn:hover{transform:translateY(-3px);}
.btn.g{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.25);box-shadow:none;margin-left:8px;}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:22px;}
.card{background:var(--white);border:1px solid var(--line);border-radius:var(--r);overflow:hidden;
box-shadow:var(--shadow-sm);transition:transform .5s var(--ease),box-shadow .5s var(--ease),border-color .4s;display:block;}
.card:hover{transform:translateY(-7px);box-shadow:var(--shadow-lg);border-color:var(--blue);}
.card .th{aspect-ratio:16/9;overflow:hidden;background:var(--line);}
.card .th img{width:100%;height:100%;object-fit:cover;transition:transform 1s var(--ease);}
.card:hover .th img{transform:scale(1.05);}
.card .bd{padding:22px 24px 26px;}
.tag{display:inline-block;font-size:11px;font-weight:800;letter-spacing:1.3px;text-transform:uppercase;color:var(--blue);margin-bottom:9px;}
.card h2{font-family:'Plus Jakarta Sans',sans-serif;font-weight:700;font-size:19.5px;letter-spacing:-.5px;line-height:1.3;margin-bottom:9px;}
:lang(hi) .card h2{letter-spacing:0;line-height:1.45;}
.card p{color:var(--muted);font-size:15px;line-height:1.75;margin-bottom:13px;}
.more{font-weight:700;font-size:14.5px;color:var(--blue);}
footer{background:var(--dark);color:#9fb0ca;padding:34px 0;text-align:center;font-size:14px;margin-top:52px;}
footer a{color:#c9d4e6;}
/* Devanagari has no letter-case and conjuncts sit tight — English tracking
   pulls the matras away from their base characters and it reads broken. */
:lang(hi) .kick,:lang(hi) .tag{letter-spacing:.6px;}
@media(max-width:640px){
  /* the nav overflowed: wordmark, language switch and CTA together were wider
     than a 375px screen, so the logo was clipped behind the buttons */
  .lg img{height:16px;}
  .lg svg{width:28px;height:28px;}
  nav .in{gap:8px;padding:0 14px;}
  .lang{padding:7px 11px;font-size:12px;}
  .cta{padding:9px 14px;font-size:12.5px;}
  .hd{padding:18px 0 20px;}
  .grid{grid-template-columns:1fr;gap:16px;}
  .card .bd{padding:18px 20px 22px;}
  .end-in{padding:34px 22px;}
  .btn.g{margin:9px 0 0;}
  article p{font-size:16.5px;}
}
@media(prefers-reduced-motion:reduce){*{transition-duration:.01ms!important;scroll-behavior:auto!important;}}
"""

def head(lang, title, meta, canon, alt, img, extra=""):
    t=T[lang]
    return f"""<!DOCTYPE html>
<html lang="{t['lang']}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{meta}">
<meta name="theme-color" content="#f6f8fc" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#080d17" media="(prefers-color-scheme: dark)">
<link rel="canonical" href="{canon}">
<link rel="alternate" hreflang="en-IN" href="{alt['en']}">
<link rel="alternate" hreflang="hi-IN" href="{alt['hi']}">
<link rel="alternate" hreflang="x-default" href="{alt['en']}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="geo.region" content="IN-UP"><meta name="geo.placename" content="Prayagraj">
<meta property="og:type" content="article"><meta property="og:site_name" content="Dental Zone">
<meta property="og:locale" content="{'en_IN' if lang=='en' else 'hi_IN'}">
<meta property="og:url" content="{canon}"><meta property="og:title" content="{title}">
<meta property="og:description" content="{meta}"><meta property="og:image" content="{img}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="96x96" href="/icon-96.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
{BOOT}
{FONTS}
{extra}
<style>{CSS}</style>
</head>
<body>
<nav><div class="in">
  <a href="/" class="lg" aria-label="Dental Zone">{MARK}<img src="/images/wordmark.png" alt="Dental Zone" width="1665" height="318"></a>
  <div class="acts">
    <a class="lang" href="{alt['hi'] if lang=='en' else alt['en']}">{t['other']}</a>
    <a class="cta" href="/#booking">{'Book' if lang=='en' else 'बुक करें'}</a>
  </div>
</div></nav>
"""

FOOT = """<footer><div class="container">
  <strong>Dental Zone</strong> — Dr. Mukesh Basantani, BDS · 26/17/3 Grand Trunk Rd, Lukarganj, Prayagraj 211003<br>
  <a href="tel:+919450629270">094506 29270</a> · Mon–Sat 10:00 AM – 8:00 PM
</div></footer>
</body></html>
"""

def words(html):
    import re
    return len(re.sub(r'<[^>]+>',' ',html).split())

def build_post(p, lang):
    t=T[lang]; c=p[lang]
    slug=p["slug"]
    alt={"en":f"{BASE}/blog/{slug}", "hi":f"{BASE}/blog/hi/{slug}"}
    canon=alt[lang]
    img=f"{BASE}/images/blog/cover-{p['img']}.jpg"
    prefix="/blog/hi" if lang=="hi" else "/blog"

    ld={"@context":"https://schema.org","@type":"BlogPosting",
        "@id":canon+"#post","headline":c["h1"],"description":c["meta"],
        "datePublished":p["date"],"dateModified":p["date"],
        "inLanguage":t["lang"],"image":[img],
        "author":{"@type":"Person","name":"Dr. Mukesh Basantani","jobTitle":"Dental Surgeon & Implantologist","url":f"{BASE}/#doctor"},
        "publisher":{"@type":"Organization","name":"Dental Zone","url":BASE+"/",
                     "logo":{"@type":"ImageObject","url":f"{BASE}/apple-touch-icon.png"}},
        "mainEntityOfPage":{"@type":"WebPage","@id":canon}}
    faqld={"@context":"https://schema.org","@type":"FAQPage",
           "mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in c["faq"]]}
    crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":t["home"],"item":BASE+"/"},
        {"@type":"ListItem","position":2,"name":t["blog"],"item":f"{BASE}{prefix}/"},
        {"@type":"ListItem","position":3,"name":c["h1"]}]}
    extra="".join(f'<script type="application/ld+json">{json.dumps(x,ensure_ascii=False)}</script>' for x in (ld,faqld,crumb))

    mins=max(2, words(c["body"])//180)
    faqs="".join(f'<div class="qa"><h3>{q}</h3><p>{a}</p></div>' for q,a in c["faq"])

    return head(lang,c["title"],c["meta"],canon,alt,img,extra)+f"""
<div class="container crumb"><a href="/">{t['home']}</a><span class="s">›</span><a href="{prefix}/">{t['blog']}</a></div>
<header class="hd"><div class="container">
  <span class="kick">{p['cat'] if lang=='en' else t['kicker']}</span>
  <h1 class="display">{c['h1']}</h1>
  <p class="lede">{c['lede']}</p>
  <div class="meta"><time datetime="{p['date']}">{p['date']}</time><span class="s">·</span>{mins} {t['mins']}</div>
</div></header>
<div class="cover"><img src="/images/blog/cover-{p['img']}.jpg" alt="{c['h1']}" width="1200" height="630"></div>
<article><div class="container">
{c['body']}
  <div class="faqs"><h2 class="display">{t['faq']}</h2>{faqs}</div>
</div></article>
<div class="end"><div class="end-in">
  <h2>{t['cta_h']}</h2><p>{t['cta_p']}</p>
  <a class="btn" href="/#booking">{t['book']} →</a><a class="btn g" href="tel:+919450629270">{t['call']}</a>
</div></div>
<div class="container" style="margin-top:34px"><a class="more" href="{prefix}/">← {t['back']}</a></div>
{FOOT}"""

def build_index(lang):
    t=T[lang]
    alt={"en":f"{BASE}/blog/","hi":f"{BASE}/blog/hi/"}
    canon=alt[lang]
    cards=""
    for p in POSTS:
        c=p[lang]; prefix="/blog/hi" if lang=="hi" else "/blog"
        cards+=f"""      <a class="card" href="{prefix}/{p['slug']}">
        <div class="th"><img src="/images/blog/cover-{p['img']}.jpg" alt="{c['h1']}" width="1200" height="630" loading="lazy" decoding="async"></div>
        <div class="bd"><span class="tag">{p['cat'] if lang=='en' else t['kicker']}</span>
          <h2>{c['h1']}</h2><p>{c['lede']}</p><span class="more">{t['read']} →</span></div>
      </a>
"""
    ld={"@context":"https://schema.org","@type":"Blog","@id":canon+"#blog",
        "name":t["idx_h1"],"description":t["idx_meta"],"inLanguage":t["lang"],"url":canon,
        "publisher":{"@type":"Organization","name":"Dental Zone","url":BASE+"/"},
        "blogPost":[{"@type":"BlogPosting","headline":p[lang]["h1"],
                     "url":f"{BASE}/blog/{'hi/' if lang=='hi' else ''}{p['slug']}",
                     "datePublished":p["date"]} for p in POSTS]}
    extra=f'<script type="application/ld+json">{json.dumps(ld,ensure_ascii=False)}</script>'
    return head(lang,t["idx_title"],t["idx_meta"],canon,alt,f"{BASE}/images/blog/cover-{POSTS[0]['img']}.jpg",extra)+f"""
<div class="container wide crumb"><a href="/">{t['home']}</a><span class="s">›</span>{t['blog']}</div>
<header class="hd"><div class="container wide">
  <span class="kick">{t['kicker']}</span>
  <h1 class="display">{t['idx_h1']}</h1>
  <p class="lede">{t['idx_lede']}</p>
</div></header>
<div class="container wide" style="padding-bottom:20px">
    <div class="grid">
{cards}    </div>
</div>
{FOOT}"""

if __name__ == "__main__":
    os.makedirs(f"{ROOT}/blog/hi", exist_ok=True)
    n=0
    for lang in ("en","hi"):
        d = f"{ROOT}/blog" if lang=="en" else f"{ROOT}/blog/hi"
        io.open(f"{d}/index.html","w",encoding="utf-8").write(build_index(lang))
        n+=1
        for p in POSTS:
            io.open(f"{d}/{p['slug']}.html","w",encoding="utf-8").write(build_post(p,lang))
            n+=1
    print(f"{n} pages written ({len(POSTS)} posts x 2 languages + 2 indexes)")
