#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genere la page HTML "Plan du site" (/plan-du-site/) : toutes les pages indexables
groupees par section, avec liens. Labels tires des <title> reels (articles via le registre).
Ajoute aussi l'URL au sitemap.xml. Nav + footer repris du gabarit article.

Usage: python3 gen_sitemap_page.py
"""
import os, re, json, html

ROOT = os.path.dirname(os.path.abspath(__file__))
GAB = os.path.join(ROOT, "ressources", "traduction-juridique-ia-guide", "index.html")
BASE = "https://lexamt.com"
TODAY = "2026-06-25"


def slice_between(s, a, b):
    i = s.index(a); j = s.index(b, i); return s[i:j + len(b)]


def shared():
    g = open(GAB, encoding="utf-8").read()
    return slice_between(g, '<header class="nav">', '</header>'), slice_between(g, '<footer class="footer">', '</footer>')


def page_path(url):
    p = url.replace(BASE, "").strip("/")
    return os.path.join(ROOT, p, "index.html") if p else os.path.join(ROOT, "index.html")


def title_of(url, registry):
    if url.rstrip("/") + "/" in registry:
        return registry[url.rstrip("/") + "/"]
    f = page_path(url)
    try:
        s = open(f, encoding="utf-8").read()
        t = re.search(r"<title>(.*?)</title>", s, re.S).group(1).strip()
    except Exception:
        return url
    t = re.sub(r"\s*\|\s*Lexa\s*$", "", t)
    t = re.sub(r"\s*:\s*aide Lexa\s*$", "", t)
    t = re.sub(r"\s*:\s*le guide complet\s*$", "", t)
    return html.unescape(t).strip()


# Registre d'articles (ordre = recence)
reg_raw = open(os.path.join(ROOT, "assets", "lexa-articles.js"), encoding="utf-8").read()
reg = json.loads(re.search(r"window\.LEXA_ARTICLES\s*=\s*(\[.*\]);", reg_raw, re.S).group(1))
registry = {a["url"]: a["title"] for a in reg}
article_urls = [BASE + a["url"] for a in reg]

# Sitemap URLs
sm = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
locs = re.findall(r"<loc>(.*?)</loc>", sm)

P = lambda s: BASE + s  # noqa

# Groupes ordonnes (titre, liste d'URL ou predicat)
discover = [P("/"), P("/lexa-traduction-juridique-solution-pro-droit/"), P("/expertise-lexa/"), P("/fonctionnalites/")]
products = [P("/lexa-texte-traduction-juridique-ia/"), P("/lexa-document-traduction-juridique/"),
            P("/lexa-word-add-on-microsoft-word/"), P("/lexa-api-connecteur-juridiques/"), P("/lexa-writing-redaction-juridique/")]
pricing = [P("/lexa-tarifs-traduction-juridique/"), P("/lexa-vs-deepl-traduction-juridique/"), P("/securite-confidentialite-traduction-juridique/")]
personas = [P("/traduction-juridique-avocats/"), P("/traduction-juridique-directions-juridiques/"), P("/traduction-juridique-legal-ops/")]
domains = sorted([u for u in locs if "/expertise-" in u and u != P("/expertise-lexa/")])
resources = [P("/ressources/"), P("/ressources/traduction-juridique-ia-guide/"), P("/ressources/ebook-traduction-juridique/"),
             P("/glossaire-traduction-juridique/"), P("/temoignages-clients/")]
aide = [P("/aide/")] + sorted([u for u in locs if u.startswith(P("/aide/")) and u != P("/aide/")])
legal = [P("/contact/"), P("/mentions-legales/"), P("/conditions-general/")]
articles = article_urls

GROUPS = [
    ("Découvrir Lexa", discover, False),
    ("Produits", products, False),
    ("Tarifs, comparatif et sécurité", pricing, False),
    ("Solutions par métier", personas, False),
    ("Domaines du droit", domains, False),
    ("Ressources", resources, False),
    ("Centre d'aide", aide, False),
    ("Informations légales", legal, False),
    ("Articles du blog", articles, True),  # wide (colonnes)
]

# Garde-fou : toutes les URL indexables couvertes ?
covered = set()
for _, urls, _ in GROUPS:
    covered |= set(urls)
indexable = [u for u in locs]
missing = [u for u in indexable if u not in covered]
if missing:
    GROUPS.append(("Autres", sorted(missing), False))


def col_html(title, urls, wide):
    lis = "\n".join('        <li><a href="%s">%s</a></li>' % (u.replace(BASE, "") or "/", html.escape(title_of(u, registry))) for u in urls)
    cls = "plan-col plan-col--wide" if wide else "plan-col"
    return '      <div class="%s">\n        <h2>%s</h2>\n        <ul>\n%s\n        </ul>\n      </div>' % (cls, html.escape(title), lis)


nav, footer = shared()
url = BASE + "/plan-du-site/"
ORG_SITE = [
    {"@type": "Organization", "@id": BASE + "/#organization", "name": "Lexa", "legalName": "Legal 230", "url": BASE,
     "logo": {"@type": "ImageObject", "url": BASE + "/assets/logo-lexa.png", "width": 512, "height": 512},
     "description": "Lexa est la solution de traduction juridique par IA développée par Legal 230, 1ère agence européenne de traduction juridique.",
     "parentOrganization": {"@type": "Organization", "name": "Legal 230"}},
    {"@type": "WebSite", "@id": BASE + "/#website", "url": BASE, "name": "Lexa", "inLanguage": "fr-FR",
     "publisher": {"@id": BASE + "/#organization"}},
]
jsonld = json.dumps({"@context": "https://schema.org", "@graph": ORG_SITE + [
    {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": "Plan du site | Lexa",
     "description": "Plan du site Lexa : toutes les pages (produits, solutions, domaines du droit, ressources, blog, centre d'aide).",
     "inLanguage": "fr-FR", "isPartOf": {"@id": BASE + "/#website"}},
    {"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Accueil", "item": BASE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Plan du site", "item": url}]},
]}, ensure_ascii=False, indent=2)

doc = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Plan du site | Lexa</title>
<meta name="description" content="Plan du site Lexa : toutes les pages du site (produits, solutions, domaines du droit, ressources, blog et centre d'aide) en un coup d'oeil.">
<meta name="author" content="Lexa, propulsé par Legal 230">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<meta name="theme-color" content="#1B3B31">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="fr-FR" href="{url}">
<link rel="alternate" hreflang="x-default" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Lexa">
<meta property="og:locale" content="fr_FR">
<meta property="og:url" content="{url}">
<meta property="og:title" content="Plan du site | Lexa">
<meta property="og:description" content="Toutes les pages du site Lexa en un coup d'oeil.">
<meta property="og:image" content="https://lexamt.com/assets/og-lexa.jpg">
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
<script type="application/ld+json">
{jsonld}
</script>
</head>
<body>

{nav}

<nav class="breadcrumb" aria-label="Fil d'Ariane">
  <div class="container">
    <ol>
      <li><a href="/">Accueil</a></li>
      <li><span class="sep">/</span><span aria-current="page">Plan du site</span></li>
    </ol>
  </div>
</nav>

<header class="legal-head">
  <div class="container">
    <span class="eyebrow">Navigation</span>
    <h1>Plan du site</h1>
    <p class="lead" style="margin-top:12px;max-width:720px">Toutes les pages du site Lexa, regroupées par thème : produits, solutions par métier, domaines du droit, ressources, blog et centre d'aide.</p>
  </div>
</header>

<section class="plan-wrap">
  <div class="container">
    <div class="plan-grid">
{cols}
    </div>
  </div>
</section>

{footer}

</body>
</html>
""".format(url=url, jsonld=jsonld, nav=nav, footer=footer,
           cols="\n".join(col_html(t, u, w) for t, u, w in GROUPS))

os.makedirs(os.path.join(ROOT, "plan-du-site"), exist_ok=True)
open(os.path.join(ROOT, "plan-du-site", "index.html"), "w", encoding="utf-8").write(doc)

# Ajout au sitemap
if url not in sm:
    entry = "  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.3</priority>\n  </url>\n" % (url, TODAY)
    sm = sm.replace("</urlset>", entry + "</urlset>")
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(sm)
    added = 1
else:
    added = 0

n = sum(len(u) for _, u, _ in GROUPS)
print("Plan du site genere : %d liens dans %d groupes" % (n, len(GROUPS)))
print("Sitemap : %d URL ajoutee(s)" % added)
print("Garde-fou pages manquantes :", missing or "aucune")
