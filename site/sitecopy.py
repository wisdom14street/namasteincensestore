"""Namaste Incense Store (namasteincensestore.com): value packs, bulk boxes and gifts. Copy written for this site only."""
import re
E = __import__('html').escape

AISLES = {
 'packs':   ('Multi-Packs & Bulk Boxes', 'Multi-Packs', 'multi-packs-bulk', 'Boxes of tubes, packs of several and bulk bags: the lowest cost per stick in the building.', '#ff6b4a'),
 'gifts':   ('Gift Sets & Kits', 'Gift Sets', 'gift-sets', 'Boxed sets, samplers, kits and bundles that are ready to hand over.', '#8b5cf6'),
 'under5':  ('Under $5', 'Under $5', 'under-5', 'Single packs, cones and small bundles that cost less than a coffee.', '#16a34a'),
 'u10':     ('$5 to $10', '$5–$10', '5-to-10', 'Bigger packs, resin jars, candles and holders in the five-to-ten range.', '#0ea5e9'),
 'u20':     ('$10 to $20', '$10–$20', '10-to-20', 'Premium boxes, larger candles and burners, still under twenty dollars.', '#f59e0b'),
 'holders': ('Holders & Burners under $20', 'Holders', 'holders-burners', 'Ash catchers, cone dishes, censers and charcoal, every one under $20.', '#64748b'),
}
def assign(x):
    p = x['price']
    if x['multi'] and x['base'] in ('sticks', 'cones', 'resins', 'smudge', 'burners'): return 'packs'
    if x['gift'] and p < 40: return 'gifts'
    if x['base'] in ('holders', 'burners'): return 'holders' if p < 20 else ''
    if p < 5: return 'under5'
    if p < 10: return 'u10'
    if p < 20: return 'u20'
    return ''

VISIT_EYEBROW = 'Grab it in person'
def STORE_DESC(S): return f'Value incense store on West 14th Street near Union Square: multi-packs, bulk boxes, gift sets and incense under $5, $10 and $20, about {S.ABOUT_N:,} items.'
REVIEW_TITLE = 'Got a good deal?'
REVIEW_TEXT = 'Leave us a quick Google review so more people near Union Square can find affordable incense. It takes under a minute.'
LOGO_SVG = '<svg viewBox="0 0 40 40"><rect x="9" y="18" width="22" height="15" rx="3" fill="#ffd23f"/><path d="M15 18v-9M20 18v-12M25 18v-9" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/><circle cx="20" cy="25.5" r="3" fill="#ff6b4a"/></svg>'
WORDMARK = 'Namaste Incense <b>Store</b>'
BAR_TEXT = 'Value packs & gifts at 2 W 14th St'
SEARCH_PLACEHOLDER = 'Search packs, gifts, scents under $10'

QUIZ = {
 'slug': 'gift-finder', 'nav': 'Gift finder', 'cta': 'Find a gift',
 'title': 'Incense Gift Finder: Ideas Under $5, $10 & $20', 'desc': 'Answer three questions to find an incense gift in stock near Union Square, from stocking stuffers under $5 to gift sets under $20.',
 'h1': 'Incense gift finder', 'lead': 'Who is it for, what do they like, and what do you want to spend? We will show gifts that are in stock right now. Your answers stay on this page.',
 'submit': 'Show gift ideas',
 'questions': [
  {'q': 'Who are you shopping for?', 'options': [
    {'label': 'Someone new to incense', 'filter': {'base': ['sticks', 'cones']}},
    {'label': 'A crystals-and-sage kind of friend', 'filter': {'base': ['smudge', 'candles']}},
    {'label': 'Someone who likes a boxed set', 'filter': {'gift': 1}},
    {'label': 'Me, stocking up', 'filter': {'multi': 1}}]},
  {'q': 'Which scents do they like?', 'options': [
    {'label': 'Classic Nag Champa', 'filter': {'fam': ['nag-champa']}},
    {'label': 'Sweet, fruity or vanilla', 'filter': {'fam': ['sweet']}},
    {'label': 'Flowers like rose or lavender', 'filter': {'fam': ['floral']}},
    {'label': 'Earthy: sandalwood, sage, resin', 'filter': {'fam': ['woods', 'herbal', 'resinous']}}]},
  {'q': 'Budget?', 'options': [
    {'label': 'Under $5', 'filter': {'maxp': 5}}, {'label': 'Under $10', 'filter': {'maxp': 10}}, {'label': 'Under $20', 'filter': {'maxp': 20}}]},
 ]}

def FOOTER_EXPLORE(S):
    return [('Gift finder', '/gift-finder/'), ('Best sellers under $5', '/best-sellers-under-5/'), ('Best sellers under $10', '/best-sellers-under-10/'), ('Best sellers under $20', '/best-sellers-under-20/'),
            ('Bulk incense sticks', '/bulk-incense-sticks/'), ('Stocking stuffers', '/stocking-stuffers/'), ('Stock-up guide', '/guide/how-to-stock-up-on-incense/'), ('Affordable incense near Union Square', '/affordable-incense-near-union-square/')]
FOOT_BLURB = 'The value counter at 2 West 14th Street: incense by the box, gifts by the dozen and plenty under ten dollars.'
HERO_BASES = ('sticks', 'cones', 'smudge', 'holders')
def HERO(S):
    return {'eyebrow': 'Value packs &middot; Bulk boxes &middot; Gifts &middot; Union Square',
            'h1': f'Incense from {S.money(S.MIN_STICK)}. <em>Boxes, bundles and gifts that go further.</em>',
            'lede': f'{S.UNDER10:,} items under $10 and {S.MULTI_N:,} multi-packs and bulk boxes, all in stock at 2 West 14th Street. Stock up in person or reserve online and grab it on your way past Union Square.',
            'shop_cta': 'Shop deals'}

def _bands(S):
    tiles = ''.join(f'<a class="scent" href="/shop/{AISLES[k][2]}/" style="--c:{AISLES[k][4]}"><b>{E(AISLES[k][0])}</b><span>{E(AISLES[k][3])}</span><small>{S.cat_count[k]} items</small></a>' for k in S.AISLE_KEYS)
    return f'<section class="wrap"><div class="sechead"><h2>Shop by budget</h2><a href="/gift-finder/">Need a gift idea? &rarr;</a></div><div class="scents">{tiles}</div></section>'
def _best(lo, hi): return lambda S: S.by_rank([x for x in S.leaders if lo <= x['price'] < hi])[:8]
def _packs(S): return S.by_rank([x for x in S.leaders if x['aisle'] == 'packs'])[:8]
def _gifts(S): return S.by_rank([x for x in S.leaders if x['aisle'] == 'gifts'])[:8]
def _new(S): return S.leaders[:8]
def _whys(S):
    return [(f'{S.UNDER10:,} items under $10', 'Every price is on the listing, so you can plan a haul before you leave home.'),
            (f'{S.MULTI_N:,} multi-packs', 'Boxes of tubes and multi-stick packs bring the cost of each stick down.'),
            (('Reserve, then grab it', f'Choose Pickup at checkout and collect on 14th Street. Orders are {S.READY.lower()}.') if S.PICKUP_ON else ('', '')),
            ('Gift-ready', 'Sets, samplers and kits that need nothing more than a bag.')]
HOME_SECTIONS = [
 {'type': 'html', 'html': _bands},
 {'type': 'grid', 'title': 'Best sellers under $5', 'select': _best(0, 5), 'href': '/best-sellers-under-5/', 'link': 'See all under $5', 'intro': 'Ranked by what customers buy most at namastebookshop.com; updated daily.'},
 {'type': 'grid', 'title': 'Biggest boxes: multi-packs & bulk', 'select': _packs, 'href': '/shop/multi-packs-bulk/', 'link': 'All multi-packs'},
 {'type': 'visit'},
 {'type': 'collections', 'title': 'Quick picks', 'items': [
   {'title': 'Stocking stuffers', 'blurb': 'Small, cheap, cheerful.', 'href': '/stocking-stuffers/', 'filter': {'maxp': 10, 'base': ['sticks', 'cones', 'smudge', 'holders']}},
   {'title': 'Bulk incense sticks', 'blurb': 'Boxes of tubes and big packs.', 'href': '/bulk-incense-sticks/', 'filter': {'multi': 1, 'base': ['sticks']}},
   {'title': 'Gift sets & kits', 'blurb': 'Ready to wrap.', 'href': '/shop/gift-sets/', 'filter': {'aisle': ['gifts']}},
   {'title': 'Nag Champa value packs', 'blurb': 'The classic, by the box.', 'href': '/nag-champa-value-packs/', 'filter': {'fam': ['nag-champa'], 'multi': 1}},
   {'title': 'Holders under $20', 'blurb': 'Catch the ash for less.', 'href': '/shop/holders-burners/', 'filter': {'aisle': ['holders']}},
   {'title': 'Best sellers under $20', 'blurb': 'Treat-yourself territory.', 'href': '/best-sellers-under-20/', 'filter': {'maxp': 20}}]},
 {'type': 'grid', 'title': 'Gift sets people pick up', 'select': _gifts, 'href': '/shop/gift-sets/', 'link': 'All gift sets'},
 {'type': 'quiz', 'title': 'Buying for someone else?', 'text': 'Three taps and we will show in-stock gift ideas within your budget.'},
 {'type': 'grid', 'title': 'Best sellers $5 to $10', 'select': _best(5, 10), 'href': '/best-sellers-under-10/', 'link': 'See all under $10'},
 {'type': 'whys', 'title': 'Why stock up here', 'items': _whys},
 {'type': 'grid', 'title': 'New on the shelves', 'select': _new, 'href': '/shop/?sort=new', 'link': 'All new'},
 {'type': 'brands', 'title': 'Brands for less', 'n': 12},
 {'type': 'review'},
 {'type': 'band', 'title': 'Reserve online, grab it in person', 'text': lambda S: 'Every price and stock level on this site comes straight from our store each day. Reserve now and pick up on 14th Street, or have it shipped from NYC.',
  'steps': lambda S: [('Fill your bag', 'Filter by budget, scent or brand.'), ('Pick Pickup at checkout', 'Secure Shopify checkout through namastebookshop.com.'), ('Swing by', f'{S.STORE_ADDR}, a few minutes from Union Square.')]},
]
def HOME_TITLE(S): return 'Namaste Incense Store | Incense Multi-Packs, Bulk & Gifts near Union Square'
def HOME_DESC(S): return f'Affordable incense near Union Square: {S.UNDER10:,} items under $10, multi-packs, bulk boxes and gift sets, from {S.money(S.MIN_STICK)}. Reserve online, pick up at 2 West 14th Street.'
def SHOP_TITLE(S): return 'Shop Value Incense, Multi-Packs & Gifts | Namaste Incense Store'
def SHOP_DESC(S): return f'{S.N:,} budget-friendly incense items: multi-packs, bulk boxes, gift sets, holders and picks under $5, $10 and $20. Pick up near Union Square or ship from NYC.'
SHOP_H1 = 'Every deal in the store'
def SHOP_SUB(S): return f'{S.N:,} items, sorted into {len(S.AISLE_KEYS)} budget aisles. Filter by scent, brand or price.'
def AISLE_TITLE(S, k): return f'{AISLES[k][0]}: Incense Deals near Union Square | Namaste Incense Store'
def AISLE_DESC(S, k): return f'{S.cat_count[k]} items in {AISLES[k][0]} at Namaste Incense Store, 2 West 14th Street, NYC. {AISLES[k][3]}'

def LANDINGS(S):
    L = []
    for cap, slug in ((5, 'best-sellers-under-5'), (10, 'best-sellers-under-10'), (20, 'best-sellers-under-20')):
        n = sum(1 for x in S.products if x['price'] < cap)
        L.append({'path': f'/{slug}/', 'title': f'Best-Selling Incense Under ${cap} | Namaste Incense Store', 'desc': f'{n} incense items under ${cap}, sorted by what sells most, in stock near Union Square, NYC.',
                  'h1': f'Best sellers under ${cap}', 'sub': f'{n} items under ${cap}, best sellers first.', 'filter': {'maxp': cap}})
    L += [
     {'path': '/bulk-incense-sticks/', 'title': 'Bulk Incense Sticks & Boxes in NYC | Namaste Incense Store', 'desc': 'Boxes of incense tubes, big stick packs and bulk incense near Union Square. Reserve online and pick up.',
      'h1': 'Bulk incense sticks', 'sub': 'Boxes, big packs and multi-tube cartons.', 'filter': {'multi': 1, 'base': ['sticks']},
      'intro': '<p class="intro">A box of tubes or a big pack usually brings the price per stick well below a single pack. Compare the listing photos to see how many tubes or sticks each one holds.</p>'},
     {'path': '/nag-champa-value-packs/', 'title': 'Nag Champa Value Packs & Boxes | Namaste Incense Store', 'desc': 'Nag Champa incense in boxes and multi-packs near Union Square, NYC.', 'h1': 'Nag Champa value packs', 'sub': 'The classic scent, by the box.', 'filter': {'fam': ['nag-champa'], 'multi': 1}},
     {'path': '/stocking-stuffers/', 'title': 'Incense Stocking Stuffers Under $10 | Namaste Incense Store', 'desc': 'Incense sticks, cones, sage and holders under $10 that fit a stocking, near Union Square.', 'h1': 'Stocking stuffers', 'sub': 'Little gifts under $10.', 'filter': {'maxp': 10, 'base': ['sticks', 'cones', 'smudge', 'holders']}},
     {'path': '/incense-sampler-gifts/', 'title': 'Incense Samplers & Variety Packs | Namaste Incense Store', 'desc': 'Incense samplers, variety packs and assorted boxes for trying several scents, near Union Square.', 'h1': 'Samplers & variety packs', 'sub': 'Try several scents in one buy.', 'filter': {'q': 'sampler|variety|assorted|collection'}},
    ]
    return L

BRAND_TEXT = {
 'hem': 'HEM sells the most boxes in our value aisles. The company, HEM Corporation, was started in India in 1983 by three Shah brothers and now has plants in Mumbai and Bengaluru.',
 'satya': "Satya's hand-rolled masala sticks come from Shrinivas Sugandhalaya in Bangalore, whose Sai Baba Nag Champa is the original of the famous blue box. Multi-packs are the cheapest way to keep it in the house.",
 'morning-star': 'Low-smoke Japanese sticks from Nippon Kodo, normally packed with a small holder, so one box is a ready-made gift.',
 'herb-earth': "Nippon Kodo's natural-scent bamboo sticks: a calm, low-smoke option in a neat box.",
 'good-karma': 'Hand-poured soy-blend intention candles in recyclable tins, made in the USA by Zensual in Southern California. They make easy gifts.',
 'sonavi': 'Sticks, bakhoor and beeswax candles imported by New Age Imports of Placentia, California.',
 'prabhujis': "Handmade in India's cottage industry and packed in recycled cardboard by Prabhuji's Gifts, a Green America certified business.",
 'coventry-creations': 'Intention candles from a family- and woman-owned maker in Ferndale, Michigan (now Coventry Products).',
 'wolf-spirit': 'US-made sage, resin incense and smudge sticks from Wolf Spirit Sage, harvested in California and the High Plains.',
 'suns-eye': "Incense, oils and sprays from Sun's Eye in Central Florida.",
 'little-smudgies': 'Twelve mini soy smudge candles to a pack from Soul Sticks, each with herbs and a crystal and about four hours of burn time: one pack, a dozen little gifts.',
 'soul-sticks': 'Masala and plant-based incense plus smudge and intention kits from Soul Sticks.',
 'archangel-incense': 'Packs of 20 natural hand-dipped sticks from Jabou in Canada, a blend for each archangel. Collect the set.',
 'fred-soll': 'Resin-dipped sticks from Tijeras, New Mexico. Each burns lying flat for one to two and a half hours, so one box lasts a long time.',
 'aloha-bay': 'Chakra candles in RSPO certified palm wax from Aloha Bay of Lower Lake, California, a World Fair Trade Organization member pouring since 1993.',
 'auroshikha': 'Hand-rolled sticks and cones from the Sri Aurobindo Ashram incense unit in Pondicherry, in business since 1973.',
 'kamini': 'Masala sticks and cones from Kamini Aromatics of Bangalore.',
 'swift-lite': 'Fast-lighting charcoal tablets made in Kent, England, by Swift-Lite International since 1957. A roll goes a long way.',
 'song-of-india': "R. Expo's incense line, run from India and Auburn, Washington; India Temple is the scent people ask for by name.",
}
def brand_intro(S, k, st):
    name = S.BRAND_NAME[k]
    t = BRAND_TEXT.get(k) or f'{name} is in stock here with {st["n"]} item{"s" if st["n"] != 1 else ""}; see the prices below.'
    cheapest = min(st['xs'], key=lambda x: x['price'])
    packs = sum(1 for x in st['xs'] if x['multi'])
    return f'<p>{E(t)}</p><p>The lowest-priced {E(name)} item today is {S.money(cheapest["price"])}' + (f', and {packs} of the listings are multi-packs or boxes.' if packs else '.') + '</p>'
def brand_faq(S, k, st):
    name = S.BRAND_NAME[k]; packs = sum(1 for x in st['xs'] if x['multi'])
    q = [(f'What is the cheapest {name} item?', f'{S.money(st["min"])} today. Prices on this page update every day from our store.'),
         (f'Do you sell {name} in bulk or multi-packs?', f'Yes, {packs} {name} listings are boxes or multi-packs.' if packs else f'Not right now; all {st["n"]} {name} listings are single items.'),
         (f'Can I pick up {name} near Union Square?', 'Yes, at 2 West 14th Street. Choose Pickup at checkout.' if st['pickup'] else 'Call 646-876-1401 to check the shelf before you visit 2 West 14th Street.')]
    return q
def BRAND_H1(S, k): return f'{S.BRAND_NAME[k]} deals'
def BRAND_TITLE(S, k, st): return f'{S.BRAND_NAME[k]} Incense Deals & Multi-Packs | Namaste Incense Store'
def BRAND_DESC(S, k, st): return f'{S.BRAND_NAME[k]} from {S.money(st["min"])}: {st["n"]} value item{"s" if st["n"] != 1 else ""} near Union Square, NYC. Pick up at 2 West 14th Street or ship.'
def BRANDS_TITLE(S): return 'Incense Brands A to Z, Value Picks | Namaste Incense Store'
def BRANDS_DESC(S): return 'All brands in the Namaste Incense Store value aisles, A to Z, with live item counts and lowest prices.'
BRANDS_H1 = 'Brands A to Z'
def BRANDS_LEAD(S, n): return f'{n} brands have value picks in stock today. Each page lists the cheapest item first, plus any boxes and multi-packs.'

PAIR = {'packs': ['holders'], 'gifts': ['holders'], 'under5': ['holders'], 'u10': ['holders'], 'u20': ['holders'], 'holders': ['packs', 'under5']}
REL_BRAND = 'More {brand} for less'
REL_SCENT = 'Other {scent} deals'
REL_PAIR = 'Add a holder or a refill'
REL_MORE = 'More in {aisle}'
def describe(S, x):
    t = E(x['title']); by = f' from {S.BRAND_NAME[x["brand"]]}' if x['brand'] else ''; a = x['aisle']
    if a == 'packs': s = [f'{t}{by} is a multi-pack or bulk buy, one of the most economical ways to keep incense on hand.', 'Check the photos for the number of tubes, sticks or pieces included.']
    elif a == 'gifts': s = [f'{t}{by} is a ready-to-give set.', 'It is a simple present for birthdays, housewarmings or a thank-you.']
    elif a == 'holders': s = [f'{t}{by} keeps ash and embers off your furniture for under $20.', 'Place it on a level, heat-safe surface.']
    else: s = [f'{t}{by} is in our {AISLES[a][0]} aisle.', f'It is a low-cost way to try {S.FAM_NAME[x["family"]].lower() + " scents" if x["family"] else "something new"}.']
    if x['base'] in ('sticks', 'cones', 'resins', 'smudge', 'candles', 'burners'): s.append('Burn it on a heat-proof surface, away from anything flammable, and stay nearby while it is lit.')
    s.append('Reserve it for pickup at 2 West 14th Street near Union Square or have it shipped from New York City. Checkout runs on Shopify through namastebookshop.com.')
    return s
def PRODUCT_DESC(S, x, v0): return f"{x['title']}: {S.money(v0['price'])} at Namaste Incense Store near Union Square. " + ('Reserve for pickup or ship from NYC.' if x['pickup'] else 'Ships from NYC.')

def ABOUT_DESC(S): return 'About Namaste Incense Store, the value incense counter at 2 West 14th Street near Union Square. A brand of Wealth Edge Ventures Inc.'
ABOUT_H1 = 'About Namaste Incense Store'
def ABOUT(S):
    return f'''<p class="lead">Namaste Incense Store is where we put the best value in the building: boxes and multi-packs, gift sets, and everything under twenty dollars.</p>
<p>Prices are pulled from our store every day, so what you see is what you pay at checkout. Want the deep catalog? Try <a href="https://namasteincense.com/">Namaste Incense</a>. Looking for sage, resin and ritual tools? See <a href="https://namasteincenseshop.com/">Namaste Incense Shop</a>.</p>
<h2>Find us</h2><p>{S.STORE_ADDR}. Call <a href="tel:{S.TEL}">{S.PHONE}</a>.</p>{S.hours_html()}{S.visit_buttons()}
<h2>The fine print</h2><p>{S.LEGAL} Checkout, payment, shipping and pickup are run by our Shopify store at <a href="{S.SHOP}" rel="noopener">namastebookshop.com</a>.</p>
<h2>Our aisles</h2><ul>{''.join(f'<li><a href="/shop/{AISLES[k][2]}/">{E(AISLES[k][0])}</a>: {E(AISLES[k][3])}</li>' for k in S.AISLE_KEYS)}</ul>
<h2>Burn responsibly</h2><p>Use a holder on a heat-safe surface, ventilate, and do not leave anything burning unattended.</p>'''
VISIT_TITLE = 'Visit the Value Incense Store near Union Square'
def VISIT_DESC(S): return f'Hours, directions and pickup for Namaste Incense Store at {S.STORE_ADDR}, a few minutes from Union Square.'
def VISIT_LEAD(S): return 'Pop in to stock up, or collect a pickup order on your way through Union Square.'
def FAQ_DESC(S): return 'Questions about multi-packs, bulk incense, gift sets, prices, pickup and shipping at Namaste Incense Store near Union Square.'
FAQ_H1 = 'Store FAQ'
def FAQ(S):
    return [('What is the cheapest incense you sell?', f'Sticks start at {S.money(S.MIN_STICK)}, and {S.UNDER10:,} items are under $10. See <a href="/best-sellers-under-5/">best sellers under $5</a>.'),
            ('Do you sell incense in bulk?', f'Yes, {S.MULTI_N:,} listings are multi-packs, boxes of tubes or bulk bags. Start with <a href="/bulk-incense-sticks/">bulk incense sticks</a>.'),
            ('Can you help me pick a gift?', 'Try the <a href="/gift-finder/">gift finder</a>, or browse <a href="/shop/gift-sets/">gift sets</a> and <a href="/stocking-stuffers/">stocking stuffers</a>.'),
            ('Where are you?', f'{S.STORE_ADDR}, on 14th Street just west of Fifth Avenue, a few minutes from the Union Square subway station.'),
            ('What are your hours?', 'Mon to Thu 11 AM to 8 PM, Fri and Sat 11 AM to 9 PM, Sun 11 AM to 7 PM. Holidays may differ.'),
            ('Can I reserve online and pick up?', 'Yes. Choose Pickup at checkout.' + (f' Orders are {S.READY.lower()}.' if S.READY else '')),
            ('Are the prices the same in store?', 'This site shows the online price from our store, refreshed daily. If anything differs at the counter, call us before you come.'),
            ('Do you ship?', 'Yes, from New York City. Shipping options and costs are shown at checkout.')]

def GUIDES(S):
    return [
     {'path': '/guide/how-to-stock-up-on-incense/', 'title': 'How to Stock Up on Incense Without Overspending', 'desc': 'Simple ways to get more incense for your money: multi-packs, boxes of tubes, cones vs sticks and storing incense so it lasts.', 'h1': 'How to stock up on incense',
      'html': '''<p class="lead">If you burn incense every day, how you buy it matters more than which brand you pick. A few habits keep the cost per stick low.</p>
<h2>Buy the box, not the tube</h2><p>Many brands sell a box of several tubes for less than the same tubes bought one at a time. Our <a href="/shop/multi-packs-bulk/">multi-packs and bulk boxes</a> aisle collects them.</p>
<h2>Compare by count</h2><p>Look at how many sticks or cones each listing holds, then divide the price. The photos usually show the count on the pack.</p>
<h2>Mix sticks and cones</h2><p>Cones burn faster and stronger, so a few go a long way for a quick scent; sticks last longer for a slow evening.</p>
<h2>Store it well</h2><p>Keep incense in a closed box or drawer, away from sunlight and heat, so the scent does not fade.</p>
<h2>Do not forget a holder</h2><p>A holder under $20 saves your tabletop. See <a href="/shop/holders-burners/">holders and burners</a>.</p>'''},
     {'path': '/guide/incense-gift-guide/', 'title': 'Incense Gift Guide: Ideas Under $5, $10 and $20', 'desc': 'Easy incense gift ideas by budget, from stocking stuffers under $5 to boxed sets under $20, all in stock near Union Square.', 'h1': 'Incense gift guide',
      'html': '''<p class="lead">Incense makes an easy gift because it is personal without being risky. Here is how to choose by budget.</p>
<h2>Under $5</h2><p>A single pack of sticks or cones in a crowd-pleasing scent like Nag Champa or sandalwood. <a href="/best-sellers-under-5/">See the best sellers</a>.</p>
<h2>Under $10</h2><p>Pair a pack with a simple holder, or choose a small sage bundle. <a href="/stocking-stuffers/">Stocking stuffers</a>.</p>
<h2>Under $20</h2><p>A boxed set, a sampler or a candle in a tin. <a href="/shop/gift-sets/">Gift sets</a> and <a href="/incense-sampler-gifts/">samplers</a>.</p>
<p>Still stuck? The <a href="/gift-finder/">gift finder</a> asks three questions and shows what is in stock.</p>'''},
     {'path': '/affordable-incense-near-union-square/', 'title': 'Affordable Incense near Union Square, East Village & Chelsea', 'store_ld': True,
      'desc': f'Cheap incense in Manhattan: {S.UNDER10:,} items under $10 and {S.MULTI_N:,} multi-packs at 2 West 14th Street, near Union Square, the East Village and Chelsea.',
      'h1': 'Affordable incense near Union Square', 'html': f'''<p class="lead">Looking for inexpensive incense in lower Manhattan? Our value counter is on 14th Street at Fifth Avenue, a short ride or walk from most of downtown.</p>
<h2>What your money gets</h2><ul><li>Sticks from {S.money(S.MIN_STICK)} and {S.UNDER10:,} items under $10.</li><li>{S.MULTI_N:,} multi-packs, boxes and bulk bags.</li><li>Gift sets, samplers and holders under $20.</li></ul>
<h2>Getting here</h2><ul><li><b>East Village:</b> the L west to Union Square or the M14A/M14D along 14th Street.</li><li><b>Union Square:</b> walk west along 14th Street to Fifth Avenue.</li><li><b>Chelsea:</b> the 1, 2, 3, F, M or L to 14th Street, then walk east.</li><li><b>Midtown:</b> the N, Q, R or W down to Union Square.</li></ul>{S.visit_block()}'''},
    ]
NOT_FOUND = 'This deal has sold out'
