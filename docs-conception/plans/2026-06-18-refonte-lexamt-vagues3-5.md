# Refonte lexamt.com · Vagues 3 à 5 (Personas, Ressources, Légal) · Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development. Contenu au standard `anthropic-skills:lexa-marketing`, design system `lexa-site/assets/lexa.css`. Héros clairs, CTA secondaire `.btn-outline`.

**Goal:** Construire les 3 pages persona, la page Ressources (index blog) + un gabarit d'article réutilisable et réel, et les 2 pages légales, sur le socle, avec SEO/GEO.

**Spec:** `docs/superpowers/specs/2026-06-18-refonte-site-lexamt-design.md` · Socle + Vagues 1-2 faits.

---

## Conventions (lire avant)

- Données de référence (chiffres, sécurité, complémentarité Lexa/Legal 230, coordonnées) : voir plan Vague 1, section Conventions.
- Jamais le caractère tiret cadratin (U+2014). Détection : `grep -rl $'\xe2\x80\x94' <chemin> && echo TROUVE || echo OK`.
- Head depuis `_partials/head.html`. Title ~60, desc ~155. `canonical`/OG/`@id` absolus. Nav (méga-menu) + footer recopiés des partials. Réutiliser composants/tokens de `lexa.css` (cartes, `.eyebrow`, boutons, FAQ `<details>`, « En bref », `.cmp`, `.testi-grid`, composants persona `.personas/.persona`, `.usecases`, `.benefits`, `.compl` déjà créés en Vague 1 sur la page Solutions).
- Pas d'`aggregateRating`. Ton non agressif. Liens internes vers vrais slugs.
- Vérif par page : grep tiret cadratin OK ; JSON-LD parse ; nav/footer ; canonical absolu.

---

## VAGUE 3 : Personas

Gabarit persona commun : nav · hero ciblé métier · bloc « En bref » (GEO) · douleurs spécifiques (3-4) · réponse Lexa point par point · cas d'usage du métier · objections traitées · preuves et chiffres (`.benefits`/`.proofline`) · passerelle complémentarité ou produits · FAQ persona (4-6 Q) · CTA · footer. JSON-LD : `@graph` (Organization `@id https://lexamt.com/#organization`, WebSite, WebPage `@id .../<slug>/#webpage`, BreadcrumbList Accueil > Solutions > Persona) + `FAQPage`. Lien retour vers la page Solutions `/lexa-traduction-juridique-solution-pro-droit/`.

### Task 1: Persona Avocats et cabinets
`lexa-site/traduction-juridique-avocats/index.html`
Head : Title `Traduction juridique pour avocats et cabinets | Lexa` ; Desc `Lexa aide avocats et cabinets à traduire contrats, actes et pièces multilingues avec 99 % de précision et une confidentialité certifiée. Essai gratuit 15 jours.` ; canonical `https://lexamt.com/traduction-juridique-avocats/`.
Contenu : douleurs (terminologie d'un contrat international, confidentialité des pièces, délais clients, cohérence entre documents) ; cas d'usage (contrats internationaux, contentieux multilingue, due diligence, pièces de procédure) ; objection DeepL/ChatGPT (en finesse) ; chiffres (99 %, 50 % délais, +500 cabinets clients) ; CTA essai + démo.
Commit : `Vague 3: page persona Avocats et cabinets` (add `lexa-site/traduction-juridique-avocats/ lexa-site/assets/`).

### Task 2: Persona Directions juridiques
`lexa-site/traduction-juridique-directions-juridiques/index.html`
Head : Title `Traduction juridique pour directions juridiques | Lexa` ; Desc `Pour les directions juridiques : traduisez vos contrats, documents de conformité et filiales étrangères en autonomie, avec cohérence terminologique et budget maîtrisé.` ; canonical `https://lexamt.com/traduction-juridique-directions-juridiques/`.
Contenu : douleurs (volume, cohérence inter-documents, budget, autonomie vs agence) ; cas d'usage (contrats fournisseurs, conformité, filiales, reporting multilingue) ; chiffres (60 % coûts, +400 directions juridiques clientes) ; complémentarité Lexa/Legal 230 ; CTA.
Commit : `Vague 3: page persona Directions juridiques`.

### Task 3: Persona Legal Ops et DSI
`lexa-site/traduction-juridique-legal-ops/index.html`
Head : Title `Traduction juridique pour Legal Ops et DSI | Lexa` ; Desc `Legal Ops et DSI : intégrez la traduction juridique à vos outils via API, gérez vos équipes, garantissez la sécurité (ISO 27001, SSO). Déploiement et démo.` ; canonical `https://lexamt.com/traduction-juridique-legal-ops/`.
Contenu : douleurs (intégration aux outils, gestion d'équipe, sécurité/SSO, gouvernance des données) ; objection « on a déjà une IA interne » traitée (suites LegalTech = analyse/recherche, pas moteur de traduction spécialisé ; ne jamais nommer Harvey/Legora, parler de « suites LegalTech » ; Lexa complémentaire via API) ; cas d'usage (déploiement équipe, API/webhooks, workflow) ; chiffres ; liens vers Lexa API + Sécurité ; CTA démo.
Commit : `Vague 3: page persona Legal Ops et DSI`.

---

## VAGUE 4 : Ressources et gabarit d'article

### Task 4: Index Ressources
`lexa-site/ressources/index.html`
Head : Title `Ressources Lexa : guides et actualités de la traduction juridique IA` (≈60) ; Desc `Guides, analyses et bonnes pratiques sur la traduction juridique par IA, la confidentialité et la LegalTech, par l'équipe Lexa propulsée par Legal 230.` ; canonical `https://lexamt.com/ressources/`.
Contenu : nav · hero · article à la une (lien vers le gabarit article réel de la Task 5) · grille de cartes d'articles (6 à 9 cartes représentatives basées sur les mots-clés du skill : « Traduction juridique par IA vs DeepL », « Confidentialité des documents juridiques », « Traduire un contrat international », « Choisir un outil de traduction pour avocats », etc. ; chaque carte = titre, catégorie, extrait ; toutes les cartes pointent vers le gabarit article réel pour cette phase, en notant via commentaire HTML qu'elles seront déclinées) · filtres de catégorie (boutons visuels, ou statiques) · encart newsletter (champ email + bouton, formulaire non fonctionnel marqué) · CTA. JSON-LD : `@graph` (Organization, WebSite, CollectionPage `@id .../ressources/#webpage`, BreadcrumbList Accueil > Ressources). Styles cartes blog en section commentée de `lexa.css` si besoin.
Commit : `Vague 4: index Ressources (blog)` (add `lexa-site/ressources/ lexa-site/assets/`).

### Task 5: Gabarit d'article (article réel, réutilisable)
`lexa-site/ressources/traduction-juridique-ia-guide/index.html` (sert de gabarit ET d'article flagship)
Head : Title `Traduction juridique par IA : le guide complet | Lexa` ; Desc `Tout comprendre sur la traduction juridique par IA : fonctionnement, précision, confidentialité, comparaison avec les outils généralistes et critères de choix.` ; canonical `https://lexamt.com/ressources/traduction-juridique-ia-guide/`.
Structure article : nav · fil d'Ariane (Accueil > Ressources > Titre) · en-tête article (catégorie, H1, méta auteur « Équipe Lexa, propulsée par Legal 230 » + date 18 juin 2026 + temps de lecture) · bloc « En bref » (40-60 mots, IA-ready) · corps H2/H3 (chaque H2 ouvre par une réponse directe : qu'est-ce que la traduction juridique par IA, comment elle atteint la précision, confidentialité, vs outils généralistes, critères de choix) · encart Lexa (CTA essai) · FAQ (4-6 People Also Ask) · maillage interne (3-5 liens vers pages produit/piliers) · CTA · footer. JSON-LD : `@graph` (Organization, WebSite, `Article` avec headline, author Organization, publisher, datePublished/dateModified 2026-06-18, mainEntityOfPage, image og) + `FAQPage` + `BreadcrumbList`. Styles article (prose, fil d'Ariane, encart) en section commentée de `lexa.css`.
Commit : `Vague 4: gabarit d'article (guide traduction juridique IA)`.

---

## VAGUE 5 : Pages légales

Gabarit légal sobre : nav · en-tête (titre + date de mise à jour) · sommaire ancré (liens vers les sections) · contenu structuré en sections avec ancres · footer. Layout lisible (largeur de lecture limitée). JSON-LD : `@graph` (Organization, WebSite, WebPage, BreadcrumbList). Styles légal (`.legal-wrap`, `.legal-toc`, prose) en section commentée de `lexa.css`.

IMPORTANT : ne pas inventer de clauses juridiques contraignantes ni de données factuelles non connues (SIRET, RCS, capital, hébergeur, directeur de publication). Utiliser les données connues (Lexa, Legal 230, 75 Boulevard Haussmann 75008 Paris, contact@lexamt.com, +33 1 84 80 21 20) et marquer les champs inconnus par un placeholder visible entre crochets, par ex. `[SIRET a completer]`, `[hebergeur a completer]`, accompagné d'un commentaire HTML `<!-- a renseigner par le service juridique -->`.

### Task 6: Mentions légales / Conditions générales
`lexa-site/conditions-general/index.html`
Head : Title `Mentions légales | Lexa` ; Desc `Mentions légales et informations sur l'éditeur du site lexamt.com, Lexa, solution de traduction juridique par IA développée par Legal 230.` ; canonical `https://lexamt.com/conditions-general/`.
Sections : Éditeur du site (Lexa / Legal 230, adresse, contact, [directeur de publication], [SIRET], [RCS], [capital]) · Hébergement ([hebergeur a completer]) · Propriété intellectuelle · Données personnelles (renvoi page Sécurité + RGPD) · Cookies · Droit applicable.
Commit : `Vague 5: page Mentions légales`.

### Task 7: CGU / CGV
`lexa-site/term-and-conditions/index.html`
Head : Title `Conditions générales d'utilisation | Lexa` ; Desc `Conditions générales d'utilisation et de vente du service Lexa, solution de traduction juridique par IA. Abonnements, essai gratuit, responsabilités.` ; canonical `https://lexamt.com/term-and-conditions/`.
Sections (structure + texte d'attente clair à valider par le juridique) : Objet · Accès au service et essai gratuit 15 jours · Abonnements et tarifs (renvoi Tarifs) · Obligations de l'utilisateur · Confidentialité et données (renvoi Sécurité) · Responsabilité · Résiliation · Droit applicable. Marquer le corps des clauses par `<!-- texte juridique a valider par le service juridique -->` et un encadré visible « Document en cours de validation juridique » si le texte n'est pas définitif.
Commit : `Vague 5: page CGU/CGV`.

### Task 8: Vérification globale Vagues 3-5
- [ ] `grep -rl $'\xe2\x80\x94' lexa-site/ && echo TROUVE || echo "OK: 0"`.
- [ ] Pour chaque nouvelle page : nav=1, footer=1, mega=1, JSON-LD parse, canonical absolu.
- [ ] Les 3 liens persona de la page Solutions résolvent désormais en 200.
- [ ] Captures de preuve (1 persona, ressources, 1 article, 1 légale).
- [ ] Commit `--allow-empty` : `Vagues 3-5: vérification globale terminée`.

## Definition of done (Vagues 3-5)
- 3 personas, index Ressources, 1 article gabarit réel, 2 pages légales construits au design system.
- JSON-LD valides (FAQPage/CollectionPage/Article selon page) ; blocs « En bref » sur personas et article.
- Liens persona résolus ; maillage interne en place ; données légales inconnues marquées comme placeholders.
- 0 tiret cadratin ; canonical/OG absolus.

## Suite
Vague 6 (finition technique) : `sitemap.xml`, `robots.txt`, `site.webmanifest`, page `404`, et contrôle SEO global de tout le site.
