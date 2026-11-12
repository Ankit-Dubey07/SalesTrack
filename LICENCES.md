# SalesTrack website: third-party licences and originality record

Last reviewed: 12 November 2026

## 1. What was written for this project

| Item | Source |
|---|---|
| HTML structure, page templates, `build.py` | Written for SalesTrack. No theme, template or page builder used. |
| CSS (`assets/css/styles.css`) | Written for SalesTrack. No CSS framework. |
| JavaScript (`assets/js/main.js`) | Written for SalesTrack. No libraries or frameworks. |
| Page copy | The client's own text. Headings, button labels and form wording were written for this site, based on that text. |
| Hero "prospect → team" diagram, favicon, section graphics | Drawn in code for this site. |
| Colour palette | Taken from the client's SalesTrack logo. |

The site is a static HTML/CSS/JS website. It doesn't track visitors, it loads nothing from Google or any other company's servers, and it sets no cookies or browser storage.

### Use of the reference website

callboxinc.co.uk was used only as a reference for general layout ideas that most service websites share, such as a hero with a call to action, service cards and a contact section. None of its text, code, images, icons, illustrations, logo or brand identity was used. Its colour scheme, fonts and illustrations were **not** reused.

## 2. Third-party resources

| Resource | Version | Licence | Commercial use | Where used | Licence text |
|---|---|---|---|---|---|
| League Spartan (font) | Fontsource 5.3.0 | SIL Open Font License 1.1 | Yes | Headings | `assets/licences/OFL-League-Spartan.txt` |
| Manrope (font) | Fontsource 5.3.0 | SIL Open Font License 1.1 | Yes | Body text | `assets/licences/OFL-Manrope.txt` |
| JetBrains Mono (font) | Fontsource 5.3.0 | SIL Open Font License 1.1 | Yes | Small labels and the clock | `assets/licences/OFL-JetBrains-Mono.txt` |
| Feather Icons | 4.29.2 | MIT | Yes, licence notice kept | Some icon outlines (e.g. phone, link) are adapted from Feather | `assets/licences/MIT-Feather-Icons.txt` |
| Lucide | 0.400.0 | ISC | Yes, licence notice kept | Some icon outlines (e.g. chat, lightbulb) follow Lucide/Feather conventions | `assets/licences/ISC-Lucide.txt` |

**Notes on these resources**
- **Fonts:** the font files are hosted with the site, in `assets/fonts/`. The OFL allows them to be embedded and used commercially, but the fonts must not be sold on their own. The licence files must stay with the font files.
- **Icons:** the icons are drawn as simple lines. Because a few are adapted from Feather and Lucide, those licence notices are kept as a precaution, whether or not every icon would need one.

No stock photos, AI-generated images, paid templates, or unlicensed fonts or images are used.

## 3. Check before launch

These items need checking by the business owner. This record is not legal advice and does not guarantee that the site is free of every possible copyright or trademark claim.

1. **Logo ownership.** The logo files (`salestrack-logo.png`, `salestrack-logo-white.png`) were supplied by the client and only had their backgrounds removed and colours adjusted. Confirm who designed the logo and that SalesTrack owns it or has a written licence to use it. If a designer or a design or AI tool made it, check that tool's terms for commercial use.
2. **"SalesTrack" name and trademark.** Before launch, search the UK IPO trademark register (and the Indian TMR and EUIPO, if you trade there) for "SalesTrack" and similar names in classes 35 (business and marketing services) and 38 (telecommunications). Software and service companies may already use similar names. A trademark attorney can do a formal clearance search.
3. **Domain.** The site assumes `www.salestrack.co.in`. Update `SITE_URL` in `build.py` if the domain is different.
4. **Business claims.** Claims such as "International market expertise" and "Experienced and professionally trained teams" come from the client's own text. Under UK consumer and advertising rules (CAP Code), the business should be able to back them up.
5. **Privacy notice (UK GDPR).** The contact form collects a name, email address, phone number and company name, and they reach SalesTrack by email. Before launch, add a privacy notice covering:
   - who the controller is
   - what data is collected, why, and the legal basis
   - how long it is kept
   - visitors' rights
   - contact details

   Also check whether the business must pay the ICO data protection fee. The notice needs the business's legal name and address, which the site doesn't have yet.
6. **Company details.** If SalesTrack is a UK limited company, the Companies Act disclosure rules require the registered name, company number and registered office address on the website.
7. **Future additions.** Any testimonials, client logos, case studies, photos or statistics must be real, used with permission, and properly licensed.
