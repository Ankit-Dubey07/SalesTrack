#!/usr/bin/env python3
"""SalesTrack static site builder. Original code written for SalesTrack (see LICENCES.md for third-party notices).
Shared components (head, header, footer, CTA, icons) live here; each page supplies its own <main>.
Run: python3 build.py  ->  writes ./dist (hostable site)."""
import json, shutil, pathlib

ROOT = pathlib.Path(__file__).parent
SRC, DIST = ROOT / "src", ROOT / "dist"
SITE_URL = "https://www.salestrack.co.in"  # update if the domain differs
EMAIL = "info@salestrack.co.in"
# Google Apps Script web app URL (apps-script/SETUP.md). Empty = form falls back to opening the visitor's email app.
FORM_ENDPOINT = "https://script.google.com/macros/s/AKfycbwOsVqzexVTQK0IEjZN9ywtNqK57M6s2IA3q4YjdpKrFP-yOH37a-nXgj7f7NMzTFer/exec"
ADDRESS_LINES = ["Daffodil, 5th Floor", "Opposite Sahas Cricket Club", "Nagpur, Maharashtra 440015", "India"]
ADDRESS = ", ".join(ADDRESS_LINES)

# ---------------------------------------------------------------- icons (24px line icons)
P = {
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5" fill="currentColor"/>',
    "users": '<path d="M16 20v-1.5a3.5 3.5 0 0 0-3.5-3.5h-5A3.5 3.5 0 0 0 4 18.5V20"/><circle cx="10" cy="8" r="3.5"/><path d="M20 20v-1.5a3.5 3.5 0 0 0-2.5-3.35M15.5 4.6a3.5 3.5 0 0 1 0 6.8"/>',
    "phone": '<path d="M21 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 1.1 4.2 2 2 0 0 1 3.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L7 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
    "transfer": '<path d="M4 8h13l-3-3M20 16H7l3 3"/>',
    "layers": '<path d="m12 3 9 5-9 5-9-5 9-5z"/><path d="m3 13 9 5 9-5"/>',
    "headset": '<path d="M4 14v-2a8 8 0 0 1 16 0v2"/><rect x="2.5" y="13" width="4" height="6" rx="1.5"/><rect x="17.5" y="13" width="4" height="6" rx="1.5"/><path d="M19.5 19a3 3 0 0 1-3 3H13"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/>',
    "chat": '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/>',
    "filter": '<path d="M3 5h18l-7 8v6l-4 2v-8L3 5z"/>',
    "handshake": '<path d="m11 17 2 2a1.4 1.4 0 0 0 2-2"/><path d="m14 14 2.5 2.5a1.4 1.4 0 0 0 2-2L15 11l-1.5 1.5a2.1 2.1 0 0 1-3-3L13 7l-1.6-1.2a3 3 0 0 0-3.4-.1L3 9"/><path d="m21 9-4.2-3.4a3 3 0 0 0-3.4 0L13 7"/><path d="M3 9v5l5.5 5.5a1.4 1.4 0 0 0 2-2"/><path d="M21 9v5l-2.5 2.5"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
    "award": '<circle cx="12" cy="9" r="6"/><path d="m8.5 14-1.5 8 5-3 5 3-1.5-8"/>',
    "check-badge": '<path d="M12 2.5 14.6 4l3 .2.9 2.9 2.2 2-1 2.9 1 2.9-2.2 2-.9 2.9-3 .2L12 21.5 9.4 20l-3-.2-.9-2.9-2.2-2 1-2.9-1-2.9 2.2-2 .9-2.9 3-.2z"/><path d="m8.5 12 2.5 2.5 4.5-5"/>',
    "scale": '<path d="M3 20h18M5 20V10M10 20V4M15 20v-7M20 20V8"/>',
    "eye": '<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    "link": '<path d="M10 14a5 5 0 0 0 7.1 0l3-3a5 5 0 0 0-7.1-7.1l-1.2 1.2"/><path d="M14 10a5 5 0 0 0-7.1 0l-3 3A5 5 0 0 0 11 20.1l1.2-1.2"/>',
    "lightbulb": '<path d="M9 18h6M10 22h4"/><path d="M12 2a7 7 0 0 0-4 12.7c.6.5 1 1.3 1 2.1V17h6v-.2c0-.8.4-1.6 1-2.1A7 7 0 0 0 12 2z"/>',
    "growth": '<path d="m3 17 6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "chev": '<path d="m6 9 6 6 6-6"/>',
    "up": '<path d="M12 19V5M6 11l6-6 6 6"/>',
    "check": '<path d="m5 12 5 5 9-10"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "copy": '<rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15V5a2 2 0 0 1 2-2h10"/>',
    "flag": '<path d="M5 21V4M5 4h11l-2 4 2 4H5"/>',
    "rocket": '<path d="M5 15c-1.5 1.5-2 5-2 5s3.5-.5 5-2"/><path d="M14.5 4.5C17 2 21 3 21 3s1 4-1.5 6.5L13 16l-5-5 6.5-6.5z"/><path d="M8 11 5 10l3-3h4M13 16l1 3 3-3v-4"/>',
    "building": '<rect x="4" y="3" width="16" height="18" rx="1.5"/><path d="M9 7h1M14 7h1M9 11h1M14 11h1M9 15h1M14 15h1M10 21v-3h4v3"/>',
}
# Several icon outlines are adapted from Feather Icons (MIT) / Lucide (ISC); notices in assets/licences/.
def icon(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{P[name]}</svg>'
ARROW = icon("arrow")

SERVICES = [
    dict(id="lead-generation", name="Lead Generation", icon="target",
         short="Targeted customer acquisition and qualified prospect generation.",
         goal="Connecting your business with the right opportunities."),
    dict(id="b2c-sales", name="B2C Sales Solutions", icon="users",
         short="Customer engagement and sales conversion support.",
         goal="Turning customer interactions into valuable business relationships."),
    dict(id="live-transfer", name="Live Transfer Solutions", icon="transfer",
         short="Connecting qualified prospects with businesses in real time.",
         goal="Delivering meaningful connections at the right time."),
    dict(id="bpo", name="BPO Services", icon="layers",
         short="Scalable outsourcing solutions designed around business requirements.",
         goal="Making business operations simpler, smarter and more efficient."),
]

WHY = [
    ("globe", "International market expertise."),
    ("award", "Experienced and professionally trained teams."),
    ("check-badge", "Quality-focused lead generation."),
    ("scale", "Scalable business operations."),
    ("eye", "Transparent communication."),
    ("handshake", "Long-term business partnerships."),
]


# ---------------------------------------------------------------- photos (client-supplied; see LICENCES.md)
PHOTOS = {
    "team-meeting": dict(widths=[668], w=668, h=381,
        alt="A business team discussing plans around a glass table in a bright office"),
    "sales-team": dict(widths=[600, 900], w=900, h=600,
        alt="Smiling sales professionals wearing headsets, working at their desks"),
    "lead-generation": dict(widths=[748], w=748, h=498,
        alt="Illustration of the lead generation process: attracting prospects, filtering them through a funnel and turning them into business growth"),
}
def photo(name, sizes="(max-width: 860px) 100vw, 50vw", cls="media"):
    d = PHOTOS[name]
    ss = lambda ext: ", ".join(f"assets/img/photos/{name}-{w}.{ext} {w}w" for w in d["widths"])
    big = max(d["widths"])
    return (f'<figure class="{cls}"><picture>'
            f'<source type="image/webp" srcset="{ss("webp")}" sizes="{sizes}">'
            f'<img src="assets/img/photos/{name}-{big}.jpg" srcset="{ss("jpg")}" sizes="{sizes}" '
            f'width="{d["w"]}" height="{d["h"]}" alt="{d["alt"]}" loading="lazy" decoding="async">'
            f'</picture></figure>')

# ---------------------------------------------------------------- shared components
PREVIEW_META = '<meta name="claude:viewport-fit-sides" content="cover">\n'
FONTS = ('<link rel="preload" href="assets/fonts/league-spartan-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>\n'
         '<link rel="preload" href="assets/fonts/manrope-latin-500-normal.woff2" as="font" type="font/woff2" crossorigin>\n'
         '<link rel="stylesheet" href="assets/css/fonts.css">')

def head(page, bare=False):
    url = SITE_URL + "/" + ("" if page["file"] == "index.html" else page["file"])
    ld = {
        "@context": "https://schema.org", "@type": "Organization", "name": "SalesTrack",
        "slogan": "Lead. Connect. Grow.", "url": SITE_URL, "email": EMAIL,
        "address": {"@type": "PostalAddress", "streetAddress": "Daffodil, 5th Floor, Opposite Sahas Cricket Club",
                    "addressLocality": "Nagpur", "addressRegion": "Maharashtra", "postalCode": "440015", "addressCountry": "IN"},
        "logo": SITE_URL + "/assets/img/salestrack-logo.png",
        "description": "Lead generation, B2C sales, live transfer and BPO services.",
        "contactPoint": {"@type": "ContactPoint", "email": EMAIL, "contactType": "sales",
                         "hoursAvailable": {"@type": "OpeningHoursSpecification",
                                            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                                            "opens": "14:30", "closes": "23:00"}},
    }
    return f'''<title>{page["title"]}</title>
{PREVIEW_META if bare else ""}<meta name="description" content="{page["desc"]}">
<meta name="theme-color" content="#0e2559">
<link rel="canonical" href="{url}">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:site_name" content="SalesTrack">
<meta property="og:title" content="{page["title"]}">
<meta property="og:description" content="{page["desc"]}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE_URL}/assets/img/salestrack-logo.png">
<meta name="twitter:card" content="summary_large_image">
{FONTS}
<link rel="stylesheet" href="assets/css/styles.css">
<script type="application/ld+json">{json.dumps(ld)}</script>'''

def header(active):
    def cur(k): return ' aria-current="page"' if k == active else ""
    dd = "".join(
        f'<a href="services.html#{s["id"]}"><span class="ic">{icon(s["icon"])}</span><span><strong>{s["name"]}</strong><span>{s["short"]}</span></span></a>'
        for s in SERVICES)
    return f'''<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap nav">
    <a class="brand" href="./" aria-label="SalesTrack home"><img src="assets/img/salestrack-logo-white.png" alt="SalesTrack — Lead. Connect. Grow." width="1295" height="338"></a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="nav-menu" aria-label="Open menu"><span></span></button>
    <nav id="nav-menu" class="nav-menu" aria-label="Main">
      <a class="nav-link" href="./"{cur("home")}>Home</a>
      <div class="nav-item has-dropdown">
        <button class="nav-link" type="button" aria-expanded="false" aria-haspopup="true"{' aria-current="page"' if active == "services" else ""}>Services {icon("chev", "chev")}</button>
        <div class="dropdown">{dd}<a href="services.html"><span class="ic">{icon("arrow")}</span><span><strong>All services</strong><span>See how each service works</span></span></a></div>
      </div>
      <a class="nav-link" href="about.html"{cur("about")}>About</a>
      <a class="nav-link" href="contact.html"{cur("contact")}>Contact</a>
      <a class="btn nav-cta" href="contact.html">Let's talk {ARROW}</a>
    </nav>
  </div>
</header>'''

def footer():
    svc = "".join(f'<li><a href="services.html#{s["id"]}">{s["name"]}</a></li>' for s in SERVICES)
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <a class="brand" href="./" aria-label="SalesTrack home"><img src="assets/img/salestrack-logo-white.png" alt="SalesTrack" width="1295" height="338" loading="lazy"></a>
        <p>Our focus is simple: quality connections, smarter solutions and sustainable growth.</p>
        <p class="footer-tag">Lead. Connect. <span>Grow.</span></p>
      </div>
      <div><h2>Services</h2><ul>{svc}</ul></div>
      <div><h2>Company</h2><ul><li><a href="./">Home</a></li><li><a href="about.html">About us</a></li><li><a href="about.html#mission">Our mission</a></li><li><a href="contact.html">Contact</a></li><li><a href="privacy.html">Privacy notice</a></li></ul></div>
      <div><h2>Get in touch</h2><ul>
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li>Monday – Friday</li>
        <li>2:30 PM – 11:00 PM IST</li>
        <li><address class="footer-address">{"<br>".join(ADDRESS_LINES)}</address></li>
      </ul></div>
    </div>
    <div class="footer-bottom"><span>© <span data-year>2026</span> SalesTrack. All rights reserved.</span><span>Lead generation · Sales support · Outsourcing</span></div>
  </div>
</footer>
<button class="to-top" type="button" aria-label="Back to top">{icon("up")}</button>'''

def cta_band(title="Let's Grow Together.", text="Looking for a reliable lead generation or outsourcing partner? SalesTrack is ready to help your business reach new customers, build stronger connections and unlock new growth opportunities."):
    return f'''<section class="cta-band" aria-labelledby="cta-title">
  <div class="wrap">
    <div class="cta-card reveal">
      <div>
        <span class="eyebrow">Let's start a conversation</span>
        <h2 id="cta-title">{title}</h2>
        <p>{text}</p>
      </div>
      <div class="actions">
        <a class="btn" href="contact.html">Let's start a conversation {ARROW}</a>
      </div>
    </div>
  </div>
</section>'''

def why_grid():
    items = "".join(f'<li class="why-item reveal" data-delay="{i%3}"><span class="ic">{icon(ic)}</span><h3>{t}</h3></li>' for i, (ic, t) in enumerate(WHY))
    return f'<ul class="why-grid">{items}</ul>'

def page_hero(crumb, eyebrow, title, lede):
    return f'''<section class="page-hero on-ink">
  <div class="wrap hero-load">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="./">Home</a><span aria-hidden="true">/</span><span>{crumb}</span></nav>
    <span class="eyebrow">{eyebrow}</span>
    <h1>{title}</h1>
    <p class="lede">{lede}</p>
  </div>
</section>'''

# ---------------------------------------------------------------- pages
def home():
    cards = "".join(f'''<a class="service-card reveal" data-delay="{i%2}" href="services.html#{s["id"]}">
      <span class="ic">{icon(s["icon"])}</span><h3>{s["name"]}</h3><p>{s["short"]}</p>
      <span class="text-link">Learn more {ARROW}</span></a>''' for i, s in enumerate(SERVICES))
    return f'''
<section class="hero on-ink" aria-labelledby="hero-title">
  <div class="wrap hero-grid">
    <div class="hero-load">
      <span class="eyebrow">Lead. Connect. Grow.</span>
      <h1 id="hero-title">Turning every opportunity into <em>business growth.</em></h1>
      <p class="lede">We are a results-driven lead generation and customer engagement company dedicated to helping businesses attract potential customers, build meaningful relationships and accelerate growth.</p>
      <div class="hero-actions">
        <a class="btn" href="contact.html">Let's start a conversation {ARROW}</a>
        <a class="btn btn-ghost" href="services.html">Explore our services</a>
      </div>
      <ul class="tagline-chips" aria-label="Our focus"><li>Quality connections</li><li>Smarter solutions</li><li>Sustainable growth</li></ul>
    </div>
    <aside class="pipeline" aria-label="How a live transfer reaches your team">
      <div class="pipeline-top"><p>From prospect to your team</p><span class="live-pill"><i></i>Real time</span></div>
      <ol class="steps">
        <li class="step"><span class="node">{icon("search")}</span><div><strong>Engage prospects</strong><span>Reach the right audience</span></div></li>
        <li class="step"><span class="node">{icon("chat")}</span><div><strong>Understand requirements</strong><span>Learn what each customer needs</span></div></li>
        <li class="step"><span class="node">{icon("filter")}</span><div><strong>Assess suitability</strong><span>Structured lead qualification</span></div></li>
        <li class="step final"><span class="node">{icon("phone")}</span><div><strong>Live transfer to your sales team</strong><span>Connected at the right time</span></div></li>
      </ol>
      <p class="pipeline-foot"><b>Fewer unnecessary conversations.</b> More relevant prospects for your business.</p>
    </aside>
  </div>
</section>

<section class="focus-strip" aria-label="Our focus">
  <div class="wrap">
    <p>Our focus is simple</p>
    <ul class="focus-list"><li>{icon("link")}Quality connections</li><li>{icon("lightbulb")}Smarter solutions</li><li>{icon("growth")}Sustainable growth</li></ul>
  </div>
</section>

<section class="section" aria-labelledby="intro-title">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">Who we are</span>
      <h2 id="intro-title">Every successful business begins with the right connection.</h2>
      {photo("team-meeting", "(max-width: 860px) 100vw, 520px", "media intro-media")}
    </div>
    <div class="prose reveal" data-delay="1">
      <p>We specialise in delivering <strong>high-quality lead generation, customer acquisition, sales support and business process solutions</strong> tailored to the unique needs of our clients.</p>
      <p>By combining skilled professionals, strategic marketing approaches and technology-driven processes, we help businesses reach the right audience and turn opportunities into measurable results.</p>
      <a class="text-link" href="about.html">More about SalesTrack {ARROW}</a>
    </div>
  </div>
</section>

<section class="section bg-surface" aria-labelledby="svc-title">
  <div class="wrap">
    <div class="head-split">
      <div class="section-head reveal">
        <span class="eyebrow">Our core services</span>
        <h2 id="svc-title">Four ways we move your business forward.</h2>
        <p class="lede">From the first conversation to the final handover, each service is tailored to your business requirements.</p>
      </div>
      <div class="reveal" data-delay="1">{photo("lead-generation", "(max-width: 860px) 100vw, 560px", "media media-illustration")}</div>
    </div>
    <div class="service-grid">{cards}</div>
  </div>
</section>

<section class="section on-ink" aria-labelledby="approach-title">
  <div class="wrap">
    <div class="head-split">
      <div class="section-head reveal">
        <span class="eyebrow">Our approach</span>
        <h2 id="approach-title">Targeted outreach. Real engagement. Qualified results.</h2>
        <p class="lede">Our approach combines targeted outreach, customer engagement and structured lead qualification to help you build a consistent sales pipeline.</p>
      </div>
      <div class="reveal" data-delay="1">{photo("sales-team", "(max-width: 860px) 100vw, 560px", "media media-dark")}</div>
    </div>
    <ol class="approach">
      <li class="reveal"><h3>Reach the right audience</h3><p>We identify and attract potential customers through strategic, targeted outreach.</p></li>
      <li class="reveal" data-delay="1"><h3>Understand their needs</h3><p>Our trained professionals engage with prospects and understand customer requirements.</p></li>
      <li class="reveal" data-delay="2"><h3>Qualify every lead</h3><p>Structured lead qualification means you spend time only on genuine business opportunities.</p></li>
      <li class="reveal" data-delay="3"><h3>Connect and convert</h3><p>We connect you with relevant prospects, helping turn opportunities into measurable results.</p></li>
    </ol>
  </div>
</section>

<section class="section" aria-labelledby="why-title">
  <div class="wrap">
    <div class="section-head center reveal">
      <span class="eyebrow">Why choose SalesTrack?</span>
      <h2 id="why-title">A partner built for quality and long-term growth.</h2>
    </div>
    {why_grid()}
  </div>
</section>

<section class="section bg-surface" aria-labelledby="who-title">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Who we work with</span>
      <h2 id="who-title">SalesTrack is here to move your business forward.</h2>
    </div>
    <div class="audience">
      <article class="reveal"><span class="tag">Growing businesses</span><h3>Expand your customer base.</h3><p>Reach new customers and build a consistent sales pipeline with targeted lead generation and sales support.</p><a class="text-link" href="services.html#lead-generation">See Lead Generation {ARROW}</a></article>
      <article class="reveal" data-delay="1"><span class="tag">Established organisations</span><h3>A reliable outsourcing partner.</h3><p>Streamline operations, improve productivity and focus on your core business with flexible, scalable outsourcing.</p><a class="text-link" style="color:var(--accent)" href="services.html#bpo">See BPO Services {ARROW}</a></article>
    </div>
  </div>
</section>

<section class="section tight on-ink mission" aria-label="Our mission">
  <div class="wrap reveal">
    <span class="eyebrow">Our mission</span>
    <blockquote><p>To empower businesses with reliable lead generation and outsourcing solutions that create <mark>meaningful connections, measurable results and long-term growth.</mark></p></blockquote>
  </div>
</section>
{cta_band()}'''

SVC_DETAIL = {
    "lead-generation": dict(
        lead="We help businesses identify, attract and connect with potential customers through strategic and targeted lead generation solutions.",
        paras=["At SalesTrack, we focus on reaching the right audience, understanding customer requirements and generating quality prospects that create genuine business opportunities.",
               "Our approach combines targeted outreach, customer engagement and structured lead qualification to help businesses build a consistent sales pipeline, improve customer acquisition and achieve sustainable growth."],
        list_title="What you get", chips=["Targeted outreach", "Customer engagement", "Structured lead qualification", "A consistent sales pipeline"]),
    "b2c-sales": dict(
        lead="At SalesTrack, we help businesses connect directly with consumers through professional and result-oriented B2C sales solutions.",
        paras=["Our trained sales professionals engage with potential customers, understand their needs, explain relevant products and services, and guide them through the customer journey.",
               "From initial customer interaction to sales conversion, we focus on delivering a professional customer experience while helping our clients increase engagement, improve conversion rates and grow their customer base."],
        list_title="The customer journey we manage",
        flow=["Engage potential customers", "Understand their needs", "Present the Right Solutions", "Drive Successful Conversions"]),
    "live-transfer": dict(
        lead="We specialise in live transfer solutions that connect businesses with interested and qualified potential customers in real time.",
        paras=["Our process involves engaging prospects, understanding their requirements and assessing their suitability before transferring the call to the relevant business or sales representative.",
               "By reducing unnecessary conversations and connecting businesses with relevant prospects, our live transfer solutions help improve sales efficiency, optimise conversion opportunities and make customer acquisition more effective."],
        list_title="How a live transfer works",
        flow=["Engage the prospect", "Understand requirements", "Assess suitability", "Transfer to your team"]),
    "bpo": dict(
        lead="SalesTrack provides flexible and scalable business process outsourcing solutions that help organisations streamline operations, improve productivity and focus on their core business activities.",
        paras=["With trained professionals, structured workflows and a quality-focused approach, we deliver outsourcing solutions tailored to each client's operational requirements.",
               "Whether you are a startup, growing business or established organisation, we help you build efficient operations while managing resources effectively."],
        list_title="Our BPO services include", chips=["Customer support", "Outbound calling", "Inbound calling", "Sales operations", "Customer engagement", "Lead management"]),
}

def services():
    tabs = "".join(f'<li><a href="#{s["id"]}">{icon(s["icon"])}{s["name"]}</a></li>' for s in SERVICES)
    blocks = []
    for i, s in enumerate(SERVICES):
        d = SVC_DETAIL[s["id"]]
        paras = "".join(f"<p>{p}</p>" for p in d["paras"])
        if "chips" in d:
            extra = '<ul class="chips">' + "".join(f"<li>{icon('check')}{c}</li>" for c in d["chips"]) + "</ul>"
        else:
            extra = '<ol class="flow">' + "".join(f"<li><span>Step {n+1}</span>{c}</li>" for n, c in enumerate(d["flow"])) + "</ol>"
        full = "Business Process Outsourcing (BPO)" if s["id"] == "bpo" else s["name"]
        blocks.append(f'''<section class="svc" id="{s["id"]}" aria-labelledby="{s["id"]}-title">
  <div class="wrap svc-grid">
    <div class="svc-aside reveal">
      <span class="svc-index">Service {i+1} of 4</span>
      <span class="ic">{icon(s["icon"])}</span>
      <h2 id="{s["id"]}-title">{full}</h2>
      <p class="summary">{s["short"]}</p>
      <div><a class="btn btn-ink" href="contact.html?service={s["id"]}">Enquire about this service {ARROW}</a></div>
    </div>
    <div class="svc-body reveal" data-delay="1">
      <p style="color:var(--text);font-size:var(--step-2);line-height:1.45;font-weight:600">{d["lead"]}</p>
      {photo("sales-team", "(max-width: 960px) 100vw, 640px") if s["id"] == "b2c-sales" else ""}
      {paras}
      <h3>{d["list_title"]}</h3>
      {extra}
      <div class="goal"><span class="ic">{icon("flag")}</span><div><small>Our goal</small><p>{s["goal"]}</p></div></div>
    </div>
  </div>
</section>''')
    return page_hero("Services", "Our core services", "Solutions built around your business.",
                     "High-quality lead generation, customer acquisition, sales support and business process solutions, tailored to the unique needs of every client.") + f'''
<nav class="svc-tabs" aria-label="Services on this page"><div class="wrap"><ul>{tabs}</ul></div></nav>
{"".join(blocks)}
{cta_band("Not sure which service fits?", "Tell us about your business and goals. We'll recommend the right mix of lead generation, sales and outsourcing support.")}'''

def about():
    return page_hero("About", "About SalesTrack", "We believe every successful business begins with the right connection.",
                     "SalesTrack is a results-driven lead generation and customer engagement company.") + f'''
<section class="section" aria-labelledby="story-title">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">Our story</span>
      <h2 id="story-title">Turning every opportunity into business growth.</h2>
    </div>
    <div class="prose reveal" data-delay="1">
      <p>At SalesTrack, we are dedicated to helping businesses <strong>attract potential customers, build meaningful relationships and accelerate growth.</strong></p>
      <p>We specialise in delivering high-quality lead generation, customer acquisition, sales support and business process solutions tailored to the unique needs of our clients.</p>
      <p>By combining skilled professionals, strategic marketing approaches and technology-driven processes, we help businesses reach the right audience and turn opportunities into measurable results.</p>
      <p class="pull">Whether you are a growing business looking to expand your customer base or an established organisation seeking a reliable outsourcing partner, SalesTrack is here to move your business forward.</p>
    </div>
  </div>
</section>

<section class="section on-ink" aria-labelledby="focus-title">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Our focus</span>
      <h2 id="focus-title">Our focus is simple.</h2>
    </div>
    <div class="pillars">
      <article class="pillar reveal"><span class="ic">{icon("link")}</span><h3>Quality connections</h3><p>Reaching the right audience and connecting your business with genuine opportunities.</p></article>
      <article class="pillar reveal" data-delay="1"><span class="ic">{icon("lightbulb")}</span><h3>Smarter solutions</h3><p>Skilled professionals, strategic marketing approaches and technology-driven processes.</p></article>
      <article class="pillar reveal" data-delay="2"><span class="ic">{icon("growth")}</span><h3>Sustainable growth</h3><p>Measurable results and long-term partnerships that keep your business moving forward.</p></article>
    </div>
  </div>
</section>

<section class="section bg-surface mission-light" id="mission" aria-labelledby="mission-title">
  <div class="wrap split">
    <div class="reveal"><span class="eyebrow">Our mission</span><h2 id="mission-title">Why we do what we do.</h2></div>
    <div class="reveal" data-delay="1"><p class="pull" style="font-size:var(--step-3)">To empower businesses with reliable lead generation and outsourcing solutions that create meaningful connections, measurable results and long-term growth.</p></div>
  </div>
</section>

<section class="section" aria-labelledby="why-title">
  <div class="wrap">
    <div class="section-head center reveal">
      <span class="eyebrow">Why choose SalesTrack?</span>
      <h2 id="why-title">What you can count on.</h2>
    </div>
    {why_grid()}
  </div>
</section>
{cta_band()}'''

def contact():
    opts = "".join(f'<option value="{s["id"]}">{s["name"]}</option>' for s in SERVICES)
    days = [(1, "Monday"), (2, "Tuesday"), (3, "Wednesday"), (4, "Thursday"), (5, "Friday"), (6, "Saturday"), (0, "Sunday")]
    week = "".join(f'<li data-day="{n}"><span>{d}</span>' + ('<span>2:30 PM – 11:00 PM</span>' if n in range(1, 6) else '<span class="closed">Closed</span>') + '</li>' for n, d in days)
    return page_hero("Contact", "Let's start a conversation", "Let's grow together.",
                     "Looking for a reliable lead generation or outsourcing partner? Tell us about your business and we'll get back to you during our working hours.") + f'''
<section class="section" aria-label="Contact SalesTrack">
  <div class="wrap contact-grid">
    <div class="form-card reveal">
      <h2>Send us an enquiry</h2>
      <p>All fields marked * are required. Please don't include website links.</p>
      <form id="enquiry-form" novalidate data-endpoint="{FORM_ENDPOINT}">
        <div class="hp" aria-hidden="true"><label for="website">Leave this field empty</label><input id="website" name="website" type="text" tabindex="-1" autocomplete="off"></div>
        <div class="form-grid">
          <div class="field"><label for="name">Full name *</label><input id="name" name="name" type="text" autocomplete="name" required maxlength="60" aria-describedby="name-err"><span class="err" id="name-err" role="alert"></span></div>
          <div class="field"><label for="email">Work email *</label><input id="email" name="email" type="email" autocomplete="email" inputmode="email" required maxlength="100" aria-describedby="email-err"><span class="err" id="email-err" role="alert"></span></div>
          <div class="field"><label for="phone">Phone *</label><input id="phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" required maxlength="20" placeholder="+91 98765 43210" aria-describedby="phone-err"><span class="err" id="phone-err" role="alert"></span></div>
          <div class="field"><label for="company">Company *</label><input id="company" name="company" type="text" autocomplete="organization" required maxlength="100" aria-describedby="company-err"><span class="err" id="company-err" role="alert"></span></div>
          <div class="field full"><label for="service">Service you're interested in *</label><select id="service" name="service" required aria-describedby="service-err"><option value="">Choose a service</option>{opts}<option value="not-sure">Not sure yet</option></select><span class="err" id="service-err" role="alert"></span></div>
          <div class="field full"><label for="message">How can we help? *</label><textarea id="message" name="message" required maxlength="2000" placeholder="Tell us about your business, your target customers and what you'd like to achieve." aria-describedby="message-err"></textarea><span class="err" id="message-err" role="alert"></span></div>
          <div class="field full"><div class="data-notice" id="data-notice"><strong>How we use your details.</strong> We use the details in this form only to reply to your enquiry and discuss the service you ask about. {"They are saved in our enquiry records (Google Sheets) and sent to our team by email, and we email you a confirmation." if FORM_ENDPOINT else "They reach us by email; nothing is stored on this website."} You can withdraw your consent or ask us to delete your details at any time by emailing <a href="mailto:{EMAIL}?subject=Privacy%20request">{EMAIL}</a>. Read the full <a href="privacy.html">Privacy Notice</a>.</div></div>
          <div class="field full"><label class="consent" for="consent"><input id="consent" name="consent" type="checkbox" aria-describedby="data-notice consent-err"><span>I have read the notice above and consent to SalesTrack using my details to respond to this enquiry. *</span></label><span class="err" id="consent-err" role="alert"></span></div>
          <div class="field full"><label class="consent" for="marketing"><input id="marketing" name="marketing" type="checkbox"><span>Optional: I'd also like occasional updates about SalesTrack services. I can unsubscribe at any time.</span></label></div>
        </div>
        <div class="form-actions"><button class="btn btn-ink" type="submit">Send enquiry {ARROW}</button><small>{"We reply Monday to Friday, 2:30 PM to 11:00 PM IST." if FORM_ENDPOINT else "Opens your email app with the details filled in."}</small></div>
        <div class="form-status" id="form-status" role="status" aria-live="polite" tabindex="-1"></div>
      </form>
    </div>

    <div class="info-stack">
      <div class="info-card dark reveal" data-delay="1">
        <span class="label">Business hours</span>
        <div class="status" data-status><i></i><span data-status-text>Monday – Friday, 2:30 PM – 11:00 PM IST</span></div>
        <div class="clock" data-ist-clock aria-label="Current time in India"></div>
        <ul class="week">{week}</ul>
        <p class="local-time" data-local-hours hidden></p>
      </div>
      <div class="info-card reveal" data-delay="2">
        <span class="label">Email us</span>
        <div class="email-row"><a href="mailto:{EMAIL}">{EMAIL}</a><button class="copy-btn" type="button" data-copy="{EMAIL}">{icon("copy")}<span>Copy</span></button></div>
        <p style="color:var(--muted)">For lead generation, sales support and outsourcing enquiries.</p>
      </div>
      <div class="info-card reveal" data-delay="3">
        <span class="label">Our office</span>
        <address class="office-address">{"<br>".join(ADDRESS_LINES)}</address>
      </div>
    </div>
  </div>
</section>'''

def privacy():
    return page_hero("Privacy notice", "Your data", "Privacy Notice",
                     "How SalesTrack collects, uses and protects personal data shared through this website, and how you can exercise your rights.") + f'''
<section class="section" aria-label="Privacy notice">
  <div class="wrap">
    <article class="legal">
      <p class="legal-meta">{"Version 3" if FORM_ENDPOINT else "Version 2"} · Last updated: 13 November 2026</p>

      <h2>1. Who we are</h2>
      <p>This website (salestrack.co.in) is operated by <strong>SalesTrack</strong>, {ADDRESS}. SalesTrack decides why and how your personal data is processed. Under India's Digital Personal Data Protection Act, 2023 (the "DPDP Act"), this makes us the <strong>Data Fiduciary</strong>.</p>
      <p><strong>Contact for data protection questions:</strong> <a href="mailto:{EMAIL}?subject=Privacy%20request">{EMAIL}</a> (subject line "Privacy request").</p>

      <h2>2. What we collect and why</h2>
      <div class="legal-table">
      <table>
        <thead><tr><th scope="col">Personal data</th><th scope="col">Why we use it</th><th scope="col">Basis</th><th scope="col">How long we keep it</th></tr></thead>
        <tbody>
          <tr><td>Enquiry form or email: name, email address, phone number, company name, service of interest and message</td><td>To reply to your enquiry, discuss the service you asked about and prepare a proposal</td><td>Your consent, given by ticking the consent box or by emailing us</td><td>Until your enquiry is resolved; longer only if you become a client or the law requires it</td></tr>
          <tr><td>Your choice about marketing updates</td><td>To send occasional updates about our services, only if you opted in</td><td>Your separate, optional consent</td><td>Until you unsubscribe or withdraw consent</td></tr>
          <tr><td>A record of your consent (the notice version and the date and time, {"saved with your enquiry record" if FORM_ENDPOINT else "included in your enquiry email"})</td><td>To show that you gave consent, as the DPDP Act requires</td><td>Legal obligation</td><td>For as long as we hold the enquiry it relates to</td></tr>
        </tbody>
      </table>
      </div>
      <p>{"When you submit the enquiry form, your details are sent over an encrypted connection to our enquiry records, which are kept in Google Sheets. We then send you a confirmation email and notify our team by email. Nothing is stored on the website itself." if FORM_ENDPOINT else "The enquiry form opens your own email app with your details filled in. Nothing is stored on this website; we receive your details only when you send that email."} We do not sell personal data, and we do not use it for automated decision-making or profiling.</p>

      <h2>3. Cookies and tracking</h2>
      <p>This website does <strong>not</strong> use cookies, analytics, advertising trackers, social media plug-ins or browser storage, and it loads no content from other websites. Our hosting provider processes basic technical data, such as IP addresses, to deliver and secure the website (see section 5).</p>

      <h2>4. Your consent and how to withdraw it</h2>
      <p>We ask for your consent before you send an enquiry, and marketing updates have a separate, optional box that is never pre-ticked. You can withdraw consent at any time, as easily as you gave it, by emailing <a href="mailto:{EMAIL}?subject=Privacy%20request">{EMAIL}</a>. Withdrawal does not affect processing that took place before it. After you withdraw, we stop processing your data for that purpose and delete it unless the law requires us to keep it. If you withdraw consent for your enquiry, we will no longer be able to respond to it.</p>

      <h2>5. Who we share it with</h2>
      <p>We share personal data only with service providers that help us run our business, and only as far as needed:</p>
      <ul>
        <li><strong>Email hosting:</strong> GoDaddy hosts our business email, so enquiry emails are stored on its servers on our behalf.</li>
{"        <li><strong>Enquiry records and emails:</strong> Google (Google Sheets and Google Apps Script) stores enquiry records and sends the confirmation and notification emails on our behalf.</li>" if FORM_ENDPOINT else ""}
        <li><strong>Website hosting:</strong> GitHub (GitHub Pages) hosts this website and processes technical connection data, such as IP addresses, to deliver and secure it, under its own privacy terms.</li>
      </ul>
      <p>These providers may store data outside India. We may also disclose personal data where the law requires it.</p>

      <h2>6. How we protect it</h2>
      <p>This website is served only over an encrypted connection (HTTPS). We take reasonable security safeguards to protect personal data in our possession, as the law requires. If a personal data breach affects you, we will inform you and the Data Protection Board of India as the law requires.</p>

      <h2>7. How long we keep it and when we delete it</h2>
      <p>We keep personal data only for as long as needed for the purpose it was collected for, as set out in section 2. We delete it when that purpose is fulfilled or you withdraw consent, whichever comes first, unless the law requires us to keep it longer.</p>

      <h2>8. Your rights</h2>
      <p>Under the DPDP Act you have the right to:</p>
      <ul>
        <li><strong>Access:</strong> get a summary of the personal data we hold about you and how we use it;</li>
        <li><strong>Correction and erasure:</strong> have your data corrected, completed, updated or deleted;</li>
        <li><strong>Withdraw consent</strong> at any time (section 4);</li>
        <li><strong>Grievance redressal:</strong> have a complaint about how we handle your data resolved by us;</li>
        <li><strong>Nominate</strong> another person to exercise your rights in the event of your death or incapacity.</li>
      </ul>
      <p><strong>How to make a request:</strong> email <a href="mailto:{EMAIL}?subject=Privacy%20request">{EMAIL}</a> with the subject line "Privacy request" and tell us which right you want to exercise. We may ask you for information to confirm your identity. We will respond as soon as possible and in any case within 90 days.</p>

      <h2>9. Complaints</h2>
      <p>Please contact us first so we can try to resolve your concern. If you are not satisfied with our response, you can complain to the <strong>Data Protection Board of India</strong>.</p>
      <p>If you are in the United Kingdom or the European Union, you may also have rights under the UK GDPR or EU GDPR, including the right to complain to your local data protection authority (in the UK, the Information Commissioner's Office).</p>

      <h2>10. Your duties</h2>
      <p>When you share personal data with us, the DPDP Act asks you to give accurate information, not to impersonate anyone, and not to file false or frivolous complaints.</p>

      <h2>11. Children</h2>
      <p>Our services are for businesses. This website is not intended for anyone under 18, and we do not knowingly collect their personal data. If we learn that we have received a child's personal data without verifiable parental consent, we will delete it.</p>

      <h2>12. Language and changes to this notice</h2>
      <p>This notice is in English. If you would like it in another language listed in the Eighth Schedule to the Constitution of India, email us and we will help. We may update this notice from time to time; the latest version and its date will always be on this page.</p>

      <h2>13. Contact</h2>
      <p><strong>SalesTrack</strong><br>{"<br>".join(ADDRESS_LINES)}<br>Email: <a href="mailto:{EMAIL}?subject=Privacy%20request">{EMAIL}</a></p>
    </article>
  </div>
</section>'''

def notfound():
    return f'''<section class="section notfound"><div class="wrap">
  <p class="code">404</p><h1>This page couldn't be found.</h1>
  <p class="lede" style="margin-inline:auto">The link may be broken or the page may have moved.</p>
  <div class="actions"><a class="btn btn-ink" href="./">Back to home {ARROW}</a><a class="btn btn-outline" href="contact.html">Contact us</a></div>
</div></section>'''

PAGES = [
    dict(file="index.html", key="home", title="SalesTrack | Lead Generation, Sales & BPO Services", fn=home,
         desc="SalesTrack is a results-driven lead generation and customer engagement company offering lead generation, B2C sales, live transfer and BPO services. Lead. Connect. Grow."),
    dict(file="services.html", key="services", title="Services | SalesTrack", fn=services,
         desc="Lead generation, B2C sales solutions, live transfer solutions and BPO services from SalesTrack, tailored to your business requirements."),
    dict(file="about.html", key="about", title="About Us | SalesTrack", fn=about,
         desc="SalesTrack helps businesses attract potential customers, build meaningful relationships and accelerate growth. Quality connections, smarter solutions, sustainable growth."),
    dict(file="contact.html", key="contact", title="Contact | SalesTrack", fn=contact,
         desc="Contact SalesTrack at info@salestrack.co.in. Business hours Monday to Friday, 2:30 PM to 11:00 PM IST."),
    dict(file="privacy.html", key="", title="Privacy Notice | SalesTrack", fn=privacy,
         desc="How SalesTrack collects, uses and protects personal information shared through salestrack.co.in."),
    dict(file="404.html", key="", title="Page Not Found | SalesTrack", fn=notfound, desc="The page you were looking for could not be found."),
]

def render(page, bare=False):
    body = f'''{header(page["key"])}
<main id="main">
{page["fn"]()}
</main>
{footer()}
<script src="assets/js/main.js" defer></script>'''
    if bare:  # body-only variant for the claude.ai preview (it adds its own skeleton)
        return head(page, True) + "\n" + body + "\n"
    return f'''<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{head(page)}
</head>
<body>
{body}
</body>
</html>
'''

FAVICON = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#0e2559"/><path d="M14 46 30 30l6 6 12-12" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/><path d="M38 16h16v16z" fill="#27b217"/></svg>'

if __name__ == "__main__":
    if DIST.exists(): shutil.rmtree(DIST)
    shutil.copytree(SRC / "assets", DIST / "assets")
    (DIST / "assets/img/favicon.svg").write_text(FAVICON)
    for p in PAGES:
        (DIST / p["file"]).write_text(render(p))
    (ROOT / "preview-index.html").write_text(render(PAGES[0], bare=True))
    urls = "".join(f"<url><loc>{SITE_URL}/{'' if p['file']=='index.html' else p['file']}</loc></url>" for p in PAGES if p['file'] != '404.html')
    (DIST / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    shutil.copy(ROOT / "LICENCES.md", DIST / "LICENCES.md")
    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
    print("built", [p["file"] for p in PAGES])
