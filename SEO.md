# Dental Zone — SEO status

Target queries: **best dentist in Allahabad**, best dentist in Prayagraj,
dental clinic in Lukarganj, root canal / implant cost in Allahabad.

Live at <https://dentalzoneprayagraj.in> (Cloudflare Pages, auto-deploys on
push to `main`).

---

## Done — on the site

| Area | State |
|---|---|
| Title / meta description | Targeted at "best dentist in Allahabad (Prayagraj)" |
| H1 | Carries **both** city names — Allahabad and Prayagraj |
| Canonical, OG, Twitter | All on `dentalzoneprayagraj.in` |
| `lang` | `en-IN` |
| Structured data | `Dentist` + `Physician` + `FAQPage`, 9 Q&As, all matching visible text |
| Rating markup | 4.6 / 199 — matches Google exactly |
| Geo | Retriangulated onto GT Road, Lukarganj (was 1.7 km off, in Chowk) |
| Sitemap + robots | Present, valid, image entries included |
| Favicons | Full set + web manifest, from the clinic logo |
| 404 page | Real page, `noindex`, returns a true 404 |
| Images | 2229 KB → 1224 KB; lazy-loaded; intrinsic dimensions set (CLS) |
| Render blocking | GSAP deferred; hero portrait preloaded as the LCP element |
| Caching | `_headers` — images cached 1 year immutable |
| Content | Local "why us" section, 12 locality mentions, treatment-cost section |
| IndexNow | Submitted — Bing + Yandex notified (HTTP 202) |

---

## Only you can do these — and they matter more than everything above

For "best dentist in allahabad", the **Google map pack sits above every organic
result**. It is ranked by your Google Business Profile, not by this website.
The site alone cannot get you into it.

In order of impact:

### 1. Google Business Profile — the single biggest lever
<https://business.google.com>
- Claim and verify the listing if you haven't
- Primary category **Dentist**; add secondary categories (Dental clinic,
  Dental implants periodontist, Orthodontist)
- List every service, set hours, add the website URL
- **Upload real photos monthly.** Profiles with fresh photos rank better
- Post updates — offers, cases, festival hours

### 2. Reviews — the strongest ranking signal you control
You have 199 at 4.6. Competitors ranking above you likely have more.
- Ask every satisfied patient, at the chair, before they leave
- Get the short link: Business Profile → **Ask for reviews** → copy
- Print it as a QR code at reception
- **Reply to every review**, good and bad. Google measures response rate
- Going 199 → 400 will move you more than any further code change

> Never buy reviews. Google detects it and it can delist you entirely.

### 3. Google Search Console — 10 minutes, do it first thing
<https://search.google.com/search-console>
- Add property `dentalzoneprayagraj.in`, verify by DNS (you're on Cloudflare,
  so it's a TXT record — easy)
- Submit `https://dentalzoneprayagraj.in/sitemap.xml`
- URL Inspection → paste the homepage → **Request Indexing**

Without this, Google finds the new content on its own schedule — often weeks.

### 4. Consistent NAP across directories
Name / Address / Phone must match the site **character for character** on
Practo, JustDial, Lybrate, Sulekha, Facebook, Apple Maps. Mismatches actively
hurt local ranking. Use exactly:

```
Dental Zone — Super Speciality Dental Hospital
26/17/3, Grand Trunk Rd, near Geetanjali Apartments,
opposite Luvkush Colony, Lukarganj, Prayagraj, Uttar Pradesh 211003
094506 29270
https://dentalzoneprayagraj.in
```

---

## Still needs an answer from you

1. **Opening hours conflict.** Site and schema say Mon–Sat 10:00–20:00. Your
   Google listing says *opens 10:30*. Google cross-checks these. Fix whichever
   is wrong — mismatch damages local trust signals.
2. **Exact coordinates.** Current geo is triangulated to a few hundred metres.
   Right-click your pin in Google Maps; the first menu item is the precise
   lat/long. Replace it in the JSON-LD and the `geo.position` meta.
3. **Real photos.** The gallery has only three genuine clinic photographs.
   Reception, waiting area, sterilisation setup and exterior signage would all
   help — a phone camera is fine. Two images in the oral-health section are
   licensed stock, clearly captioned as illustrative; swap them when you can.

---

## Realistic timeline

- **Days 1–3** — Google recrawls; title and description update in results
- **Week 1–2** — rich results (stars, FAQ dropdowns) may start appearing
- **Week 3–8** — ranking movement for long-tail queries ("root canal cost in
  Prayagraj", "dentist in Lukarganj")
- **Month 3–6** — competitive movement on "best dentist in Allahabad", and
  only if the Business Profile and review count are being worked in parallel

Nobody ranks #1 for a competitive local term overnight, and any service that
promises otherwise is selling link spam that will get you penalised.
