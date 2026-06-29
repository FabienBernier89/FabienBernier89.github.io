# Refonte lexamt.com · Vague 7 (Domaines d'expertise + nav enrichie) · Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development. Contenu au standard `anthropic-skills:lexa-marketing`, design system `lexa-site/assets/lexa.css`. Héros clairs, CTA secondaire `.btn-outline`.

**Goal:** Créer les 12 pages de domaines du droit (liées depuis la page Expertise du vrai lexamt.com) et enrichir le méga-menu avec des déroulants Solutions (personas) et Expertise (domaines), propagés sur tout le site.

**Spec:** `docs/superpowers/specs/2026-06-18-refonte-site-lexamt-design.md` · Socle + Vagues 1-6 faits.

---

## Conventions

- Données de référence (chiffres, sécurité, complémentarité, 4 étapes IA, 900+ lexiques) : voir plan Vague 1.
- Jamais le caractère tiret cadratin (U+2014). Détection : `grep -rl $'\xe2\x80\x94' <chemin> && echo TROUVE || echo OK`.
- Head depuis `_partials/head.html`. Title ~60, desc ~155. `canonical`/OG/`@id` absolus. Nav (NOUVELLE, voir Task A) + footer recopiés des partials. Réutiliser composants/tokens de `lexa.css`.
- Pas d'`aggregateRating`. Liens internes vers vrais slugs.

### Les 12 domaines (slug réel préservé)
1. Droit des sociétés `/expertise-droit-des-societes/`
2. Droit commercial `/expertise-droit-commercial/`
3. Droit des contrats `/expertise-droit-des-contrats/`
4. Droit fiscal `/expertise-droit-fiscal/`
5. Propriété intellectuelle `/expertise-propriete-intellectuelle/`
6. Droit social `/expertise-droit-social/`
7. Droit immobilier `/expertise-droit-immobilier/`
8. Banque et finance `/expertise-banque-et-finance/`
9. Arbitrage international `/expertise-arbitrage-international/`
10. Contentieux `/expertise-page-contentieux/`
11. Immigration internationale `/expertise-droit-de-limmigration/`
12. Droit public `/expertise-droit-public/`

### Gabarit page domaine (ordre des sections)
1. Nav (partial enrichi).
2. Hero clair : eyebrow « Expertise · [Domaine] », H1 « Traduction juridique en [domaine] » (ou formulation adaptée), sous-titre, CTA primaire essai `.btn-emerald` + secondaire `.btn-outline` (démo).
3. Bloc « En bref » (GEO, 40-60 mots) : Lexa traduit les documents de [domaine] avec la terminologie exacte, moteur spécialisé, 900+ lexiques, 99 % de précision, confidentialité.
4. Pourquoi le [domaine] exige une traduction spécialisée (enjeux terminologiques propres au domaine).
5. Documents que Lexa traduit dans ce domaine (liste concrète, propre au domaine).
6. L'expertise Lexa en [domaine] (moteur spécialisé parmi les 14, terminologie validée par juri-linguistes, lexiques officiels appliqués).
7. Cas d'usage concrets du domaine.
8. FAQ (3-5 questions propres au domaine) en `<details>`.
9. Maillage : lien vers la page Expertise `/expertise-lexa/`, 1-2 autres domaines liés, 1 produit pertinent (Documents/Texte), CTA.
10. CTA final + footer (partial).

JSON-LD : `@graph` (Organization `@id https://lexamt.com/#organization`, WebSite, WebPage `@id .../<slug>/#webpage`, BreadcrumbList Accueil > Expertise > [Domaine]) + `FAQPage`.

Contenu spécialisé par domaine (repères, à enrichir au standard skill) :
- Droit des sociétés : statuts, pactes d'associés, assemblées, fusions-acquisitions, K-bis.
- Droit commercial : CGV/CGA, contrats de distribution, baux commerciaux, litiges commerciaux.
- Droit des contrats : contrats internationaux, clauses (confidentialité, résiliation), conditions générales.
- Droit fiscal : conventions fiscales, contrôles et redressements, documentation prix de transfert, TVA.
- Propriété intellectuelle : brevets, marques, dessins et modèles, contrats de licence, contentieux PI.
- Droit social : contrats de travail, accords collectifs, procédures, documents RH multilingues.
- Droit immobilier : actes de vente, baux, promesses, due diligence immobilière.
- Banque et finance : conventions de crédit, garanties, documentation financière, conformité.
- Arbitrage international : clauses compromissoires, mémoires, sentences, règlements CCI/CIRDI.
- Contentieux : pièces de procédure, conclusions, jugements, traduction pour audiences.
- Immigration internationale : visas, titres de séjour, actes d'état civil, dossiers consulaires.
- Droit public : marchés publics, contrats administratifs, textes réglementaires.

---

## Task A : Nav enrichie (Produits + Solutions + Expertise déroulants)

**Files:** Modify `lexa-site/_partials/nav.html`, `lexa-site/assets/lexa.css`.

Nouvelle nav (gauche vers droite) : logo · **Produits** (déroulant 5 produits, existant) · **Solutions** (déroulant : 3 personas + lien « Toutes les solutions » vers le hub) · **Expertise** (déroulant large multi-colonnes : 12 domaines + lien « Notre expertise IA » vers `/expertise-lexa/`) · Tarifs · Ressources · Contact · `.nav-cta`.

- Déclencheurs Solutions et Expertise : un `<a>` cliquable vers la page hub (`/lexa-traduction-juridique-solution-pro-droit/` et `/expertise-lexa/`) avec chevron, ET un panneau déroulant au hover/focus-within (comme Produits). Réutiliser le même mécanisme CSS que `.nav-item-mega`.
- Panneau Solutions : 3 liens persona (Avocats `/traduction-juridique-avocats/`, Directions juridiques `/traduction-juridique-directions-juridiques/`, Legal Ops & DSI `/traduction-juridique-legal-ops/`) + lien hub.
- Panneau Expertise : 12 liens domaines (libellé + slug ci-dessus), disposés en 3 colonnes (panneau large, ex. 720-760px), + lien « Notre expertise IA » vers `/expertise-lexa/`.
- Styles : généraliser `.nav-item-mega`/`.mega-panel` ou ajouter `.mega-panel--wide` (3 colonnes) ; responsive sous 940px (les panneaux ne cassent pas la nav mobile). Aucun nouveau token de couleur.

- [ ] Step 1 : mettre à jour `nav.html` avec les 3 déclencheurs et leurs panneaux.
- [ ] Step 2 : ajouter/généraliser les styles dans `lexa.css` (section méga-menu).
- [ ] Step 3 : vérifier `grep -rl $'\xe2\x80\x94'` = OK ; nav.html contient les 3 panneaux, 5 produits + 3 personas + 12 domaines avec bons slugs.
- [ ] Step 4 : commit `Vague 7: nav enrichie (Solutions et Expertise deroulants)` (add `lexa-site/_partials/nav.html lexa-site/assets/lexa.css`). (La propagation aux pages existantes est la Task C.)

## Task B : 12 pages de domaine

Construire les 12 pages selon le gabarit domaine (recopier la nouvelle nav du partial). Commits individuels : `Vague 7: page domaine [Nom]` (add le dossier + `lexa-site/assets/`). Vérif par page : grep tiret cadratin OK ; JSON-LD parse (FAQPage + BreadcrumbList) ; nav (3 déroulants) + footer ; canonical absolu ; « En bref » ; maillage vers Expertise.

- [ ] B1 Droit des sociétés `lexa-site/expertise-droit-des-societes/index.html`
- [ ] B2 Droit commercial `lexa-site/expertise-droit-commercial/index.html`
- [ ] B3 Droit des contrats `lexa-site/expertise-droit-des-contrats/index.html`
- [ ] B4 Droit fiscal `lexa-site/expertise-droit-fiscal/index.html`
- [ ] B5 Propriété intellectuelle `lexa-site/expertise-propriete-intellectuelle/index.html`
- [ ] B6 Droit social `lexa-site/expertise-droit-social/index.html`
- [ ] B7 Droit immobilier `lexa-site/expertise-droit-immobilier/index.html`
- [ ] B8 Banque et finance `lexa-site/expertise-banque-et-finance/index.html`
- [ ] B9 Arbitrage international `lexa-site/expertise-arbitrage-international/index.html`
- [ ] B10 Contentieux `lexa-site/expertise-page-contentieux/index.html`
- [ ] B11 Immigration internationale `lexa-site/expertise-droit-de-limmigration/index.html`
- [ ] B12 Droit public `lexa-site/expertise-droit-public/index.html`

## Task C : Propager la nav enrichie sur toutes les pages existantes

**Files:** toutes les pages `lexa-site/**/index.html` déjà construites (accueil + ~19 pages + 404).

La nav est dupliquée dans chaque page. Remplacer le bloc `<header class="nav">...</header>` par la nouvelle nav du partial dans chaque page existante. Méthode : script Python qui, pour chaque fichier, remplace par regex non-greedy `<header class="nav">.*?</header>` (DOTALL) par le contenu de `_partials/nav.html`. La page 404 (`lexa-site/404.html`) contient aussi la nav inline : la mettre à jour également.

- [ ] Step 1 : script de propagation (Python), appliqué à toutes les pages SAUF celles déjà créées avec la nouvelle nav (domaines de Task B). Vérifier 1 seul `<header class="nav">` par page après coup.
- [ ] Step 2 : `grep -rl $'\xe2\x80\x94' lexa-site/` = OK.
- [ ] Step 3 : commit `Vague 7: propagation de la nav enrichie sur tout le site`.

## Task D : Vérification globale Vague 7

- [ ] `grep -rl $'\xe2\x80\x94' lexa-site/` = OK.
- [ ] Les 12 slugs domaine répondent en 200 ; JSON-LD parse ; BreadcrumbList Accueil > Expertise > Domaine.
- [ ] Le méga-menu (sur l'accueil et une page au hasard) contient bien les 3 panneaux : 5 produits, 3 personas, 12 domaines, tous les liens résolvent en 200.
- [ ] Mettre à jour `sitemap.xml` : ajouter les 12 URLs domaine.
- [ ] Captures de preuve (méga-menu déployé, 1 page domaine).
- [ ] Commit `Vague 7: verification globale (12 domaines + nav enrichie)`.

## Definition of done
- 12 pages domaine au gabarit, contenu spécialisé, JSON-LD valides, slugs réels préservés.
- Nav enrichie (Produits + Solutions + Expertise déroulants) propagée sur 100 % des pages.
- sitemap.xml à jour (31 URLs) ; 0 tiret cadratin ; tous liens internes en 200.
