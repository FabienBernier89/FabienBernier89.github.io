# Package d'intégration · nouvelle version du site Lexa (lexamt.com)

Ce package contient **tout le nécessaire** pour que votre intégrateur (et son Claude Code) remplace le site Lexa actuel par la nouvelle version, sans perdre le référencement.

## Contenu du package

```
lexa-package-integration/
├── CLAUDE.md                          ← Règles du projet, lues automatiquement par Claude Code
├── LISEZ-MOI.md                       ← Ce fichier
├── 00-PROMPT-INTEGRATION-WORDPRESS.md ← LE cahier des charges complet (tâche maître, à lire en 1er)
├── CHARTE-ET-REGLES-LEXA.md           ← Identité de marque + règles contenu / SEO / accessibilité
├── site-statique/                     ← LA SOURCE DE VÉRITÉ : tout le site, prêt à porter
│   ├── index.html + 1 dossier par page (slug)/index.html   (88 pages HTML)
│   ├── assets/   (lexa.css, lexa.js, lexa-demos.js, lexa-article.js, images,
│   │              og-lexa.jpg, logo-lexa.png, ebook-lexa-guide.pdf, favicons…)
│   ├── _partials/  (en-tête / nav / pied de page de référence)
│   ├── _build/     (sources régénérables : e-book HTML, JSON de contenu, scripts de rendu)
│   ├── gen_*.py    (générateurs : articles de blog, centre d'aide, plan du site)
│   ├── sitemap.xml, robots.txt, site.webmanifest, 404.html, favicon.*
│   └── INTEGRATION-WORDPRESS.md  (copie du cahier des charges, embarquée avec le site)
└── docs-conception/                   ← Specs et plans de conception (contexte, facultatif)
    ├── specs/   (document de design de la refonte)
    └── plans/   (plans d'implémentation par vague)
```

## Par où commencer (pour l'intégrateur)

1. Ouvrir ce dossier avec **Claude Code** : le fichier `CLAUDE.md` est chargé automatiquement.
2. Lire **`00-PROMPT-INTEGRATION-WORDPRESS.md`** de bout en bout : c'est le plan d'action complet (architecture, préservation des URLs, formulaires, gabarit d'article, robots/SEO, Google Analytics, déploiement, recette).
3. Garder **`CHARTE-ET-REGLES-LEXA.md`** sous la main pour les règles de marque et de contenu.
4. Traiter **`site-statique/`** comme la référence absolue du balisage, du design, des contenus et des données structurées.

## Points qui demandent une info de votre part (Legal 230 / Lexa)

Le prompt les détaille (§10), mais en résumé l'intégrateur aura besoin de :
- les accès WordPress + hébergement + dépôt ;
- l'export Google Search Console des URLs indexées ;
- **l'outil exact qui reçoit aujourd'hui les formulaires et crée les deals/leads** (à confirmer : ce n'est pas forcément HubSpot) ;
- l'ID Google Analytics / GTM et la vérification Search Console actuels ;
- la bannière cookies (CMP) en place ;
- la structure de permaliens actuelle des articles.

## Rappels critiques

- **Conserver les URLs existantes** (référencement). 301 uniquement où un slug change (`/term-and-conditions/` → `/conditions-general/`).
- **Créer les pages nouvelles** absentes du site actuel (centre d'aide, fonctionnalités, plan du site, etc. : voir la liste des 83 URLs dans le prompt).
- **Formulaires** : reprendre exactement la mécanique CRM existante, après l'avoir confirmée avec nous.
- **Futurs articles** : un gabarit unique garantit qu'ils adoptent automatiquement la mise en page.
- **Aucun tiret cadratin** (signe « tiret long ») nulle part.

---

*Préparé pour Legal 230 / Lexa. Source de vérité : `site-statique/`.*
