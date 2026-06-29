# Refonte lexamt.com · Vague 8 (Nav 4 onglets + ressources SEO) · Plan

> REQUIRED SUB-SKILL: superpowers:subagent-driven-development. Contenu au standard `anthropic-skills:lexa-marketing`, design system `lexa-site/assets/lexa.css`.

**Goal:** Réorganiser la navigation en 4 onglets (Produits / Solutions / Tarifs / Ressources), inspirée de Tomorro, ranger toutes les pages au bon endroit, et créer 3 ressources SEO (e-book, témoignages, glossaire FR/EN par domaine).

**Spec:** `docs/superpowers/specs/2026-06-18-refonte-site-lexamt-design.md` · Socle + Vagues 1-7 faits.

---

## Conventions

- Jamais le tiret cadratin (U+2014). Détection : `grep -rl $'\xe2\x80\x94' <chemin> && echo TROUVE || echo OK`.
- Head depuis `_partials/head.html`. canonical/OG/`@id` absolus. Nav (NOUVELLE, Task B) + footer recopiés des partials. Héros clairs, CTA secondaire `.btn-outline`.
- Données de référence : voir plan Vague 1.

## Nouvelle architecture de navigation (4 onglets)

1. **Produits** (méga-menu, inchangé) : Lexa Texte, Documents, Word, API, Writing + pied « Voir les tarifs ».
2. **Solutions** (méga-menu 2 colonnes) :
   - Colonne « Par métier » : Avocats, Directions juridiques, Legal Ops & DSI (items avec icônes) + pied « Toutes les solutions » (hub).
   - Colonne « Par domaine du droit » : les 12 domaines (liens compacts, 2 sous-colonnes) + pied « Notre expertise IA » (vers `/expertise-lexa/`).
3. **Tarifs** : lien simple.
4. **Ressources** (méga-menu 2 colonnes) :
   - Colonne « À lire » : Blog & guides (`/ressources/`), Comparatif Lexa vs DeepL, Sécurité & confidentialité (items avec icônes).
   - Colonne « Outils & guides » : E-book, Témoignages clients, Glossaire juridique (items avec icônes).
   - Pied « Toutes les ressources » (vers `/ressources/`).

**Zone CTA droite** : « Connexion » (lien vers `https://portail.lexamt.fr/fr/users/login/?next=/fr/`) + bouton « Essai gratuit 15 j » (vers `/lexa-tarifs-traduction-juridique/`). Le tel et le Contact quittent la barre principale (restent dans le footer ; Contact reste atteignable par les CTA « Demander une démo »).

L'onglet **Expertise** disparaît de la barre : ses 12 domaines passent dans Solutions, la page `/expertise-lexa/` devient le pied « Notre expertise IA ». Comparatif et Sécurité remontent dans Ressources.

---

## Task A : 3 ressources SEO

### A1 · Glossaire juridique FR/EN par domaine → `lexa-site/glossaire-traduction-juridique/index.html`
Head : Title `Glossaire juridique FR / EN par domaine du droit | Lexa` ; Desc ~155 ; canonical `https://lexamt.com/glossaire-traduction-juridique/`.
Contenu : nav · hero (« Le glossaire de la traduction juridique ») · bloc « En bref » · intro courte · 12 sections (une par domaine du droit, dans l'ordre des pages domaine) ; chaque section = un titre de domaine + un tableau de 6 à 8 termes : colonne Terme (FR), colonne Traduction (EN), colonne Définition courte. Termes JUSTES et propres au domaine (ex. sociétés : statuts/articles of association, pacte d'associés/shareholders agreement ; contrats : clause résolutoire/termination clause ; arbitrage : sentence/award, clause compromissoire/arbitration clause ; etc.). · maillage vers la page domaine correspondante depuis chaque section · CTA · footer.
JSON-LD : `@graph` (Organization `@id https://lexamt.com/#organization`, WebSite, WebPage `@id .../glossaire-traduction-juridique/#webpage`, BreadcrumbList Accueil > Ressources > Glossaire) + `DefinedTermSet` optionnel (ou FAQPage). Styles tableau glossaire en section commentée de lexa.css.
Commit : `Vague 8: glossaire juridique FR/EN par domaine`.

### A2 · Témoignages clients → `lexa-site/temoignages-clients/index.html`
Head : Title `Témoignages clients : ils traduisent avec Lexa | Lexa` ; Desc ~155 ; canonical `https://lexamt.com/temoignages-clients/`.
Contenu : nav · hero · bloc chiffres (4,9/5, +500 cabinets, +400 directions juridiques) · grille de témoignages par rôle (réutiliser le format anonymisé par rôle de l'accueil, 6 à 9 cartes ; PAS de noms ni d'entreprises inventés ; commentaire HTML `<!-- temoignages a remplacer par des avis nominatifs valides -->`) · section par profil (avocats / directions juridiques / legal ops) · CTA essai. PAS d'`aggregateRating` (avis non vérifiés). · footer.
JSON-LD : `@graph` (Organization, WebSite, WebPage `@id .../temoignages-clients/#webpage`, BreadcrumbList Accueil > Ressources > Témoignages). Pas de Review/aggregateRating tant que non nominatifs.
Commit : `Vague 8: page témoignages clients (anonymisés, a completer)`.

### A3 · E-book téléchargeable (landing) → `lexa-site/ressources/ebook-traduction-juridique/index.html`
Head : Title `E-book : le guide de la traduction juridique par IA | Lexa` ; Desc ~155 ; canonical `https://lexamt.com/ressources/ebook-traduction-juridique/`.
Contenu : nav · hero landing (titre du guide + sous-titre + visuel/mockup de couverture en CSS) · bloc « Ce que vous allez apprendre » (sommaire en 5-6 points : pourquoi l'IA juridique, précision et lexiques, confidentialité, intégration aux workflows, choisir son outil, checklist) · bénéfices · **formulaire de téléchargement** (champs nom, email pro, société ; bouton « Télécharger le guide » ; formulaire NON fonctionnel, marqué par commentaire ; le PDF `/assets/ebook-lexa-guide.pdf` est un placeholder a fournir, lien `download`) · réassurance (sans engagement) · CTA essai · footer.
JSON-LD : `@graph` (Organization, WebSite, WebPage `@id .../ebook-traduction-juridique/#webpage`, BreadcrumbList Accueil > Ressources > E-book).
Commit : `Vague 8: landing e-book telechargeable`.

Vérif par page : grep tiret cadratin OK ; JSON-LD parse ; nav + footer ; canonical absolu ; « En bref » (glossaire) ; maillage.

## Task B : Nav 4 onglets (méga-menus 2 colonnes)

**Files:** `lexa-site/_partials/nav.html`, `lexa-site/assets/lexa.css`.

- Onglets : Produits (méga-menu produits existant), Solutions (méga-menu 2 colonnes : Par métier + Par domaine), Tarifs (lien), Ressources (méga-menu 2 colonnes : À lire + Outils & guides). Retirer l'onglet Expertise et l'onglet Contact de `.nav-links`.
- CTA droite : « Connexion » (lien portail) + bouton « Essai gratuit 15 j ». Retirer le tel de `.nav-cta`.
- Styles : ajouter un layout panneau multi-colonnes (`.mega-cols` flex, `.mega-col` avec séparateur vertical `border-left`, chaque colonne a `.mega-head` + items + `.mega-foot`). Conserver l'ancrage commun (tous les panneaux ouverts sous Produits, sans décalage) et le style Acolad (badges d'icônes, fond dégradé). Responsive ≤940px : colonnes empilées.
- Icônes : réutiliser celles des produits/personas ; pour Ressources, icônes simples (livre, bouclier, étoile, glossaire/list, e-book/download).

- [ ] B1 : écrire le nouveau `nav.html` (4 onglets, méga-menus 2 colonnes, CTA Connexion + Essai).
- [ ] B2 : styles `.mega-cols` / `.mega-col` dans lexa.css (+ responsive).
- [ ] B3 : vérifier en preview que les 4 onglets et les panneaux 2 colonnes s'ouvrent à la même position, look correct.

## Task C : Propagation + vérification + sitemap

- [ ] Propager le nouveau `nav.html` sur toutes les pages (script Python, regex `<header class="nav">.*?</header>`, + `404.html`).
- [ ] `grep -rl $'\xe2\x80\x94' lexa-site/` = OK.
- [ ] Tous les liens du méga-menu résolvent en 200 (produits, personas, 12 domaines, ressources, 3 nouvelles pages).
- [ ] Ajouter au `sitemap.xml` : glossaire, témoignages, e-book (34 URLs).
- [ ] Captures (Solutions 2 colonnes, Ressources 2 colonnes, glossaire).
- [ ] Commit `Vague 8: nav 4 onglets + propagation + sitemap`.

## Definition of done
- Nav à 4 onglets (Produits / Solutions / Tarifs / Ressources) propagée sur 100 % des pages ; Expertise et Contact retirés de la barre ; CTA Connexion + Essai.
- Méga-menus 2 colonnes (Solutions, Ressources) ancrés à la position Produits, style Acolad.
- 3 ressources créées (glossaire FR/EN par domaine, témoignages anonymisés, landing e-book).
- JSON-LD valides, sitemap à jour, 0 tiret cadratin, tous liens internes en 200.

## À fournir par Fabien
- Le PDF de l'e-book (`/assets/ebook-lexa-guide.pdf`).
- Les témoignages clients nominatifs validés (pour remplacer les anonymisés et activer un jour un `aggregateRating`).
