# Charte et règles · site Lexa (référence pour l'intégration et les contenus futurs)

Ce document résume l'identité de marque et les règles à respecter pendant l'intégration WordPress, **et** pour toute édition ou rédaction future (articles, pages). La **source de vérité technique** reste le code de `site-statique/` (notamment `assets/lexa.css` pour les valeurs exactes de couleurs et de typo).

---

## 1. Identité de marque

- **Nom** : Lexa · **Site** : lexamt.com
- **Éditeur** : Legal 230 (1re agence européenne de traduction juridique) · à mentionner comme gage de crédibilité.
- **Tagline officielle** : « Le traducteur qui parle votre langage juridique. »
- **Genre de la marque : MASCULIN** (« Le traducteur … »). Ne jamais accorder Lexa au féminin.
- **Positionnement** : solution SaaS de traduction juridique par IA, pour les professionnels du droit.
- **Adresse** : 75 Boulevard Haussmann, 75008 Paris · **Contact commercial** : contact@lexamt.com, +33 1 84 80 21 20 · **Support** : support@lexamt.com.

### Lexa vs Legal 230 (complémentarité)
- **Lexa** : self-service, abonnement, traduction quotidienne instantanée, non certifiée.
- **Legal 230** : full-service, sur devis, traductions assermentées / dossiers complexes.
- Message : « Lexa pour traduire au quotidien en autonomie. Legal 230 quand la traduction engage votre responsabilité. »

---

## 2. Chiffres clés autorisés (ne pas inventer ni modifier)

+500 cabinets d'avocats clients · +400 directions juridiques clientes · 4,9/5 de satisfaction · 50 % de délais en moins · 60 % de coûts en moins · 99 % de précision juridique · +40 langues · +900 lexiques officiels intégrés (CJUE, OMPI, OIT…) · 60 millions de documents juridiques d'entraînement · 14 moteurs spécialisés par domaine · essai gratuit 15 jours sans carte bancaire.

> Les valeurs déjà présentes dans les pages sont validées. Ne pas les altérer. Ne pas afficher de chiffres non vérifiés.

---

## 3. Charte graphique

Les **valeurs exactes** sont dans `site-statique/assets/lexa.css` (variables CSS). Utiliser ces variables, ne pas coder les couleurs en dur.

- **Palette implémentée** : vert foncé `--green` (#1B3B31, couleur signature), vert émeraude `--emerald` (#38a06e, CTA/accents), émeraude foncé `--emerald-d` (#2c8459, contraste AA), bleu marine `--navy` (#0f3144), fonds clairs `--bg`/`--bg-2`, blanc.
- **Typographie** : **Montserrat** (Google Fonts), chargée en non bloquant (`media="print" onload` + repli `<noscript>`). Conserver ce mode de chargement.
- **Logo** : wordmark texte « Lex » (vert foncé) + « a » (émeraude). À conserver tel quel. Fichiers : `assets/logo-lexa.png` (512×512, logo Organization), `favicon.svg` et déclinaisons.
- **Image sociale** : `assets/og-lexa.jpg` (1200×630). `logo-lexa.png` et `og-lexa.jpg` sont des visuels de marque propres, remplaçables par des versions designées plus tard.
- **Règles visuelles** : coins arrondis (cartes 8px, boutons 6px), espaces blancs généreux, style SaaS épuré, max 3 couleurs par visuel.

---

## 4. Produits (pour mémoire)

- **Lexa Texte** : traduction temps réel par copier-coller, score qualité par segment.
- **Lexa Documents** : import de fichiers (+30 formats), mise en page préservée (OCR), traitement par lots.
- **Lexa Word** : module Microsoft Word natif.
- **Lexa API** : API REST, webhooks, SLA.
- **Lexa Writing** (« Personnaliser » dans l'app) : reformulation, anonymisation, résumé, changement de style.

Sécurité (argument central) : ISO 27001/9001/20000-1, SOC, chiffrement AES-256, hébergement Europe, RGPD, données supprimées après une période de rétention configurable, aucune donnée client utilisée pour l'entraînement.

---

## 5. Règles de contenu

- **Bloc « En bref »** (résumé TL;DR en tête) : **uniquement sur les articles de blog**. Jamais sur les pages produit, persona, domaine, ou autres.
- **Aucun tiret cadratin** (signe « tiret long ») : ni dans le contenu, ni dans le code. Remplacer par « : », « , », « - » ou « · ».
- **Français accentué** correct partout.
- **Ton** : expert et concret pour les juristes ; moderne et orienté performance pour les profils Legal Ops / DSI. Jamais agressif. Valoriser ce que Lexa fait en plus, sans attaquer frontalement les concurrents (DeepL, ChatGPT, etc.).
- **Structure d'article SEO** (à respecter pour les futurs articles, voir le gabarit `single`) : En bref → introduction → H2/H3 (chaque section démarre par une réponse directe) → encart Lexa + CTA essai gratuit → checklist → conclusion + CTA → FAQ (4 à 6 questions) → maillage interne (3 à 5 liens).
- **CTA principaux** : « Essayez Lexa gratuitement pendant 15 jours » et « Demandez une démonstration ».

---

## 6. Règles SEO (préservation du référencement acquis)

- **Conserver les URLs** : même slug pour toute page déjà indexée ; 301 si un slug change (cas explicite : `/term-and-conditions/` → `/conditions-general/`).
- **Reproduire la structure de permaliens actuelle** (les articles de blog sont à plat, ex. `/erreur-de-traduction-juridique-cout/`, sans préfixe `/blog/` ni date).
- **Conserver** : `<title>` (≤ 60 car.), meta description (≤ 155 car.), canonical, hreflang `fr-FR` + `x-default`, Open Graph, Twitter card, et le **JSON-LD** de chaque page.
- **Sitemap** complet soumis à Search Console ; **robots.txt** autorisant l'indexation ; vérifier que l'option WordPress « ne pas indexer » est désactivée en production.

---

## 7. Règles d'accessibilité (déjà intégrées, à préserver)

- `<a class="skip-link">` juste après `<body>`, `<main id="main">` autour du contenu principal.
- `aria-hidden="true"` sur les SVG décoratifs.
- Onglets de démo au motif ARIA tabs (rôles + navigation clavier) ; méga-menu avec `<button>` + `aria-haspopup` + ouverture au clavier via `:focus-within`.
- Labels `for`/`id` sur les champs de formulaire ; contrastes conformes (CTA en `--emerald-d`).
- Menu mobile en `<details>` sous 940px.

Ne retire aucun de ces éléments lors du portage en thème.

---

## 8. Règle d'or de l'intégration

**Tu intègres, tu n'éditorialises pas.** Le contenu, les chiffres, les slugs et les métadonnées sont validés. En cas de doute, se référer au site actuel et à Google Search Console plutôt que de présumer.
