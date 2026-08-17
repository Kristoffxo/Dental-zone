"""Generate the service landing pages.

One page per query cluster. A single homepage can only rank for so much; these
give Google a distinct, substantial page to match against "root canal treatment
in allahabad", "dental implant cost prayagraj" and so on.

Content is written per page, not templated filler — near-duplicate service pages
are treated as thin content and can drag the whole site down.
"""
import io, os, json

BASE = "https://dentalzoneprayagraj.in"
OUT = "/Users/aryanbasantani/Desktop/dentalzone/services"

CSS = """
:root{--bg:#f6f8fc;--ink:#0b1220;--muted:#5f6b81;--line:#e4eaf3;--blue:#1660ff;
--blue-soft:#5fb0ff;--gold:#c8912a;--red:#d92b2b;--sky:#4fb3e8;--dark:#070c18;--white:#fff;
--ease:cubic-bezier(.16,.84,.44,1);--shadow-sm:0 8px 24px rgba(11,18,32,.06);
--shadow-md:0 22px 60px rgba(11,18,32,.09);--shadow-lg:0 40px 100px rgba(11,18,32,.14);
--r:26px;color-scheme:light;}
[data-theme="dark"]{--bg:#080d17;--ink:#e7eef9;--muted:#93a3bb;--line:#1e2839;--blue:#4d8bff;
--blue-soft:#7cbcff;--gold:#e0ad4a;--red:#ff6b6b;--sky:#6cc4f5;--dark:#05080f;--white:#111827;
--shadow-sm:0 8px 24px rgba(0,0,0,.45);--shadow-md:0 22px 60px rgba(0,0,0,.55);
--shadow-lg:0 40px 100px rgba(0,0,0,.65);color-scheme:dark;}
*{margin:0;padding:0;box-sizing:border-box;}
html{scroll-behavior:smooth;}
body{font-family:'Manrope',system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--ink);
font-size:17px;line-height:1.7;-webkit-font-smoothing:antialiased;overflow-x:hidden;}
a{text-decoration:none;color:inherit;}img{display:block;max-width:100%;}
.container{max-width:860px;margin:0 auto;padding:0 28px;}
.display{font-family:'Plus Jakarta Sans',system-ui,sans-serif;font-weight:700;letter-spacing:-1.6px;line-height:1.1;}
.nav{position:sticky;top:0;z-index:100;background:var(--white);border-bottom:1px solid var(--line);padding:15px 0;}
.nav .inner{max-width:1100px;margin:0 auto;padding:0 28px;display:flex;align-items:center;justify-content:space-between;gap:20px;}
.logo{display:flex;align-items:center;gap:11px;}
.logo svg{width:38px;height:38px;flex-shrink:0;}
.logo .l1{font-family:'Plus Jakarta Sans',sans-serif;font-weight:800;font-size:20px;letter-spacing:-.9px;color:var(--red);line-height:1;}
.logo .l1 span{color:var(--blue);}
.navcta{background:var(--blue);color:#fff;padding:11px 22px;border-radius:999px;font-weight:700;font-size:14.5px;
box-shadow:0 12px 30px rgba(22,96,255,.28);transition:transform .4s var(--ease);}
.navcta:hover{transform:translateY(-2px);}
.crumbs{padding:22px 0 0;font-size:13.5px;color:var(--muted);font-weight:600;}
.crumbs a:hover{color:var(--blue);}
.crumbs .sep{opacity:.4;margin:0 8px;}
.head{padding:34px 0 30px;}
.kicker{display:inline-flex;align-items:center;gap:9px;font-size:12px;font-weight:800;letter-spacing:2.6px;
text-transform:uppercase;color:var(--blue);margin-bottom:18px;}
.head h1{font-size:clamp(31px,5vw,50px);margin-bottom:20px;}
.head .lede{font-size:19.5px;line-height:1.85;color:var(--muted);}
article{padding:14px 0 30px;}
article h2{font-family:'Plus Jakarta Sans',sans-serif;font-weight:700;letter-spacing:-1px;
font-size:clamp(23px,3vw,30px);margin:44px 0 16px;line-height:1.25;}
article h3{font-family:'Plus Jakarta Sans',sans-serif;font-weight:700;font-size:19px;margin:28px 0 10px;letter-spacing:-.4px;}
article p{margin-bottom:20px;color:#3f4a5f;font-size:17.5px;line-height:1.9;}
[data-theme="dark"] article p{color:#c2cee0;}
article strong{color:var(--ink);font-weight:700;}
article ul{margin:0 0 22px 0;padding-left:22px;}
article li{margin-bottom:11px;color:#3f4a5f;font-size:17px;line-height:1.85;}
[data-theme="dark"] article li{color:#c2cee0;}
.callout{margin:34px 0;padding:28px 32px;border-radius:20px;background:var(--white);
border-left:4px solid var(--blue);box-shadow:var(--shadow-sm);font-size:16.5px;line-height:1.85;color:var(--muted);}
.callout strong{color:var(--ink);}
.warn{border-left-color:var(--red);}
.faq{margin:44px 0 10px;}
.faq h2{margin-bottom:20px;}
.qa{background:var(--white);border:1px solid var(--line);border-radius:18px;padding:24px 28px;margin-bottom:14px;box-shadow:var(--shadow-sm);}
.qa h3{margin:0 0 8px;font-size:17.5px;}
.qa p{margin:0;font-size:16.5px;}
.cta{margin:52px auto 0;max-width:860px;padding:0 28px;}
.cta-in{background:linear-gradient(150deg,#070c18,#12294f);color:#fff;border-radius:30px;padding:54px 40px;text-align:center;}
.cta-in h2{font-family:'Plus Jakarta Sans',sans-serif;font-weight:700;letter-spacing:-1.2px;font-size:clamp(24px,3.4vw,34px);margin-bottom:14px;}
.cta-in p{color:#b6c7e0;font-size:16.5px;line-height:1.8;max-width:520px;margin:0 auto 26px;}
.btn{display:inline-flex;align-items:center;gap:10px;padding:16px 32px;border-radius:999px;font-weight:700;font-size:16px;
background:var(--blue);color:#fff;box-shadow:0 16px 40px rgba(22,96,255,.34);transition:transform .4s var(--ease);}
.btn:hover{transform:translateY(-3px);}
.btn.ghost{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.25);box-shadow:none;margin-left:10px;}
.related{padding:52px 0 70px;}
.related h2{font-family:'Plus Jakarta Sans',sans-serif;font-weight:700;font-size:22px;letter-spacing:-.7px;margin-bottom:18px;}
.rgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;}
.rgrid a{background:var(--white);border:1px solid var(--line);border-radius:16px;padding:18px 22px;font-weight:700;font-size:15.5px;
box-shadow:var(--shadow-sm);transition:transform .4s var(--ease),border-color .3s;}
.rgrid a:hover{transform:translateY(-4px);border-color:var(--blue);color:var(--blue);}
footer{background:var(--dark);color:#9fb0ca;padding:40px 0;text-align:center;font-size:14.5px;}
footer a{color:#c9d4e6;}
@media(max-width:640px){.cta-in{padding:40px 24px;}.btn.ghost{margin:10px 0 0;}}
@media(prefers-reduced-motion:reduce){*{transition-duration:.01ms!important;scroll-behavior:auto!important;}}
"""

MARK = ('<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
 '<path d="M50 93 C50 93 9 64 9 37 C9 20 22 10 34.5 10 C43 10 50 16.5 50 16.5 C50 16.5 57 10 65.5 10 C78 10 91 20 91 37 C91 64 50 93 50 93 Z" fill="none" stroke="#d92b2b" stroke-width="7.5" stroke-linecap="round" stroke-linejoin="round"/>'
 '<path d="M50 28 C36 28 27 35 27 46 C27 53 28.5 58 28 65 C27.3 74 29.5 82 34 82.8 C37.8 83.5 39.6 79.5 40.6 72.5 C41.6 65.5 44.5 62 50 62 C55.5 62 58.4 65.5 59.4 72.5 C60.4 79.5 62.2 83.5 66 82.8 C70.5 82 72.7 74 72 65 C71.5 58 73 53 73 46 C73 35 64 28 50 28 Z" fill="#fff" stroke="#d92b2b" stroke-width="2.6" stroke-linejoin="round"/>'
 '<path d="M38.5 44 Q42.5 39 46.5 44" fill="none" stroke="#d92b2b" stroke-width="3.4" stroke-linecap="round"/>'
 '<circle cx="58" cy="42.5" r="3.2" fill="#d92b2b"/>'
 '<path d="M40 51.5 Q50 60.5 60 51.5" fill="none" stroke="#d92b2b" stroke-width="3.6" stroke-linecap="round"/></svg>')

THEME_BOOT = """<script>
(function(){try{var s=localStorage.getItem('dz-theme');
var d=s?s==='dark':window.matchMedia('(prefers-color-scheme: dark)').matches;
document.documentElement.setAttribute('data-theme',d?'dark':'light');}
catch(e){document.documentElement.setAttribute('data-theme','light');}})();
</script>"""


def page(s, others):
    faq_ld = {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in s["faqs"]]
    }
    svc_ld = {
        "@context": "https://schema.org", "@type": "MedicalWebPage",
        "@id": f"{BASE}/services/{s['slug']}#page",
        "name": s["h1"], "description": s["meta"], "inLanguage": "en-IN",
        "url": f"{BASE}/services/{s['slug']}",
        "about": {"@type": "MedicalProcedure", "name": s["procedure"],
                  "procedureType": "https://schema.org/NoninvasiveProcedure"},
        "provider": {"@type": "Dentist", "@id": f"{BASE}/#clinic"},
        "audience": {"@type": "MedicalAudience", "geographicArea": {
            "@type": "AdministrativeArea", "name": "Prayagraj (Allahabad), Uttar Pradesh"}},
    }
    crumb_ld = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Services", "item": BASE + "/#services"},
            {"@type": "ListItem", "position": 3, "name": s["short"]},
        ]}

    faq_html = "\n".join(
        f'      <div class="qa"><h3>{q}</h3><p>{a}</p></div>' for q, a in s["faqs"])
    rel_html = "\n".join(
        f'      <a href="/services/{o["slug"]}">{o["short"]} in Allahabad →</a>' for o in others)

    return f"""<!DOCTYPE html>
<html lang="en-IN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{s['title']}</title>
<meta name="description" content="{s['meta']}">
<meta name="theme-color" content="#f6f8fc" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#080d17" media="(prefers-color-scheme: dark)">
<link rel="canonical" href="{BASE}/services/{s['slug']}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="geo.region" content="IN-UP">
<meta name="geo.placename" content="Prayagraj, Allahabad">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Dental Zone">
<meta property="og:locale" content="en_IN">
<meta property="og:url" content="{BASE}/services/{s['slug']}">
<meta property="og:title" content="{s['title']}">
<meta property="og:description" content="{s['meta']}">
<meta property="og:image" content="{BASE}/images/images-2.jpeg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="96x96" href="/icon-96.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
{THEME_BOOT}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet">
<script type="application/ld+json">{json.dumps(svc_ld)}</script>
<script type="application/ld+json">{json.dumps(faq_ld)}</script>
<script type="application/ld+json">{json.dumps(crumb_ld)}</script>
<style>{CSS}</style>
</head>
<body>

<nav class="nav">
  <div class="inner">
    <a href="/" class="logo" aria-label="Dental Zone home">{MARK}<span class="l1">Dental<span>Zone</span></span></a>
    <a href="/#booking" class="navcta">Book Appointment</a>
  </div>
</nav>

<div class="container crumbs">
  <a href="/">Home</a><span class="sep">›</span><a href="/#services">Services</a><span class="sep">›</span>{s['short']}
</div>

<header class="head">
  <div class="container">
    <span class="kicker">{s['kicker']}</span>
    <h1 class="display">{s['h1']}</h1>
    <p class="lede">{s['lede']}</p>
  </div>
</header>

<article>
  <div class="container">
{s['body']}

    <div class="faq">
      <h2 class="display">Common questions</h2>
{faq_html}
    </div>
  </div>
</article>

<div class="cta">
  <div class="cta-in">
    <h2>{s['cta_h']}</h2>
    <p>{s['cta_p']}</p>
    <a class="btn" href="/#booking">Book an appointment →</a>
    <a class="btn ghost" href="tel:+919450629270">Call 094506 29270</a>
  </div>
</div>

<div class="container related">
  <h2>Other treatments at Dental Zone</h2>
  <div class="rgrid">
{rel_html}
      <a href="/">Best dentist in Allahabad →</a>
  </div>
</div>

<footer>
  <div class="container">
    <strong>Dental Zone</strong> — Dr. Mukesh Basantani, BDS · 26/17/3 Grand Trunk Rd, Lukarganj, Prayagraj 211003<br>
    <a href="tel:+919450629270">094506 29270</a> · Mon–Sat 10:00 AM – 8:00 PM
  </div>
</footer>

</body>
</html>
"""


SERVICES = [
{
 "slug": "root-canal-treatment-allahabad",
 "short": "Root Canal Treatment",
 "procedure": "Root canal treatment",
 "kicker": "Root Canal Treatment",
 "title": "Root Canal Treatment in Allahabad (Prayagraj) | Dental Zone",
 "meta": "Painless root canal treatment in Allahabad by Dr. Mukesh Basantani, BDS — 50,000+ RCTs performed. Rotary equipment, most cases in one or two sittings. Call 094506 29270.",
 "h1": "Root canal treatment in Allahabad",
 "lede": "It is the treatment we are best known for across Prayagraj, and the one patients arrive most afraid of. Almost nobody leaves still afraid of it.",
 "cta_h": "Toothache that won't settle?",
 "cta_p": "Book a consultation and we'll tell you honestly whether you need a root canal, a filling, or nothing at all.",
 "body": """    <h2>Does a root canal actually hurt?</h2>
    <p>
      This is the first thing almost everyone asks, so let's deal with it honestly.
      <strong>The pain people associate with root canals is the pain that sends them to the
      dentist in the first place</strong> — an inflamed or infected nerve, which is genuinely
      one of the worst pains the body produces. The treatment is what stops it.
    </p>
    <p>
      With modern anaesthesia and rotary instruments, most patients describe the procedure
      itself as no worse than having a filling. You will feel pressure and hear the
      equipment. You should not feel pain. If you do at any point, tell us and we stop and
      add more anaesthetic — you are not being brave by enduring it.
    </p>

    <h2>How to tell you might need one</h2>
    <ul>
      <li>Pain that lingers for minutes after something hot or cold, rather than fading immediately</li>
      <li>A deep ache that wakes you at night or throbs when you lie down</li>
      <li>Pain when biting on one particular tooth</li>
      <li>A tooth that has darkened compared with its neighbours</li>
      <li>A small pimple-like swelling on the gum near a tooth, which may come and go</li>
      <li>A tooth that hurt badly and then stopped — this often means the nerve has died, not healed</li>
    </ul>
    <p>
      That last one catches people out constantly. Pain disappearing on its own is not
      usually good news, and the infection carries on quietly underneath.
    </p>

    <h2>What actually happens</h2>
    <p>
      The tooth is numbed. A small opening is made in the crown, the infected pulp is
      removed, and the canals inside the root are cleaned and shaped with fine rotary
      files. They are then disinfected, dried, and sealed. Finally the opening is filled.
    </p>
    <p>
      <strong>Most cases are done in one or two sittings.</strong> A molar with four canals,
      or a tooth with an active abscess, may need an extra visit — sometimes an
      antibiotic and a few days for the infection to settle before the canals can be
      properly sealed.
    </p>

    <h3>The crown afterwards</h3>
    <p>
      A treated back tooth is more brittle than a healthy one and can split under chewing
      force. For molars and premolars we almost always recommend a crown afterwards. It is
      not an upsell — a fractured root-treated tooth usually cannot be saved, and you lose
      both the tooth and the money spent treating it. Front teeth often do not need one.
    </p>

    <div class="callout">
      <strong>Cost depends mostly on which tooth it is.</strong> A front tooth has a single
      canal; a molar can have three or four and takes considerably longer. Existing
      infection and whether a crown is needed also change the figure. We examine the tooth,
      take an X-ray, and give you a firm number before anything begins.
    </div>

    <h2>What happens if you leave it</h2>
    <p>
      Infection in a tooth does not resolve by itself. It spreads into the bone at the root
      tip, and from there into the surrounding tissue. What starts as a tooth that needs one
      appointment becomes a facial swelling, an extraction, and eventually a gap that needs
      an implant or a bridge to close. Waiting almost never makes the problem smaller or
      cheaper.
    </p>""",
 "faqs": [
  ("How many sittings does a root canal take?",
   "Most root canals are completed in one or two sittings. A molar with several canals, or a tooth with an active abscess, sometimes needs a third visit — occasionally with a few days in between to let an infection settle before the canals are sealed."),
  ("Will I need a crown after my root canal?",
   "For back teeth, almost always. A root-treated molar becomes brittle and can split under chewing force, and a fractured root-treated tooth usually cannot be saved. Front teeth often do not need a crown."),
  ("Is a root canal better than just removing the tooth?",
   "Nearly always, yes. Your own tooth keeps the bone around it healthy and the neighbouring teeth in position. An extraction is cheaper on the day but often leads to an implant or bridge later, which costs considerably more."),
  ("Can a root canal be done in one day in Allahabad?",
   "Often, yes. Straightforward cases at Dental Zone in Lukarganj are regularly completed in a single sitting. Whether yours can be depends on the tooth and whether there is active infection, which we can tell you after an examination and X-ray."),
 ],
},
{
 "slug": "dental-implants-allahabad",
 "short": "Dental Implants",
 "procedure": "Dental implant",
 "kicker": "Dental Implants",
 "title": "Dental Implants in Allahabad (Prayagraj) | Cost & Procedure | Dental Zone",
 "meta": "Dental implants in Allahabad by Dr. Mukesh Basantani — 19 years as a specialist implantologist. What drives the cost, who is a candidate, and how long it takes. Call 094506 29270.",
 "h1": "Dental implants in Allahabad",
 "lede": "The closest thing dentistry has to giving you the tooth back. Placed by a specialist implantologist with nineteen years of focused experience.",
 "cta_h": "Missing a tooth?",
 "cta_p": "An examination and X-ray will tell us whether an implant is right for you, and exactly what it will cost. No obligation to proceed.",
 "body": """    <h2>What an implant actually is</h2>
    <p>
      An implant is a small titanium post placed into the jawbone where the root of the
      missing tooth used to be. Over the following months the bone grows onto its surface
      and locks it in place — a process called osseointegration. A crown is then fixed on
      top.
    </p>
    <p>
      That bone integration is the whole point, and it is why implants behave differently
      from a bridge or a denture. <strong>The post transmits chewing force into the jawbone,
      which keeps that bone alive.</strong> Bone that has no tooth root in it slowly resorbs,
      which is why people who have worn dentures for many years develop a collapsed look
      around the mouth.
    </p>

    <h2>Are you a candidate?</h2>
    <p>
      The main question is bone. There needs to be enough of it, in the right place, to
      hold the implant. Where a tooth has been missing for years, the bone has often thinned
      and a graft is needed first — this adds both cost and several months to the timeline.
      An X-ray tells us quickly which situation you are in.
    </p>
    <p>Two other factors matter:</p>
    <ul>
      <li><strong>Gum health.</strong> Active gum disease has to be treated before an implant goes in, or the same process will attack the implant.</li>
      <li><strong>Smoking and uncontrolled diabetes</strong> both measurably reduce success rates, because both interfere with healing. Neither is automatically disqualifying, but we will be straight with you about the odds.</li>
    </ul>

    <h2>How long it takes</h2>
    <p>
      Placing the implant is usually a single appointment under local anaesthetic, and most
      patients are surprised by how undramatic it is — considerably less eventful than an
      extraction. The waiting is the long part. <strong>Expect roughly three to six months
      between placement and the final crown</strong> while the bone integrates. If a graft is
      needed first, add several months to that.
    </p>
    <p>
      A temporary tooth can usually be arranged for the gap in the meantime, so you are not
      walking around with a visible space.
    </p>

    <div class="callout">
      <strong>What drives the cost:</strong> whether you need a bone graft, the implant
      system used, and how many teeth are being replaced. Replacing several adjacent teeth
      does not usually need one implant per tooth — a bridge supported on two implants is
      often both better and cheaper. We give you the figure after the examination.
    </div>

    <h2>The honest alternatives</h2>
    <p>
      An implant is not automatically the right answer, and it would be dishonest to pretend
      otherwise.
    </p>
    <h3>A bridge</h3>
    <p>
      Faster and cheaper, and completed in weeks rather than months. The cost is that the
      teeth on either side have to be shaved down to carry it — healthy tooth structure you
      do not get back. If those neighbouring teeth already need crowns anyway, a bridge can
      make very good sense.
    </p>
    <h3>A removable denture</h3>
    <p>
      The least expensive option by a wide margin, and sometimes the right one — particularly
      where several teeth are missing or where health conditions make surgery unwise. It
      does not preserve bone, and most people find it less comfortable.
    </p>

    <h2>How long do they last?</h2>
    <p>
      With good hygiene and regular checkups, implants routinely last decades. The titanium
      post itself does not decay. What does fail them is gum disease around the implant, so
      the maintenance is exactly the maintenance for natural teeth — brushing, cleaning
      between them, and a professional clean every six months.
    </p>""",
 "faqs": [
  ("How much does a dental implant cost in Allahabad?",
   "It depends mainly on whether the bone needs grafting first, the implant system used, and how many teeth are being replaced. Rather than quote a misleading range, we examine the site, take an X-ray, and give a firm figure before treatment begins."),
  ("Is getting an implant painful?",
   "The placement is done under local anaesthetic and most patients report it as less eventful than an extraction. There is some soreness for a few days afterwards, usually manageable with ordinary painkillers."),
  ("How long does the whole process take?",
   "Typically three to six months from placement to the final crown, because the bone needs that time to integrate with the implant. If a bone graft is needed first, add several months. A temporary tooth can usually fill the gap meanwhile."),
  ("Implant or bridge — which is better?",
   "An implant preserves the jawbone and leaves neighbouring teeth untouched, but costs more and takes months. A bridge is faster and cheaper but requires filing down the two adjacent teeth. If those teeth already need crowns, a bridge is often the sensible choice."),
 ],
},
{
 "slug": "braces-and-aligners-allahabad",
 "short": "Braces & Aligners",
 "procedure": "Orthodontic treatment",
 "kicker": "Braces & Aligners",
 "title": "Braces & Aligners in Allahabad (Prayagraj) | Orthodontist | Dental Zone",
 "meta": "Braces and clear aligners in Allahabad — 1,000+ orthodontic cases by Dr. Mukesh Basantani, certified orthodontist. Metal, ceramic and aligner options for children and adults.",
 "h1": "Braces &amp; aligners in Allahabad",
 "lede": "Over a thousand fixed orthodontic cases completed here — a large share of them adults who assumed they had missed their chance.",
 "cta_h": "Thinking about straightening your teeth?",
 "cta_p": "A consultation will tell you which options genuinely suit your case, how long it would take, and what it would cost.",
 "body": """    <h2>You are almost certainly not too old</h2>
    <p>
      This is the single most common reason people never ask. Teeth move throughout life —
      that is precisely why they drift out of alignment in the first place — and the biology
      that lets an orthodontist move them deliberately does not switch off at a particular
      age.
    </p>
    <p>
      <strong>A significant share of the orthodontic cases completed at Dental Zone have been
      adults</strong>, many of them in their thirties and forties. Treatment in an adult
      generally takes somewhat longer than in a teenager, because the bone remodels more
      slowly. That is the main difference. It is not a barrier.
    </p>

    <h2>The three options, honestly compared</h2>

    <h3>Metal braces</h3>
    <p>
      The most effective option for complex movement, and the least expensive. Modern
      brackets are far smaller than the ones people remember from the nineties. If your case
      involves significant rotation or teeth that need moving a long way, this is often the
      only option that will genuinely do the job, and we will say so.
    </p>

    <h3>Ceramic braces</h3>
    <p>
      Mechanically much the same as metal, but with tooth-coloured brackets that are far less
      noticeable at conversational distance. They cost more and are slightly more fragile.
      A good middle ground for adults who need fixed braces but work in front of people.
    </p>

    <h3>Clear aligners</h3>
    <p>
      A series of removable transparent trays, changed every week or two. The advantages are
      real: nearly invisible, removable for eating and brushing, no dietary restrictions.
    </p>
    <p>
      The catch is equally real — <strong>they only work while you are wearing them, which
      needs to be twenty to twenty-two hours a day.</strong> Patients who cannot commit to
      that end up with treatment that takes far longer than promised, or does not finish
      properly. Aligners also handle some movements less predictably than fixed braces. They
      suit mild to moderate crowding well.
    </p>

    <div class="callout">
      <strong>How long it takes:</strong> most cases run twelve to twenty-four months. The
      length depends on how far the teeth have to move, not on which appliance you choose.
      Anyone promising a straight result in three months is either treating a very mild case
      or not telling you the whole story.
    </div>

    <h2>What treatment is actually like</h2>
    <p>
      After the braces go on, expect a few days of tenderness — teeth feel bruised rather
      than sharply painful, and soft food helps. That settles. You will then come in every
      four to six weeks for adjustments, which are quick.
    </p>
    <p>
      With fixed braces, cleaning becomes more work and matters more. Food traps around
      brackets, and the most common bad outcome in orthodontics is not crooked teeth — it is
      straight teeth with permanent white decalcification marks where plaque sat against the
      enamel for eighteen months. We will show you how to avoid that.
    </p>

    <h2>Retainers are not optional</h2>
    <p>
      Teeth have a memory. Left alone after treatment, they drift back toward where they
      started, and this is the single most common reason people end up needing orthodontics
      twice. <strong>Wearing your retainer as instructed is what makes the result
      permanent.</strong> Plan on it being a long-term habit, not a few months.
    </p>

    <h2>Children</h2>
    <p>
      A first orthodontic assessment around ages seven to nine is worthwhile, not because
      treatment usually starts then, but because some bite problems are far easier to guide
      while the jaw is still growing. Most children who need braces get them in early
      adolescence once the adult teeth are through.
    </p>""",
 "faqs": [
  ("Am I too old for braces?",
   "Almost certainly not. Teeth can be moved at any age, and a significant share of the orthodontic cases completed at Dental Zone have been adults. Treatment usually takes somewhat longer in adults because bone remodels more slowly, but age itself is not a barrier."),
  ("How long do braces take?",
   "Most cases take twelve to twenty-four months. The length is determined by how far the teeth need to move rather than by which appliance you choose. Anyone promising a straight result in a few months is either treating a very mild case or overselling."),
  ("Are clear aligners as good as braces?",
   "For mild to moderate crowding, yes. For complex rotations or teeth that need moving a long distance, fixed braces remain more predictable. Aligners also depend entirely on you wearing them twenty to twenty-two hours a day — treatment stalls if you do not."),
  ("Do braces hurt?",
   "There is tenderness for a few days after fitting and after each adjustment — teeth feel bruised rather than sharply painful, and soft food helps. It settles quickly and most patients stop noticing the braces within a couple of weeks."),
 ],
},
{
 "slug": "emergency-dentist-allahabad",
 "short": "Dental Emergencies",
 "procedure": "Emergency dental treatment",
 "kicker": "Dental Emergencies",
 "title": "Emergency Dentist in Allahabad (Prayagraj) | Same-Day Care | Dental Zone",
 "meta": "Severe toothache, swelling or a broken tooth in Allahabad? Dental Zone in Lukarganj prioritises emergencies for same-day care. What to do right now — call 094506 29270.",
 "h1": "Emergency dentist in Allahabad",
 "lede": "Severe pain, facial swelling and knocked-out teeth are treated as priority. Here is what to do in the meantime.",
 "cta_h": "In pain right now?",
 "cta_p": "Call the clinic directly rather than booking online — we can advise you immediately and get you seen sooner.",
 "body": """    <div class="callout warn">
      <strong>Go to a hospital emergency department, not a dental clinic, if</strong> a
      swelling is closing your eye, spreading down your neck, or making it hard to swallow or
      breathe; if you have a high fever with facial swelling; or if you have had a significant
      blow to the head or a suspected jaw fracture. These need urgent medical care, not
      dentistry.
    </div>

    <h2>A knocked-out adult tooth</h2>
    <p>
      This is the one genuine race against the clock in dentistry. A tooth put back within
      about thirty minutes has a good chance of surviving. After a couple of hours, it usually
      does not.
    </p>
    <ul>
      <li><strong>Pick it up by the crown</strong> — the chewing part — never by the root.</li>
      <li>If it is dirty, rinse it briefly in milk or saline. Do not scrub it, and do not use soap or tap water for long: the delicate cells on the root surface are what allow it to reattach.</li>
      <li><strong>If you can, put it straight back in the socket</strong> and bite gently on a clean cloth to hold it.</li>
      <li>If you cannot, keep it in <strong>milk</strong> — or in the patient's own saliva, held inside the cheek if they are old enough not to swallow it. Do not store it in water.</li>
      <li>Get to a dentist immediately.</li>
    </ul>
    <p>
      Baby teeth are the exception: a knocked-out milk tooth should <em>not</em> be replanted,
      because doing so can damage the adult tooth developing above it. Still get the child
      seen.
    </p>

    <h2>Severe toothache</h2>
    <p>
      Ordinary painkillers taken as directed on the packet, and a cold compress against the
      cheek. Keep your head elevated — lying flat increases blood pressure in the tooth and is
      why dental pain so reliably worsens at night.
    </p>
    <p>
      <strong>Never hold an aspirin against the gum.</strong> It is an acid and burns the
      tissue, which leaves you with a chemical burn on top of the toothache. Clove oil is a
      reasonable short-term measure on the tooth itself, but keep it off the gum.
    </p>

    <h2>Facial swelling</h2>
    <p>
      Swelling means infection has moved out of the tooth and into the surrounding tissue.
      This is the symptom we treat most urgently, because the space it spreads into next
      matters a great deal.
    </p>
    <p>
      Painkillers will mask it. They will not stop it. An abscess needs the source dealt with —
      drainage, root canal treatment, or extraction — and antibiotics alone are a delaying
      measure, not a cure. If the swelling is growing quickly, do not wait for an appointment
      slot; call.
    </p>

    <h2>A broken or chipped tooth</h2>
    <p>
      Rinse your mouth with warm water and keep any fragment — it can sometimes be bonded back
      on. If a sharp edge is cutting your tongue or cheek, a piece of sugar-free chewing gum
      pressed over it is a serviceable temporary cover.
    </p>
    <p>
      A chip in the enamel can usually wait a day or two. A break that exposes pink or red
      tissue in the middle of the tooth has reached the nerve and needs seeing quickly.
    </p>

    <h2>A lost filling or crown</h2>
    <p>
      Rarely a true emergency, but do not leave it long — the tooth underneath is unprotected
      and can decay or fracture quickly. Keep the crown if you have it; it can often be
      recemented. Avoid chewing on that side and keep the area clean.
    </p>

    <h2>Bleeding that will not stop after an extraction</h2>
    <p>
      Some oozing for several hours is normal. For active bleeding, bite firmly on a clean
      rolled gauze or a damp cloth for a full twenty minutes without lifting it to check —
      checking every two minutes is the most common reason it will not stop. Avoid rinsing,
      spitting and hot drinks for the rest of the day. If it is still bleeding heavily after
      that, call us.
    </p>""",
 "faqs": [
  ("What counts as a dental emergency?",
   "Severe or worsening pain, facial swelling, a knocked-out or broken tooth, and bleeding that will not stop. Swelling that is spreading toward the eye or neck, or affecting swallowing or breathing, needs a hospital emergency department rather than a dental clinic."),
  ("Can I get same-day dental treatment in Allahabad?",
   "Dental Zone in Lukarganj treats emergencies as priority cases and does its best to see you the same day. Call 094506 29270 directly rather than booking online, so we can advise you immediately."),
  ("What should I do if my tooth is knocked out?",
   "Hold it by the crown, never the root. Rinse briefly in milk if dirty, then put it back in the socket if you can and bite gently on a cloth. If you cannot, keep it in milk or the patient's saliva — never water — and get to a dentist within the hour."),
  ("How do I stop severe tooth pain at night?",
   "Take ordinary painkillers as directed, apply a cold compress to the cheek, and keep your head elevated with extra pillows — lying flat raises pressure in the tooth, which is why dental pain worsens at night. Never place aspirin against the gum; it causes a chemical burn."),
 ],
},
]

os.makedirs(OUT, exist_ok=True)
for s in SERVICES:
    others = [o for o in SERVICES if o["slug"] != s["slug"]][:3]
    html = page(s, others)
    path = os.path.join(OUT, s["slug"] + ".html")
    io.open(path, "w", encoding="utf-8").write(html)
    words = len(" ".join(s["body"].split()).split())
    print(f"  {s['slug']:<38} {len(html)//1024:>3} KB  ~{words} words body")
print(f"\n{len(SERVICES)} service pages written to {OUT}")
