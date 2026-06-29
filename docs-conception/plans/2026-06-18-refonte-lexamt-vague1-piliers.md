# Refonte lexamt.com · Vague 1 (Nav, Contact, Piliers) · Plan d'implémentation

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development. Steps use checkbox (`- [ ]`) syntax. Chaque page de contenu doit être rédigée au standard du skill `anthropic-skills:lexa-marketing` (top 1% LegalTech B2B) et respecter le design system de `lexa-site/assets/lexa.css`.

**Goal:** Poser la nav canonique (méga-menu Produits), unifier la page contact sur le socle, et construire les 5 pages piliers (Solutions, Expertise, Sécurité, Comparatif vs DeepL, Tarifs) au design system partagé, avec SEO/GEO complet.

**Architecture:** Site statique multi-pages. Chaque page = `lexa-site/<slug>/index.html`, chargeant `/assets/lexa.css` et (si interactif) `/assets/lexa.js`. Nav et footer recopiés depuis `_partials/` à l'identique. JSON-LD spécifique par page avant `</head>`.

**Tech Stack:** HTML5, CSS3 (Montserrat, variables custom), JS vanilla guardé, JSON-LD. Vérification via preview (port 8791, serveur `lexa-site`) et grep.

**Spec:** `docs/superpowers/specs/2026-06-18-refonte-site-lexamt-design.md`
**Socle (Vague 0):** `lexa-site/assets/lexa.css`, `lexa-site/assets/lexa.js`, `lexa-site/_partials/{head,nav,footer}.html`, `lexa-site/index.html`.

---

## Conventions (lire avant de commencer)

### Données de référence (skill Lexa, à utiliser tel quel)
- Tagline : « Le traducteur qui parle votre langage juridique. »
- Chiffres : +500 cabinets, +400 directions juridiques, 4.9/5 satisfaction, 50 % de délais en moins, 60 % de coûts en moins, 99 % de précision, 40+ langues, 900+ lexiques officiels (CJUE, OMPI, OIT), 60 M de documents juridiques, 14 moteurs spécialisés, essai gratuit 15 jours sans carte bancaire.
- Produits : Lexa Texte, Lexa Documents, Lexa Word (4,90 € HT), Lexa API, Lexa Writing.
- Tarifs (HT, mensuel / annuel) : Essentiel 6,90 / 5,90 (400 000 car., 3 fichiers) ; Standard 23,90 / 21,90 (1 500 000 car., 25 fichiers) ; Premium 44,90 / 39,90 (illimité, 100 fichiers) ; Enterprise sur mesure (dès 25 utilisateurs) ; Lexa Word 4,90. Remise 10 % en annuel. Inclus partout : glossaires illimités, spécialisation par domaine, historique illimité, contrôle qualité, instructions personnalisées, protection des données.
- Sécurité : ISO 27001, ISO 9001:2015, ISO 20000-1:2018, STAR Cloud Security Alliance, AICPA SOC, Cyber Essentials ; chiffrement SSL/TLS + AES-256 (FIPS 140-2 niveau 3) ; hébergement Europe ; RGPD ; suppression des données sous 7 jours ; aucune donnée client utilisée pour l'entraînement ; SLA et NDA sur demande.
- 12 domaines : droit des affaires, pénal, fiscal, propriété intellectuelle, contrats, social, immobilier, banque/finance, commercial, arbitrage international, immigration, droit public.
- Architecture IA en 4 étapes : entraînement juridique (60 M docs alignés 30+ langues), entraînement spécialisé (14 moteurs), entraînement terminologique (juri-linguistes), lexiques officiels (900+).
- Tableau comparatif (Lexa / DeepL / Google Translate) : spécialisation juridique (oui / non / non), lexiques juridiques (900+ / à faire soi-même / non), confidentialité (garantie RGPD+ISO / variable / faible), précision (99 % / moyenne / faible), relecture expert (oui / non / non), fonctionnalités avancées (oui / oui / non).
- Complémentarité : Lexa en self-service au quotidien ; Legal 230 quand la traduction engage la responsabilité (assermenté, dossiers complexes, langues rares, volumes).
- Coordonnées : 75 Boulevard Haussmann, 75008 Paris ; contact@lexamt.com ; +33 1 84 80 21 20.
- Ton : montrer ce que Lexa fait en plus, ne pas dénigrer DeepL/ChatGPT par leur nom de façon agressive ; ne jamais promettre le remplacement total d'un traducteur humain (relecture expert en option) ; pas de chiffres non vérifiés ; pas de `aggregateRating`.

### Règles transverses
- **Jamais le caractère tiret cadratin (U+2014)** nulle part. Pour le détecter sans le taper : `grep -rl $'\xe2\x80\x94' lexa-site/ && echo TROUVE || echo OK`.
- Head : repartir du gabarit `_partials/head.html`, remplacer les variables, placer les JSON-LD avant `</head>`. Title ~60 car., description ~155 car.
- Liens internes root-relative vers les vrais slugs ; `canonical`, Open Graph, `@id` JSON-LD en URL absolue `https://lexamt.com/<slug>/`.
- Nav et footer : recopier les partials à l'identique (après la tâche 1 pour la nav).
- Réutiliser au maximum les composants existants de `lexa.css` (boutons `.btn`/`.btn-emerald`/`.btn-ghost`, `.container`, `.eyebrow`, sections alternées, cartes, `.cmp` tableau comparatif, `.sec-grid` cartes sécurité, FAQ `<details>`, carrousel `.testi-grid`). Ne créer de nouveaux composants que si nécessaire, dans une section commentée de `lexa.css`.
- GEO : sur Expertise, Sécurité, Comparatif et Solutions, ajouter un bloc « En bref » (réponse directe 40 à 60 mots) juste après le hero. FAQ structurée + JSON-LD `FAQPage` sur chaque page pilier.
- JSON-LD commun par page profonde : `@graph` avec `Organization` (réutiliser `@id https://lexamt.com/#organization`), `WebSite` (`#website`), `WebPage` (`#webpage` propre à la page), `BreadcrumbList` (Accueil > Page). Ajouter les types spécifiques indiqués par tâche.

### Vérification standard par page (rappel)
Après création, pour chaque page : recharger dans la preview 8791, `preview_console_logs` (0 erreur), `preview_eval` (JSON-LD parse, CSS chargé en 200), `preview_screenshot` desktop, et `grep -rl $'\xe2\x80\x94'` (0). Vérifier que la nav et le footer sont présents et identiques aux partials.

---

## Task 1: Nav canonique avec méga-menu Produits

**Files:**
- Modify: `lexa-site/_partials/nav.html`
- Modify: `lexa-site/assets/lexa.css` (styles du dropdown, section commentée)
- Modify: `lexa-site/index.html` (remplacer le bloc nav par la nav canonique)

Nav cible (gauche vers droite) : logo, **Produits** (déclencheur de méga-menu), Solutions, Expertise, Tarifs, Ressources, Contact, puis `.nav-cta` (tel + bouton essai). Le méga-menu Produits liste les 5 produits avec libellé + courte description, en CSS pur (hover + focus-within, accessible au clavier), sans dépendance JS.

- [ ] **Step 1: Écrire le markup du méga-menu dans `nav.html`**

Insérer, en premier item de `.nav-links`, un conteneur `.nav-item-mega` contenant un `<button class="nav-mega-trigger" aria-expanded="false">Produits</button>` et un `<div class="mega-panel">` avec 5 liens (titre + description courte) vers : `/lexa-texte-traduction-juridique-ia/` (Lexa Texte, « Traduction en temps réel, style préservé »), `/lexa-document-traduction-juridique/` (Lexa Documents, « +30 formats, mise en page intacte »), `/lexa-word-add-on-microsoft-word/` (Lexa Word, « Traduire dans Word »), `/lexa-api-connecteur-juridiques/` (Lexa API, « Intégration à vos outils »), `/lexa-writing-redaction-juridique/` (Lexa Writing, « Reformuler, anonymiser, résumer »). Garder ensuite Solutions, Expertise, Tarifs, Ressources, Contact.

- [ ] **Step 2: Ajouter les styles du méga-menu dans `lexa.css`**

À la fin de `lexa.css`, ajouter une section `/* ===== Mega-menu Produits ===== */` : `.nav-item-mega{position:relative}`, panneau masqué par défaut (`opacity:0;visibility:hidden;transform:translateY(6px)`) révélé au `:hover` et `:focus-within` du `.nav-item-mega`, panneau `position:absolute` largeur ~560px, fond blanc, ombre douce, coins arrondis, grille 2 colonnes de liens, titres en `var(--ink)` + descriptions en `var(--muted)`. Le déclencheur reprend le style des autres liens nav. Sous 940px, le méga-menu se replie (les produits deviennent des liens simples ou le panneau s'ouvre en accordéon). Aucun nouveau token de couleur.

- [ ] **Step 3: Appliquer la nav canonique à `index.html`**

Repérer le bloc `<header class="nav">...</header>` dans `lexa-site/index.html` et le remplacer intégralement par le contenu de `_partials/nav.html` (avec Edit). Vérifier qu'il n'en reste qu'un seul.

- [ ] **Step 4: Vérifier en preview**

Recharger `/`. `preview_eval` : confirmer que `.nav-item-mega` existe, que le `.mega-panel` est masqué au repos et visible au survol (vérifier via `getComputedStyle` après `:hover` simulé ou via présence DOM + visibilité), et que les 5 liens produits pointent vers les bons slugs. `preview_screenshot`. `preview_console_logs` 0 erreur.

- [ ] **Step 5: Vérifier tiret cadratin + commit**

```bash
cd "/Users/fabienbernier/Claude project"
grep -rl $'\xe2\x80\x94' lexa-site/_partials/nav.html lexa-site/assets/lexa.css lexa-site/index.html && echo TROUVE || echo OK
git add lexa-site/_partials/nav.html lexa-site/assets/lexa.css lexa-site/index.html
git commit -m "Vague 1: nav canonique avec méga-menu Produits"
```

---

## Task 2: Unifier la page contact sur le socle

**Files:**
- Modify: `lexa-site/assets/lexa.css` (porter les composants propres à contact, en Montserrat)
- Create: `lexa-site/contact/index.html` (déjà créé en Vague 0 ? non : contact a été reporté ici. Le créer depuis `lexa-contact.html`)

Source : `lexa-contact.html` (racine du repo). Composants propres à contact à porter dans `lexa.css` (absents du socle) : `.form-card .form-wrap .form-eyebrow .form-group .form-row .form-secure .form-promise .btn-submit .req .consent .contact-card .ct-txt .steps .steps-grid .steps-head .step .hero-quote .hero-tag .hero-trust .trust-foot .why-list .sec-pills .pill .rating .av .com .arrow .dot .q-ic .sub`. Ignorer `.googleapis`/`.gstatic` (faux positifs issus des URLs de polices).

- [ ] **Step 1: Lister précisément les blocs CSS à porter**

```bash
cd "/Users/fabienbernier/Claude project"
# Visualiser le CSS de contact (lignes 11 a 446) pour reperer les regles des classes ci-dessus
sed -n '11,446p' lexa-contact.html | grep -n -E '^\s*\.(form-|contact-card|steps|step|hero-quote|hero-tag|hero-trust|trust-foot|why-list|sec-pills|pill|rating|av|com|arrow|dot|q-ic|sub|ct-txt|req|consent|btn-submit)'
```

- [ ] **Step 2: Porter ces règles dans `lexa.css`**

Copier les règles CSS correspondantes (et leurs media queries) à la fin de `lexa.css`, dans une section `/* ===== Composants page Contact ===== */`. **Retirer toute déclaration `font-family` faisant référence à Plus Jakarta Sans ou Inter** : ces composants doivent hériter de Montserrat (le `body{font-family:'Montserrat'...}` du socle s'applique). Ne pas redéfinir les variables `:root` (déjà identiques dans le socle). Dédupliquer : si une classe existe déjà dans le socle, ne pas la réintroduire.

- [ ] **Step 3: Reconstruire `contact/index.html` avec CSS externe et head complet**

```bash
cd "/Users/fabienbernier/Claude project"
mkdir -p lexa-site/contact
```
Reconstruire la page : repartir du `<body>` de `lexa-contact.html` (tout ce qui suit `</head>`), et construire un nouveau `<head>` à partir du gabarit `_partials/head.html` avec :
- `{{TITLE}}` : `Contact Lexa : parlez à un expert en traduction juridique par IA` (sans tiret cadratin ; remplace l'ancien titre qui en contenait un)
- `{{DESC}}` : reprendre la description existante de contact, raccourcie à ~155 car.
- `{{CANONICAL}}` et `{{OG_URL}}` : `https://lexamt.com/contact/`
- `{{OG_TITLE}}` : `Contact Lexa · Parlez à un expert en traduction juridique`
- `{{OG_DESC}}` : courte phrase de prise de contact / démo.
Lier `/assets/lexa.css`. Si la page contient un script interactif (validation de formulaire), l'extraire dans `lexa.js` (guardé) ou le garder inline minimal ; sinon ne pas charger `lexa.js`.

- [ ] **Step 4: Recopier nav et footer canoniques**

Insérer le `_partials/nav.html` (avec méga-menu, issu de la tâche 1) en tête de `<body>` et le `_partials/footer.html` en fin, en remplacement de la nav/footer d'origine de contact si présents.

- [ ] **Step 5: Ajouter le JSON-LD ContactPage**

Avant `</head>`, ajouter un `<script type="application/ld+json">` avec `@graph` : `Organization` (`@id https://lexamt.com/#organization`, mêmes données qu'à l'accueil), `WebSite`, `ContactPage` (`@id https://lexamt.com/contact/#webpage`, url absolue, `about` → organization), `BreadcrumbList` (Accueil > Contact).

- [ ] **Step 6: Corriger les liens internes**

Appliquer la table de correspondance des liens (voir plan Vague 0, section Conventions) sur `lexa-site/contact/index.html`.

- [ ] **Step 7: Vérifier en preview + tiret cadratin**

Recharger `/contact/`. `preview_screenshot` : la page doit être stylée en Montserrat, formulaire et étapes correctement rendus (composants portés). `preview_console_logs` 0 erreur. `preview_eval` : JSON-LD parse, CSS 200. Puis :
```bash
cd "/Users/fabienbernier/Claude project"
grep -rl $'\xe2\x80\x94' lexa-site/contact/ lexa-site/assets/lexa.css && echo TROUVE || echo OK
```
Expected : OK (0). Vérifier en particulier que le `<title>` n'a plus de tiret cadratin.

- [ ] **Step 8: Commit**

```bash
cd "/Users/fabienbernier/Claude project"
git add lexa-site/contact/ lexa-site/assets/lexa.css
git commit -m "Vague 1: page contact unifiée sur le socle (Montserrat, SEO complet, ContactPage)"
```

---

## Task 3: Page Tarifs

**Files:**
- Create: `lexa-site/lexa-tarifs-traduction-juridique/index.html`
- Modify: `lexa-site/assets/lexa.css` (cartes de prix + bascule, section commentée)
- Modify: `lexa-site/assets/lexa.js` (module bascule mensuel/annuel, guardé)

**Head SEO :** Title `Tarifs Lexa : traduction juridique par IA dès 6,90 €/mois` ; Desc `Essentiel, Standard, Premium, Enterprise : glossaires illimités, spécialisation juridique, confidentialité ISO 27001. Essai gratuit 15 jours, sans carte bancaire.` ; canonical `https://lexamt.com/lexa-tarifs-traduction-juridique/`.

**Sections :**
1. Nav (partial).
2. Hero : eyebrow « Tarifs », titre court, sous-titre, bascule mensuel / annuel (-10 %).
3. Grille de 4 plans (cartes) avec prix HT, plafond caractères/fichiers, liste de bénéfices, CTA essai ; plan Standard marqué « populaire ». Encart Lexa Word 4,90.
4. Tableau comparatif des fonctionnalités par plan (réutiliser le style `.cmp` du socle si adapté, sinon nouveau tableau).
5. Bloc « Inclus dans tous les plans » (les 6 éléments de la liste de référence).
6. Bandeau Enterprise : sur mesure, dès 25 utilisateurs, CTA « Demander une démo » → `/contact/`.
7. FAQ tarifs (facturation, résiliation, essai, annuel vs mensuel) en `<details>`.
8. CTA final + footer (partial).

**JS :** ajouter dans `lexa.js` un module guardé `if(document.querySelector('[data-billing-toggle]'))` qui bascule l'affichage des prix mensuel/annuel (attributs `data-price-monthly` / `data-price-annual`).

**JSON-LD :** `@graph` (Organization, WebSite, WebPage `#webpage`, BreadcrumbList) + `Product` « Lexa » avec `AggregateOffer` (lowPrice 4.90, highPrice 44.90, priceCurrency EUR, offerCount) **et** un `Offer` par plan (Essentiel 6.90, Standard 23.90, Premium 44.90, Lexa Word 4.90 ; Enterprise sans prix). + `FAQPage`.

- [ ] **Step 1: Créer le dossier et la page**

```bash
cd "/Users/fabienbernier/Claude project"
mkdir -p lexa-site/lexa-tarifs-traduction-juridique
```
Construire `index.html` : head (gabarit + JSON-LD), nav (partial), sections 2 à 8 ci-dessus rédigées au standard skill Lexa, footer (partial), `<script src="/assets/lexa.js" defer></script>`.

- [ ] **Step 2: Ajouter styles cartes de prix + bascule dans `lexa.css`**

Section `/* ===== Tarifs ===== */` : grille responsive de cartes, carte « populaire » accentuée (bordure émeraude), bascule (segmented control), prix grand format. Réutiliser tokens et boutons existants.

- [ ] **Step 3: Ajouter le module bascule dans `lexa.js`**

Module guardé qui, au clic sur la bascule, met à jour les montants affichés et un état actif. Ne s'exécute que si `[data-billing-toggle]` existe.

- [ ] **Step 4: Vérifier en preview**

Recharger `/lexa-tarifs-traduction-juridique/`. Vérifier : 4 plans affichés, bascule fonctionnelle (les prix changent), tableau lisible, JSON-LD parse (Product + Offers + FAQPage), 0 erreur console. `preview_screenshot`.

- [ ] **Step 5: Tiret cadratin + commit**

```bash
cd "/Users/fabienbernier/Claude project"
grep -rl $'\xe2\x80\x94' lexa-site/lexa-tarifs-traduction-juridique/ lexa-site/assets/ && echo TROUVE || echo OK
git add lexa-site/lexa-tarifs-traduction-juridique/ lexa-site/assets/
git commit -m "Vague 1: page Tarifs (4 plans, bascule mensuel/annuel, JSON-LD Product)"
```

---

## Task 4: Page Expertise

**Files:**
- Create: `lexa-site/expertise-lexa/index.html`
- Modify (si besoin): `lexa-site/assets/lexa.css`

**Head SEO :** Title `Expertise Lexa : l'IA de traduction entraînée sur le droit` ; Desc `Comment Lexa atteint 99 % de précision : 60 M de documents juridiques, 14 moteurs spécialisés, 900+ lexiques officiels et relecture expert. Découvrez notre expertise IA.` ; canonical `https://lexamt.com/expertise-lexa/`.

**Sections :** nav · hero « Une IA qui ne traduit pas seulement : elle comprend le droit » · bloc « En bref » · architecture IA en 4 étapes (cartes ou timeline) · 12 domaines juridiques (grille) · 40+ langues · Lexa Quality (score par segment + relecture expert en option) · bloc passerelle vers Sécurité (lien `/securite-confidentialite-traduction-juridique/`) · autorité Legal 230 (1ère agence européenne) · FAQ · CTA · footer.

**JSON-LD :** `@graph` (Organization, WebSite, WebPage, BreadcrumbList) + `FAQPage`.

- [ ] **Step 1: Créer le dossier et la page**

```bash
cd "/Users/fabienbernier/Claude project"
mkdir -p lexa-site/expertise-lexa
```
Rédiger la page au standard skill (réutiliser composants socle : cartes, sections alternées, grilles). Réutiliser la structure de la section « Pourquoi Lexa » et « sécurité » de l'accueil si pertinent.

- [ ] **Step 2: Vérifier en preview**

Recharger `/expertise-lexa/`. JSON-LD parse, bloc « En bref » présent en tête, 12 domaines affichés, lien vers Sécurité, 0 erreur console. `preview_screenshot`.

- [ ] **Step 3: Tiret cadratin + commit**

```bash
cd "/Users/fabienbernier/Claude project"
grep -rl $'\xe2\x80\x94' lexa-site/expertise-lexa/ && echo TROUVE || echo OK
git add lexa-site/expertise-lexa/ lexa-site/assets/
git commit -m "Vague 1: page Expertise (architecture IA 4 étapes, domaines, GEO)"
```

---

## Task 5: Page Sécurité et confidentialité

**Files:**
- Create: `lexa-site/securite-confidentialite-traduction-juridique/index.html`
- Modify (si besoin): `lexa-site/assets/lexa.css`

**Head SEO :** Title `Sécurité et confidentialité de vos documents juridiques | Lexa` ; Desc `Lexa protège vos documents : chiffrement AES-256, hébergement Europe, RGPD, suppression sous 7 jours, zéro entraînement sur vos données. Certifié ISO 27001.` ; canonical `https://lexamt.com/securite-confidentialite-traduction-juridique/`.

**Sections :** nav · hero trust « Vos documents les plus sensibles, entre de bonnes mains » · bloc « En bref » · grille des certifications (ISO 27001, ISO 9001, ISO 20000-1, STAR CSA, AICPA SOC, Cyber Essentials) · chiffrement (AES-256 + SSL/TLS, FIPS 140-2 niveau 3) · hébergement Europe · conformité RGPD · rétention (suppression sous 7 jours) · zéro entraînement sur données client · NDA et SLA sur demande · mention « page conçue pour vos appels d'offres » · FAQ confidentialité · CTA · footer. Réutiliser `.sec-grid` / `.sec-item` du socle pour les cartes.

**JSON-LD :** `@graph` (Organization, WebSite, WebPage, BreadcrumbList) + `FAQPage`.

- [ ] **Step 1: Créer le dossier et la page**

```bash
cd "/Users/fabienbernier/Claude project"
mkdir -p lexa-site/securite-confidentialite-traduction-juridique
```

- [ ] **Step 2: Vérifier en preview**

Recharger la page. Certifications affichées, bloc « En bref », JSON-LD parse, 0 erreur console. `preview_screenshot`.

- [ ] **Step 3: Tiret cadratin + commit**

```bash
cd "/Users/fabienbernier/Claude project"
grep -rl $'\xe2\x80\x94' lexa-site/securite-confidentialite-traduction-juridique/ && echo TROUVE || echo OK
git add lexa-site/securite-confidentialite-traduction-juridique/ lexa-site/assets/
git commit -m "Vague 1: page Sécurité et confidentialité (certifications, RGPD, GEO)"
```

---

## Task 6: Page Comparatif vs DeepL

**Files:**
- Create: `lexa-site/lexa-vs-deepl-traduction-juridique/index.html`
- Modify (si besoin): `lexa-site/assets/lexa.css`

**Head SEO :** Title `Lexa vs DeepL : quelle traduction juridique par IA choisir ?` ; Desc `Comparatif Lexa, DeepL, ChatGPT et Google Translate pour la traduction juridique : spécialisation, lexiques officiels, confidentialité, précision. L'alternative spécialisée.` ; canonical `https://lexamt.com/lexa-vs-deepl-traduction-juridique/`.

**Sections :** nav · hero « Ces outils traduisent. Lexa comprend le droit. » · bloc « En bref » · grand tableau comparatif Lexa / DeepL / ChatGPT / Google Translate (6 critères de la liste de référence ; réutiliser `.cmp`) · explication critère par critère (spécialisation, lexiques, confidentialité, précision, relecture expert, formats) · traitement de l'objection « on utilise déjà DeepL / ChatGPT » (montrer le « en plus », ton non agressif) · complémentarité possible via API · FAQ · CTA · footer.

**JSON-LD :** `@graph` (Organization, WebSite, WebPage, BreadcrumbList) + `FAQPage`.

- [ ] **Step 1: Créer le dossier et la page**

```bash
cd "/Users/fabienbernier/Claude project"
mkdir -p lexa-site/lexa-vs-deepl-traduction-juridique
```

- [ ] **Step 2: Vérifier en preview**

Recharger la page. Tableau comparatif lisible, ton conforme (pas de dénigrement nominatif agressif), JSON-LD parse, 0 erreur console. `preview_screenshot`.

- [ ] **Step 3: Tiret cadratin + commit**

```bash
cd "/Users/fabienbernier/Claude project"
grep -rl $'\xe2\x80\x94' lexa-site/lexa-vs-deepl-traduction-juridique/ && echo TROUVE || echo OK
git add lexa-site/lexa-vs-deepl-traduction-juridique/ lexa-site/assets/
git commit -m "Vague 1: page Comparatif vs DeepL (tableau, objections, GEO)"
```

---

## Task 7: Page Solutions (hub)

**Files:**
- Create: `lexa-site/lexa-traduction-juridique-solution-pro-droit/index.html`
- Modify (si besoin): `lexa-site/assets/lexa.css`

**Head SEO :** Title `Lexa : la traduction juridique par IA pour les pros du droit` ; Desc `Avocats, directions juridiques, Legal Ops, notaires : Lexa traduit vos documents juridiques avec 99 % de précision et une confidentialité certifiée. Essai gratuit 15 jours.` ; canonical `https://lexamt.com/lexa-traduction-juridique-solution-pro-droit/`.

**Sections :** nav · hero métiers du droit · bloc « En bref » · 3 cartes persona qui routent vers les futures pages persona (Avocats & cabinets → `/traduction-juridique-avocats/`, Directions juridiques → `/traduction-juridique-directions-juridiques/`, Legal Ops & DSI → `/traduction-juridique-legal-ops/`) · sections Notaires et Compliance (sans page dédiée) · cas d'usage transverses (contrat international, due diligence, contentieux multilingue, CGV multilingues) · bénéfices chiffrés (50 % délais, 60 % coûts, 99 % précision) · complémentarité Lexa / Legal 230 (tableau) · témoignages (réutiliser `.testi-grid`) · CTA · footer.

Note : les 3 liens persona pointeront vers des pages construites en Vague 3 ; les liens sont posés dès maintenant (ils résolvent en production une fois ces pages créées).

**JSON-LD :** `@graph` (Organization, WebSite, WebPage, BreadcrumbList) + `FAQPage`.

- [ ] **Step 1: Créer le dossier et la page**

```bash
cd "/Users/fabienbernier/Claude project"
mkdir -p lexa-site/lexa-traduction-juridique-solution-pro-droit
```

- [ ] **Step 2: Vérifier en preview**

Recharger la page. 3 cartes persona avec liens corrects, tableau de complémentarité, témoignages, JSON-LD parse, 0 erreur console. `preview_screenshot`.

- [ ] **Step 3: Tiret cadratin + commit**

```bash
cd "/Users/fabienbernier/Claude project"
grep -rl $'\xe2\x80\x94' lexa-site/lexa-traduction-juridique-solution-pro-droit/ && echo TROUVE || echo OK
git add lexa-site/lexa-traduction-juridique-solution-pro-droit/ lexa-site/assets/
git commit -m "Vague 1: page Solutions hub (personas, cas d'usage, complémentarité)"
```

---

## Task 8: Vérification globale Vague 1

**Files:** aucun nouveau ; contrôle sur `lexa-site/`.

- [ ] **Step 1: Tiret cadratin global**

```bash
cd "/Users/fabienbernier/Claude project"
grep -rl $'\xe2\x80\x94' lexa-site/ && echo "TROUVE, a corriger" || echo "OK: 0 tiret cadratin partout"
```

- [ ] **Step 2: Cohérence nav et footer sur toutes les pages**

```bash
cd "/Users/fabienbernier/Claude project"
for f in lexa-site/index.html lexa-site/*/index.html; do printf "%s nav=%s footer=%s mega=%s\n" "$f" "$(grep -c 'class="nav-links"' "$f")" "$(grep -c 'class="footer"' "$f")" "$(grep -c 'nav-item-mega' "$f")"; done
```
Expected : chaque page a 1 nav, 1 footer, 1 méga-menu.

- [ ] **Step 3: JSON-LD valide sur chaque page**

Avec `preview_eval` (port 8791), charger chaque slug et `JSON.parse` tous les `application/ld+json`. 0 erreur. Vérifier les types attendus par page (Tarifs : Product+AggregateOffer ; les autres : FAQPage + BreadcrumbList).

- [ ] **Step 4: Liens internes (pas de 404 de structure)**

```bash
cd "/Users/fabienbernier/Claude project"
grep -rho 'href="/[a-z][^"]*"' lexa-site/*/index.html lexa-site/index.html | sort -u
```
Vérifier que tous les href internes correspondent à des slugs prévus (existants ou à venir en Vague 2/3). Aucun ancien slug inventé.

- [ ] **Step 5: Captures de preuve**

`preview_screenshot` desktop des 6 pages (contact, tarifs, expertise, sécurité, comparatif, solutions).

- [ ] **Step 6: Commit de clôture**

```bash
cd "/Users/fabienbernier/Claude project"
git add -A lexa-site/
git commit -m "Vague 1: vérification globale terminée" --allow-empty
```

---

## Definition of done (Vague 1)

- Nav canonique avec méga-menu Produits, appliquée à l'accueil et à toutes les nouvelles pages.
- Contact unifiée sur le socle (Montserrat), head SEO complet, JSON-LD ContactPage, titre sans tiret cadratin.
- 5 pages piliers construites au design system, contenu refondu au standard skill Lexa, blocs « En bref » sur Expertise/Sécurité/Comparatif/Solutions.
- Tarifs : 4 plans + bascule fonctionnelle + JSON-LD Product/AggregateOffer.
- JSON-LD valide partout, liens internes vers vrais slugs, `canonical`/OG absolus.
- 0 tiret cadratin sur tout `lexa-site/`.

## Suite

Vague 2 (Produits : Texte, Documents, Word, API, Writing) puis Vague 3 (Personas) une fois la Vague 1 validée. Le méga-menu et les pages piliers servent de référence de composants.
