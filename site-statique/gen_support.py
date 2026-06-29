#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generateur du centre de support Lexa (/aide/).
- Lit _build/support.json (sortie du workflow : [{key,title,intro,items:[{q,a}]}]).
- Reutilise la nav + le footer du gabarit article.
- Produit /aide/index.html (hub : hero + recherche + 14 cartes) et /aide/<key>/index.html
  (accordeons FAQ + JSON-LD FAQPage + lien retour + CTA contact).
- Met a jour sitemap.xml.

Usage: python3 gen_support.py
"""
import json, os, html, datetime, re
from urllib.parse import quote  # noqa

ROOT = os.path.dirname(os.path.abspath(__file__))
GABARIT = os.path.join(ROOT, "ressources", "traduction-juridique-ia-guide", "index.html")
DATA = os.path.join(ROOT, "_build", "support.json")
SITEMAP = os.path.join(ROOT, "sitemap.xml")
BASE = "https://lexamt.com"
TODAY = "2026-06-24"

# Ordre + libelle court (carte du hub) + icone (inner SVG)
SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">%s</svg>')
CATS = [
    ("decouvrir-lexa", "Ce qu'est Lexa, pour qui, langues et domaines couverts.",
     '<circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/>'),
    ("demarrer", "Créer un compte, lancer l'essai gratuit et faire ses premiers pas.",
     '<polygon points="5 3 19 12 5 21 5 3"/>'),
    ("traduire-un-texte", "Traduire un texte, choisir le domaine, lire le score qualité.",
     '<polyline points="4 7 4 4 20 4 20 7"/><line x1="9" y1="20" x2="15" y2="20"/><line x1="12" y1="4" x2="12" y2="20"/>'),
    ("traduire-un-document", "Importer un fichier, préserver la mise en page, traiter par lots.",
     '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/>'),
    ("lexa-writing", "Reformuler, anonymiser, résumer et adapter le style.",
     '<path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/>'),
    ("lexa-word", "Installer et utiliser Lexa directement dans Microsoft Word.",
     '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>'),
    ("lexa-api", "Intégrer Lexa à vos outils via l'API et les webhooks.",
     '<polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/>'),
    ("lexiques-glossaires", "Créer, importer et appliquer vos lexiques pour une terminologie cohérente.",
     '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>'),
    ("historique", "Retrouver, réutiliser, exporter et supprimer vos traductions.",
     '<path d="M3 3v5h5"/><path d="M3.05 13A9 9 0 1 0 6 5.3L3 8"/><polyline points="12 7 12 12 15 15"/>'),
    ("qualite-relecture", "Comprendre le score qualité et demander une relecture experte.",
     '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>'),
    ("securite-confidentialite", "Chiffrement, RGPD, hébergement, rétention et certifications.",
     '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/>'),
    ("gestion-equipe-licences", "Inviter des utilisateurs, gérer les rôles, les sièges et le SSO.",
     '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>'),
    ("abonnements-facturation", "Plans, paiement, factures et changement d'abonnement.",
     '<rect x="1" y="4" width="22" height="16" rx="2" ry="2"/><line x1="1" y1="10" x2="23" y2="10"/>'),
    ("compte-parametres", "Profil, mot de passe, préférences et dépannage.",
     '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>'),
]
DESC = {k: d for (k, d, _) in CATS}
ICON = {k: SVG % s for (k, _, s) in CATS}
ORDER = [k for (k, _, _) in CATS]

# Titres accentues (les titres venant du workflow etaient en ASCII)
TITLES = {
    "decouvrir-lexa": "Découvrir Lexa",
    "demarrer": "Démarrer avec Lexa",
    "traduire-un-texte": "Traduire un texte (Lexa Texte)",
    "traduire-un-document": "Traduire un document (Lexa Documents)",
    "lexa-writing": "Personnaliser (réécriture)",
    "lexa-word": "Lexa Word (module Microsoft Word)",
    "lexa-api": "Lexa API (intégration)",
    "lexiques-glossaires": "Lexiques et glossaires",
    "historique": "Historique et gestion des traductions",
    "qualite-relecture": "Qualité et relecture",
    "securite-confidentialite": "Sécurité et confidentialité",
    "gestion-equipe-licences": "Gestion d'équipe, licences et utilisateurs",
    "abonnements-facturation": "Abonnements et facturation",
    "compte-parametres": "Compte, paramètres et dépannage",
}


def ctitle(k, fallback=""):
    return TITLES.get(k, fallback)

ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" '
         'stroke-linejoin="round"><path d="M5 12h14M13 5l7 7-7 7"/></svg>')
CHEVRON = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" '
           'stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>')
ARROW_L = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" '
           'stroke-linejoin="round"><path d="M19 12H5M11 19l-7-7 7-7"/></svg>')


def slice_between(src, a, b):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + len(b)]


def load_shared():
    g = open(GABARIT, encoding="utf-8").read()
    return slice_between(g, '<header class="nav">', '</header>'), slice_between(g, '<footer class="footer">', '</footer>')


HEAD = """<!DOCTYPE html>
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
<meta property="og:type" content="website">
<meta property="og:site_name" content="Lexa">
<meta property="og:locale" content="fr_FR">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://lexamt.com/assets/og-lexa.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
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
<script type="application/ld+json">
{jsonld}
</script>
</head>
<body>

{nav}
"""

CONTACT = """
<!-- CONTACT / AIDE SUPPLEMENTAIRE -->
<section class="final-cta">
  <div class="container">
    <div class="final-cta-inner">
      <h2>Vous ne trouvez pas votre réponse ?</h2>
      <p>Notre équipe vous répond et vous accompagne dans la prise en main de Lexa.</p>
      <div class="final-cta-btns">
        <a href="mailto:support@lexamt.com" class="btn btn-emerald">Contacter le support</a>
        <a href="/contact/" class="btn-outline">Demander une démo</a>
      </div>
      <p class="micro">support@lexamt.com · +33 1 84 80 21 20</p>
    </div>
  </div>
</section>
"""


def org_site():
    return [
        {"@type": "Organization", "@id": BASE + "/#organization", "name": "Lexa", "legalName": "Legal 230", "url": BASE,
         "logo": {"@type": "ImageObject", "url": BASE + "/assets/logo-lexa.png", "width": 512, "height": 512},
         "description": "Lexa est la solution de traduction juridique par IA développée par Legal 230, 1ère agence européenne de traduction juridique.",
         "parentOrganization": {"@type": "Organization", "name": "Legal 230"}},
        {"@type": "WebSite", "@id": BASE + "/#website", "url": BASE, "name": "Lexa", "inLanguage": "fr-FR",
         "publisher": {"@id": BASE + "/#organization"}},
    ]


def jsonld_hub(url):
    g = {"@context": "https://schema.org", "@graph": org_site() + [
        {"@type": "CollectionPage", "@id": url + "#webpage", "url": url, "name": "Centre d'aide Lexa",
         "description": "Le centre d'aide de Lexa : guides pas a pas et reponses sur la traduction de texte et de documents, Lexa Writing, Word, API, les lexiques, l'historique, la gestion d'equipe, la securite et la facturation.",
         "inLanguage": "fr-FR", "isPartOf": {"@id": BASE + "/#website"}},
        {"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Accueil", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Centre d'aide", "item": url}]},
    ]}
    return json.dumps(g, ensure_ascii=False, indent=2)


def jsonld_cat(url, title, items):
    g = {"@context": "https://schema.org", "@graph": org_site() + [
        {"@type": "FAQPage", "@id": url + "#faq", "name": title + " - Aide Lexa",
         "inLanguage": "fr-FR", "isPartOf": {"@id": BASE + "/#website"},
         "mainEntity": [{"@type": "Question", "name": it["q"],
                         "acceptedAnswer": {"@type": "Answer", "text": it["a"]}} for it in items]},
        {"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Accueil", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Centre d'aide", "item": BASE + "/aide/"},
            {"@type": "ListItem", "position": 3, "name": title, "item": url}]},
    ]}
    return json.dumps(g, ensure_ascii=False, indent=2)


def build_hub(by_key, nav, footer):
    url = BASE + "/aide/"
    cards = []
    index = []
    for k in ORDER:
        c = by_key.get(k)
        if not c:
            continue
        n = len(c.get("items", []))
        t = ctitle(k, c["title"])
        cards.append(
            '      <a class="help-cat" href="/aide/%s/">\n'
            '        <div class="hic">%s</div>\n'
            '        <h3>%s</h3>\n'
            '        <p>%s</p>\n'
            '        <div class="hc-foot"><span class="hc-count">%d question%s</span><span class="hc-go">%s</span></div>\n'
            '      </a>' % (k, ICON[k], html.escape(t), html.escape(DESC[k]), n, "s" if n > 1 else "", CHEVRON))
        for i, it in enumerate(c.get("items", [])):
            index.append({"q": it["q"], "c": t, "u": "/aide/%s/#q-%s-%d" % (k, k, i)})
    title = "Centre d'aide Lexa : guides et réponses | Lexa"
    desc = "Le centre d'aide de Lexa : guides pas à pas pour traduire vos textes et documents, utiliser Lexa Writing, Word et l'API, gérer vos lexiques, votre historique, votre équipe, la sécurité et la facturation."
    body = HEAD.format(title=html.escape(title), desc=html.escape(desc), url=url, jsonld=jsonld_hub(url), nav=nav)
    body += """
<!-- HERO CENTRE D'AIDE -->
<section class="pillar-hero">
  <div class="container">
    <span class="eyebrow">Centre d'aide</span>
    <h1>Comment pouvons-nous vous aider ?</h1>
    <p class="lead">Guides pas à pas et réponses pour tirer le meilleur de Lexa, de votre première traduction à la gestion de votre équipe.</p>
    <div class="help-search">
      <input type="search" id="helpSearch" placeholder="Rechercher une question (ex : traduire un document, facturation, équipe...)" aria-label="Rechercher dans le centre d'aide" autocomplete="off">
      <div class="help-results" id="helpResults" role="listbox"></div>
    </div>
  </div>
</section>

<!-- CATEGORIES -->
<section class="segments">
  <div class="container">
    <div class="help-cats">
"""
    body += "\n".join(cards)
    body += """
    </div>
  </div>
</section>
"""
    body += CONTACT
    body += "\n" + footer + "\n"
    body += """
<script>
window.LEXA_HELP = %s;
(function(){
  var input=document.getElementById('helpSearch'), box=document.getElementById('helpResults');
  if(!input||!box) return;
  var data=window.LEXA_HELP||[];
  function norm(s){return (s||'').toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'');}
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  input.addEventListener('input',function(){
    var q=norm(input.value.trim());
    if(q.length<2){box.classList.remove('on');box.innerHTML='';return;}
    var hits=data.filter(function(d){return norm(d.q).indexOf(q)>-1||norm(d.c).indexOf(q)>-1;}).slice(0,8);
    if(!hits.length){box.innerHTML='<div class="empty">Aucune réponse trouvée. Contactez-nous : contact@lexamt.com</div>';box.classList.add('on');return;}
    box.innerHTML=hits.map(function(d){return '<a href="'+d.u+'">'+esc(d.q)+'<span class="rc">'+esc(d.c)+'</span></a>';}).join('');
    box.classList.add('on');
  });
  document.addEventListener('click',function(e){ if(!box.contains(e.target)&&e.target!==input) box.classList.remove('on'); });
})();
</script>
</body>
</html>
""" % json.dumps(index, ensure_ascii=False)
    return url, body


def build_cat(c, nav, footer, present):
    k = c["key"]; title = ctitle(k, c["title"]); url = BASE + "/aide/%s/" % k
    items = c.get("items", [])
    acc = []
    for i, it in enumerate(items):
        acc.append(
            '      <details class="faq-item" id="q-%s-%d">\n'
            '        <summary>%s</summary>\n'
            '        <div class="prose faq-answer">%s</div>\n'
            '      </details>' % (k, i, html.escape(it["q"]), it["a"]))
    title_tag = "%s : aide Lexa | Lexa" % title
    intro_raw = c.get("intro", "") or ("<p>" + title + " : guides et réponses pour utiliser Lexa.</p>")
    intro_text = re.sub(r"<[^>]+>", "", intro_raw).strip()
    desc = html.escape((intro_text or (title + " : guides et réponses pour utiliser Lexa."))[:155])
    # Sidebar de navigation entre les rubriques (active surlignee)
    side = []
    for kk in present:
        active = " active" if kk == k else ""
        side.append('          <a href="/aide/%s/" class="%s">%s<span>%s</span></a>' % (kk, active.strip(), ICON[kk], html.escape(ctitle(kk))))
    side_html = "\n".join(side)
    body = HEAD.format(title=html.escape(title_tag), desc=desc, url=url, jsonld=jsonld_cat(url, title, items), nav=nav)
    body += """
<nav class="breadcrumb" aria-label="Fil d'Ariane">
  <div class="container">
    <ol>
      <li><a href="/">Accueil</a></li>
      <li><span class="sep">/</span><a href="/aide/">Centre d'aide</a></li>
      <li><span class="sep">/</span><span aria-current="page">{title}</span></li>
    </ol>
  </div>
</nav>

<section class="help-page">
  <div class="container">
    <div class="help-layout">
      <details class="help-side" open>
        <summary class="hs-toggle"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg> Toutes les rubriques</summary>
        <a href="/aide/" class="hs-back">{arrowl} Centre d'aide</a>
        <span class="hs-head">Rubriques</span>
        <nav>
{side}
        </nav>
      </details>
      <div class="help-main">
        <span class="eyebrow">Centre d'aide</span>
        <h1>{title}</h1>
        <div class="lead">{intro}</div>
        <div class="faq-list">
{acc}
        </div>
      </div>
    </div>
  </div>
</section>
""".format(title=html.escape(title), arrowl=ARROW_L, intro=intro_raw, acc="\n".join(acc), side=side_html)
    body += CONTACT
    body += "\n" + footer + "\n"
    body += """
<script>
/* ouvre automatiquement la question ciblee par #ancre */
(function(){
  function openHash(){ if(location.hash){ var el=document.querySelector(location.hash); if(el&&el.tagName==='DETAILS'){ el.open=true; el.scrollIntoView({block:'center'}); } } }
  if(document.readyState!=='loading') openHash(); else document.addEventListener('DOMContentLoaded',openHash);
  window.addEventListener('hashchange',openHash);
})();
</script>
</body>
</html>
"""
    return url, body


def update_sitemap(urls):
    sm = open(SITEMAP, encoding="utf-8").read()
    add = []
    for u, pr in urls:
        if u in sm:
            continue
        add.append("  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>%s</priority>\n  </url>" % (u, TODAY, pr))
    if add:
        sm = sm.replace("</urlset>", "\n".join(add) + "\n</urlset>")
        open(SITEMAP, "w", encoding="utf-8").write(sm)
    return len(add)


def main():
    nav, footer = load_shared()
    cats = json.load(open(DATA, encoding="utf-8"))
    by_key = {c["key"]: c for c in cats}
    sm_urls = []
    # hub
    hub_url, hub_html = build_hub(by_key, nav, footer)
    os.makedirs(os.path.join(ROOT, "aide"), exist_ok=True)
    open(os.path.join(ROOT, "aide", "index.html"), "w", encoding="utf-8").write(hub_html)
    sm_urls.append((hub_url, "0.7"))
    # categories
    present = [k for k in ORDER if k in by_key]
    n = 0
    for k in ORDER:
        c = by_key.get(k)
        if not c:
            continue
        url, page = build_cat(c, nav, footer, present)
        d = os.path.join(ROOT, "aide", k)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(page)
        sm_urls.append((url, "0.6"))
        n += 1
    added = update_sitemap(sm_urls)
    total_q = sum(len(c.get("items", [])) for c in cats)
    print("Hub /aide/ + %d pages categorie generes (%d questions au total)" % (n, total_q))
    print("Sitemap : %d URL ajoutees" % added)
    bad = sum(json.dumps(c, ensure_ascii=False).count("—") for c in cats)
    print("Em-dash dans les donnees :", bad)


if __name__ == "__main__":
    main()
