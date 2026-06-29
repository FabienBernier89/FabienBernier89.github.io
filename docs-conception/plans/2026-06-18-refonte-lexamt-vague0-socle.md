# Refonte lexamt.com · Vague 0 (Socle) · Plan d'implémentation

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extraire le design system de l'accueil dans un socle partagé (`lexa.css`, `lexa.js`, partials head/nav/footer) et rebrancher l'accueil dessus, avec liens internes corrigés vers les vrais slugs.

**Architecture:** Site statique multi-pages. Un dossier `lexa-site/` contient les assets partagés et une page par dossier (folder/index.html pour des URLs propres avec slash final). Le CSS et le JS deviennent des fichiers externes uniques ; chaque page n'embarque que son HTML et ses données structurées JSON-LD spécifiques.

**Tech Stack:** HTML5, CSS3 (variables custom, Montserrat), JavaScript vanilla (IIFE défensive), JSON-LD. Vérification via le serveur de preview (`mcp__Claude_Preview__*`) et grep.

**Spec de référence:** `docs/superpowers/specs/2026-06-18-refonte-site-lexamt-design.md`

**Raffinement vs spec:** la spec listait des fichiers plats `slug.html`. On passe à `slug/index.html` (un dossier par page) pour que les URLs propres avec slash final (`/expertise-lexa/`) résolvent localement ET en production. L'accueil reste `lexa-site/index.html`.

### Note sur la page contact (sortie de la Vague 0)

La spec classait contact en « existant rebranché ». À l'inspection, `lexa-contact.html` partage les mêmes variables CSS que l'accueil mais utilise une autre police (Plus Jakarta Sans + Inter au lieu de Montserrat), possède ses propres composants (formulaire) absents du CSS de l'accueil, n'a ni canonical, ni Open Graph, ni JSON-LD, et son `<title>` contient un tiret cadratin. La rebrancher proprement est donc un portage (fusion de ses styles propres dans `lexa.css` en police unifiée + complétion SEO + correction du titre), pas un simple échange de balises. Pour garder la Vague 0 nette et concrète, contact est traité en première tâche du plan Vague 1, une fois `lexa.css` figé.

---

## Conventions de vérification (lire avant de commencer)

Ce projet est un site statique : le « test » d'une tâche est une vérification observable, pas un test unitaire. Les commandes de vérification standard :

- **Tiret cadratin (doit toujours être 0) :** `grep -rl $'\xe2\x80\x94' lexa-site/ && echo "TROUVE, a corriger" || echo "OK: 0 tiret cadratin"` (on cherche l'octet UTF-8 du caractère pour ne pas le taper).
- **Preview :** démarrer une fois avec `preview_start` (cwd `lexa-site`), puis `preview_eval` / `preview_screenshot`.
- **JSON-LD valide :** `preview_eval` qui `JSON.parse` chaque `script[type="application/ld+json"]`.
- **Pas d'erreur console :** `preview_console_logs` après chargement.

Table de correspondance des liens (ancien → vrai slug), utilisée à la tâche 5 :

| Ancien href | Nouveau href |
|---|---|
| `href="https://lexamt.com"` | `href="/"` |
| `https://lexamt.com/inscription` | `/lexa-tarifs-traduction-juridique/` |
| `https://lexamt.com/contact` | `/contact/` |
| `https://lexamt.com/tarifs` | `/lexa-tarifs-traduction-juridique/` |
| `https://lexamt.com/produit` | `/lexa-traduction-juridique-solution-pro-droit/` |
| `https://lexamt.com/securite` | `/securite-confidentialite-traduction-juridique/` |
| `https://lexamt.com/blog` | `/ressources/` |
| `https://lexamt.com/lexa-texte` | `/lexa-texte-traduction-juridique-ia/` |
| `https://lexamt.com/lexa-documents` | `/lexa-document-traduction-juridique/` |
| `https://lexamt.com/lexa-word` | `/lexa-word-add-on-microsoft-word/` |
| `https://lexamt.com/lexa-api` | `/lexa-api-connecteur-juridiques/` |
| `https://lexamt.com/lexa-writing` | `/lexa-writing-redaction-juridique/` |
| `https://lexamt.com/mentions-legales` | `/conditions-general/` |
| `https://lexamt.com/confidentialite` | `/securite-confidentialite-traduction-juridique/` |
| `https://lexamt.com/cgv` | `/term-and-conditions/` |

ATTENTION : ne jamais faire de remplacement global du domaine (`s|https://lexamt.com|...|`). Cela casserait `canonical`, Open Graph et les `@id` JSON-LD qui doivent rester en URL absolue. Utiliser uniquement les remplacements de chemins précis ci-dessus.

---

## Task 1: Créer l'arborescence du socle

**Files:**
- Create: `lexa-site/`, `lexa-site/assets/`, `lexa-site/assets/img/`, `lexa-site/_partials/`

- [ ] **Step 1: Créer les dossiers**

```bash
cd "/Users/fabienbernier/Claude project"
mkdir -p lexa-site/assets/img lexa-site/_partials
```

- [ ] **Step 2: Vérifier la structure**

Run: `find lexa-site -type d | sort`
Expected:
```
lexa-site
lexa-site/_partials
lexa-site/assets
lexa-site/assets/img
```

---

## Task 2: Extraire le design system dans `assets/lexa.css`

**Files:**
- Create: `lexa-site/assets/lexa.css`
- Source: `lexa-homepage.html:47-532` (bloc `<style>...</style>`)

- [ ] **Step 1: Extraire le contenu CSS (sans les balises style)**

```bash
cd "/Users/fabienbernier/Claude project"
sed -n '48,531p' lexa-homepage.html > lexa-site/assets/lexa.css
```

- [ ] **Step 2: Vérifier l'extraction**

Run: `head -1 lexa-site/assets/lexa.css && echo "---" && grep -c -- "--emerald:#38a06e" lexa-site/assets/lexa.css && wc -l lexa-site/assets/lexa.css`
Expected: la première ligne contient `:root{`, le token emerald est présent (1), le fichier fait environ 484 lignes.

- [ ] **Step 3: Vérifier absence de tiret cadratin**

Run: `grep -l $'\xe2\x80\x94' lexa-site/assets/lexa.css && echo TROUVE || echo "OK: 0"`
Expected: `OK: 0`

- [ ] **Step 4: Commit**

```bash
cd "/Users/fabienbernier/Claude project"
git add lexa-site/assets/lexa.css
git commit -m "Socle: extraction du design system dans lexa.css"
```

---

## Task 3: Extraire le JS dans `assets/lexa.js` et le rendre défensif

**Files:**
- Create: `lexa-site/assets/lexa.js`
- Source: `lexa-homepage.html:1373-1622` (bloc `<script>...</script>`, IIFE du simulateur)

Le JS actuel pilote uniquement le simulateur de l'accueil et déréférence des éléments du DOM sans garde. Sur une page sans simulateur, il planterait. On ajoute un garde-fou en première instruction de l'IIFE : si l'ancre `.demo` est absente, on sort proprement.

- [ ] **Step 1: Extraire le contenu JS (sans les balises script)**

```bash
cd "/Users/fabienbernier/Claude project"
sed -n '1374,1621p' lexa-homepage.html > lexa-site/assets/lexa.js
```

- [ ] **Step 2: Vérifier l'extraction**

Run: `head -1 lexa-site/assets/lexa.js && grep -c "buildLangGrid" lexa-site/assets/lexa.js`
Expected: la première ligne est `(function(){`, `buildLangGrid` est présent.

- [ ] **Step 3: Insérer le garde-fou en tête de l'IIFE**

Avec l'outil Edit sur `lexa-site/assets/lexa.js`, remplacer la première ligne :

old_string:
```
(function(){
```
new_string:
```
(function(){
  // Le simulateur ne s'exécute que sur les pages qui le contiennent.
  if(!document.querySelector(".demo")) return;
```

- [ ] **Step 4: Vérifier le garde-fou**

Run: `sed -n '1,3p' lexa-site/assets/lexa.js`
Expected: ligne 1 `(function(){`, ligne 2 le commentaire, ligne 3 `if(!document.querySelector(".demo")) return;`

- [ ] **Step 5: Commit**

```bash
cd "/Users/fabienbernier/Claude project"
git add lexa-site/assets/lexa.js
git commit -m "Socle: extraction du JS dans lexa.js avec garde-fou .demo"
```

---

## Task 4: Créer les partials de référence (head, nav, footer)

**Files:**
- Create: `lexa-site/_partials/head.html`
- Create: `lexa-site/_partials/nav.html`
- Create: `lexa-site/_partials/footer.html`

Ces fichiers sont la source de vérité maintenue à l'identique, recopiée dans chaque page (pas d'injection JS, pour le SEO). Pour la Vague 0, nav et footer reprennent la structure existante de l'accueil avec les vrais slugs. Le méga-menu Produits sera ajouté en Vague 1 quand les pages produits existeront.

- [ ] **Step 1: Créer `head.html` (gabarit documenté)**

Créer `lexa-site/_partials/head.html` avec :
```html
<!-- GABARIT HEAD COMMUN. Remplacer les variables {{...}} par page.
     {{TITLE}}        title unique, cible ~60 caracteres
     {{DESC}}         meta description ~155 caracteres
     {{CANONICAL}}    URL absolue de la page, ex https://lexamt.com/expertise-lexa/
     {{OG_TITLE}}     titre social accrocheur
     {{OG_DESC}}      description sociale
     {{OG_URL}}       = {{CANONICAL}}
     Les JSON-LD specifiques a la page se placent juste avant </head>. -->
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{TITLE}}</title>
<meta name="description" content="{{DESC}}">
<meta name="author" content="Lexa, propulsé par Legal 230">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<meta name="theme-color" content="#1B3B31">
<meta name="format-detection" content="telephone=no">
<link rel="canonical" href="{{CANONICAL}}">
<link rel="alternate" hreflang="fr-FR" href="{{CANONICAL}}">
<link rel="alternate" hreflang="x-default" href="{{CANONICAL}}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Lexa">
<meta property="og:locale" content="fr_FR">
<meta property="og:url" content="{{OG_URL}}">
<meta property="og:title" content="{{OG_TITLE}}">
<meta property="og:description" content="{{OG_DESC}}">
<meta property="og:image" content="https://lexamt.com/assets/og-lexa.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Lexa, la traduction juridique par IA développée par Legal 230">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{{OG_TITLE}}">
<meta name="twitter:description" content="{{OG_DESC}}">
<meta name="twitter:image" content="https://lexamt.com/assets/og-lexa.jpg">
<link rel="icon" href="https://lexamt.com/favicon.svg" type="image/svg+xml">
<link rel="icon" href="https://lexamt.com/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="https://lexamt.com/apple-touch-icon.png">
<link rel="manifest" href="https://lexamt.com/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/lexa.css">
```

- [ ] **Step 2: Créer `nav.html` à partir de la nav de l'accueil**

Repérer les bornes de la nav puis la copier :
```bash
cd "/Users/fabienbernier/Claude project"
grep -n '<header class="nav">\|</header>' lexa-homepage.html
```
Copier le bloc `<header class="nav">...</header>` dans `lexa-site/_partials/nav.html`, puis appliquer la table de correspondance des liens (section Conventions) avec l'outil Edit. Liens nav finaux : logo → `/`, Solutions → `/lexa-traduction-juridique-solution-pro-droit/`, Expertise → `/expertise-lexa/`, Tarifs → `/lexa-tarifs-traduction-juridique/`, Ressources → `/ressources/`, Contact → `/contact/`, bouton essai → `/lexa-tarifs-traduction-juridique/`, tel inchangé.

- [ ] **Step 3: Créer `footer.html` à partir du footer de l'accueil**

```bash
cd "/Users/fabienbernier/Claude project"
grep -n '<footer class="footer">\|</footer>' lexa-homepage.html
```
Copier le bloc `<footer class="footer">...</footer>` dans `lexa-site/_partials/footer.html`, puis appliquer la table de correspondance des liens (produits, légal, contact) avec l'outil Edit.

- [ ] **Step 4: Vérifier les partials (liens corrects, 0 tiret cadratin)**

Run:
```bash
cd "/Users/fabienbernier/Claude project"
grep -rl $'\xe2\x80\x94' lexa-site/_partials/ && echo "TROUVE, a corriger" || echo "OK: 0 tiret cadratin"
grep -o 'href="[^"]*"' lexa-site/_partials/nav.html lexa-site/_partials/footer.html | sort -u
```
Expected: 0 tiret cadratin ; aucun href interne ne contient `/produit`, `/tarifs`, `/blog`, `/securite`, `/inscription` (tous remplacés par les vrais slugs).

- [ ] **Step 5: Commit**

```bash
cd "/Users/fabienbernier/Claude project"
git add lexa-site/_partials/
git commit -m "Socle: partials head, nav, footer avec vrais slugs"
```

---

## Task 5: Rebrancher l'accueil sur le socle (`lexa-site/index.html`)

**Files:**
- Create: `lexa-site/index.html` (reconstruit depuis `lexa-homepage.html`)

On reconstruit le fichier en remplaçant le bloc `<style>` par un `<link>` et le bloc `<script>` IIFE par un `<script src>`. Les JSON-LD en tête (lignes 535-689) sont conservés tels quels.

- [ ] **Step 1: Reconstruire index.html avec CSS et JS externes**

```bash
cd "/Users/fabienbernier/Claude project"
{ sed -n '1,46p' lexa-homepage.html; \
  echo '<link rel="stylesheet" href="/assets/lexa.css">'; \
  sed -n '533,1372p' lexa-homepage.html; \
  echo '<script src="/assets/lexa.js" defer></script>'; \
  sed -n '1623,$p' lexa-homepage.html; } > lexa-site/index.html
```

- [ ] **Step 2: Vérifier que les blocs inline ont disparu et les externes sont présents**

Run:
```bash
cd "/Users/fabienbernier/Claude project"
grep -c "<style>" lexa-site/index.html
grep -c 'href="/assets/lexa.css"' lexa-site/index.html
grep -c 'src="/assets/lexa.js"' lexa-site/index.html
grep -c "application/ld+json" lexa-site/index.html
```
Expected : `<style>` = 0, lexa.css = 1, lexa.js = 1, JSON-LD = 2 (graph + FAQPage conservés).

- [ ] **Step 3: Corriger les liens internes vers les vrais slugs**

Appliquer la table de correspondance (section Conventions) sur `lexa-site/index.html`. Script de remplacement précis (BSD sed, macOS) :
```bash
cd "/Users/fabienbernier/Claude project"
f=lexa-site/index.html
sed -i '' 's|href="https://lexamt.com/inscription"|href="/lexa-tarifs-traduction-juridique/"|g' "$f"
sed -i '' 's|href="https://lexamt.com/contact"|href="/contact/"|g' "$f"
sed -i '' 's|href="https://lexamt.com/tarifs"|href="/lexa-tarifs-traduction-juridique/"|g' "$f"
sed -i '' 's|href="https://lexamt.com/produit"|href="/lexa-traduction-juridique-solution-pro-droit/"|g' "$f"
sed -i '' 's|href="https://lexamt.com/securite"|href="/securite-confidentialite-traduction-juridique/"|g' "$f"
sed -i '' 's|href="https://lexamt.com/blog"|href="/ressources/"|g' "$f"
sed -i '' 's|href="https://lexamt.com/lexa-texte"|href="/lexa-texte-traduction-juridique-ia/"|g' "$f"
sed -i '' 's|href="https://lexamt.com/lexa-documents"|href="/lexa-document-traduction-juridique/"|g' "$f"
sed -i '' 's|href="https://lexamt.com/lexa-word"|href="/lexa-word-add-on-microsoft-word/"|g' "$f"
sed -i '' 's|href="https://lexamt.com/lexa-api"|href="/lexa-api-connecteur-juridiques/"|g' "$f"
sed -i '' 's|href="https://lexamt.com/lexa-writing"|href="/lexa-writing-redaction-juridique/"|g' "$f"
sed -i '' 's|href="https://lexamt.com/mentions-legales"|href="/conditions-general/"|g' "$f"
sed -i '' 's|href="https://lexamt.com/confidentialite"|href="/securite-confidentialite-traduction-juridique/"|g' "$f"
sed -i '' 's|href="https://lexamt.com/cgv"|href="/term-and-conditions/"|g' "$f"
sed -i '' 's|href="https://lexamt.com"|href="/"|g' "$f"
```

- [ ] **Step 4: Vérifier que canonical et JSON-LD restent absolus**

Run:
```bash
cd "/Users/fabienbernier/Claude project"
grep -o '<link rel="canonical"[^>]*>' lexa-site/index.html
grep -c 'https://lexamt.com/#organization' lexa-site/index.html
```
Expected : canonical = `https://lexamt.com/` (absolu, intact), `@id` organization présent (1). Si l'un est cassé, le remplacement global interdit a été utilisé : revenir au step 1.

- [ ] **Step 5: Démarrer la preview et vérifier le rendu**

Démarrer le serveur de preview avec cwd `lexa-site`. Charger `/`. Puis :
- `preview_console_logs` : aucune erreur JS.
- `preview_screenshot` (viewport desktop 1320) : la page s'affiche identique à l'accueil d'avant (hero vert, dégradé sur « langage juridique », stats, simulateur, sections).
- `preview_eval` : vérifier que le simulateur fonctionne (changer d'onglet `.dtab`, lancer une traduction) et que les 2 JSON-LD parsent.

- [ ] **Step 6: Vérifier liens et tiret cadratin**

Run:
```bash
cd "/Users/fabienbernier/Claude project"
grep -l $'\xe2\x80\x94' lexa-site/index.html && echo TROUVE || echo "OK: 0"
grep -o 'href="/[^"]*"' lexa-site/index.html | sort -u
```
Expected : 0 tiret cadratin ; les href internes pointent tous vers de vrais slugs.

- [ ] **Step 7: Commit**

```bash
cd "/Users/fabienbernier/Claude project"
git add lexa-site/index.html
git commit -m "Socle: accueil rebranché sur lexa.css/lexa.js, liens vers vrais slugs"
```

---

## Task 6: Vérification globale du socle et de l'accueil

**Files:**
- Aucun nouveau fichier. Contrôle final sur `lexa-site/`.

- [ ] **Step 1: Contrôle tiret cadratin sur tout le socle**

Run:
```bash
cd "/Users/fabienbernier/Claude project"
grep -rl $'\xe2\x80\x94' lexa-site/ && echo "TROUVE, a corriger" || echo "OK: 0 tiret cadratin partout"
```
Expected : `OK: 0 tiret cadratin partout`.

- [ ] **Step 2: Contrôle JSON-LD de l'accueil**

Avec `preview_eval` sur `/` : récupérer tous les `script[type="application/ld+json"]`, faire `JSON.parse` sur chacun, confirmer 0 erreur. Attendu : graphe (Organization, WebSite, SoftwareApplication, WebPage) + FAQPage.

- [ ] **Step 3: Contrôle des assets partagés**

Run:
```bash
cd "/Users/fabienbernier/Claude project"
grep -c 'href="/assets/lexa.css"' lexa-site/index.html
grep -c 'src="/assets/lexa.js"' lexa-site/index.html
test -f lexa-site/assets/lexa.css && test -f lexa-site/assets/lexa.js && echo "assets OK"
```
Expected : l'accueil charge le CSS (1) et le JS (1) partagés ; les deux fichiers existent.

- [ ] **Step 4: Capture de preuve**

`preview_screenshot` de `/` en desktop pour archive visuelle. Confirmer le rendu identique à l'avant-refonte.

- [ ] **Step 5: Commit de clôture (si modifications résiduelles)**

```bash
cd "/Users/fabienbernier/Claude project"
git add -A lexa-site/
git commit -m "Socle: vérification globale Vague 0 terminée" --allow-empty
```

---

## Definition of done (Vague 0)

- `lexa-site/assets/lexa.css` et `lexa-site/assets/lexa.js` sont les sources uniques du design system et du simulateur.
- `lexa-site/index.html` (accueil) rend à l'identique de l'avant-refonte, sur les assets partagés, sans erreur console.
- Tous les liens internes de l'accueil pointent vers les vrais slugs ; `canonical`, Open Graph et JSON-LD restent en URL absolue.
- Partials `head.html`, `nav.html`, `footer.html` prêts à servir de référence pour la Vague 1.
- 0 tiret cadratin sur tout `lexa-site/`.
- JSON-LD valide sur l'accueil.

## Suite

Une fois la Vague 0 construite et validée, rédiger le plan de la Vague 1 dans cet ordre :
1. **Unifier et compléter la page contact sur le socle** (première tâche) : fusionner ses composants propres (formulaire) dans `lexa.css` en police Montserrat, recâbler sur les assets partagés, compléter la tête SEO (canonical, Open Graph, JSON-LD `ContactPage`), corriger le tiret cadratin du `<title>`, corriger les liens.
2. **Pages piliers** : Solutions, Expertise, Sécurité, Comparatif, Tarifs, en réutilisant les classes CSS et l'API JS désormais figées.
3. Ajouter le méga-menu Produits dans la nav partagée.
