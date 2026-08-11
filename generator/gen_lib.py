"""Shared layout + page shell for the Bender Realty static site generator."""
import html as _html
import json
import os

# GitHub Pages prefix; swap BASE to "" and SITE_URL to the production domain at launch.
BASE = "/bender-realty-site"
SITE_URL = "https://howard1081.github.io/bender-realty-site"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PHONE = "(423) 472-2173"
PHONE_TEL = "4234722173"
PM_PHONE = "(423) 476-5518"
PM_PHONE_TEL = "4234765518"
EMAIL = "bender@bender-realty.com"
PM_EMAIL = "propadmin@bender-realty.com"
ADDRESS = "425 25th Street NW, Cleveland, TN 37311"

def esc(s):
    return _html.escape(s, quote=True)

def u(path):
    """Internal URL with base prefix. path like '/buy/'"""
    return BASE + path

def abs_u(path):
    return SITE_URL + path

ORG_SCHEMA = {
    "@context": "https://schema.org",
    "@type": "RealEstateAgent",
    "@id": SITE_URL + "/#organization",
    "name": "Bender Realty",
    "url": SITE_URL + "/",
    "telephone": "+1-423-472-2173",
    "email": EMAIL,
    "foundingDate": "1969",
    "slogan": "Experience. Integrity. Results.",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "425 25th Street NW",
        "addressLocality": "Cleveland",
        "addressRegion": "TN",
        "postalCode": "37311",
        "addressCountry": "US",
    },
    "geo": {"@type": "GeoCoordinates", "latitude": 35.1791, "longitude": -84.8899},
    "areaServed": [
        {"@type": "AdministrativeArea", "name": "Bradley County, TN"},
        {"@type": "AdministrativeArea", "name": "Polk County, TN"},
        {"@type": "AdministrativeArea", "name": "McMinn County, TN"},
        {"@type": "AdministrativeArea", "name": "Meigs County, TN"},
        {"@type": "AdministrativeArea", "name": "Hamilton County, TN"},
    ],
}

NAV_ITEMS = [
    ("Home", "/"),
    ("Search Listings", "/search/"),
    ("Buy", "/buy/"),
    ("Sell", "/sell/"),
    ("Areas We Serve", "/areas-we-serve/"),
    ("Property Management", "/property-management/"),
    ("Commercial", "/commercial/"),
    ("About", "/about/"),
    ("Contact", "/contact/"),
]

BRAND_SVG = '''<svg class="brand-mark" viewBox="0 0 100 46" aria-hidden="true"><polygon points="8,42 34,14 48,29 41,36 34,28 20,42" fill="#6D0619"/><polygon points="34,14 44,4 92,42 78,42 44,15" fill="#C59F64"/></svg>'''

def header(active_path=""):
    links = []
    for label, path in NAV_ITEMS:
        cls = ' class="active"' if path != "/" and active_path.startswith(path) else ""
        links.append(f'<a href="{u(path)}"{cls}>{label}</a>')
    return f'''<div class="topbar">
  <div class="container topbar-inner">
    <span class="topbar-tag">Serving Southeast Tennessee Since 1969</span>
    <div class="topbar-contact">
      <a href="tel:{PHONE_TEL}">&#9742;&nbsp;{PHONE}</a>
      <a href="mailto:{EMAIL}">&#9993;&nbsp;{EMAIL}</a>
    </div>
  </div>
</div>
<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="{u('/')}" aria-label="Bender Realty home">
      <img class="brand-logo" src="{u('/img/bender-logo.png')}" alt="Bender Realty" width="96" height="75">
    </a>
    <nav class="main-nav" aria-label="Primary">
      {''.join(links)}
    </nav>
    <a class="btn btn-primary nav-cta" href="{u('/sell/home-valuation/')}">What's My Home Worth?</a>
    <details class="mobile-nav">
      <summary aria-label="Open menu"><span></span><span></span><span></span></summary>
      <nav aria-label="Mobile">
        {''.join(links)}
      </nav>
    </details>
  </div>
</header>'''

def footer():
    return f'''<footer class="site-footer">
  <div class="gold-rule"></div>
  <div class="container footer-grid">
    <div class="f-brand">
      <a class="brand brand-light" href="{u('/')}">
        <img class="brand-mark-img" src="{u('/img/bender-mark.png')}" alt="" width="62" height="24">
        <span class="brand-text">BENDER<span class="brand-sub">R&thinsp;E&thinsp;A&thinsp;L&thinsp;T&thinsp;Y</span></span>
      </a>
      <p>Experience. Integrity. Results.<br>Your trusted real estate partner in Southeast Tennessee since 1969.</p>
    </div>
    <div class="f-col">
      <h4>Quick Links</h4>
      <a href="{u('/')}">Home</a><a href="{u('/search/')}">Search Listings</a><a href="{u('/buy/')}">Buy</a><a href="{u('/sell/')}">Sell</a><a href="{u('/property-management/')}">Property Management</a><a href="{u('/rentals/')}">Rentals</a><a href="{u('/commercial/')}">Commercial</a><a href="{u('/about/our-agents/')}">Our Agents</a><a href="{u('/blog/')}">Blog</a><a href="{u('/contact/')}">Contact</a>
    </div>
    <div class="f-col">
      <h4>Areas We Serve</h4>
      <a href="{u('/areas-we-serve/bradley-county/cleveland/')}">Cleveland, TN</a><a href="{u('/areas-we-serve/bradley-county/charleston/')}">Charleston, TN</a><a href="{u('/areas-we-serve/mcminn-county/athens/')}">Athens, TN</a><a href="{u('/areas-we-serve/bradley-county/')}">Bradley County</a><a href="{u('/areas-we-serve/polk-county/')}">Polk County</a><a href="{u('/areas-we-serve/mcminn-county/')}">McMinn County</a><a href="{u('/areas-we-serve/meigs-county/')}">Meigs County</a><a href="{u('/areas-we-serve/hamilton-county/')}">Hamilton County</a>
    </div>
    <div class="f-col">
      <h4>Contact Us</h4>
      <p>425 25th Street NW<br>Cleveland, TN 37311</p>
      <p><a href="tel:{PHONE_TEL}">{PHONE}</a></p>
      <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      <p>Property Management:<br><a href="tel:{PM_PHONE_TEL}">{PM_PHONE}</a></p>
    </div>
  </div>
  <div class="container footer-bottom">
    <span>&copy; 2026 Bender Realty. All rights reserved. &nbsp;|&nbsp; Equal Housing Opportunity &nbsp;|&nbsp; REALTOR&reg;</span>
    <span><a href="{u('/privacy-policy/')}">Privacy Policy</a> &nbsp;|&nbsp; <a href="{u('/terms-of-use/')}">Terms of Use</a> &nbsp;|&nbsp; <a href="{u('/accessibility/')}">Accessibility</a> &nbsp;|&nbsp; <a href="{u('/sitemap/')}">Sitemap</a></span>
  </div>
</footer>'''

def breadcrumbs(crumbs):
    """crumbs: list of (label, path); last item is current page (no link)."""
    items = ['<a href="%s">Home</a>' % u("/")]
    schema_items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": abs_u("/")}]
    for i, (label, path) in enumerate(crumbs):
        pos = i + 2
        if i == len(crumbs) - 1:
            items.append(f'<span aria-current="page">{esc(label)}</span>')
            schema_items.append({"@type": "ListItem", "position": pos, "name": label})
        else:
            items.append(f'<a href="{u(path)}">{esc(label)}</a>')
            schema_items.append({"@type": "ListItem", "position": pos, "name": label, "item": abs_u(path)})
    nav = ('<nav class="breadcrumbs" aria-label="Breadcrumb"><div class="container">'
           + ' <span class="bc-sep">&#8250;</span> '.join(items) + "</div></nav>")
    schema = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": schema_items}
    return nav, schema

def faq_section(faqs, title_html='Frequently Asked <span class="accent">Questions</span>'):
    if not faqs:
        return "", None
    rows = "".join(
        f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faqs
    )
    section = f'''<section class="section faq alt-bg">
  <div class="container">
    <h2 class="section-title">{title_html}</h2>
    <div class="faq-list">{rows}</div>
  </div>
</section>'''
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faqs
        ],
    }
    return section, schema

def cta_band(heading="Ready to Make Your", accent="Move", text="Whether you're buying, selling, or just exploring your options, our team is here to help.", btn_label="Contact Us Today", btn_href="/contact/"):
    return f'''<section class="cta-band">
  <div class="container cta-grid">
    <div class="testimonial">
      <span class="quote-mark">&#8220;</span>
      <p>Bender Realty went above and beyond to help us find our dream home. Their local knowledge and dedication made the entire process smooth and stress-free.</p>
      <p class="attrib">&mdash; Jessica and Mark R.</p>
      <p class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</p>
    </div>
    <div class="cta-box">
      <h2>{heading} <span style="color:var(--burgundy);">{accent}</span>?</h2>
      <p>{esc(text)}</p>
      <a class="btn btn-primary" href="{u(btn_href)}">{btn_label} &#8594;</a>
    </div>
  </div>
</section>'''

def page_hero(kicker, title_html, sub=""):
    sub_html = f'<p class="ph-sub">{sub}</p>' if sub else ""
    return f'''<section class="page-hero">
  <div class="container">
    <span class="hero-kicker">{kicker}</span>
    <h1>{title_html}</h1>
    {sub_html}
  </div>
</section>'''

def idx_placeholder(label):
    return f'''<div class="idx-placeholder">
  <span class="idx-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5 21 21"/></svg></span>
  <p><strong>Live MLS listings: {esc(label)}</strong></p>
  <p class="idx-note">The River Counties MLS / IDX feed will display current listings here once connected.</p>
  <a class="btn btn-outline" href="{u('/search/')}">Search All Listings &#8594;</a>
</div>'''

def render_page(path, title, description, crumbs, body, extra_schema=None, faqs=None, faq_title=None, active_nav="", og_type="website", include_cta=True):
    """path like '/buy/' -> writes OUT/buy/index.html"""
    bc_html, bc_schema = breadcrumbs(crumbs) if crumbs else ("", None)
    faq_html, faq_schema = ("", None)
    if faqs:
        kwargs = {}
        if faq_title:
            kwargs["title_html"] = faq_title
        faq_html, faq_schema = faq_section(faqs, **kwargs)
    schemas = [ORG_SCHEMA]
    if bc_schema:
        schemas.append(bc_schema)
    if faq_schema:
        schemas.append(faq_schema)
    if extra_schema:
        schemas.extend(extra_schema if isinstance(extra_schema, list) else [extra_schema])
    schema_tags = "\n".join(
        '<script type="application/ld+json">%s</script>' % json.dumps(s, separators=(",", ":"))
        for s in schemas
    )
    canonical = abs_u(path)
    cta = cta_band() if include_cta else ""
    doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Bender Realty">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(description)}">
<meta name="geo.region" content="US-TN">
<meta name="geo.placename" content="Cleveland, Tennessee">
{schema_tags}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Marcellus&family=Lato:wght@300;400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{u('/css/styles.css')}?v=2">
</head>
<body>
{header(active_nav or path)}
{bc_html}
<main>
{body}
{faq_html}
{cta}
</main>
{footer()}
</body>
</html>'''
    rel = path.strip("/")
    out_dir = os.path.join(OUT, rel) if rel else OUT
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "index.html")
    with open(out_file, "w") as f:
        f.write(doc)
    return path
