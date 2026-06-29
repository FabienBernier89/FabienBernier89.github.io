# Refonte complète du site lexamt.com (Lexa) · Design / Spec

Date : 2026-06-18
Statut : validé (brainstorming), prêt pour le plan d'implémentation
Porteur : Fabien Bernier (responsable marketing, Legal 230)

## 1. Contexte et objectif

Refondre l'intégralité des pages marketing du site lexamt.com (Lexa, solution de
traduction juridique par IA développée par Legal 230). La refonte s'appuie sur le
design system déjà validé sur l'accueil et la page contact, et sur l'ensemble des
consignes établies (positionnement, SEO/GEO, typographie). Objectif business :
générer des essais gratuits (15 jours, sans carte bancaire) et des demandes de démo
Enterprise, tout en préservant le ranking Google actuel.

## 2. Décisions validées

- Architecture : CSS + JS partagés (`lexa.css` / `lexa.js`), un HTML léger par page.
- Contenu : refonte complète (positionnement + best practices SEO/GEO), le site
  actuel sert de référence et non de modèle.
- Blog : page index `/ressources/` + un gabarit d'article réutilisable (pas de
  migration de tous les articles pour l'instant).
- Langue : français uniquement pour cette phase (EN traitée plus tard).
- Slugs : on conserve les slugs existants pour préserver le SEO ; on n'optimise que
  les slugs des pages nouvelles.
- Pages ajoutées au périmètre : Comparatif vs DeepL, Sécurité dédiée, Lexa Writing,
  et les 3 pages persona dès cette phase.

## 3. Contraintes et règles non négociables

- Jamais de tiret cadratin (le caractère em dash), ni dans le contenu, ni dans le
  code, ni dans les commentaires. Utiliser « : », « · », la virgule ou le trait
  d'union à la place.
- Tout le contenu en français.
- Standard de rédaction : skill Lexa marketing (top 1% LegalTech B2B SaaS).
- Positionnement : valoriser ce que Lexa fait en plus, ne pas attaquer frontalement
  DeepL / ChatGPT / IA internes. Complémentarité Lexa (self-service) vs Legal 230
  (full-service, assermenté).
- Pas de chiffres ni de cas clients non vérifiés. Pas de note/avis (`aggregateRating`)
  tant que les avis réels nominatifs ne sont pas fournis.
- Préservation des URLs : aucune URL existante changée sans 301.
- Accueil : pas de grille tarifaire (les prix vivent sur la page Tarifs).

## 4. Architecture technique

### Arborescence
```
lexa-site/
  assets/
    lexa.css          design system complet (tokens, base, composants, sections, responsive)
    lexa.js           modules interactifs (simulateurs, grille langues, FAQ, carrousels, nav mobile)
    img/              og-*.jpg, logos cabinets, favicons (placeholders, vrais fichiers fournis par Fabien)
  index.html                                          /
  lexa-traduction-juridique-solution-pro-droit.html   hub Solutions
  traduction-juridique-avocats.html                   persona
  traduction-juridique-directions-juridiques.html     persona
  traduction-juridique-legal-ops.html                 persona
  expertise-lexa.html
  securite-confidentialite-traduction-juridique.html  (new)
  lexa-vs-deepl-traduction-juridique.html             (new, comparatif)
  lexa-tarifs-traduction-juridique.html
  lexa-texte-traduction-juridique-ia.html
  lexa-document-traduction-juridique.html
  lexa-word-add-on-microsoft-word.html
  lexa-api-connecteur-juridiques.html
  lexa-writing-redaction-juridique.html               (new)
  contact.html
  ressources.html
  article-modele.html                                 gabarit blog
  conditions-general.html
  term-and-conditions.html
  _partials/          nav.html, footer.html, head.html (références maintenues à l'identique)
```

### Design system (`lexa.css`)
Source unique de vérité. Extraction du CSS déjà validé de l'accueil : palette
navy / vert foncé / émeraude / sauge, Montserrat, composants (boutons, cartes,
sections alternées, méga-menu, marquee, carrousels). Les pages existantes (accueil,
contact) sont refactorées pour pointer dessus. Une retouche de design = un seul
fichier modifié.

Tokens de référence (déjà en place sur l'accueil) :
`--green:#1B3B31`, `--green-grad`, `--emerald:#38a06e`, `--emerald-d:#2c8459`,
`--sage:#79b399`, `--green-pale:#CDEAD6`, `--navy:#0f3144`, `--ink:#0a2018`,
`--line:#E7ECEA`, `--bg:#F4F8F6`.

### Comportements interactifs (`lexa.js`)
Un seul fichier, chaque page active ce dont elle a besoin : simulateur de traduction
texte, simulateur de traduction document, grille 36 langues, FAQ accordéon, carrousel
d'avis, menu mobile, bascule mensuel/annuel (Tarifs).

### Nav, footer, head
Markup dupliqué dans chaque page (copie identique), pas injecté en JS, pour que les
liens soient dans le HTML (SEO + moteurs IA). Copie de référence dans `_partials/`,
propagée sur toutes les pages à chaque changement. À l'intégration CMS, nav/footer
deviendront un composant unique côté CMS.

### Liens internes et URLs
Liens internes root-relative vers les vrais slugs (maillage SEO, préservation des
URLs). `canonical` et Open Graph en URL absolue. Correction des liens de l'accueil
actuelle qui pointent vers des slugs inventés (`/tarifs`, `/inscription`,
`/securite`). Le lien `/securite` pointe désormais vers la nouvelle page Sécurité.

## 5. Inventaire des pages et slugs

| Famille | Page | Slug | Statut |
|---|---|---|---|
| Existant | Accueil | `/` | rebranché |
| Existant | Contact | `/contact/` | rebranché |
| Pilier | Solutions (hub) | `/lexa-traduction-juridique-solution-pro-droit/` | existant |
| Pilier | Expertise | `/expertise-lexa/` | existant |
| Pilier | Sécurité | `/securite-confidentialite-traduction-juridique/` | new |
| Pilier | Comparatif vs DeepL | `/lexa-vs-deepl-traduction-juridique/` | new |
| Pilier | Tarifs | `/lexa-tarifs-traduction-juridique/` | existant |
| Persona | Avocats & cabinets | `/traduction-juridique-avocats/` | new |
| Persona | Directions juridiques | `/traduction-juridique-directions-juridiques/` | new |
| Persona | Legal Ops & DSI | `/traduction-juridique-legal-ops/` | new |
| Produit | Lexa Texte | `/lexa-texte-traduction-juridique-ia/` | existant |
| Produit | Lexa Documents | `/lexa-document-traduction-juridique/` | existant |
| Produit | Lexa Word | `/lexa-word-add-on-microsoft-word/` | existant |
| Produit | Lexa API | `/lexa-api-connecteur-juridiques/` | existant |
| Produit | Lexa Writing | `/lexa-writing-redaction-juridique/` | new |
| Ressources | Index blog | `/ressources/` | existant |
| Ressources | Gabarit article | (modèle) | new |
| Légal | Conditions générales | `/conditions-general/` | existant |
| Légal | CGU | `/term-and-conditions/` | existant |

## 6. Blueprints par page

### Accueil `/`
Déjà construite. Rebranchée sur le socle (CSS/JS externes), liens internes corrigés.
Structure conservée : nav, hero, stats, démo (texte + document), piliers, produits,
comparaison, sécurité, témoignages, FAQ, CTA final, footer.

### Solutions hub
Hero métiers du droit · promesse globale · routage vers les 3 personas · sections
Notaires et Compliance · cas d'usage transverses · bénéfices chiffrés (50 % délais,
60 % coûts, 99 % précision) · complémentarité Lexa / Legal 230 · témoignages · CTA.

### Personas (Avocats, Directions juridiques, Legal Ops)
Gabarit commun : hero ciblé · bloc « En bref » · douleurs spécifiques du persona ·
réponse Lexa point par point · cas d'usage du métier · objections traitées (DeepL,
IA interne pour Legal Ops) · preuves et chiffres · FAQ persona · CTA essai + démo.

### Expertise
Hero « une IA entraînée exclusivement sur le droit » · bloc « En bref » ·
architecture en 4 étapes (60 M docs, 14 moteurs, terminologie validée, 900+ lexiques
CJUE/OMPI/OIT) · 12 domaines juridiques · 40+ langues · Lexa Quality (score par
segment, relecture expert) · lien vers Sécurité · autorité Legal 230 · FAQ · CTA.

### Sécurité et confidentialité
Hero trust · bloc « En bref » · certifications (ISO 27001, ISO 9001, ISO 20000-1,
STAR CSA, SOC, Cyber Essentials) · chiffrement AES-256 + SSL/TLS · hébergement Europe
· conformité RGPD · rétention (suppression 7 jours) · zéro entraînement sur données
client · NDA / SLA sur demande · FAQ confidentialité · CTA + mention « page envoyable
en appel d'offres ».

### Comparatif vs DeepL
Hero « Ces outils traduisent. Lexa comprend le droit. » · bloc « En bref » · tableau
comparatif (Lexa / DeepL / ChatGPT / Google Translate sur spécialisation juridique,
lexiques, confidentialité, précision, relecture expert, formats) · explication par
critère · objection « on utilise déjà DeepL » traitée · complémentarité possible via
API · FAQ · CTA. Ton : montrer le « en plus », pas dénigrer.

### Tarifs
Hero · bascule mensuel / annuel (-10 %) · 4 plans (Essentiel 6,90 · Standard 23,90 ·
Premium 44,90 · Enterprise sur mesure) + encart Lexa Word 4,90 · tableau comparatif
des fonctionnalités par plan · « inclus dans tous les plans » · bandeau Enterprise
(démo, dès 25 utilisateurs) · FAQ facturation/résiliation/essai · CTA essai gratuit.

### Produits (Texte, Documents, Word, API, Writing)
Gabarit commun : hero produit · problème résolu · fonctionnalités clés · démo ou
visuel · cas d'usage · specs · tarif d'entrée + CTA · FAQ produit · cross-sell.
- Texte : temps réel, préservation du style, domaine, instructions, Lexa Quality.
  Réutilise le simulateur de traduction texte de l'accueil.
- Documents : import +30 formats, OCR mise en page, traitement par lots, 100 pages.
  Réutilise le simulateur document.
- Word : plugin natif Win/Mac, traduire sans quitter Word, lexiques, 4,90 €.
- API : REST, webhooks, SLA, intégration DMS/LMS, extraits de code, haute dispo.
- Writing : reformulation, anonymisation, changement de style, résumé automatique.

### Ressources (index)
Hero · article à la une · grille de cartes filtrable par catégorie · encart
newsletter · CTA.

### Gabarit d'article
Fil d'Ariane · H1 + méta (auteur « Équipe Lexa, propulsée par Legal 230 », date) ·
bloc « En bref » (40-60 mots, IA-ready) · corps H2/H3 (chaque section ouvre par une
réponse directe) · encart Lexa + CTA · FAQ (People Also Ask) · maillage interne
(3-5 liens produit). Optimisé AI Overviews.

### Légal (Conditions générales, CGU)
Gabarit sobre : sommaire ancré + contenu structuré. Design propre, contenu repris.

## 7. Plan SEO / GEO

### Head commun (partial)
Title unique (cible ~60 caractères), meta description ~155, canonical absolu,
Open Graph + Twitter Card, hreflang fr-FR + x-default, robots
(`index, follow, max-image-preview:large, max-snippet:-1`), favicons, theme-color.

### JSON-LD par type de page
- Toutes les pages : `@graph` avec `Organization` + `WebSite` + `WebPage`.
- Pages profondes : `BreadcrumbList`.
- Produits : `SoftwareApplication` + `Offer`.
- Tarifs : `Product` + `AggregateOffer` (les 4 plans en `Offer`).
- Accueil, Expertise, Sécurité, Comparatif, personas, produits : `FAQPage`.
- Gabarit article : `Article` + `FAQPage` + `BreadcrumbList`.
- Contact : `ContactPage`.
- Ressources : `CollectionPage`.
- Pas de `aggregateRating` tant que les avis réels ne sont pas fournis.

### GEO / AI Overviews
Bloc « En bref » (réponse directe 40-60 mots) en tête des pages Expertise, Sécurité,
Comparatif et personas. FAQ structurée partout. Entités nommées explicitement
(lexiques CJUE / OMPI / OIT, ISO 27001, 14 moteurs spécialisés, 60 M de documents).
Tableaux comparatifs lisibles par les LLM.

### Maillage interne (hub-and-spoke)
Solutions → personas. Expertise ↔ Sécurité ↔ Comparatif. Produits en cross-sell.
Tout converge vers Tarifs et l'essai gratuit. Liens contextuels + footer.

### Fichiers techniques (vague finale)
`sitemap.xml` (toutes les URLs réelles + nouvelles), `robots.txt`, `site.webmanifest`,
page `404`. Contrôle SEO global (Rich Results, validité JSON-LD, balises uniques,
0 tiret cadratin).

## 8. Ordre de construction (vagues)

- Vague 0 · Socle : extraire `lexa.css` / `lexa.js` depuis l'accueil, rebrancher
  accueil + contact.
- Vague 1 · Piliers : Solutions, Expertise, Sécurité, Comparatif, Tarifs.
- Vague 2 · Produits : Texte, Documents, Word, API, Writing.
- Vague 3 · Personas : Avocats, Directions juridiques, Legal Ops.
- Vague 4 · Ressources : index + gabarit article.
- Vague 5 · Légal : 2 pages.
- Vague 6 · Finition technique : sitemap, robots, manifest, 404, contrôle SEO global.

## 9. Definition of done (par page)

- Design system respecté (socle partagé, aucun style en dur divergent).
- Responsive vérifié (desktop, tablette, mobile).
- 0 tiret cadratin.
- Head SEO complet (title, description, canonical, OG, Twitter, hreflang, robots).
- JSON-LD présent et valide (parse sans erreur).
- Liens internes corrects (vrais slugs, maillage en place).
- Contenu refondu au standard skill Lexa marketing.
- Vérifié en preview (rendu + absence d'erreurs console).

## 10. Hors périmètre (cette phase)

- Version anglaise `/en/`.
- Migration de tous les articles de blog existants (seul le gabarit est produit).
- Portail applicatif `portail.lexamt.fr`.
- Intégration CMS / WordPress (les fichiers sont des pages statiques prêtes à
  intégrer ou héberger ; l'intégration est une étape ultérieure).

## 11. Assets à fournir et points ouverts

- Logos réels des cabinets (Legal 500) en blanc, taille homogène (Fabien les envoie).
- Avis clients nominatifs validés (pour remplacer les placeholders + activer un jour
  le `aggregateRating`).
- Visuels sociaux et favicons : `/assets/og-lexa.jpg` (1200x630), `/assets/logo-lexa.png`,
  `/favicon.svg`, `/favicon.ico`, `/apple-touch-icon.png`, `/site.webmanifest`.
- Confirmer que Lexa Writing est bien commercialisé (sinon retirer la page).
- Valider les slugs des pages nouvelles (section 5).
