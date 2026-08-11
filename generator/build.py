#!/usr/bin/env python3
"""Build all Bender Realty static pages."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_lib import (render_page, u, abs_u, esc, page_hero, idx_placeholder, BASE,
                     SITE_URL, OUT, PHONE, PHONE_TEL, PM_PHONE, PM_PHONE_TEL, EMAIL, PM_EMAIL)
import data

PAGES = []  # collected paths for sitemap

def add(path, *args, **kwargs):
    render_page(path, *args, **kwargs)
    PAGES.append(path)

def card_grid(items, cls="hub-grid"):
    """items: list of (href, title, text)"""
    cards = "".join(
        f'''<a class="hub-card" href="{u(href)}">
      <h3>{esc(title)}</h3>
      <p>{esc(text)}</p>
      <span class="text-link">Learn More &#8594;</span>
    </a>''' for href, title, text in items)
    return f'<div class="{cls}">{cards}</div>'

def prose(paragraphs):
    return "".join(f"<p>{p}</p>" for p in paragraphs)

def content_section(inner, container_class="container content-narrow", alt=False):
    cls = "section alt-bg" if alt else "section"
    return f'<section class="{cls}"><div class="{container_class}">{inner}</div></section>'

def h2(base, accent, left=False):
    l = " left" if left else ""
    return f'<h2 class="section-title{l}">{base} <span class="accent">{accent}</span></h2>'

def place_schema(name, kind="City", desc=""):
    s = {"@context": "https://schema.org", "@type": "Place", "name": name,
         "address": {"@type": "PostalAddress", "addressRegion": "TN", "addressCountry": "US"}}
    if desc:
        s["description"] = desc
    return s

def geo_faqs(name, county=None, seat=None):
    county_txt = f" in {county}" if county else ""
    return [
        (f"Does Bender Realty serve {name}?",
         f"Yes. Bender Realty helps buyers, sellers, and property owners throughout {name}{county_txt} and the surrounding Southeast Tennessee communities, from our office in Cleveland, TN."),
        (f"How do I find homes for sale in {name}?",
         f"You can search current {name} listings on our website, or contact a Bender Realty agent at {PHONE} for a customized list matched to your price range and needs."),
        (f"What is my home in {name} worth?",
         f"Request a free home valuation from Bender Realty. We prepare a comparative market analysis using recent {name}-area sales — no cost, no obligation."),
    ]

# ---------------------------------------------------------------- Areas We Serve
def build_areas():
    # hub
    county_cards = "".join(f'''<a class="comm-tile wide" href="{u('/areas-we-serve/%s/' % c['slug'])}">
      <img src="{c['img']}" alt="Scenery in {esc(c['name'])} Tennessee" loading="lazy">
      <div class="comm-info">
        <span class="comm-kicker">{c['kicker']}</span>
        <span class="comm-name">{esc(c['name'])}</span>
        <span class="comm-link">Explore {esc(c['name'])} &#8594;</span>
      </div>
    </a>''' for c in data.COUNTIES)
    body = page_hero("Southeast Tennessee", 'Areas We <span class="gold">Serve</span>',
                     "Five counties. Dozens of communities. One local team since 1969.")
    body += content_section(
        h2("Our Southeast Tennessee", "Service Area") +
        prose([
            "Bender Realty serves buyers, sellers, renters, and investors across Southeast Tennessee — anchored in Cleveland and Bradley County, and extending through Polk, McMinn, and Meigs counties and the greater Chattanooga communities of Hamilton County.",
            "Every county below links to detailed community pages with local insight, market guidance, and current listings. We also assist clients in neighboring counties throughout the region — if you don't see your community listed, call us and we'll help.",
        ]))
    body += f'<section class="section alt-bg"><div class="container"><div class="comm-mosaic areas-mosaic">{county_cards}</div></div></section>'
    add("/areas-we-serve/", "Areas We Serve | Bender Realty — Southeast Tennessee Real Estate",
        "Bender Realty serves Cleveland, Bradley County, Polk, McMinn, Meigs, and Hamilton counties. Explore every Southeast Tennessee community we cover.",
        [("Areas We Serve", "/areas-we-serve/")], body,
        faqs=[
            ("What counties does Bender Realty cover?", "Bender Realty covers Bradley, Polk, McMinn, Meigs, and Hamilton counties in Southeast Tennessee, with our office located in Cleveland, TN. We also assist clients in neighboring counties throughout the region."),
            ("Where is Bender Realty located?", f"Our office is at 425 25th Street NW, Cleveland, TN 37311 — call {PHONE} or stop by during business hours."),
            ("Can Bender Realty help me outside these counties?", "Often, yes. We regularly assist clients in adjoining Southeast Tennessee counties and can refer you to a trusted partner anywhere else in the state."),
        ])

    for c in data.COUNTIES:
        cslug, cname = c["slug"], c["name"]
        cpath = f"/areas-we-serve/{cslug}/"
        comm_items = [(f"/areas-we-serve/{cslug}/{s}/", n, b.split(". ")[0] + ".") for s, n, b in c["communities"]]
        body = page_hero(f"{c['kicker']}", f'{esc(cname)} <span class="gold">Real Estate</span>',
                         f"Homes, land, and local guidance across {cname}, Tennessee.")
        body += content_section(
            h2(f"Living in", cname) + prose([c["blurb"], c["extra"]]))
        body += content_section(
            h2(f"Communities in", cname, left=True) + card_grid(comm_items), "container", alt=True)
        body += content_section(h2(f"Search Homes in", cname, left=True) + idx_placeholder(f"Homes for sale in {cname}, TN"), "container")
        add(cpath, f"{cname} TN Real Estate | Homes for Sale & Local Guide | Bender Realty",
            f"Explore {cname}, Tennessee real estate with Bender Realty — community guides, homes for sale, land, and local market expertise since 1969.",
            [("Areas We Serve", "/areas-we-serve/"), (cname, cpath)], body,
            extra_schema=place_schema(f"{cname}, Tennessee", "AdministrativeArea", c["blurb"]),
            faqs=geo_faqs(cname))

        # community pages
        others = c["communities"]
        for i, (s, n, blurb) in enumerate(others):
            path = f"/areas-we-serve/{cslug}/{s}/"
            nearby = [(f"/areas-we-serve/{cslug}/{s2}/", n2, b2.split(". ")[0] + ".")
                      for s2, n2, b2 in others if s2 != s][:3]
            body = page_hero(cname, f'{esc(n)} <span class="gold">Real Estate</span>',
                             f"Homes for sale and local insight in {n}, Tennessee.")
            body += content_section(
                h2("About", n) + prose([
                    blurb,
                    f"Bender Realty has connected buyers and sellers in {n} and across {cname} since 1969. Our agents live and work in this market — we can tell you what a property should sell for, which streets flood, and where the value is heading. Whether you're buying your first home, selling a longtime family property, or looking for land, we bring local answers to every step.",
                ]))
            body += content_section(h2("Homes for Sale in", n, left=True) + idx_placeholder(f"Homes for sale in {n}, TN"), "container", alt=True)
            body += content_section(h2("Nearby", "Communities", left=True) + card_grid(nearby), "container")
            add(path, f"{n} TN Real Estate | Homes for Sale in {n} | Bender Realty",
                f"Search homes for sale in {n}, Tennessee and get local guidance from Bender Realty — serving {cname} and Southeast Tennessee since 1969.",
                [("Areas We Serve", "/areas-we-serve/"), (cname, cpath), (n, path)], body,
                extra_schema=place_schema(f"{n}, Tennessee", "City", blurb),
                faqs=geo_faqs(n, county=cname))

# ---------------------------------------------------------------- Homes for sale
def build_hfs():
    hub_path = "/homes-for-sale/"
    type_items = [(f"/homes-for-sale/{s}/", t, blurb.split(". ")[0] + ".") for s, t, _h1, blurb, _extra in data.HOME_TYPES]
    geo_items = [(f"/homes-for-sale/{s}/", f"{n} Homes for Sale", f"Search current homes for sale in {n}, Tennessee.") for s, n, _c in data.HFS_GEO]
    body = page_hero("Search by Place or Property Type", 'Homes for <span class="gold">Sale</span>',
                     "Find your next home across Cleveland, Bradley County, and Southeast Tennessee.")
    body += content_section(
        h2("Find Homes for Sale in", "Southeast Tennessee") + prose([
            "Start your home search the local way. Browse homes for sale by community — Cleveland, Athens, Ooltewah, Decatur, and more — or by the property styles Southeast Tennessee is known for: lakefront, acreage, farms, cabins, and new construction.",
            "Every listing page connects to live MLS data from the River Counties Association of REALTORS, and every search is backed by a Bender Realty agent who knows the market street by street.",
        ]))
    body += content_section(h2("Browse by", "Location", left=True) + card_grid(geo_items), "container", alt=True)
    body += content_section(h2("Browse by", "Property Type", left=True) + card_grid(type_items), "container")
    add(hub_path, "Homes for Sale in Cleveland TN & Southeast Tennessee | Bender Realty",
        "Browse homes for sale in Cleveland TN, Bradley County, and Southeast Tennessee by location or property type — lakefront, acreage, new construction, and more.",
        [("Homes for Sale", hub_path)], body,
        faqs=[
            ("How current are the listings on this site?", "Listing data comes from the River Counties MLS feed and is refreshed continuously, so you see homes as they hit the market."),
            ("Can I get alerts when new homes match my search?", "Yes — contact a Bender Realty agent and we'll set up automatic alerts matched to your locations, price range, and property type."),
            ("Do I pay Bender Realty to help me buy a home?", "In most transactions the buyer's agent is compensated through the transaction. We'll explain exactly how compensation works before you sign anything."),
        ])

    for s, t, h1, blurb, extra in data.HOME_TYPES:
        path = f"/homes-for-sale/{s}/"
        body = page_hero("Property Type", f'{esc(t)} <span class="gold">for Sale</span>', "")
        body += content_section(h2(t.split(" ")[0], " ".join(t.split(" ")[1:]) or "Homes") + prose([blurb, extra]))
        body += content_section(idx_placeholder(f"{t} for sale in Southeast Tennessee"), "container", alt=True)
        related = [(f"/homes-for-sale/{s2}/", t2, b2.split(". ")[0] + ".") for s2, t2, _h, b2, _e in data.HOME_TYPES if s2 != s][:3]
        body += content_section(h2("Related", "Searches", left=True) + card_grid(related), "container")
        add(path, f"{h1} | Bender Realty", blurb.split(". ")[0] + ".",
            [("Homes for Sale", hub_path), (t, path)], body,
            faqs=[
                (f"Where can I find {t.lower()} in Southeast Tennessee?", blurb),
                (f"What should I know before buying {t.lower().rstrip('s')} property?", extra),
                ("How do I start my search?", f"Browse current listings above, or call Bender Realty at {PHONE} and an agent will build a custom search around your needs."),
            ])

    for s, n, cslug in data.HFS_GEO:
        path = f"/homes-for-sale/{s}/"
        county = next(c for c in data.COUNTIES if c["slug"] == cslug)
        body = page_hero(county["name"], f'Homes for Sale in <span class="gold">{esc(n)}</span>', "")
        body += content_section(
            h2(f"{n}", "Homes for Sale") + prose([
                f"Search current homes for sale in {n}, Tennessee — updated continuously from the River Counties MLS. {county['blurb']}",
                f"Want the inside track? A Bender Realty agent can alert you the moment a new {n} listing hits the market, and tell you what it should really sell for.",
            ]))
        body += content_section(idx_placeholder(f"Homes for sale in {n}, TN"), "container", alt=True)
        body += content_section(
            h2("Learn More About", n, left=True) +
            card_grid([
                (f"/areas-we-serve/{cslug}/", f"{county['name']} Guide", f"Neighborhoods, lifestyle, and market insight across {county['name']}."),
                ("/buy/", "Buyer Services", "How Bender Realty guides buyers from search to closing."),
                ("/sell/home-valuation/", "What's My Home Worth?", "Free comparative market analysis from local experts."),
            ]), "container")
        add(path, f"Homes for Sale in {n} TN | Bender Realty",
            f"Browse homes for sale in {n}, Tennessee with Bender Realty — live MLS listings, local guidance, and market expertise since 1969.",
            [("Homes for Sale", hub_path), (n, path)], body, faqs=geo_faqs(n, county=county["name"]))

# ---------------------------------------------------------------- Land
def build_land():
    hub = "/land/"
    items = [(f"/land/{s}/", t, b.split(". ")[0] + ".") for s, t, b in data.LAND_TYPES]
    body = page_hero("Acreage · Farms · Waterfront", 'Land for <span class="gold">Sale</span>',
                     "Farms, timber, hunting tracts, and lakefront lots across Southeast Tennessee.")
    body += content_section(
        h2("Southeast Tennessee", "Land Specialists") + prose([
            "Land is different. Pricing an acreage tract, reading a soil map, walking a boundary, understanding greenbelt taxes — it takes local experience that most residential-only agents don't have. Bender Realty has brokered Southeast Tennessee land since 1969.",
            "Browse land by county or by use below, or tell us what you're looking for and we'll find it — including off-market tracts that never hit the MLS.",
        ]))
    body += content_section(card_grid(items), "container", alt=True)
    add(hub, "Land for Sale in Southeast Tennessee | Farms, Acreage & Lots | Bender Realty",
        "Land for sale across Bradley, Polk, McMinn, and Meigs counties — farms, hunting land, acreage, and lakefront lots with local guidance from Bender Realty.",
        [("Land", hub)], body,
        faqs=[
            ("What should I check before buying land in Tennessee?", "Key items include legal access, utilities availability, soil suitability (perc test for septic), zoning and restrictions, flood zones, and boundary surveys. A Bender Realty land agent walks you through each."),
            ("What is greenbelt status?", "Tennessee's Greenbelt Law allows qualifying agricultural, forest, or open-space land to be taxed at use value rather than market value — often a major property-tax savings. We can tell you if a tract qualifies."),
            ("Does Bender Realty sell hunting land?", "Yes — hunting and recreational tracts across Polk, Meigs, McMinn, and Bradley counties are a specialty, including land adjoining the Cherokee National Forest."),
        ])
    for s, t, b in data.LAND_TYPES:
        path = f"/land/{s}/"
        related = [(f"/land/{s2}/", t2, b2.split(". ")[0] + ".") for s2, t2, b2 in data.LAND_TYPES if s2 != s][:3]
        body = page_hero("Land & Acreage", f'{esc(t)}', "")
        body += content_section(h2(t.rsplit(" ", 1)[0], t.rsplit(" ", 1)[1]) + prose([
            b,
            f"Every land purchase raises questions — access, utilities, soils, restrictions, taxes. Call Bender Realty at {PHONE} and get answers from agents who work land every week.",
        ]))
        body += content_section(idx_placeholder(t), "container", alt=True)
        body += content_section(h2("More", "Land Searches", left=True) + card_grid(related), "container")
        add(path, f"{t} | Southeast Tennessee | Bender Realty", b.split(". ")[0] + ".",
            [("Land", hub), (t, path)], body,
            faqs=[
                (f"How do I find {t.lower()}?", b),
                ("Can Bender Realty help me sell land?", "Yes. We market land to the buyers who actually purchase it — farmers, builders, investors, and recreational buyers — with pricing built from real comparable land sales."),
            ])

# ---------------------------------------------------------------- Buy & Sell
def build_buy():
    hub = "/buy/"
    items = [(f"/buy/{s}/", t, paras[0].split(". ")[0] + ".") for s, t, _h1, paras, _f in data.BUY_PAGES]
    body = page_hero("Buyer Services", 'Buy a Home with <span class="gold">Confidence</span>',
                     "Local guidance for every step, from pre-approval to keys in hand.")
    body += content_section(
        h2("Buying a Home in", "Southeast Tennessee") + prose([
            "Buying a home is the biggest purchase most people ever make — and the process rewards preparation. Bender Realty buyers get a local agent who knows the neighborhoods, the pricing, and the pitfalls, plus a step-by-step process refined over 55 years.",
            "Start with the guides below, then let's talk about what you're looking for.",
        ]))
    body += content_section(card_grid(items), "container", alt=True)
    add(hub, "Buy a Home in Cleveland TN | Buyer Services | Bender Realty",
        "Buyer services from Bender Realty — financing preparation, offers, closing guidance, first-time buyer help, and relocation support across Southeast Tennessee.",
        [("Buy", hub)], body,
        faqs=[
            ("Why should I use a buyer's agent?", "A buyer's agent represents your interests — not the seller's. Your Bender Realty agent advises on pricing, negotiates on your behalf, coordinates inspections, and manages every deadline through closing."),
            ("How do I start the home buying process?", "Two first steps: talk with a lender about pre-approval, and talk with a Bender Realty agent about what you're looking for. We'll handle the rest step by step."),
            ("Does Bender Realty work with first-time buyers?", "Constantly — and we enjoy it. We explain every step in plain language and connect you with programs like THDA loans that can lower your costs."),
        ])
    for s, t, h1, paras, faqs in data.BUY_PAGES:
        path = f"/buy/{s}/"
        body = page_hero("Buyer Guide", esc(t), "")
        body += content_section(h2(t.rsplit(" ", 1)[0] if " " in t else t, t.rsplit(" ", 1)[1] if " " in t else "") + prose(paras))
        related = [(f"/buy/{s2}/", t2, p2[0].split(". ")[0] + ".") for s2, t2, _h, p2, _f in data.BUY_PAGES if s2 != s][:3]
        body += content_section(h2("More Buyer", "Guides", left=True) + card_grid(related), "container", alt=True)
        add(path, f"{h1} | Bender Realty", paras[0].split(". ")[0] + ".",
            [("Buy", hub), (t, path)], body, faqs=faqs)

def build_sell():
    hub = "/sell/"
    items = [(f"/sell/{s}/", t, paras[0].split(". ")[0] + ".") for s, t, _h1, paras, _f in data.SELL_PAGES]
    geo_items = [(f"/sell/{s}/", t, b.split(". ")[0] + ".") for s, t, b in data.SELL_GEO]
    body = page_hero("Seller Services", 'Sell for <span class="gold">Top Dollar</span>',
                     "Pricing, preparation, and marketing built around your local market.")
    body += content_section(
        h2("Selling Your Home in", "Southeast Tennessee") + prose([
            "The difference between an average sale and a great one comes down to three things: accurate pricing, smart preparation, and marketing that reaches the right buyers. Bender Realty has delivered all three for Southeast Tennessee sellers since 1969.",
            "Start with a free home valuation, then explore our seller guides below.",
        ]))
    body += content_section(card_grid(items), "container", alt=True)
    body += content_section(h2("Sell in Your", "Community", left=True) + card_grid(geo_items), "container")
    add(hub, "Sell Your Home in Cleveland TN | Seller Services | Bender Realty",
        "Sell your Southeast Tennessee home with Bender Realty — free valuation, preparation guidance, professional marketing, and expert negotiation since 1969.",
        [("Sell", hub)], body,
        faqs=[
            ("How much is my home worth?", "Request a free comparative market analysis from Bender Realty. We use recent local sales, current competition, and 55 years of pricing experience — no cost, no obligation."),
            ("What does it cost to sell a home?", "Typical seller costs include commission, title and closing fees, and prorated taxes. We provide a net-proceeds estimate before you list so there are no surprises."),
            ("How long will it take to sell my home?", "It depends on price, condition, and location — correctly priced Cleveland-area homes often go under contract within weeks. Your agent will give you an honest local timeline."),
        ])
    for s, t, h1, paras, faqs in data.SELL_PAGES:
        path = f"/sell/{s}/"
        body = page_hero("Seller Guide", esc(t), "")
        if s in ("home-valuation", "request-a-home-evaluation"):
            form = f'''<div class="lead-form-wrap">
  <form class="lead-form" onsubmit="return false;">
    <h3>Request Your Free Valuation</h3>
    <div class="lf-row"><label>Name<input type="text" name="name" autocomplete="name"></label>
    <label>Phone<input type="tel" name="phone" autocomplete="tel"></label></div>
    <label>Email<input type="email" name="email" autocomplete="email"></label>
    <label>Property Address<input type="text" name="address" autocomplete="street-address"></label>
    <label>Tell us about your home (optional)<textarea name="notes" rows="3"></textarea></label>
    <button class="btn btn-primary" type="submit">Get My Free Valuation &#8594;</button>
    <p class="lf-note">No obligation. A local Bender Realty agent will follow up with your analysis.</p>
  </form>
</div>'''
            body += content_section(h2(t.rsplit(" ", 1)[0], t.rsplit(" ", 1)[1]) + prose(paras) + form)
        else:
            body += content_section(h2(t.rsplit(" ", 1)[0] if " " in t else t, t.rsplit(" ", 1)[1] if " " in t else "") + prose(paras))
        related = [(f"/sell/{s2}/", t2, p2[0].split(". ")[0] + ".") for s2, t2, _h, p2, _f in data.SELL_PAGES if s2 != s][:3]
        body += content_section(h2("More Seller", "Guides", left=True) + card_grid(related), "container", alt=True)
        add(path, f"{h1} | Bender Realty", paras[0].split(". ")[0] + ".",
            [("Sell", hub), (t, path)], body, faqs=faqs)
    for s, t, b in data.SELL_GEO:
        path = f"/sell/{s}/"
        name = t.replace("Sell Your Home in ", "")
        body = page_hero("Seller Services", esc(t), "")
        body += content_section(h2("Selling in", name) + prose([
            b,
            "Every sale starts with an accurate number. Request a free comparative market analysis and we'll show you exactly what your home should bring in today's market — and the plan to get it.",
        ]))
        body += content_section(
            card_grid([
                ("/sell/home-valuation/", "Free Home Valuation", "Find out what your home is worth in today's market."),
                ("/sell/prepare-your-home-for-sale/", "Prepare Your Home", "The highest-return steps before you list."),
                ("/sell/marketing-plan/", "Our Marketing Plan", "How we get your home in front of the right buyers."),
            ]), "container", alt=True)
        add(path, f"{t} | Bender Realty", b.split(". ")[0] + ".",
            [("Sell", "/sell/"), (t, path)], body,
            faqs=[
                (f"How do I sell my home in {name.replace(' TN','')}?", f"Start with a free Bender Realty home valuation. We analyze recent {name.replace(' TN','')} sales, recommend a pricing and preparation strategy, and market your home to qualified buyers across the region."),
                ("What's the first step to selling?", f"Request a free comparative market analysis or call us at {PHONE}. There's no obligation — just an honest local read on your home's value."),
            ])

# ---------------------------------------------------------------- PM, Rentals, Commercial
def build_pm():
    hub = "/property-management/"
    body = page_hero("For Property Owners", 'Property <span class="gold">Management</span>',
                     "About 500 units under management across the Cleveland TN area.")
    body += content_section(
        h2("Southeast Tennessee's", "Property Management Team") + prose([
            "Owning rental property should build wealth, not consume your weekends. Bender Realty manages approximately 500 rental units across Cleveland and Southeast Tennessee — handling leasing, rent collection, maintenance, inspections, and accounting for owners who want performance without the phone calls.",
            f"Our property management division has its own dedicated staff and phone line ({PM_PHONE}), backed by the market knowledge of a full-service brokerage. Whether you own one rental house or a portfolio, we treat your property like the investment it is.",
        ]))
    body += content_section(
        card_grid([
            ("/property-management/services/", "Management Services", "Leasing, maintenance, rent collection, inspections, and owner reporting."),
            ("/property-management/owner-faq/", "Owner FAQ", "Fees, leases, maintenance policy, and how owner payments work."),
            ("/property-management/free-rental-analysis/", "Free Rental Analysis", "Find out what your property should rent for in today's market."),
        ]), "container", alt=True)
    add(hub, "Property Management in Cleveland TN | ~500 Units Managed | Bender Realty",
        "Full-service property management in Cleveland TN — leasing, maintenance, rent collection, and reporting for rental owners. About 500 units managed since 1969.",
        [("Property Management", hub)], body,
        faqs=[
            ("What does Bender Realty property management include?", "Marketing and leasing, tenant screening, rent collection, maintenance coordination, periodic inspections, and monthly owner statements — full-service management for residential rental property."),
            ("How many properties does Bender Realty manage?", "Approximately 500 rental units across Cleveland and the surrounding Southeast Tennessee area."),
            ("How do I get started with property management?", f"Request a free rental analysis or call our property management office at {PM_PHONE}. We'll evaluate your property, recommend a rental rate, and explain our management agreement."),
        ])
    pm_children = [
        ("services", "Management Services", "Property Management Services in Cleveland TN",
         ["Bender Realty's full-service management covers the entire rental cycle, so ownership stays profitable and hands-off.",
          "<strong>Leasing & marketing:</strong> professional listings, showings, and applications. <strong>Tenant screening:</strong> credit, criminal, eviction, income, and rental history checks on every adult applicant. <strong>Rent collection:</strong> online payment options, firm and fair enforcement, and direct-deposit owner disbursements.",
          "<strong>Maintenance:</strong> a vetted vendor network, 24/7 emergency response, and repair coordination with owner-approval thresholds you set. <strong>Inspections:</strong> move-in, move-out, and periodic condition reports with photos. <strong>Accounting:</strong> monthly statements and year-end tax documentation.",
          "One relationship, one monthly statement, and a property that performs. That's the goal."],
         [("Do you handle maintenance calls?", "Yes — tenants contact us, not you. We coordinate repairs through vetted vendors, honor your approval threshold for larger items, and handle emergencies 24/7."),
          ("How do you screen tenants?", "Every adult applicant is screened for credit, income (typically 3x rent), rental history, eviction records, and criminal background — consistently and in compliance with fair housing law."),
          ("When do owners get paid?", "Owner disbursements are sent monthly by direct deposit, accompanied by a full statement of income and expenses.")]),
        ("owner-faq", "Owner FAQ", "Property Management Owner FAQ | Bender Realty",
         ["Straight answers to the questions rental owners ask us most. Don't see yours? Call the property management office and ask — we'd rather you know exactly how we work before you sign anything.",
          "Our management agreement spells out fees, responsibilities, approval thresholds, and how to end the relationship if you're ever unhappy. No lock-in tricks, no surprise charges — 55 years in this community doesn't survive on fine print."],
         [("What are your management fees?", "Fees depend on property type and portfolio size. Contact our property management office for current fee schedules — we'll put everything in writing before you commit."),
          ("Who holds the security deposit?", "Security deposits are held in accordance with Tennessee law and accounted for at move-out with a documented condition comparison."),
          ("What if my tenant stops paying rent?", "We follow a firm, legally compliant process: notices, communication, payment plans where appropriate, and coordination of eviction proceedings when necessary."),
          ("Can I use my own contractor?", "In most cases yes — tell us your preferred vendors and approval limits, and we'll coordinate around them."),
          ("How do you set the rental rate?", "We run a rental market analysis using comparable leased properties in your area — priced to minimize vacancy while maximizing income.")]),
        ("free-rental-analysis", "Free Rental Analysis", "Free Rental Analysis — What Should Your Property Rent For?",
         ["What should your property rent for? Guessing costs money in both directions: price too high and vacancy eats your return; too low and you leave rent on the table every month.",
          "Our free rental analysis compares your property against actual leased comparables in the Cleveland area market — not asking prices — and gives you a realistic rate, an estimate of demand, and recommendations to maximize your return.",
          "Fill out the form below or call our property management team and we'll get started."],
         [("Is the rental analysis really free?", "Yes — free and no obligation. It's how we start every owner conversation."),
          ("What does the analysis include?", "A recommended rental rate based on leased comparables, expected time-to-lease, and any recommendations that would improve your property's rentability or rate.")]),
    ]
    for s, t, h1, paras, faqs in pm_children:
        path = f"/property-management/{s}/"
        body = page_hero("Property Management", esc(t), "")
        inner = h2(t.rsplit(" ", 1)[0] if " " in t else t, t.rsplit(" ", 1)[1] if " " in t else "") + prose(paras)
        if s == "free-rental-analysis":
            inner += f'''<div class="lead-form-wrap"><form class="lead-form" onsubmit="return false;">
    <h3>Request Your Free Rental Analysis</h3>
    <div class="lf-row"><label>Name<input type="text" name="name"></label><label>Phone<input type="tel" name="phone"></label></div>
    <label>Email<input type="email" name="email"></label>
    <label>Rental Property Address<input type="text" name="address"></label>
    <button class="btn btn-primary" type="submit">Get My Rental Analysis &#8594;</button>
    <p class="lf-note">Our property management team will respond within one business day.</p>
  </form></div>'''
        body += content_section(inner)
        body += content_section(
            card_grid([(f"/property-management/{s2}/", t2, p2[0].split(". ")[0].replace("<strong>","").replace("</strong>","") + ".")
                       for s2, t2, _h, p2, _f in pm_children if s2 != s]
                      + [("/rentals/", "Looking to Rent?", "Browse available rentals and tenant resources.")]), "container", alt=True)
        add(path, f"{h1} | Bender Realty", re.sub("<[^>]+>", "", paras[0]).split(". ")[0] + ".",
            [("Property Management", hub), (t, path)], body, faqs=faqs)

def build_rentals():
    hub = "/rentals/"
    body = page_hero("For Renters", 'Rentals in <span class="gold">Cleveland TN</span>',
                     "Houses, apartments, and student housing across the Cleveland area.")
    body += content_section(
        h2("Find Your Next", "Rental") + prose([
            "Bender Realty manages approximately 500 rental units across Cleveland and Southeast Tennessee — houses, duplexes, and apartments at a range of price points, professionally managed by a local team you can actually reach.",
            f"Browse available rentals below, apply online, or call our property management office at {PM_PHONE}.",
        ]))
    body += content_section(
        card_grid([
            ("/rentals/available/", "Available Rentals", "Browse current rental listings in the Cleveland area."),
            ("/rentals/student-housing/", "Student Housing", "Rentals near Lee University and Cleveland State."),
            ("/rentals/apply/", "Apply Online", "Application requirements and how to apply."),
            ("/rentals/tenant-resources/", "Tenant Resources", "Pay rent, request maintenance, and tenant FAQs."),
        ]), "container", alt=True)
    add(hub, "Rentals in Cleveland TN | Houses & Apartments for Rent | Bender Realty",
        "Houses and apartments for rent in Cleveland TN from Bender Realty Property Management — about 500 professionally managed units, including student housing near Lee University.",
        [("Rentals", hub)], body,
        faqs=[
            ("How do I see available rentals?", "Browse our available rentals page for current listings with photos, rents, and details, or call the property management office for what's coming available."),
            ("What do I need to qualify for a rental?", "Typical requirements include verifiable income (commonly 3x the monthly rent), acceptable rental history, and background screening. Specific criteria are listed with each property."),
            ("Do you offer student housing?", "Yes — we manage rentals near Lee University and Cleveland State Community College that work well for students, including options for roommate groups."),
        ])
    rentals_children = [
        ("available", "Available Rentals", "Available Rentals in Cleveland TN",
         ["Current Bender Realty rental listings for the Cleveland area appear below, updated as units become available.",
          "Each listing includes rent, deposit, bedrooms and baths, pet policy, and application requirements. Units move quickly — if you see a fit, apply promptly or call the property management office."],
         [("How often are rental listings updated?", "Continuously — units appear as soon as they're ready to market and come down when leased."),
          ("Can I schedule a showing?", f"Yes — contact our property management office at {PM_PHONE} to arrange a showing of any available unit.")], True),
        ("student-housing", "Student Housing", "Student Housing near Lee University & Cleveland State | Cleveland TN",
         ["Cleveland is a college town — Lee University sits just off downtown and Cleveland State Community College serves the region — and Bender Realty manages rental housing that fits student life.",
          "Options range from walk-to-campus houses and apartments near Lee to affordable units convenient to Cleveland State. Roommate groups are common, and we can advise on lease structures that work for students and parents alike.",
          "Parents: professionally managed housing means maintenance gets handled, communication is documented, and the lease protects everyone. Call us early — the best student units for fall lease up quickly in spring."],
         [("Do you have rentals near Lee University?", "Yes — houses and apartments within walking or short driving distance of Lee's campus are among our most popular units. Contact us early in the spring semester for fall availability."),
          ("Can students with no rental history apply?", "Yes — student applicants commonly use a parent or guardian as guarantor. We'll explain exactly what's needed when you apply."),
          ("When should I start looking for fall housing?", "Spring semester — the best-located student units are typically leased by early summer.")], False),
        ("apply", "Apply for a Rental", "Apply for a Bender Realty Rental",
         ["Ready to apply? Here's how our application process works and what you'll need.",
          "<strong>What we look for:</strong> verifiable income (typically 3x monthly rent), acceptable rental or mortgage history, and standard background screening for every adult occupant. <strong>What you'll need:</strong> photo ID, proof of income (recent pay stubs or equivalent), and rental history contact information.",
          "Applications are processed in the order received. Approved applicants secure the unit with the deposit; we'll walk you through lease signing and move-in from there."],
         [("How long does application processing take?", "Most applications are processed within 1–3 business days once all documentation is received."),
          ("Is there an application fee?", "Application fees and current requirements are listed with each property listing — everything is disclosed before you apply."),
          ("Do you accept pets?", "Pet policy varies by property and is listed with each unit. Where pets are allowed, pet deposits or fees apply.")], False),
        ("tenant-resources", "Tenant Resources", "Tenant Resources | Pay Rent & Request Maintenance",
         ["Everything current tenants need, in one place.",
          "<strong>Pay rent online:</strong> tenants can pay securely through our online tenant portal. <strong>Maintenance requests:</strong> submit non-emergency requests through the portal for documented, tracked service; for after-hours emergencies (flooding, no heat, safety issues), call the property management line.",
          f"Questions about your lease, renewal, or account? Call the property management office at {PM_PHONE} or email {PM_EMAIL}."],
         [("How do I pay my rent?", "Through the online tenant portal — secure, documented, and available 24/7. Contact the office if you need portal access."),
          ("How do I request maintenance?", "Submit a request through the tenant portal for standard repairs. For emergencies like flooding or loss of heat, call the property management office immediately."),
          ("Who do I contact about my lease?", f"Call the property management office at {PM_PHONE} or email {PM_EMAIL} — our team handles renewals, questions, and account matters.")], False),
    ]
    for s, t, h1, paras, faqs, show_idx in rentals_children:
        path = f"/rentals/{s}/"
        body = page_hero("Rentals", esc(t), "")
        inner = h2(t.rsplit(" ", 1)[0] if " " in t else t, t.rsplit(" ", 1)[1] if " " in t else "") + prose(paras)
        body += content_section(inner)
        if show_idx:
            body += content_section(idx_placeholder("Available rentals in the Cleveland TN area — AppFolio feed"), "container", alt=True)
        body += content_section(
            card_grid([(f"/rentals/{s2}/", t2, re.sub("<[^>]+>", "", p2[0]).split(". ")[0] + ".")
                       for s2, t2, _h, p2, _f, _i in rentals_children if s2 != s][:3]), "container", alt=not show_idx)
        add(path, f"{h1} | Bender Realty", re.sub("<[^>]+>", "", paras[0]).split(". ")[0] + ".",
            [("Rentals", hub), (t, path)], body, faqs=faqs)

def build_commercial():
    hub = "/commercial/"
    body = page_hero("Commercial Real Estate", 'Commercial <span class="gold">Services</span>',
                     "Sales, leasing, and investment property across Cleveland and Southeast Tennessee.")
    body += content_section(
        h2("Commercial Real Estate,", "Done Locally") + prose([
            "Commercial real estate rewards specialized knowledge — and Bender Realty's commercial practice brings credentialed expertise (CCIM, CPM) to sales, leasing, site selection, and investment analysis across Cleveland, Bradley County, and Southeast Tennessee.",
            "From retail and office space to industrial sites and multi-family investments, we combine local market intelligence with the analytical tools institutional buyers expect.",
        ]))
    body += content_section(
        card_grid([
            ("/commercial/for-sale/", "Commercial for Sale", "Retail, office, industrial, and investment property listings."),
            ("/commercial/for-lease/", "Commercial for Lease", "Available lease space across the Cleveland area."),
            ("/commercial/site-selection/", "Site Selection", "Location analysis for businesses entering or expanding in the region."),
            ("/commercial/investment-analysis/", "Investment Analysis", "Cap rates, cash flow, and 1031 exchange guidance."),
        ]), "container", alt=True)
    add(hub, "Commercial Real Estate in Cleveland TN | Sales, Leasing & Investment | Bender Realty",
        "Commercial real estate services in Cleveland TN — sales, leasing, site selection, and investment analysis with CCIM/CPM-credentialed local expertise.",
        [("Commercial", hub)], body,
        faqs=[
            ("What commercial services does Bender Realty offer?", "Commercial sales and acquisitions, landlord and tenant lease representation, site selection, and investment analysis across Cleveland and Southeast Tennessee."),
            ("What do CCIM and CPM mean?", "CCIM (Certified Commercial Investment Member) and CPM (Certified Property Manager) are among the most rigorous professional credentials in commercial real estate — signifying advanced training in investment analysis and property management."),
            ("Can you help my business find space in Cleveland?", f"Yes — tell us your space, location, and budget requirements and we'll identify options, including properties not publicly listed. Call {PHONE} to start."),
        ])
    comm_children = [
        ("for-sale", "Commercial for Sale", "Commercial Property for Sale in Cleveland TN",
         ["Commercial property for sale across Cleveland, Bradley County, and Southeast Tennessee — retail, office, industrial, land, and investment properties.",
          "Cleveland's growth corridor along I-75, the APD-40 bypass, and the Paul Huff Parkway retail district all present distinct opportunities. We help buyers match property to strategy, with realistic underwriting on income properties."], True),
        ("for-lease", "Commercial for Lease", "Commercial Space for Lease in Cleveland TN",
         ["Available commercial lease space in the Cleveland area — retail storefronts, office suites, flex space, and industrial.",
          "We represent both landlords seeking qualified tenants and businesses seeking space. Either way, lease terms matter as much as rent: CAM charges, escalations, build-out allowances, and renewal options all affect your true cost."], True),
        ("site-selection", "Site Selection", "Commercial Site Selection in Southeast Tennessee",
         ["Choosing the right location may be the most important commercial decision a business makes. Our site-selection work combines traffic patterns, demographics, zoning, utilities, and growth trajectories across Cleveland and Southeast Tennessee.",
          "The region's fundamentals are compelling: I-75 logistics access, no state income tax, aggressive industrial recruitment, and a growing consumer base. We help retailers, medical practices, industrial users, and developers find the site that fits."], False),
        ("investment-analysis", "Investment Analysis", "Commercial Investment Analysis | Cap Rates & 1031 Exchanges",
         ["Investment real estate decisions deserve real analysis — not back-of-napkin math. Our CCIM-trained commercial practice underwrites income property the institutional way: net operating income, cap rates, cash-on-cash returns, and debt sensitivity.",
          "Considering a 1031 exchange? Timing rules are strict (45-day identification, 180-day closing), and Southeast Tennessee's inventory of replacement properties moves quickly. We help exchangers plan ahead and execute cleanly."], False),
    ]
    for s, t, h1, paras, show_idx in comm_children:
        path = f"/commercial/{s}/"
        body = page_hero("Commercial", esc(t), "")
        body += content_section(h2(t.rsplit(" ", 1)[0], t.rsplit(" ", 1)[1]) + prose(paras))
        if show_idx:
            body += content_section(idx_placeholder(t + " — Cleveland TN area"), "container", alt=True)
        body += content_section(
            card_grid([(f"/commercial/{s2}/", t2, p2[0].split(". ")[0] + ".")
                       for s2, t2, _h, p2, _i in comm_children if s2 != s][:3]), "container", alt=not show_idx)
        add(path, f"{h1} | Bender Realty", paras[0].split(". ")[0] + ".",
            [("Commercial", hub), (t, path)], body,
            faqs=[
                (f"Does Bender Realty handle {t.lower()}?", paras[0]),
                ("How do I get started?", f"Call Bender Realty at {PHONE} and ask for the commercial team, or send a note through our contact page — we'll set up a conversation about your requirements."),
            ])

# ---------------------------------------------------------------- About, Contact
def build_about():
    hub = "/about/"
    body = page_hero("Since 1969", 'About <span class="gold">Bender Realty</span>',
                     "Experience. Integrity. Results. — for more than 55 years.")
    body += content_section(
        h2("A Cleveland Institution", "Since 1969") + prose([
            "Bender Realty opened its doors in Cleveland, Tennessee in 1969 — and has spent more than five decades helping Southeast Tennessee families buy, sell, rent, and invest. Through every market cycle since, our approach hasn't changed: local knowledge, honest advice, and results.",
            "Today Bender Realty is a full-service firm: residential sales across five counties, approximately 500 rental units under management, and a credentialed commercial practice — all from our office at 425 25th Street NW in Cleveland.",
            "We're not the biggest firm in Tennessee, and that's the point. We're the firm that knows this market house by house, and the one your neighbors have trusted for generations.",
        ]))
    body += content_section(
        card_grid([
            ("/about/our-agents/", "Our Agents", "Meet the local experts behind Bender Realty."),
            ("/about/our-office/", "Our Office", "Visit us at 425 25th Street NW, Cleveland TN."),
            ("/about/reviews/", "Reviews", "What our clients say about working with us."),
            ("/about/community/", "In the Community", "Our roots and involvement in Cleveland and beyond."),
            ("/about/careers/", "Careers", "Build your real estate career with Bender Realty."),
        ]), "container", alt=True)
    add(hub, "About Bender Realty | Cleveland TN Real Estate Since 1969",
        "Bender Realty has served Cleveland TN and Southeast Tennessee since 1969 — residential sales, ~500 rental units managed, and commercial expertise under one roof.",
        [("About", hub)], body,
        faqs=[
            ("How long has Bender Realty been in business?", "Bender Realty was founded in 1969 and has served Cleveland and Southeast Tennessee continuously for more than 55 years."),
            ("What services does Bender Realty offer?", "Residential buying and selling, property management (~500 units), commercial sales and leasing, land brokerage, and rentals — a full-service local firm."),
            ("Where is Bender Realty's office?", f"425 25th Street NW, Cleveland, TN 37311. Call us at {PHONE}."),
        ])
    # agents
    body = page_hero("Our Team", 'Meet Our <span class="gold">Agents</span>',
                     "Local experts across residential, commercial, and property management.")
    body += content_section(
        h2("The People Behind", "Bender Realty") + prose([
            "Around twenty agents call Bender Realty home — full-time local professionals who live in the communities they serve. Between them: decades of Cleveland-area experience, specialized land and lake knowledge, commercial credentials including CCIM, CPM, CRS, and GRI, and one shared standard for how clients are treated.",
            data.AGENTS_NOTE,
        ]) + f'<div style="margin-top:28px;"><a class="btn btn-primary" href="{u("/contact/")}">Get Matched with an Agent &#8594;</a></div>')
    add("/about/our-agents/", "Our Agents | Bender Realty Cleveland TN",
        "Meet the Bender Realty team — around 20 local agents serving Cleveland TN and Southeast Tennessee with residential, commercial, and land expertise.",
        [("About", hub), ("Our Agents", "/about/our-agents/")], body,
        faqs=[
            ("How many agents does Bender Realty have?", "Around twenty full-time local agents, covering residential, land, lake, and commercial specialties across Southeast Tennessee."),
            ("How do I choose the right agent?", f"Tell us what you're doing — buying, selling, investing, or leasing — and we'll match you with the agent whose specialty and coverage area fit best. Call {PHONE} to get started."),
        ])
    # office
    body = page_hero("Visit Us", 'Our Cleveland <span class="gold">Office</span>',
                     "425 25th Street NW, Cleveland, Tennessee 37311")
    body += content_section(
        h2("One Office,", "Five Counties") + prose([
            "Bender Realty operates from a single office in the heart of Cleveland — at 425 25th Street NW, just off Keith Street and minutes from downtown. From here, our agents cover Bradley, Polk, McMinn, Meigs, and Hamilton counties.",
            f"Sales office: {PHONE} &nbsp;·&nbsp; Property management: {PM_PHONE} &nbsp;·&nbsp; Email: {EMAIL}",
            "Office hours are Monday through Friday, 8:30 AM to 5:00 PM, and our agents show property seven days a week by appointment.",
        ]) + f'<div style="margin-top:28px;"><a class="btn btn-outline" href="https://www.google.com/maps/search/?api=1&query=425+25th+Street+NW+Cleveland+TN+37311" rel="noopener" target="_blank">Get Directions &#8594;</a></div>')
    add("/about/our-office/", "Our Office | Bender Realty | 425 25th Street NW, Cleveland TN",
        "Visit Bender Realty at 425 25th Street NW, Cleveland, TN 37311. Sales: (423) 472-2173 · Property Management: (423) 476-5518.",
        [("About", hub), ("Our Office", "/about/our-office/")], body,
        faqs=[
            ("What are Bender Realty's office hours?", "Monday through Friday, 8:30 AM to 5:00 PM — and our agents show property seven days a week by appointment."),
            ("Where do I park?", "On-site parking is available at our office at 425 25th Street NW, Cleveland."),
        ])
    # reviews
    reviews = [
        ("Bender Realty went above and beyond to help us find our dream home. Their local knowledge and dedication made the entire process smooth and stress-free.", "Jessica and Mark R."),
        ("They managed our rental property for years without a single headache on our end. Statements on time, good tenants, problems handled.", "D. Sutton, property owner"),
        ("Sold our home in nine days at full asking price. The pricing advice and photos made the difference.", "The Hendersons"),
        ("As first-time buyers we had a thousand questions. Our agent answered every one and never rushed us.", "Amber T."),
    ]
    review_cards = "".join(f'''<div class="review-card">
      <p class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</p>
      <p>&#8220;{esc(q)}&#8221;</p>
      <p class="attrib">&mdash; {esc(a)}</p>
    </div>''' for q, a in reviews)
    body = page_hero("Client Reviews", 'What Our Clients <span class="gold">Say</span>', "")
    body += content_section(
        h2("Reviews &", "Testimonials") + prose([
            "The best measure of a real estate firm is what its clients say afterward. Here's a sample — and we're glad to connect you with past clients as references.",
        ]) + f'<div class="review-grid">{review_cards}</div>'
        + '<p class="idx-note" style="margin-top:24px;">Sample testimonials shown; verified review feeds (Google, Testimonial Tree) will be connected here.</p>')
    add("/about/reviews/", "Reviews & Testimonials | Bender Realty Cleveland TN",
        "Read what clients say about buying, selling, and renting with Bender Realty in Cleveland TN and Southeast Tennessee.",
        [("About", hub), ("Reviews", "/about/reviews/")], body,
        faqs=[
            ("Where can I read Bender Realty reviews?", "Right here on our reviews page, and on our Google Business Profile. We're also glad to provide references from past clients on request."),
            ("Can I leave a review?", "Please do — reviews on Google help neighbors find us. If anything about your experience wasn't right, call us first so we can fix it."),
        ])
    # community
    body = page_hero("Local Roots", 'In the <span class="gold">Community</span>', "")
    body += content_section(
        h2("Invested in", "Southeast Tennessee") + prose([
            "A firm doesn't last 55 years in one town without giving back to it. Bender Realty and our agents support local schools, youth sports, charitable organizations, and community events across Cleveland and Bradley County — because this is home, not just a market.",
            "Our agents serve on local boards, coach teams, and volunteer across the community. When you work with Bender Realty, you're working with neighbors.",
        ]))
    add("/about/community/", "Community Involvement | Bender Realty Cleveland TN",
        "Bender Realty has supported Cleveland TN schools, charities, and community organizations for more than 55 years. Local roots, local commitment.",
        [("About", hub), ("Community", "/about/community/")], body)
    # careers
    body = page_hero("Join Our Team", 'Careers at <span class="gold">Bender Realty</span>', "")
    body += content_section(
        h2("Build Your Career", "With Us") + prose([
            "Whether you're newly licensed or an experienced agent looking for a better home, Bender Realty offers what big-box brokerages can't: a 55-year local brand, genuine mentorship, built-in property management and commercial referral streams, and a culture where agents help each other.",
            "We keep our team intentionally sized — around twenty agents — so every agent gets broker support, office resources, and leads without getting lost in a crowd.",
            f"Interested? Call {PHONE} and ask for the broker, or send a confidential note through our contact page.",
        ]) + f'<div style="margin-top:28px;"><a class="btn btn-primary" href="{u("/contact/")}">Start a Confidential Conversation &#8594;</a></div>')
    add("/about/careers/", "Real Estate Careers in Cleveland TN | Join Bender Realty",
        "Join Bender Realty — a 55-year Cleveland TN brand with mentorship, referral streams from property management and commercial, and a supportive team culture.",
        [("About", hub), ("Careers", "/about/careers/")], body,
        faqs=[
            ("Does Bender Realty accept new agents?", "Yes — we welcome newly licensed agents and provide real mentorship to build your business the right way."),
            ("What makes Bender Realty different for agents?", "A trusted 55-year local brand, referral flow from ~500 managed rentals and a commercial practice, and a team small enough that you're never just a number."),
        ])

def build_contact():
    body = page_hero("We're Here to Help", 'Contact <span class="gold">Bender Realty</span>',
                     "Call, email, or send a message — a local team member will respond promptly.")
    contact_info = f'''<div class="contact-grid">
  <div class="contact-info">
    <h3>Office</h3>
    <p>425 25th Street NW<br>Cleveland, TN 37311</p>
    <h3>Phone</h3>
    <p>Sales: <a href="tel:{PHONE_TEL}">{PHONE}</a><br>Property Management: <a href="tel:{PM_PHONE_TEL}">{PM_PHONE}</a></p>
    <h3>Email</h3>
    <p>General: <a href="mailto:{EMAIL}">{EMAIL}</a><br>Property Management: <a href="mailto:{PM_EMAIL}">{PM_EMAIL}</a></p>
    <h3>Hours</h3>
    <p>Monday&ndash;Friday: 8:30 AM &ndash; 5:00 PM<br>Showings by appointment 7 days a week</p>
  </div>
  <form class="lead-form" onsubmit="return false;">
    <h3>Send Us a Message</h3>
    <div class="lf-row"><label>Name<input type="text" name="name"></label><label>Phone<input type="tel" name="phone"></label></div>
    <label>Email<input type="email" name="email"></label>
    <label>I need help with
      <select name="dept"><option>Buying a home</option><option>Selling a home</option><option>Property management</option><option>Renting</option><option>Commercial</option><option>Something else</option></select>
    </label>
    <label>Message<textarea name="message" rows="4"></textarea></label>
    <button class="btn btn-primary" type="submit">Send Message &#8594;</button>
  </form>
</div>'''
    body += content_section(h2("Get in", "Touch") + contact_info, "container")
    add("/contact/", "Contact Bender Realty | Cleveland TN Real Estate | (423) 472-2173",
        "Contact Bender Realty in Cleveland TN — sales (423) 472-2173, property management (423) 476-5518, or send a message online. Office at 425 25th Street NW.",
        [("Contact", "/contact/")], body,
        faqs=[
            ("What's the fastest way to reach Bender Realty?", f"Call the office at {PHONE} during business hours. For property management matters, call {PM_PHONE} directly."),
            ("Can I schedule a showing online?", "Yes — use our schedule-a-showing form with the property address, or call and we'll set it up immediately."),
        ], include_cta=False)
    # showing
    body = page_hero("See a Property", 'Schedule a <span class="gold">Showing</span>', "")
    body += content_section(h2("Schedule a", "Showing") + prose([
        "Found a property you want to see? Tell us which one and when works for you — we'll confirm your showing promptly.",
    ]) + f'''<div class="lead-form-wrap"><form class="lead-form" onsubmit="return false;">
    <h3>Request a Showing</h3>
    <div class="lf-row"><label>Name<input type="text" name="name"></label><label>Phone<input type="tel" name="phone"></label></div>
    <label>Email<input type="email" name="email"></label>
    <label>Property Address or MLS #<input type="text" name="property"></label>
    <label>Preferred Days/Times<input type="text" name="times"></label>
    <button class="btn btn-primary" type="submit">Request Showing &#8594;</button>
  </form></div>''')
    add("/contact/schedule-a-showing/", "Schedule a Showing | Bender Realty",
        "Schedule a property showing with Bender Realty — tell us the property and your preferred times, and we'll confirm promptly.",
        [("Contact", "/contact/"), ("Schedule a Showing", "/contact/schedule-a-showing/")], body, include_cta=False)
    # ask a question
    body = page_hero("Questions Welcome", 'Ask a <span class="gold">Question</span>', "")
    body += content_section(h2("Ask Us", "Anything") + prose([
        "Not ready to buy or sell — just have a question? Ask away. Real estate, rentals, land, the local market: if we know the answer (and after 55 years, we usually do), you'll have it quickly.",
    ]) + f'''<div class="lead-form-wrap"><form class="lead-form" onsubmit="return false;">
    <h3>Your Question</h3>
    <div class="lf-row"><label>Name<input type="text" name="name"></label><label>Email<input type="email" name="email"></label></div>
    <label>Question<textarea name="question" rows="4"></textarea></label>
    <button class="btn btn-primary" type="submit">Send Question &#8594;</button>
  </form></div>''')
    add("/contact/ask-a-question/", "Ask a Question | Bender Realty",
        "Have a real estate question about Cleveland TN or Southeast Tennessee? Ask Bender Realty — quick answers from local experts.",
        [("Contact", "/contact/"), ("Ask a Question", "/contact/ask-a-question/")], body, include_cta=False)

# ---------------------------------------------------------------- Search & listings
def build_search():
    body = page_hero("MLS Search", 'Search <span class="gold">Listings</span>',
                     "Every active listing in the River Counties MLS, updated continuously.")
    body += content_section(idx_placeholder("Full MLS map & grid search — River Counties MLS"), "container")
    body += content_section(
        h2("Popular", "Searches", left=True) +
        card_grid([
            ("/homes-for-sale/cleveland/", "Cleveland Homes", "Homes for sale in Cleveland TN."),
            ("/homes-for-sale/lakefront/", "Lakefront", "Waterfront on Chickamauga & Watts Bar."),
            ("/homes-for-sale/acreage/", "Acreage", "Homes with land across the region."),
            ("/homes-for-sale/new-construction/", "New Construction", "New builds in growing communities."),
            ("/land/", "Land", "Farms, lots, and recreational tracts."),
            ("/homes-for-sale/", "All Categories", "Browse every location and property type."),
        ]), "container", alt=True)
    add("/search/", "Search Homes for Sale | MLS Listings | Bender Realty",
        "Search every active MLS listing in Cleveland TN and Southeast Tennessee — map search, filters, and instant alerts from Bender Realty.",
        [("Search Listings", "/search/")], body)
    for slug, title, kicker, blurb in [
        ("featured", "Featured Listings", "Bender Realty Exclusives", "Hand-picked current listings represented by Bender Realty agents — see them here first."),
        ("open-houses", "Open Houses", "Visit This Week", "Upcoming open houses across Cleveland and Southeast Tennessee. Stop by — no appointment needed."),
        ("sold", "Recently Sold", "Market Results", "Recently closed sales across our market — proof of pricing, and useful intel if you're planning your own move."),
    ]:
        path = f"/listings/{slug}/"
        body = page_hero(kicker, esc(title), "")
        body += content_section(h2(title.split(" ")[0], " ".join(title.split(" ")[1:])) + prose([blurb]))
        body += content_section(idx_placeholder(title), "container", alt=True)
        add(path, f"{title} | Bender Realty Cleveland TN", blurb,
            [("Search Listings", "/search/"), (title, path)], body)

# ---------------------------------------------------------------- Blog
def build_blog():
    hub = "/blog/"
    cat_items = [(f"/blog/category/{s}/", n, d) for s, n, d in data.BLOG_CATEGORIES]
    post_cards = "".join(f'''<a class="hub-card" href="{u('/blog/%s/' % ps)}">
      <span class="pop-kicker" style="color:var(--gold-deep);font-family:var(--font-ui);font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;">{esc(dict((s,n) for s,n,_ in data.BLOG_CATEGORIES)[cat])}</span>
      <h3>{esc(pt)}</h3>
      <p>{esc(pd)}</p>
      <span class="text-link">Read More &#8594;</span>
    </a>''' for ps, pt, cat, pd, _paras in data.BLOG_POSTS)
    body = page_hero("News & Insight", 'The Bender Realty <span class="gold">Blog</span>',
                     "Market reports, local guides, and real estate advice for Southeast Tennessee.")
    body += content_section(h2("Latest", "Posts", left=True) + f'<div class="hub-grid">{post_cards}</div>', "container")
    body += content_section(h2("Browse by", "Category", left=True) + card_grid(cat_items), "container", alt=True)
    add(hub, "Blog | Cleveland TN Real Estate News & Market Reports | Bender Realty",
        "Cleveland TN market reports, moving guides, lake living, and real estate advice from Bender Realty — local insight for Southeast Tennessee.",
        [("Blog", hub)], body)
    for s, n, d in data.BLOG_CATEGORIES:
        path = f"/blog/category/{s}/"
        posts_in = [(f"/blog/{ps}/", pt, pd) for ps, pt, cat, pd, _p in data.BLOG_POSTS if cat == s]
        body = page_hero("Blog Category", esc(n), d)
        inner = h2(n, "Articles", left=True)
        if posts_in:
            inner += card_grid(posts_in)
        else:
            inner += "<p>New articles in this category are coming soon. In the meantime, explore the latest posts on our <a href='%s'>blog home</a>.</p>" % u("/blog/")
        body += content_section(inner, "container")
        add(path, f"{n} | Bender Realty Blog", d, [("Blog", hub), (n, path)], body)
    for ps, pt, cat, pd, paras in data.BLOG_POSTS:
        path = f"/blog/{ps}/"
        cat_name = dict((s, n) for s, n, _ in data.BLOG_CATEGORIES)[cat]
        body = page_hero(cat_name, esc(pt), "")
        body += content_section("<article>" + prose(paras) + "</article>")
        body += content_section(
            h2("Keep", "Reading", left=True) +
            card_grid([(f"/blog/{ps2}/", pt2, pd2) for ps2, pt2, _c, pd2, _p in data.BLOG_POSTS if ps2 != ps]
                      + [(f"/blog/category/{cat}/", f"More in {cat_name}", "Browse every article in this category.")]),
            "container", alt=True)
        schema = {
            "@context": "https://schema.org", "@type": "BlogPosting",
            "headline": pt, "description": pd,
            "author": {"@type": "Organization", "name": "Bender Realty"},
            "publisher": {"@type": "Organization", "name": "Bender Realty"},
            "mainEntityOfPage": abs_u(path),
            "datePublished": "2026-08-11",
        }
        add(path, f"{pt} | Bender Realty Blog", pd, [("Blog", "/blog/"), (pt, path)], body,
            extra_schema=schema, og_type="article")

# ---------------------------------------------------------------- Legal & utility
def build_utility():
    legal = [
        ("privacy-policy", "Privacy Policy",
         ["Bender Realty respects your privacy. This policy describes the information we collect through this website and how we use it.",
          "<strong>Information we collect.</strong> When you submit a form (contact, valuation, showing request, or application inquiry), we collect the details you provide — typically your name, contact information, and message — solely to respond to your request and provide real estate services.",
          "<strong>How we use it.</strong> We use your information to respond to inquiries, provide requested services, and, with your consent, send relevant market updates. We do not sell your personal information.",
          "<strong>Cookies & analytics.</strong> This site may use standard analytics tools to understand site usage and improve our services. You can control cookies through your browser settings.",
          "<strong>Contact.</strong> Questions about this policy? Contact Bender Realty at bender@bender-realty.com or (423) 472-2173."]),
        ("terms-of-use", "Terms of Use",
         ["Welcome to the Bender Realty website. By using this site, you agree to these terms.",
          "<strong>Informational purposes.</strong> Content on this site is provided for general information about real estate in Southeast Tennessee and is not legal, tax, or financial advice. Consult appropriate professionals for advice specific to your situation.",
          "<strong>Listing data.</strong> Property information is believed accurate but is not guaranteed and should be independently verified. Listing data may be provided by the MLS and is subject to its terms.",
          "<strong>Intellectual property.</strong> Site content, design, and branding are the property of Bender Realty and may not be reproduced without permission.",
          "<strong>Contact.</strong> Questions about these terms? Contact Bender Realty at bender@bender-realty.com."]),
        ("accessibility", "Accessibility Statement",
         ["Bender Realty is committed to making this website accessible to all users, including people with disabilities.",
          "We aim to follow the Web Content Accessibility Guidelines (WCAG) 2.1 Level AA — including semantic page structure, descriptive alt text, sufficient color contrast, and keyboard-navigable interfaces — and we work to improve accessibility continuously.",
          "<strong>Need assistance?</strong> If any part of this site is difficult to use, or you'd like information in an alternative format, call us at (423) 472-2173 or email bender@bender-realty.com and we'll gladly help.",
          "We also honor fair housing principles in everything we do. Equal Housing Opportunity."]),
        ("fair-housing", "Fair Housing",
         ["Bender Realty supports and complies with the Fair Housing Act and Tennessee fair housing laws. We provide equal professional service to all, without regard to race, color, religion, sex, disability, familial status, or national origin.",
          "Every listing we represent and every rental we manage is offered on an equal opportunity basis. Our agents and staff receive fair housing training, and we take our obligations under the law — and to our community — seriously.",
          "<strong>Equal Housing Opportunity.</strong> If you believe you have experienced housing discrimination, you may file a complaint with the U.S. Department of Housing and Urban Development (HUD) at hud.gov or 1-800-669-9777."]),
        ("dmca-mls-compliance", "DMCA & MLS Compliance",
         ["<strong>MLS data.</strong> Listing information displayed on this site may be provided through the River Counties Association of REALTORS MLS Internet Data Exchange (IDX) program. Data is deemed reliable but not guaranteed, is for consumers' personal, non-commercial use, and may not be used for any purpose other than identifying prospective properties.",
          "<strong>Copyright.</strong> If you believe content on this site infringes your copyright, please send a notice compliant with the Digital Millennium Copyright Act (DMCA) to bender@bender-realty.com including: identification of the work, the allegedly infringing material's location, your contact information, and a statement of good-faith belief.",
          "We respond promptly to valid notices."]),
    ]
    for s, t, paras in legal:
        path = f"/{s}/"
        body = page_hero("Bender Realty", esc(t), "")
        body += content_section("<article>" + prose(paras) + "</article>")
        add(path, f"{t} | Bender Realty", f"{t} for the Bender Realty website.",
            [(t, path)], body, include_cta=False)
    # HTML sitemap
    def links_list(paths):
        return "<ul class='sitemap-list'>" + "".join(
            f"<li><a href='{u(p)}'>{esc(p)}</a></li>" for p in paths) + "</ul>"
    groups = {}
    for p in sorted(PAGES):
        top = p.strip("/").split("/")[0] or "home"
        groups.setdefault(top, []).append(p)
    inner = h2("HTML", "Sitemap")
    for top in sorted(groups):
        inner += f"<h3 style='margin-top:26px;'>/{esc(top)}/</h3>" + links_list(groups[top])
    body = page_hero("Every Page", 'Site <span class="gold">Map</span>', "")
    body += content_section(inner)
    add("/sitemap/", "Sitemap | Bender Realty", "Complete page index for the Bender Realty website.",
        [("Sitemap", "/sitemap/")], body, include_cta=False)
    # 404 (root 404.html for GitHub Pages)
    body = page_hero("Page Not Found", 'Let&#8217;s Get You <span class="gold">Home</span>',
                     "The page you're looking for doesn't exist — but these will help.")
    body += content_section(
        card_grid([
            ("/", "Homepage", "Start fresh from the Bender Realty homepage."),
            ("/search/", "Search Listings", "Find homes for sale across Southeast Tennessee."),
            ("/areas-we-serve/", "Areas We Serve", "Browse every community we cover."),
            ("/contact/", "Contact Us", "Call or message us — we'll point you the right way."),
        ]), "container")
    render_page("/404/", "Page Not Found | Bender Realty",
                "The page you requested was not found. Search homes for sale or browse communities with Bender Realty.",
                [], body, include_cta=False)
    os.replace(os.path.join(OUT, "404", "index.html"), os.path.join(OUT, "404.html"))
    os.rmdir(os.path.join(OUT, "404"))
    # thank you
    body = page_hero("Message Received", 'Thank <span class="gold">You</span>',
                     "A member of our team will follow up shortly.")
    body += content_section(prose([
        "Thanks for reaching out to Bender Realty. We've received your message and a local team member will respond promptly — usually within one business day.",
        f"Need something faster? Call us at {PHONE} (sales) or {PM_PHONE} (property management).",
    ]) + f'<div style="margin-top:24px;"><a class="btn btn-primary" href="{u("/")}">Back to Homepage &#8594;</a></div>')
    render_page("/thank-you/", "Thank You | Bender Realty",
                "Thanks for contacting Bender Realty — we'll respond promptly.",
                [("Thank You", "/thank-you/")], body, include_cta=False)

# ---------------------------------------------------------------- sitemap.xml & robots
def build_sitemap_xml():
    urls = ["/"] + sorted(PAGES)
    entries = "".join(
        f"<url><loc>{abs_u(p)}</loc><changefreq>weekly</changefreq></url>" for p in urls)
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                + entries + "</urlset>")
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")

# ---------------------------------------------------------------- homepage link prefixing
def fix_homepage():
    p = os.path.join(OUT, "index.html")
    with open(p) as f:
        html = f.read()
    # prefix root-relative internal links that aren't already prefixed
    html = re.sub(r'href="/(?!/|bender-realty-site)', 'href="%s/' % BASE, html)
    html = html.replace('href="css/styles.css"', 'href="%s/css/styles.css"' % BASE)
    # canonical/OG to live URL
    html = html.replace('https://bender-realty.com/', SITE_URL + '/')
    with open(p, "w") as f:
        f.write(html)

if __name__ == "__main__":
    build_areas()
    build_hfs()
    build_land()
    build_buy()
    build_sell()
    build_pm()
    build_rentals()
    build_commercial()
    build_about()
    build_contact()
    build_search()
    build_blog()
    build_utility()
    build_sitemap_xml()
    fix_homepage()
    print(f"Built {len(PAGES)+1} pages (incl. homepage) + sitemap.xml + robots.txt + 404.html + thank-you")
