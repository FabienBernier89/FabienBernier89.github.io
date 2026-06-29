# Refonte lexamt.com · Vague 2 (Produits) · Plan d'implémentation

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development. Contenu rédigé au standard `anthropic-skills:lexa-marketing`, design system `lexa-site/assets/lexa.css`.

**Goal:** Construire les 5 pages produit (Lexa Texte, Documents, Word, API, Writing) sur le socle, selon un gabarit produit commun, avec SEO/GEO complet.

**Architecture:** Site statique. Chaque page = `lexa-site/<slug>/index.html`, charge `/assets/lexa.css`. Nav (méga-menu) et footer recopiés des partials. Héros clairs, CTA secondaire en `.btn-outline`.

**Spec:** `docs/superpowers/specs/2026-06-18-refonte-site-lexamt-design.md` · **Socle + Vague 1 faits.**

---

## Conventions (lire avant)

### Données produit (skill Lexa)
- **Lexa Texte** (`/lexa-texte-traduction-juridique-ia/`) : copier-coller ou saisie directe, traduction en temps réel, préservation du style (gras, italique, souligné), sélection du domaine juridique, instructions personnalisées, score Lexa Quality par segment.
- **Lexa Documents** (`/lexa-document-traduction-juridique/`) : import de fichiers (+30 formats : Word, PDF, Excel, PowerPoint, XLIFF, TXT), préservation parfaite de la mise en page via OCR intégré, traitement par lots, documents jusqu'à 100 pages.
- **Lexa Word** (`/lexa-word-add-on-microsoft-word/`) : plugin Microsoft Word natif (Windows et Mac), traduit tout ou partie sans quitter Word, application des lexiques dans le document, 4,90 € HT/utilisateur/mois.
- **Lexa API** (`/lexa-api-connecteur-juridiques/`) : API REST complète, intégration aux outils existants (LMS, DMS, workflow juridique), webhooks, SLA garantis, haute disponibilité, support technique dédié.
- **Lexa Writing** (`/lexa-writing-redaction-juridique/`, page nouvelle) : reformulation, anonymisation (noms, chiffres), changement de style (formel/informel), résumé automatique. Pour adapter un document selon l'audience ou le contexte.
- Chiffres transverses, sécurité, tarifs, complémentarité : voir le plan Vague 1 (section Conventions, données de référence).

### Gabarit produit commun (ordre des sections)
1. Nav (partial, méga-menu).
2. Hero clair : eyebrow (nom du produit), titre orienté bénéfice, sous-titre, CTA primaire `.btn-emerald` (Essayer gratuitement → `/lexa-tarifs-traduction-juridique/`) + CTA secondaire `.btn-outline` (Demander une démo → `/contact/`).
3. Bloc « En bref » (GEO, 40 à 60 mots).
4. Problème résolu (le pain point du produit).
5. Fonctionnalités clés (3 à 5 cartes, réutiliser composants de cartes du socle).
6. Visuel / mockup du produit (statique ; pour Texte et Documents, un visuel d'interface inspiré du simulateur de l'accueil, sans dépendance JS).
7. Cas d'usage concrets.
8. Specs / points techniques (pour API : webhooks, SLA, formats de réponse, extraits de code).
9. Tarif d'entrée + CTA (renvoi vers Tarifs).
10. FAQ produit (4 à 6 questions) en `<details>`.
11. Cross-sell : 2 ou 3 liens vers les autres produits.
12. CTA final + footer (partial).

### Règles transverses
- Jamais le caractère tiret cadratin (U+2014). Détection : `grep -rl $'\xe2\x80\x94' <chemin> && echo TROUVE || echo OK`.
- Head depuis `_partials/head.html`. Title ~60 car., description ~155. `canonical`/OG/`@id` absolus `https://lexamt.com/<slug>/`.
- Réutiliser les composants/tokens de `lexa.css`. Nouveaux composants seulement si nécessaire, en section commentée en fin de `lexa.css`.
- JSON-LD par page : `@graph` (Organization `@id https://lexamt.com/#organization`, WebSite, WebPage `@id .../<slug>/#webpage`, BreadcrumbList Accueil > Produits > Nom) + `SoftwareApplication` (name, applicationCategory BusinessApplication, operatingSystem adapté, `offers` Offer avec le prix d'entrée pertinent, publisher → organization) + `FAQPage`.
- Pas d'`aggregateRating`. Ton non agressif. Pas de promesse de remplacement du traducteur humain (relecture expert en option).
- Liens internes vers vrais slugs. CTA secondaire `.btn-outline` (héros clairs).

### Vérification par page (rappel)
`grep -rl $'\xe2\x80\x94'` = OK ; JSON-LD parse (python3/node) ; nav (nav-item-mega) + footer ; canonical absolu ; bloc « En bref » présent ; cross-sell présent.

---

## Task 1: Lexa Texte

**Files:** Create `lexa-site/lexa-texte-traduction-juridique-ia/index.html` ; Modify si besoin `lexa-site/assets/lexa.css`.
**Head:** Title `Lexa Texte : traduction juridique en temps réel par IA` ; Desc `Collez votre texte juridique, choisissez le domaine, obtenez une traduction précise en temps réel avec score qualité par segment. Style préservé. Essai gratuit 15 jours.` ; canonical `https://lexamt.com/lexa-texte-traduction-juridique-ia/`.
**Contenu:** gabarit produit avec les données Lexa Texte. SoftwareApplication operatingSystem « Web », offer prix d'entrée 6,90 EUR (plan Essentiel). Cross-sell vers Documents + Word.

- [ ] **Step 1:** `mkdir -p lexa-site/lexa-texte-traduction-juridique-ia` puis créer la page (gabarit produit, contenu skill).
- [ ] **Step 2:** Vérifier (grep tiret cadratin OK, JSON-LD parse, nav/footer, En bref, cross-sell).
- [ ] **Step 3:** Commit : `git add lexa-site/lexa-texte-traduction-juridique-ia/ lexa-site/assets/` ; message `Vague 2: page Lexa Texte`.

## Task 2: Lexa Documents

**Files:** Create `lexa-site/lexa-document-traduction-juridique/index.html` ; Modify si besoin `lexa.css`.
**Head:** Title `Lexa Documents : traduisez vos fichiers juridiques, mise en page intacte` (raccourcir a ~60 si besoin) ; Desc `Importez Word, PDF, Excel, PowerPoint : Lexa traduit jusqu'à 100 pages en préservant parfaitement la mise en page grâce à l'OCR. Traitement par lots. Essai 15 jours.` ; canonical `https://lexamt.com/lexa-document-traduction-juridique/`.
**Contenu:** +30 formats, OCR mise en page, traitement par lots, 100 pages. SoftwareApplication operatingSystem « Web ». Cross-sell vers Texte + Word.

- [ ] **Step 1:** créer le dossier + la page.
- [ ] **Step 2:** vérifier (idem).
- [ ] **Step 3:** Commit : `git add lexa-site/lexa-document-traduction-juridique/ lexa-site/assets/` ; message `Vague 2: page Lexa Documents`.

## Task 3: Lexa Word

**Files:** Create `lexa-site/lexa-word-add-on-microsoft-word/index.html` ; Modify si besoin `lexa.css`.
**Head:** Title `Lexa Word : la traduction juridique directement dans Word` ; Desc `Le plugin Microsoft Word natif (Windows et Mac) qui traduit tout ou partie de vos documents sans quitter Word, lexiques appliqués. Dès 4,90 € HT/mois.` ; canonical `https://lexamt.com/lexa-word-add-on-microsoft-word/`.
**Contenu:** plugin natif Win/Mac, traduire sans quitter Word, lexiques dans le doc, 4,90 €. SoftwareApplication operatingSystem « Windows, macOS », offer 4.90 EUR. Cross-sell vers Texte + Documents.

- [ ] **Step 1:** créer le dossier + la page.
- [ ] **Step 2:** vérifier.
- [ ] **Step 3:** Commit : `git add lexa-site/lexa-word-add-on-microsoft-word/ lexa-site/assets/` ; message `Vague 2: page Lexa Word`.

## Task 4: Lexa API

**Files:** Create `lexa-site/lexa-api-connecteur-juridiques/index.html` ; Modify si besoin `lexa.css`.
**Head:** Title `Lexa API : intégrez la traduction juridique à vos outils` ; Desc `API REST pour intégrer la traduction juridique de Lexa à vos LMS, DMS et workflows. Webhooks, SLA garantis, haute disponibilité, support dédié. Documentation et démo.` ; canonical `https://lexamt.com/lexa-api-connecteur-juridiques/`.
**Contenu:** REST, webhooks, SLA, intégration LMS/DMS/workflow, haute dispo, support dédié. Inclure un bloc « extrait de code » (exemple d'appel API REST en `<pre><code>`, fictif mais réaliste, sans secret). Ton orienté Legal Ops / DSI. CTA primaire « Demander une démo » → `/contact/` (audience Enterprise), secondaire « Voir les tarifs » → Tarifs. SoftwareApplication operatingSystem « Web, API ». Cross-sell vers Documents + Writing.

- [ ] **Step 1:** créer le dossier + la page (avec bloc code stylé ; styles code en section commentée de lexa.css si besoin).
- [ ] **Step 2:** vérifier (le `<pre>` ne contient pas de tiret cadratin).
- [ ] **Step 3:** Commit : `git add lexa-site/lexa-api-connecteur-juridiques/ lexa-site/assets/` ; message `Vague 2: page Lexa API`.

## Task 5: Lexa Writing

**Files:** Create `lexa-site/lexa-writing-redaction-juridique/index.html` ; Modify si besoin `lexa.css`.
**Head:** Title `Lexa Writing : reformuler, anonymiser et résumer vos textes juridiques` (raccourcir a ~60) ; Desc `Le module rédactionnel de Lexa : reformulation, anonymisation des noms et chiffres, changement de style, résumé automatique. Adaptez vos documents juridiques.` ; canonical `https://lexamt.com/lexa-writing-redaction-juridique/`.
**Contenu:** reformulation, anonymisation (noms, chiffres), changement de style (formel/informel), résumé automatique. SoftwareApplication operatingSystem « Web ». Cross-sell vers Texte + Documents.

- [ ] **Step 1:** créer le dossier + la page.
- [ ] **Step 2:** vérifier.
- [ ] **Step 3:** Commit : `git add lexa-site/lexa-writing-redaction-juridique/ lexa-site/assets/` ; message `Vague 2: page Lexa Writing`.

## Task 6: Vérification globale Vague 2

- [ ] **Step 1:** `grep -rl $'\xe2\x80\x94' lexa-site/ && echo TROUVE || echo "OK: 0"`.
- [ ] **Step 2:** Pour les 5 pages : nav=1, footer=1, mega=1 ; JSON-LD parse (SoftwareApplication + Offer + FAQPage + BreadcrumbList) ; canonical absolu ; CTA secondaire lisible (pas `btn-ghost` sur héros clair).
- [ ] **Step 3:** Vérifier que le méga-menu de la nav pointe vers ces 5 pages désormais existantes (liens cohérents).
- [ ] **Step 4:** Captures de preuve (preview 8791) des 5 pages.
- [ ] **Step 5:** Commit de clôture `--allow-empty` : `Vague 2: vérification globale terminée`.

## Definition of done (Vague 2)
- 5 pages produit construites au gabarit commun, design system respecté, contenu standard skill.
- JSON-LD SoftwareApplication + Offer + FAQPage valides ; blocs « En bref » présents.
- Cross-sell entre produits ; méga-menu cohérent.
- 0 tiret cadratin ; canonical/OG absolus.

## Suite
Vague 3 (Personas : Avocats, Directions juridiques, Legal Ops), puis Vague 4 (Ressources : index + gabarit article), Vague 5 (Légal), Vague 6 (sitemap, robots, manifest, 404, contrôle SEO global).
