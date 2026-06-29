# Prompt d'intégration WordPress · nouvelle version du site Lexa (lexamt.com)

> À transmettre tel quel au Claude Code (ou à l'agent / développeur) de l'intégrateur.
> Objectif : remplacer l'actuel site WordPress de Lexa par cette nouvelle version, **sans perdre le SEO**, en gardant les URLs existantes, en branchant les formulaires sur notre CRM, et en garantissant que tous les futurs articles de blog adopteront automatiquement la nouvelle mise en page.

---

## 0. Rôle et mission

Tu es chargé d'intégrer dans **WordPress** une nouvelle version, déjà conçue et validée, du site **Lexa** (lexamt.com · solution de traduction juridique par IA de Legal 230). Cette nouvelle version doit **remplacer la version actuellement en ligne**, page par page, en **conservant les URLs existantes** (le référencement déjà acquis ne doit pas être perdu), et en **créant** les pages nouvelles qui n'existent pas encore.

La mission est réussie quand :
1. Chaque URL aujourd'hui indexée par Google répond toujours (même slug) avec le nouveau contenu, ou est redirigée en 301 vers son équivalent.
2. Les formulaires (contact + e-book) créent bien un « deal » / une entrée dans notre CRM, **avec exactement la mécanique déjà utilisée sur le site actuel**.
3. Tout nouvel article publié dans WordPress hérite automatiquement de la mise en page « article » de cette nouvelle version.
4. robots.txt, sitemap XML, balises SEO/JSON-LD, Google Analytics et Search Console sont opérationnels et vérifiés.
5. Le déploiement applique la redirection 301 demandée et la compression + cache sur les assets.

---

## 1. Source de vérité

La nouvelle version est livrée sous forme d'un **site statique HTML/CSS/JS complet** dans le dossier **`lexa-site/`** (branche git `feature/lexa-site-refonte`). C'est la **référence absolue** pour : le balisage de chaque page, le design system, les contenus, les données structurées JSON-LD, les métadonnées, le sitemap et le robots.txt.

Structure :
- `lexa-site/index.html` + un dossier par page (`<slug>/index.html`) = URLs propres.
- `lexa-site/assets/lexa.css` : design system complet (≈ 4000 lignes, palette vert `#1B3B31` / émeraude `#38a06e`, police **Montserrat**).
- `lexa-site/assets/lexa.js` : nav, simulateurs de démo de l'accueil, onglets (motif ARIA tabs), bascule tarifs mensuel/annuel.
- `lexa-site/assets/lexa-demos.js` : démos embarquées des pages produit (Word / API / Writing).
- `lexa-site/assets/lexa-article.js` + `lexa-articles.js` : bloc « Derniers articles » + registre des articles.
- `lexa-site/favicon.svg`, `favicon.ico`, `favicon-16/32.png`, `apple-touch-icon.png`, `assets/img/icon-*.png`, `site.webmanifest`.
- `lexa-site/assets/og-lexa.jpg` (1200×630, image Open Graph) + `assets/logo-lexa.png` (512×512, logo Organization JSON-LD).
- `lexa-site/assets/ebook-lexa-guide.pdf` : le lead magnet téléchargeable.
- `lexa-site/sitemap.xml`, `lexa-site/robots.txt`.

**Tu n'as pas à réinventer le design ni le contenu : tu portes ce qui existe dans WordPress.**

---

## 1 bis. Prévisualiser la nouvelle version avant toute intégration

Avant de porter quoi que ce soit dans WordPress, ouvre le site complet en local pour tout vérifier (rendu, navigation, démos, contenus, données). Le site est **100 % statique** : il suffit de le servir via un petit serveur HTTP local.

**Important** : les pages référencent les assets en **chemin absolu** (`/assets/…`, `/favicon.svg`). Il faut donc servir le dossier **`site-statique/` comme racine web** : un simple double-clic sur un `.html` (protocole `file://`) ne chargera ni le CSS ni le JS. Une **connexion internet** est nécessaire pour la police Montserrat (Google Fonts).

**Option 1 · Python** (déjà présent sur macOS / Linux, rien à installer) :
```
cd site-statique
python3 -m http.server 8000
```
Puis ouvrir http://localhost:8000/

**Option 2 · Node** :
```
cd site-statique
npx serve .        # ou : npx http-server -p 8000
```

**Option 3 · VS Code** : extension « Live Server », clic droit sur `site-statique/index.html` puis « Open with Live Server ».

Les **URLs propres** fonctionnent telles quelles (chaque page est un `index.html` dans son dossier) : navigation, méga-menus, démos interactives, centre d'aide et téléchargement de l'e-book sont tous testables. Pour **parcourir l'intégralité** des pages, ouvrir **`/plan-du-site/`** (toutes les pages regroupées par section) ou se référer à `sitemap.xml`.

**Partager la prévisualisation avec l'équipe (sans WordPress)** : déposer le dossier `site-statique/` sur un hébergeur statique gratuit (Netlify Drop, Vercel, Cloudflare Pages, GitHub Pages) pour obtenir une URL temporaire de validation. Laisser cette préproduction **non indexable** (robots `Disallow` ou protection par mot de passe pendant la revue).

---

## 2. Principe d'architecture WordPress

Construis un **thème WordPress sur mesure** (theme classique PHP ou theme par blocs FSE, au choix selon l'existant ; privilégie la cohérence avec la stack actuelle de lexamt.com).

Règles structurantes :
- **Mutualise l'en-tête et le pied de page.** Dans la version statique, la nav (avec méga-menus) et le footer sont dupliqués dans chaque page. Dans WordPress, ils deviennent **un seul `header.php` / `footer.php`** (ou template parts FSE), pour qu'une modification se répercute partout. Reprends le balisage exact (`<header class="nav">…</header>` et `<footer class="footer">…</footer>`) et les méga-menus.
- **Enqueue les assets partagés** via `wp_enqueue_style` / `wp_enqueue_script` : `lexa.css`, `lexa.js`, `lexa-demos.js`, `lexa-article.js`, Montserrat (avec le chargement non bloquant déjà en place : `media="print" onload` + repli `<noscript>`), favicons et manifest. Conserve les chemins `/assets/…` à la racine (voir §10 cache).
- **Une page fixe = un gabarit dédié** (Page Template PHP, ou pattern/blocs verrouillés). Ne reconstruis pas chaque page « à la main » dans l'éditeur de façon fragile : le corps unique de chaque page (entre `<main id="main">` et `<footer>`) doit être fidèlement reproduit. Le contenu de ces pages est **statique éditorial** (peu d'édition future attendue), donc des gabarits de thème sont acceptables et plus robustes que du page-builder.
- **Préserve l'accessibilité déjà en place** : le `<a class="skip-link">` après `<body>`, le `<main id="main">`, les `aria-hidden` sur les SVG décoratifs, les `aria-*` des onglets et du méga-menu, les `label for/id`. Ne les retire pas.
- **Conserve le JSON-LD de chaque page** (balises `<script type="application/ld+json">`). Pour les pages fixes, port direct. Pour les articles, génération dynamique (voir §5).
- **Zéro tiret cadratin** : ne jamais utiliser ce signe (le tiret long) dans le contenu ou le code produit ; préférer « : », « , », « - » ou « · ». C'est une règle de marque stricte.

---

## 3. Préservation des URLs et SEO (priorité n°1)

C'est le point le plus sensible. **Aucune URL aujourd'hui indexée ne doit se retrouver en 404.**

Procédure obligatoire :
1. **Établis l'inventaire des URLs actuellement en ligne et indexées** : exporte depuis Google Search Console (rapport Pages / Couverture), le sitemap actuel, et un crawl complet du site live (Screaming Frog ou équivalent).
2. **Compare** cet inventaire à la liste des 83 URLs de la nouvelle version (ci-dessous, et dans `lexa-site/sitemap.xml`).
3. Pour chaque URL **qui existe déjà et est conservée** : la nouvelle page doit répondre **au même slug exact** (même casse, même slash final). Configure les permaliens WordPress en conséquence (slug de page/article identique). Ne laisse pas WordPress préfixer les articles par `/blog/`, `/category/`, une date, etc. si ce n'est pas le format actuel : **reproduis la structure de permaliens du site actuel** (les articles de blog sont aujourd'hui à plat, ex. `/erreur-de-traduction-juridique-cout/`).
4. Pour chaque URL **du site actuel qui n'existe plus** dans la nouvelle version (le cas échéant) : mets une **redirection 301** vers la page équivalente la plus pertinente. Documente chaque redirection dans une table.
5. Pour chaque URL **nouvelle** (créée dans cette refonte, absente du site actuel) : crée la page, ajoute-la au sitemap, pas de redirection nécessaire.
6. **Redirection 301 explicite à mettre en place** (changement de slug volontaire) :
   `/term-and-conditions/` → `/conditions-general/` (301 permanent, niveau serveur).
   La page `/conditions-general/` porte les CGU réelles ; `/mentions-legales/` est une page distincte (nouvelle).

### Liste des 83 URLs de la nouvelle version

À confronter à Search Console pour classer chacune en « conservée » ou « nouvelle » (les slugs produits / personas / domaines / articles reprennent volontairement les slugs réels du site actuel ; les pages marquées **NOUVELLE** sont à créer).

**Pages principales**
- `/` (accueil)
- `/lexa-traduction-juridique-solution-pro-droit/` (hub Solutions)
- `/expertise-lexa/`
- `/fonctionnalites/` · **NOUVELLE probable**
- `/securite-confidentialite-traduction-juridique/`
- `/lexa-vs-deepl-traduction-juridique/`
- `/lexa-tarifs-traduction-juridique/`
- `/contact/`
- `/conditions-general/` (CGU · cible du 301 depuis `/term-and-conditions/`)
- `/mentions-legales/` · **NOUVELLE probable**
- `/plan-du-site/` · **NOUVELLE**

**Produits** : `/lexa-texte-traduction-juridique-ia/`, `/lexa-document-traduction-juridique/`, `/lexa-word-add-on-microsoft-word/`, `/lexa-api-connecteur-juridiques/`, `/lexa-writing-redaction-juridique/`

**Solutions par métier (personas)** : `/traduction-juridique-avocats/`, `/traduction-juridique-directions-juridiques/`, `/traduction-juridique-legal-ops/`

**Domaines du droit (14)** : `/expertise-droit-des-societes/`, `/expertise-droit-commercial/`, `/expertise-droit-de-la-concurrence/` *(NOUVELLE probable)*, `/expertise-droit-penal/` *(NOUVELLE probable)*, `/expertise-droit-des-contrats/`, `/expertise-droit-fiscal/`, `/expertise-propriete-intellectuelle/`, `/expertise-droit-social/`, `/expertise-droit-immobilier/`, `/expertise-banque-et-finance/`, `/expertise-arbitrage-international/`, `/expertise-page-contentieux/`, `/expertise-droit-de-limmigration/`, `/expertise-droit-public/`

**Ressources** : `/ressources/` (hub blog), `/ressources/traduction-juridique-ia-guide/` (guide pilier), `/glossaire-traduction-juridique/`, `/temoignages-clients/`, `/ressources/ebook-traduction-juridique/` (landing e-book)

**Articles de blog (30)** : `/traduction-automatique-dans-un-contentieux/`, `/erreur-de-traduction-juridique-cout/`, `/gain-de-temps-en-traduction-juridique/`, `/traduction-ia-pour-des-documents-juridiques/`, `/alternative-a-chatgpt-traduction-juridique/`, `/ia-generaliste-juridique-traduction-juridique/`, `/faux-equivalents-traduction-juridique-francais-anglais/`, `/alternative-a-gemini-traduction-juridique-ia/`, `/deepl-traduction-juridique-fiable/`, `/cout-de-traduction-juridique/`, `/alternative-deepl-traduction-juridique-avocat/`, `/traduction-automatique-par-ia-tendances-2026/`, `/ia-traduction-juridique-heures-gagnees/`, `/meilleure-alternative-deepl-traduction-juridique-par-ia/`, `/traduction-juridique-par-ia/`, `/comment-bien-aborder-une-traduction-juridique-avec-ia/`, `/traduction-juridique-et-contentieux-international/`, `/les-incoherences-juridiques-dans-un-contrat-avec-lia/`, `/la-traduction-juridique-rgpd-avec-lexa/`, `/lexiques-juridiques-multilingues-dans-votre-quotidien/`, `/traduction-medicale-juridique-par-l-ia/`, `/traduction-juridique-ia-directions-juridiques-avec-ia/`, `/traduction-juridique-dappels-doffres-publics-par-ia/`, `/traduction-juridique-par-lia/`, `/comment-lia-traduit-les-expressions-juridique/`, `/ia-et-raisonnement-juridique-ce-que-lia-peut-comprendre/`, `/traduction-juridique-par-ia-pratique-plus-durable/`, `/lexique-juridique-pour-traduction-juridique-par-ia/`, `/traduction-juridique-de-contrat-par-ia/`, `/traduction-juridique-ia-vs-humaine-que-choisir/`

**Centre d'aide (hub + 14 rubriques, NOUVEAU)** : `/aide/`, `/aide/decouvrir-lexa/`, `/aide/demarrer/`, `/aide/traduire-un-texte/`, `/aide/traduire-un-document/`, `/aide/lexa-writing/`, `/aide/lexa-word/`, `/aide/lexa-api/`, `/aide/lexiques-glossaires/`, `/aide/historique/`, `/aide/qualite-relecture/`, `/aide/securite-confidentialite/`, `/aide/gestion-equipe-licences/`, `/aide/abonnements-facturation/`, `/aide/compte-parametres/`

> ⚠️ Les mentions « NOUVELLE probable » sont à **vérifier** contre Search Console / le site actuel : si l'une de ces URLs existe déjà sous un slug légèrement différent, conserve l'ancien slug ou pose un 301.

---

## 4. Pages fixes → pages WordPress

Pour chaque page listée ci-dessus hors articles de blog : crée une **Page WordPress** (ou un gabarit) au slug exact, qui restitue fidèlement le corps de la page statique correspondante (`lexa-site/<slug>/index.html`).

Points d'attention par famille :
- **Accueil, produits, hub fonctionnalités** : contiennent des **démos interactives** (`.demo`, `.pdemo[data-sim]`, onglets `.dtab[data-panel]`). Conserve le balisage exact et charge `lexa.js` + `lexa-demos.js` pour que les animations et la navigation clavier fonctionnent.
- **Tarifs** : bascule mensuel/annuel gérée par `lexa.js`. Conserve les `data-*` des cartes de prix et le JSON-LD `Product`/`AggregateOffer`.
- **Glossaire** : gros tableau de termes FR/EN + JSON-LD `DefinedTermSet` (85 termes). Restituer tel quel.
- **Centre d'aide** : le hub `/aide/` embarque une **recherche live JS** (index de 158 questions, filtre sans accents) et 14 cartes ; chaque rubrique `/aide/<key>/` est en layout « docs » (sidebar sticky des 14 rubriques + accordéons FAQ + JSON-LD `FAQPage`). Reproduis le JS de recherche et les deep-links `#q-<key>-<i>`. Tu peux modéliser les rubriques en pages ou en CPT, du moment que les URLs et le rendu sont identiques.
- **Pages légales** : CGU réelles sur `/conditions-general/` (texte juridique à reprendre verbatim) ; mentions légales sur `/mentions-legales/`.

---

## 5. Articles de blog → gabarit unique (garantie de format pour le futur)

**Exigence clé du client : tout nouvel article publié plus tard doit automatiquement adopter la mise en page de cette nouvelle version.** C'est donc un **gabarit d'article WordPress** (`single.php` ou template de bloc « single post ») qui pilote le rendu, pas une mise en forme manuelle article par article.

1. **Importe les 30 articles** comme des **Posts WordPress** (titre, slug exact, contenu, extrait, catégorie, date, image si présente). Catégories existantes : *Bonnes pratiques*, *Traduction IA*, *Comparatifs*, *Confidentialité*.
2. **Crée le gabarit `single` d'article** reproduisant exactement la structure de `lexa-site/ressources/traduction-juridique-ia-guide/index.html` et des pages article :
   - héros d'article (titre, méta, fil d'Ariane) ;
   - bloc **« En bref »** en tête (résumé TL;DR · réservé aux articles de blog, **ne jamais l'ajouter sur les autres types de page**) ;
   - styles `.prose` pour le corps (H2 commençant par une réponse directe, listes, encadrés, citations) ;
   - **boutons de partage** Facebook / X / LinkedIn ;
   - bloc **FAQ** (`FAQPage`) ;
   - bloc **« Derniers articles »** : dans WordPress, remplace le registre JS statique par une **requête native `WP_Query`** des articles de la **même catégorie** (en reprenant le balisage `.la-card`), pour que tout nouvel article soit automatiquement pris en compte. Conserve la pondération par rubrique.
   - **JSON-LD généré dynamiquement** depuis les champs du post : `Article` (auteur « Équipe Lexa, propulsée par Legal 230 », datePublished/dateModified), `FAQPage` (depuis un champ répétable ou parsé du contenu), `BreadcrumbList`.
   - **Métadonnées** : `<title>` ≤ 60 caractères, meta description ≤ 155, canonical, Open Graph (`og:image` = `og-lexa.jpg` par défaut ou l'image à la une), Twitter card.
3. **Modèle de rédaction** : fournis dans le back-office un **modèle d'article** (pattern de blocs réutilisable, ou template de contenu, ou article « modèle » dupliquable) qui pré-remplit la structure attendue (En bref, H2 en réponses directes, encart Lexa + CTA essai gratuit, checklist, conclusion + CTA, FAQ, maillage interne 3 à 5 liens). Ainsi les rédacteurs partent toujours du bon squelette.
4. Le **hub `/ressources/`** liste les articles (cartes statiques SEO + filtres de catégorie). En WP, génère la liste via une boucle d'articles, en conservant le rendu des cartes et les filtres.

---

## 5 bis. Pages et ressources annexes (ne rien oublier)

Au-delà des pages « marketing » et des articles, la nouvelle version comporte plusieurs sous-sites et ressources spéciales. **Aucun ne doit être laissé de côté.** Reprends chacun fidèlement depuis `lexa-site/`.

- **Centre d'aide / support `/aide/`** (sous-site complet, 15 pages) : le hub `/aide/` (héro + **moteur de recherche live en JS** indexant 158 questions, filtre insensible aux accents + 14 cartes de rubrique) et les **14 pages rubrique** `/aide/<key>/` en **layout « docs »** (barre latérale sticky des 14 rubriques + accordéons `.faq-item` + **deep-links** `#q-<key>-<i>` qui ouvrent la bonne question). Conserver le JS de recherche, le balisage des accordéons, le JSON-LD `FAQPage` par rubrique et `CollectionPage` sur le hub. Modélisation libre (pages, ou type de contenu dédié), tant que les URLs et le rendu sont identiques.
- **Guide e-book au format PDF** : le fichier `lexa-site/assets/ebook-lexa-guide.pdf` doit être **uploadé et servi à l'URL `/assets/ebook-lexa-guide.pdf`** (avec le cache long du §9). Il est délivré par la landing `/ressources/ebook-traduction-juridique/` **uniquement après une soumission de formulaire valide** (mécanique de gating, voir §6). Vérifier que le lien de téléchargement final pointe bien vers ce chemin.
- **Guide pilier** `/ressources/traduction-juridique-ia-guide/` : longue page éditoriale « guide complet » (ce n'est PAS un article de blog), à intégrer comme **page fixe** dédiée.
- **Glossaire juridique** `/glossaire-traduction-juridique/` : grand tableau de **85 termes FR/EN** + JSON-LD `DefinedTermSet`. Restituer le tableau tel quel.
- **Témoignages clients** `/temoignages-clients/` : page de preuves sociales (les avis nominatifs réels et l'`aggregateRating` seront ajoutés plus tard par Legal 230 ; intégrer la page telle quelle pour l'instant).
- **Plan du site** `/plan-du-site/` : page HTML listant toutes les URLs par section (à tenir à jour si l'arborescence change).
- **Page 404 personnalisée** : reproduire la 404 de la version statique dans le `404.php` (ou template 404) du thème.
- **Favicons, manifest, icônes PWA, image sociale** : servir depuis la racine `/favicon.svg`, `/favicon.ico`, `/favicon-16.png`, `/favicon-32.png`, `/apple-touch-icon.png`, `/site.webmanifest`, `/assets/img/icon-192.png`, `/assets/img/icon-512.png`, `/assets/img/icon-maskable-512.png`, plus `/assets/og-lexa.jpg` (Open Graph) et `/assets/logo-lexa.png` (logo Organization JSON-LD). Conserver le bloc `<head>` d'icônes présent sur chaque page.
- **Scripts interactifs** : `lexa.js` (nav, démos accueil, onglets, bascule tarifs), `lexa-demos.js` (démos produit Word/API/Writing), `lexa-article.js` (+ logique « derniers articles ») à charger là où c'est nécessaire pour que les modules interactifs fonctionnent.
- **robots.txt + sitemap.xml** : voir §7.

---

## 6. Formulaires → CRM (reprendre la mécanique actuelle)

Il y a **2 formulaires** à brancher. La règle est de **réutiliser exactement l'outil et la mécanique déjà en place sur le site actuel lexamt.fr / lexamt.com** pour la réception des demandes et la création des « deals ».

**Étape 1 · Identifier l'outil utilisé (ne rien présumer).** L'outil de réception des formulaires **n'est pas connu d'avance et n'est pas forcément HubSpot**. La première action est donc de **poser explicitement la question à Legal 230 / Lexa** :
> « Quel outil reçoit aujourd'hui les soumissions des formulaires du site et y crée les deals / leads ? (CRM, outil marketing, plugin WordPress de formulaire type Gravity Forms ou Contact Form 7, webhook/endpoint maison, etc.) Comment est-il intégré, et vers quelle destination les demandes arrivent-elles ? »

En complément, **inspecte le site actuel pour confirmer** : balisage des formulaires existants, requêtes réseau émises à la soumission, plugins WordPress actifs. Une fois l'outil confirmé, récupère : le mode d'intégration (embed de formulaire, endpoint/webhook, ou plugin), la destination (pipeline / liste / boîte de réception), le mapping des champs, les notifications internes et le suivi de conversion. **Ne code rien tant que l'outil n'est pas confirmé par le client.**

**Étape 2 · Reproduire à l'identique** sur les nouveaux formulaires, en conservant l'UX de la nouvelle version :

- **Formulaire de contact** (`/contact/`). Champs présents dans le markup (actuellement avec `id`, à mapper aux propriétés CRM) :
  - `ct-nom` (texte) → Nom / Prénom
  - `ct-email` (email) → Email
  - `ct-tel` (tél) → Téléphone
  - `ct-taille` (select) → Taille de la structure
  - `ct-sujet` (select) → Sujet de la demande
  - `ct-besoin` (textarea) → Message / besoin
  - case à cocher **consentement RGPD** (obligatoire, à conserver et à journaliser)
  À la soumission : créer le deal/contact dans le CRM **comme aujourd'hui**, afficher l'état de confirmation, déclencher la notification interne habituelle.

- **Formulaire e-book** (`/ressources/ebook-traduction-juridique/`). Mécanique de lead magnet **gaté** : le bouton du héros pointe vers `#ebook-form` ; **le PDF (`/assets/ebook-lexa-guide.pdf`) ne se télécharge qu'après une soumission valide**, suivie d'un écran de remerciement. Dans le code statique, un placeholder `var LEAD_ENDPOINT = '';` (bloc `<script>` de la page) attend l'endpoint. Remplace cette mécanique par l'intégration CRM réelle (même outil que le contact), **en préservant le gating** : pas de soumission valide → pas de téléchargement. Le lead doit créer un deal/contact taggé « e-book ».

**Contraintes** : respecter le RGPD (consentement, finalité), ne jamais exposer de clé privée côté client, conserver le style visuel des formulaires (carte blanche, focus émeraude). Tester qu'un envoi réel crée bien un deal côté CRM avant la mise en ligne.

---

## 7. robots.txt, sitemap, JSON-LD, métadonnées

- **robots.txt** : le site doit autoriser l'indexation et référencer le sitemap. Cible (équivalent à `lexa-site/robots.txt`) :
  ```
  User-agent: *
  Allow: /

  Sitemap: https://lexamt.com/sitemap.xml
  ```
  Si tu utilises Yoast / Rank Math (sitemap dynamique), assure-toi que l'URL du sitemap déclarée dans robots.txt est la bonne et qu'aucune règle `Disallow` parasite n'est ajoutée. **Vérifie impérativement que l'option WordPress « Demander aux moteurs de recherche de ne pas indexer ce site » (Réglages → Lecture) est DÉSACTIVÉE en production** (cause classique de désindexation après refonte).
- **Sitemap XML** : soit servir/maintenir `sitemap.xml` (83 URLs), soit laisser le SEO plugin le générer ; dans tous les cas il doit couvrir toutes les pages indexables, exclure la 404 et la page de redirection `/term-and-conditions/`, puis être **soumis dans Google Search Console** après mise en ligne.
- **JSON-LD** : conserver/reproduire les données structurées de chaque page (Organization + WebSite globaux, WebPage, BreadcrumbList, plus FAQPage / Product / SoftwareApplication / Article / DefinedTermSet / Service selon les pages). Valider via le test des résultats enrichis Google.
- **Métadonnées** : conserver `<title>`, meta description, canonical, hreflang (`fr-FR` + `x-default`), Open Graph et Twitter de chaque page. Ne pas laisser le SEO plugin écraser des titres/descriptions déjà optimisés (≤ 60 / ≤ 155).

---

## 8. Google Analytics, GTM et Search Console

La version statique livrée **ne contient aucun tag analytics** (volontairement). Il faut **reporter le tracking du site actuel** :
- **Récupère l'ID GA4** (et/ou le conteneur **Google Tag Manager**) déjà utilisé sur lexamt.com, ainsi que la **vérification Google Search Console** (balise meta ou enregistrement DNS).
- Intègre le tag (de préférence via **GTM** unique dans le `header.php`, ou GA4 directement) de façon à charger sur **toutes les pages**.
- Reconduis les **événements / conversions** existants : à minima envoi des formulaires (contact + démo), téléchargement de l'e-book, clics sur les CTA « Essai gratuit » et « Demander une démo ». Reproduis ce qui est déjà suivi sur le site actuel.
- Après mise en ligne : vérifie en temps réel que GA4 reçoit les vues, que les conversions se déclenchent, et **resoumets le sitemap dans Search Console** ; surveille la couverture et les 404 les jours suivants.
- Respecte la **gestion du consentement cookies** déjà en place (CMP) : le tracking non essentiel ne doit se déclencher qu'après consentement.

---

## 9. Performance et déploiement

- **Redirection 301 (serveur)** : `/term-and-conditions/` → `/conditions-general/` (permanent). À placer au niveau serveur (`.htaccess` Apache, `nginx.conf`, ou plugin de redirection fiable), pas seulement en meta-refresh.
- **Compression** : activer **Brotli** (et gzip en repli) sur les réponses textuelles (HTML, CSS, JS, SVG, JSON, XML).
- **Cache des assets** : sur **`/assets/`** (CSS, JS, images, polices, PDF), poser un **cache long** (`Cache-Control: public, max-age=31536000, immutable`, ≈ 1 an). Pour permettre les mises à jour sans purge manuelle, **versionne les assets** (nom de fichier hashé, ou paramètre `?v=` mis à jour à chaque déploiement). Les HTML/pages restent en cache court.
- Conserver le **chargement non bloquant de la police** déjà en place et la **préconnexion** aux domaines de polices.
- Servir le site en **HTTPS** intégral, HTTP/2 ou HTTP/3 si disponible.
- Optimiser les images livrées si besoin (WebP/AVIF en complément), sans casser les références `og:image` (garder un JPG/PNG pour les réseaux sociaux).

---

## 10. À obtenir de Legal 230 / Lexa avant de démarrer

Demande ces éléments (l'agent ne peut pas les inventer) :
1. Accès **WordPress** (admin), hébergement (FTP/SSH, panel) et accès au **dépôt** contenant `lexa-site/`.
2. Export **Google Search Console** des URLs indexées + accès GSC.
3. **L'outil exact qui reçoit les formulaires et crée les deals/leads** sur le site actuel (à confirmer explicitement par Legal 230 : ce n'est pas forcément HubSpot) et ses paramètres d'intégration : mode (embed de formulaire, endpoint/webhook, ou plugin), destination (pipeline / liste / boîte de réception), mapping de champs, notifications.
4. **ID GA4 / conteneur GTM** et méthode de **vérification Search Console** actuels.
5. La **CMP / bannière cookies** en place (ou consigne si à reconduire).
6. Confirmation de la **structure de permaliens** actuelle des articles (pour la reproduire à l'identique).
7. Le **texte juridique des CGU** validé (si différent de celui présent dans `/conditions-general/`).

---

## 11. Checklist de recette avant mise en ligne (go-live)

Travaille d'abord sur un **environnement de préproduction** (staging non indexable : `Disallow` ou HTTP auth pendant les tests, à retirer en prod). Avant bascule :

- [ ] Crawl complet du staging (Screaming Frog) : **0 lien interne cassé**, 0 404, 0 chaîne de redirection.
- [ ] **Diff URLs** : chaque URL indexée du site actuel répond (même slug) ou est 301 → documenté dans une table de redirections.
- [ ] 301 `/term-and-conditions/` → `/conditions-general/` testée (code 301, pas 302).
- [ ] Chaque page fixe est fidèle à la version statique (visuel + balisage + JSON-LD).
- [ ] Gabarit article : un **nouvel article de test** publié hérite bien de toute la mise en page (En bref, prose, partage, FAQ, derniers articles, JSON-LD). Puis supprimé.
- [ ] Formulaire contact : un envoi réel crée le deal dans le CRM + notification + écran de confirmation.
- [ ] Formulaire e-book : pas de soumission valide → pas de PDF ; soumission valide → deal CRM + téléchargement + remerciement.
- [ ] robots.txt correct, indexation autorisée, option « ne pas indexer » désactivée.
- [ ] Sitemap XML complet et accessible.
- [ ] JSON-LD valide (test résultats enrichis) sur un échantillon de chaque type de page.
- [ ] GA4/GTM charge sur toutes les pages ; conversions (formulaires, e-book, CTA) déclenchées ; consentement cookies respecté.
- [ ] Démos interactives (accueil + produits) et onglets fonctionnent, y compris au clavier.
- [ ] Centre d'aide : recherche live, 14 rubriques et deep-links `#q-...` opérationnels.
- [ ] Guide e-book : PDF bien servi à `/assets/ebook-lexa-guide.pdf` et délivré uniquement après soumission valide.
- [ ] Lighthouse (mobile + desktop) : perf, accessibilité, SEO au vert ; Core Web Vitals corrects.
- [ ] Brotli/gzip actif ; cache long sur `/assets/` vérifié (en-têtes de réponse).
- [ ] Favicons + manifest + apple-touch-icon servis depuis la racine.
- [ ] Page 404 personnalisée en place.

Après mise en ligne : resoumettre le sitemap dans Search Console, surveiller la couverture / les 404 / le trafic GA pendant 2 à 4 semaines, garder les redirections en place durablement.

---

## 12. Contraintes de contenu et de marque à respecter

- Ne **pas** modifier les contenus, titres, slugs ou métadonnées validés : tu intègres, tu n'éditorialises pas.
- **Pas de tiret cadratin** nulle part (ne jamais utiliser ce signe).
- Le bloc **« En bref »** est réservé aux **articles de blog** (jamais sur produits / personas / domaines / autres pages).
- Conserver le **logo texte Lexa** actuel (« Lex » + « a » émeraude), la palette et la typo Montserrat.
- Chiffres de marque : ne pas altérer les valeurs présentes (elles sont validées).
- Respecter l'accessibilité déjà intégrée (skip-link, `<main>`, ARIA, contrastes).

---

*Document de référence pour l'intégration. Source de vérité = le dossier `lexa-site/`. En cas de doute sur une URL ou une mécanique, se référer au site actuel et à Search Console plutôt que de présumer.*
