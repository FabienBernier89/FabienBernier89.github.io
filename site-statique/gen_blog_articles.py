#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generateur des pages articles du blog Lexa.
- Lit _build/articles.json (sortie du workflow d'extraction, nettoyee).
- Reutilise la nav + le footer du gabarit article (source de verite).
- Produit <slug>/index.html pour chaque article (slug a plat = slug live, ranking preserve).
- Inclut : partage social (FB / X / LinkedIn), maillage "Pour aller plus loin",
  FAQ + JSON-LD (Article + FAQPage + BreadcrumbList), bloc dynamique "Derniers articles".
- Regenere assets/lexa-articles.js (registre alimentant le bloc derniers articles + l'index).
- Met a jour sitemap.xml.

Usage: python3 gen_blog_articles.py
"""
import json, os, re, html, datetime
from urllib.parse import quote

ROOT = os.path.dirname(os.path.abspath(__file__))
GABARIT = os.path.join(ROOT, "ressources", "traduction-juridique-ia-guide", "index.html")
DATA = os.path.join(ROOT, "_build", "articles.json")
SITEMAP = os.path.join(ROOT, "sitemap.xml")
REGISTRY = os.path.join(ROOT, "assets", "lexa-articles.js")

# Ordre du listing live (page 1 -> page 5), index 0 = plus recent.
ORDER = [
    "traduction-automatique-dans-un-contentieux",
    "erreur-de-traduction-juridique-cout",
    "gain-de-temps-en-traduction-juridique",
    "traduction-ia-pour-des-documents-juridiques",
    "alternative-a-chatgpt-traduction-juridique",
    "ia-generaliste-juridique-traduction-juridique",
    "faux-equivalents-traduction-juridique-francais-anglais",
    "alternative-a-gemini-traduction-juridique-ia",
    "deepl-traduction-juridique-fiable",
    "cout-de-traduction-juridique",
    "alternative-deepl-traduction-juridique-avocat",
    "traduction-automatique-par-ia-tendances-2026",
    "ia-traduction-juridique-heures-gagnees",
    "meilleure-alternative-deepl-traduction-juridique-par-ia",
    "traduction-juridique-par-ia",
    "comment-bien-aborder-une-traduction-juridique-avec-ia",
    "traduction-juridique-et-contentieux-international",
    "les-incoherences-juridiques-dans-un-contrat-avec-lia",
    "la-traduction-juridique-rgpd-avec-lexa",
    "lexiques-juridiques-multilingues-dans-votre-quotidien",
    "traduction-medicale-juridique-par-l-ia",
    "traduction-juridique-ia-directions-juridiques-avec-ia",
    "traduction-juridique-dappels-doffres-publics-par-ia",
    "traduction-juridique-par-lia",
    "comment-lia-traduit-les-expressions-juridique",
    "ia-et-raisonnement-juridique-ce-que-lia-peut-comprendre",
    "traduction-juridique-par-ia-pratique-plus-durable",
    "lexique-juridique-pour-traduction-juridique-par-ia",
    "traduction-juridique-de-contrat-par-ia",
    "traduction-juridique-ia-vs-humaine-que-choisir",
]

MOIS = ["", "janvier", "février", "mars", "avril", "mai", "juin", "juillet",
        "août", "septembre", "octobre", "novembre", "décembre"]

BASE = "https://lexamt.com"
AUTHOR = "Équipe Lexa, propulsée par Legal 230"

# Normalisation des libelles de categorie (l'enum du workflow etait sans accent)
CAT_DISPLAY = {"Confidentialite": "Confidentialité"}
CHIP_ORDER = ["Traduction IA", "Confidentialité", "Bonnes pratiques", "Comparatifs", "LegalTech"]


def cat_display(c):
    return CAT_DISPLAY.get(c, c)


def truncate(s, n=155):
    s = (s or "").strip()
    if len(s) <= n:
        return s
    return s[:n].rsplit(" ", 1)[0].rstrip(" ,;:.") + "…"

ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
         'stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 5l7 7-7 7"/></svg>')

ICON_USER = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
             'stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/>'
             '<path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/></svg>')
ICON_CAL = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
            'stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/>'
            '<line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>')
ICON_CLOCK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
              'stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>')
ICON_FB = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M24 12.07C24 5.4 18.63 0 12 0S0 5.4 0 '
           '12.07c0 6.03 4.39 11.03 10.13 11.93v-8.44H7.08v-3.49h3.05V9.41c0-3.02 1.79-4.69 4.53-4.69 1.31 0 2.69.24 '
           '2.69.24v2.97h-1.52c-1.49 0-1.96.93-1.96 1.89v2.25h3.33l-.53 3.49h-2.8v8.44C19.61 23.1 24 18.1 24 12.07z"/></svg>')
ICON_X = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 '
          '11.24h-6.66l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 '
          '4.126H5.117z"/></svg>')
ICON_LI = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-'
           '3.04-1.85 0-2.13 1.45-2.13 2.94v5.67H9.35V9h3.42v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 '
           '5.45v6.29zM5.34 7.43a2.07 2.07 0 1 1 0-4.14 2.07 2.07 0 0 1 0 4.14zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 '
           '0 0 .77 0 1.72v20.56C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.72V1.72C24 .77 23.2 0 22.22 0z"/></svg>')


def slice_between(src, start_marker, end_marker, include_end=True):
    i = src.index(start_marker)
    j = src.index(end_marker, i)
    return src[i:(j + len(end_marker)) if include_end else j]


def load_shared():
    with open(GABARIT, encoding="utf-8") as f:
        g = f.read()
    nav = slice_between(g, '<header class="nav">', '</header>')
    footer = slice_between(g, '<footer class="footer">', '</footer>')
    # JSON-LD Organization + WebSite (les 2 premiers noeuds du @graph du gabarit)
    return nav, footer


def date_for(slug):
    i = ORDER.index(slug) if slug in ORDER else 0
    d = datetime.date(2026, 6, 20) - datetime.timedelta(days=i * 6)
    return d


def fr_date(d):
    return "%d %s %d" % (d.day, MOIS[d.month], d.year)


def share_block(url, title):
    enc_u = quote(url, safe="")
    enc_t = quote(title, safe="")
    return (
        '<div class="article-share" aria-label="Partager cet article">\n'
        '      <span class="as-label">Partager</span>\n'
        '      <a class="sh-fb" href="https://www.facebook.com/sharer/sharer.php?u=%s" target="_blank" rel="noopener" aria-label="Partager sur Facebook">%s</a>\n'
        '      <a class="sh-tw" href="https://twitter.com/intent/tweet?url=%s&amp;text=%s" target="_blank" rel="noopener" aria-label="Partager sur X (Twitter)">%s</a>\n'
        '      <a class="sh-li" href="https://www.linkedin.com/sharing/share-offsite/?url=%s" target="_blank" rel="noopener" aria-label="Partager sur LinkedIn">%s</a>\n'
        '    </div>' % (enc_u, ICON_FB, enc_u, enc_t, ICON_X, enc_u, ICON_LI)
    )


def jsonld(a, url, d):
    org = {
        "@type": "Organization", "@id": BASE + "/#organization", "name": "Lexa",
        "legalName": "Legal 230", "url": BASE,
        "logo": {"@type": "ImageObject", "url": BASE + "/assets/logo-lexa.png", "width": 512, "height": 512},
        "description": "Lexa est la solution de traduction juridique par IA développée par Legal 230, 1ère agence européenne de traduction juridique.",
        "parentOrganization": {"@type": "Organization", "name": "Legal 230"},
    }
    website = {
        "@type": "WebSite", "@id": BASE + "/#website", "url": BASE, "name": "Lexa",
        "inLanguage": "fr-FR", "publisher": {"@id": BASE + "/#organization"},
    }
    article = {
        "@type": "Article", "@id": url + "#article",
        "headline": a["h1"], "description": a["metaDescription"],
        "inLanguage": "fr-FR",
        "datePublished": d.isoformat(), "dateModified": d.isoformat(),
        "author": {"@type": "Organization", "name": "Lexa", "url": BASE},
        "publisher": {"@id": BASE + "/#organization"},
        "image": BASE + "/assets/og-lexa.jpg",
        "mainEntityOfPage": {"@id": url + "#webpage"},
        "isPartOf": {"@id": BASE + "/#website"},
    }
    faq = {
        "@type": "FAQPage", "@id": url + "#faq",
        "mainEntity": [
            {"@type": "Question", "name": q["q"],
             "acceptedAnswer": {"@type": "Answer", "text": q["a"]}}
            for q in a.get("faq", [])
        ],
    }
    crumbs = {
        "@type": "BreadcrumbList", "@id": url + "#breadcrumb",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Accueil", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Ressources", "item": BASE + "/ressources/"},
            {"@type": "ListItem", "position": 3, "name": a["h1"], "item": url},
        ],
    }
    webpage = {
        "@type": "WebPage", "@id": url + "#webpage", "url": url,
        "name": a["titleTag"] + " | Lexa", "description": a["metaDescription"],
        "inLanguage": "fr-FR", "isPartOf": {"@id": BASE + "/#website"},
        "primaryImageOfPage": {"@type": "ImageObject", "url": BASE + "/assets/og-lexa.jpg"},
        "datePublished": d.isoformat(), "dateModified": d.isoformat(),
    }
    graph = {"@context": "https://schema.org", "@graph": [org, website, webpage, article, faq, crumbs]}
    return json.dumps(graph, ensure_ascii=False, indent=2)


def build_page(a, nav, footer):
    slug = a["slug"]
    url = "%s/%s/" % (BASE, slug)
    d = date_for(slug)
    title = a["titleTag"] + " | Lexa"
    desc = a["metaDescription"]
    h1 = a["h1"]
    eyebrow = a.get("eyebrow", a.get("category", "Article"))

    # FAQ HTML
    faq_items = "\n".join(
        '      <details class="faq-item">\n'
        '        <summary>%s</summary>\n'
        '        <p>%s</p>\n'
        '      </details>' % (html.escape(q["q"]), q["a"]) for q in a.get("faq", [])
    )

    # Maillage interne
    il = "\n".join(
        '        <li><a href="%s">%s %s</a></li>' % (html.escape(l["href"]), ARROW, html.escape(l["label"]))
        for l in a.get("internalLinks", [])
    )

    share = share_block(url, h1)

    head = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="author" content="Lexa, propulsé par Legal 230">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<meta name="theme-color" content="#1B3B31">
<meta name="format-detection" content="telephone=no">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="fr-FR" href="{url}">
<link rel="alternate" hreflang="x-default" href="{url}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Lexa">
<meta property="og:locale" content="fr_FR">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{ogtitle}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://lexamt.com/assets/og-lexa.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Lexa, la traduction juridique par IA développée par Legal 230">
<meta property="article:published_time" content="{iso}">
<meta property="article:modified_time" content="{iso}">
<meta property="article:author" content="Équipe Lexa, propulsée par Legal 230">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{ogtitle}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="https://lexamt.com/assets/og-lexa.jpg">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap" media="print" onload="this.media='all'"><noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap"></noscript>
<link rel="stylesheet" href="/assets/lexa.css">

<!-- ============ DONNÉES STRUCTURÉES (JSON-LD) ============ -->
<script type="application/ld+json">
{jsonld}
</script>
</head>
<body>

<!-- NAV -->
{nav}

<!-- FIL D'ARIANE -->
<nav class="breadcrumb" aria-label="Fil d'Ariane">
  <div class="container">
    <ol>
      <li><a href="/">Accueil</a></li>
      <li><span class="sep">/</span><a href="/ressources/#articles">Ressources</a></li>
      <li><span class="sep">/</span><span aria-current="page">{h1}</span></li>
    </ol>
  </div>
</nav>

<!-- EN-TÊTE D'ARTICLE -->
<header class="article-head">
  <div class="container">
    <span class="eyebrow">{eyebrow}</span>
    <h1>{h1}</h1>
    <div class="article-meta">
      <span class="am">{ic_user} <b>{author}</b></span>
      <span class="am">{ic_cal} {date_fr}</span>
      <span class="am">{ic_clock} {mins} min de lecture</span>
    </div>
    {share}
  </div>
</header>

<!-- CORPS D'ARTICLE -->
<article class="article-body">
  <div class="container prose">

    <div class="brief-card">
      <span class="brief-label">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
        En bref
      </span>
      <p>{brief}</p>
    </div>

{body}

  </div>
</article>

<!-- MAILLAGE INTERNE -->
<section class="internal-links">
  <div class="container">
    <div class="il-card">
      <h2>Pour aller plus loin</h2>
      <ul>
{il}
      </ul>
    </div>
  </div>
</section>

<!-- FAQ -->
<section class="faq">
  <div class="container">
    <div class="faq-head">
      <span class="eyebrow">Questions fréquentes</span>
      <h2>Vos questions, en clair</h2>
    </div>
    <div class="faq-list">
{faq}
    </div>
  </div>
</section>

<!-- DERNIERS ARTICLES (dynamique) -->
<section class="latest-articles" id="latest-articles">
  <div class="container">
    <div class="la-head">
      <span class="eyebrow">À lire aussi</span>
      <h2>Les derniers articles</h2>
    </div>
    <div class="la-grid" id="latest-articles-grid" data-count="3"></div>
  </div>
</section>

<!-- FINAL CTA -->
<section class="final-cta">
  <div class="container">
    <div class="final-cta-inner">
      <h2>Traduisez le droit, sans rien laisser au hasard</h2>
      <p>Mettez la précision juridique de Lexa à l'épreuve de vos propres documents. Ou réservez une démo avec un expert qui connaît votre métier.</p>
      <div class="final-cta-btns">
        <a href="/lexa-tarifs-traduction-juridique/" class="btn btn-emerald">
          Essayer gratuitement
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 5l7 7-7 7"/></svg>
        </a>
        <a href="/contact/" class="btn-outline">Demander une démo</a>
      </div>
      <p class="micro">Essai gratuit 15 jours · Sans carte bancaire · Sans engagement</p>
    </div>
  </div>
</section>

<!-- FOOTER -->
{footer}

<script src="/assets/lexa-articles.js"></script>
<script src="/assets/lexa-article.js" defer></script>
</body>
</html>
""".format(
        title=html.escape(title), desc=html.escape(desc), url=url,
        ogtitle=html.escape(a["titleTag"]), iso=d.isoformat(), jsonld=jsonld(a, url, d),
        nav=nav, h1=html.escape(h1), eyebrow=html.escape(eyebrow),
        ic_user=ICON_USER, ic_cal=ICON_CAL, ic_clock=ICON_CLOCK,
        author=AUTHOR, date_fr=fr_date(d), mins=a.get("readingMinutes", 7),
        share=share, brief=a["brief"], body=a["bodyHTML"], il=il, faq=faq_items, footer=footer,
    )
    return head, url, d


def build_registry(arts_by_slug):
    """Registre ordonne (plus recent -> plus ancien) pour le bloc derniers articles + l'index."""
    items = []
    for slug in ORDER:
        a = arts_by_slug.get(slug)
        if not a:
            continue
        items.append({
            "url": "/%s/" % slug,
            "title": a["h1"],
            "cat": cat_display(a.get("category", "Article")),
            "excerpt": a.get("excerpt", a.get("metaDescription", "")),
            "date": date_for(slug).isoformat(),
        })
    body = json.dumps(items, ensure_ascii=False, indent=1)
    return ("/* lexa-articles.js : registre des articles du blog (genere par gen_blog_articles.py).\n"
            "   Ordonne du plus recent au plus ancien. Alimente le bloc \"Derniers articles\"\n"
            "   (lexa-article.js) et peut alimenter la grille de l'index ressources. */\n"
            "window.LEXA_ARTICLES = %s;\n" % body)


def update_sitemap(urls_dates):
    with open(SITEMAP, encoding="utf-8") as f:
        sm = f.read()
    add = []
    for url, d in urls_dates:
        if url in sm:
            continue
        add.append(
            "  <url>\n"
            "    <loc>%s</loc>\n"
            "    <lastmod>%s</lastmod>\n"
            "    <changefreq>monthly</changefreq>\n"
            "    <priority>0.6</priority>\n"
            "  </url>" % (url, d.isoformat())
        )
    if add:
        sm = sm.replace("</urlset>", "\n".join(add) + "\n</urlset>")
        with open(SITEMAP, "w", encoding="utf-8") as f:
            f.write(sm)
    return len(add)


def build_index_blocks(arts_by_slug):
    """Genere (1) la section blog complete avec 30 cartes statiques, (2) les chips de filtre utiles."""
    cards = []
    cats_present = []
    for slug in ORDER:
        a = arts_by_slug.get(slug)
        if not a:
            continue
        cat = cat_display(a.get("category", "Article"))
        if cat not in cats_present:
            cats_present.append(cat)
        cards.append(
            '      <a class="blog-card" href="/%s/">\n'
            '        <div class="blog-thumb">\n'
            '          <span class="bt-cat">%s</span>\n'
            '          <span class="bt-mark">Lexa</span>\n'
            '        </div>\n'
            '        <div class="blog-body">\n'
            '          <h3>%s</h3>\n'
            '          <p>%s</p>\n'
            '          <span class="more">Lire l\'article %s</span>\n'
            '        </div>\n'
            '      </a>' % (slug, html.escape(cat), html.escape(a["h1"]),
                           html.escape(truncate(a.get("excerpt", ""))), ARROW)
        )
    blog = ('<section class="blog">\n  <div class="container">\n    <div class="blog-grid">\n\n'
            + "\n\n".join(cards) + "\n\n    </div>\n  </div>\n</section>")
    chips = ['      <span class="cat-chip active">Tous les articles</span>']
    for c in CHIP_ORDER:
        if c in cats_present:
            chips.append('      <span class="cat-chip">%s</span>' % html.escape(c))
    return blog, "\n".join(chips)


def update_index(arts_by_slug):
    p = os.path.join(ROOT, "ressources", "index.html")
    h = open(p, encoding="utf-8").read()
    blog, chips = build_index_blocks(arts_by_slug)
    # 1) remplace toute la section blog (cartes placeholder -> 30 cartes reelles)
    s = h.index('<section class="blog">')
    e = h.index('<section class="newsletter">')
    h = h[:s] + blog + "\n\n" + h[e:]
    # 2) remplace les chips dans la barre de filtres
    a = h.index('<section class="cat-filters"')
    cs = h.index('<div class="container">', a) + len('<div class="container">')
    ce = h.index('</div>', cs)
    h = h[:cs] + "\n" + chips + "\n    " + h[ce:]
    open(p, "w", encoding="utf-8").write(h)
    return sum(1 for s in ORDER if s in arts_by_slug)


def main():
    nav, footer = load_shared()
    arts = json.load(open(DATA, encoding="utf-8"))
    by_slug = {a["slug"]: a for a in arts}
    urls_dates = []
    n = 0
    for a in arts:
        page, url, d = build_page(a, nav, footer)
        outdir = os.path.join(ROOT, a["slug"])
        os.makedirs(outdir, exist_ok=True)
        with open(os.path.join(outdir, "index.html"), "w", encoding="utf-8") as f:
            f.write(page)
        urls_dates.append((url, d))
        n += 1
    with open(REGISTRY, "w", encoding="utf-8") as f:
        f.write(build_registry(by_slug))
    added = update_sitemap(urls_dates)
    nb_idx = update_index(by_slug)
    print("Pages generees : %d" % n)
    print("Registre : %s (%d entrees)" % (REGISTRY, len([s for s in ORDER if s in by_slug])))
    print("Sitemap : %d URL ajoutees" % added)
    print("Index ressources : grille regeneree (%d cartes)" % nb_idx)
    # garde-fou em-dash
    bad = 0
    for a in arts:
        blob = json.dumps(a, ensure_ascii=False)
        bad += blob.count("—")
    print("Em-dash dans les donnees : %d" % bad)


if __name__ == "__main__":
    main()
