# Mises à jour à intégrer dans le skill « lexa-marketing »

Deux blocs prêts à coller : **(A)** une nouvelle section « SITE INTERNET », **(B)** une charte graphique complétée et exacte (valeurs tirées du code du site), réutilisable pour tout document commercial ou marketing.

> Note de cohérence à arbitrer : le skill mentionnait le vert foncé `#063b1c` comme couleur principale. La nouvelle version du site utilise en réalité **`#1B3B31`** comme vert signature (plus profond, légèrement bleuté). Pour l'homogénéité marque (site + documents), il est recommandé d'adopter la palette du site ci-dessous comme référence unique. Conserver `#063b1c` uniquement si un usage historique l'impose.

---

# (A) Nouvelle section à ajouter : `## SITE INTERNET (lexamt.com)`

## SITE INTERNET (lexamt.com)

Le site lexamt.com a été entièrement refondu (nouvelle version 2026). Toute production web (page, article, landing) doit s'inscrire dans ce cadre.

### Principes
- **Un type de page = un gabarit distinct.** Ne jamais réutiliser le template d'une famille pour une autre. On bannit la répétition de « grilles de cartes à icône » d'une page à l'autre.
- **On vend l'usage, pas une liste de fonctions.** Chaque page met en scène le bénéfice concret et, quand c'est possible, montre le produit en action.
- **SEO et GEO au niveau top 1 %** dès la conception (voir règles ci-dessous).
- **Marque au masculin** (« Le traducteur … »). **Jamais de tiret cadratin** (utiliser « : », « , », « - », « · »). Français accentué correct.

### Familles de pages
- **Accueil** : héros centré sur fond vert dégradé avec halo lumineux, démo interactive, barre de confiance, chiffres clés, piliers.
- **Hub Solutions** + **Expertise Lexa** (autorité, architecture IA en 4 étapes) + **Fonctionnalités** (hub groupé par usage : traduire / spécialiser / rédiger / intégrer et piloter, avec aperçu du tableau de bord de suivi et du score Lexa Quality).
- **5 pages produit** (Lexa Texte, Documents, Word, API, Writing) : héros clair + **démo interactive embarquée** propre à chaque produit + cas d'usage + tableau de caractéristiques.
- **3 pages métier (personas)** : avocats, directions juridiques, Legal Ops & DSI (panneaux « sans outil / avec Lexa » + scénarios).
- **14 pages de domaine du droit** : terminologie FR/EN dédiée + scénarios + maillage.
- **Réassurance / conversion** : Sécurité et confidentialité (mur de certifications), Comparatif vs DeepL (grand tableau), Tarifs (bascule mensuel / annuel).
- **Ressources** : blog (30 articles optimisés), **glossaire juridique FR/EN**, **e-book** téléchargeable (lead magnet gaté par formulaire), **centre d'aide** (hub + 14 rubriques + recherche).
- **Légales** + **plan du site** + **404**.

### Patterns d'interface réutilisables
Héros centré (fond foncé) ou « split » (produit) ; méga-menus à carte vedette ; bandeau de chiffres sur carte vert foncé ; sections en zigzag texte + visuel ; étapes numérotées ; cas d'usage sur fond vert foncé ; tableaux de specs et de terminologie ; comparatifs « sans / avec » ; mur de badges de certification ; cartes éditoriales cliquables ; **mockups en CSS** (fenêtre d'app, ruban Word, bloc de code API, panneaux bilingues, tableau de bord avec donut de consommation).

### Règles éditoriales web
- **Bloc « En bref »** (résumé TL;DR en tête) : **uniquement sur les articles de blog**. Jamais sur produits / personas / domaines / autres pages.
- **Structure d'article SEO** (ordre) : En bref → introduction (problème terrain) → H2/H3 (chaque section démarre par une réponse directe) → encart Lexa + CTA essai gratuit → checklist / actions → conclusion + CTA → FAQ (4 à 6 questions) → maillage interne (3 à 5 liens).
- **CTA** : « Essayez Lexa gratuitement pendant 15 jours » (principal) et « Demandez une démonstration » (Enterprise / équipe).

### SEO / GEO et technique
- **Préserver les URLs existantes** : ne jamais changer un slug indexé sans redirection 301.
- **Données structurées JSON-LD** par type (Organization, WebSite, WebPage, BreadcrumbList, FAQPage, Product, SoftwareApplication, Article, DefinedTermSet, Service).
- **Métadonnées** : title ≤ 60 caractères, meta description ≤ 155, canonical, hreflang, Open Graph / Twitter.
- **Fils d'Ariane** visuels + maillage interne systématiques.
- **Accessibilité** : skip-link, `<main>`, ARIA, contrastes conformes (CTA en émeraude foncé), navigation clavier, menu mobile.
- **Performance** : police Montserrat en chargement non bloquant, assets en cache long.
- **Intégration** : site porté sous WordPress ; formulaires branchés sur l'outil CRM existant ; gabarit d'article unique garantissant le format des futures publications.

---

# (B) Charte graphique à mettre à jour : `## CHARTE GRAPHIQUE LEXA`

(Remplace / complète la section existante. Valeurs exactes issues du design system du site, réutilisables pour slides, PDF, one-pagers, visuels sociaux.)

## CHARTE GRAPHIQUE LEXA

### Palette (référence unique, site + documents)
| Rôle | Nom | Hex |
|------|-----|-----|
| Vert signature (fonds foncés, structurant) | green | **#1B3B31** |
| Variantes de vert foncé | green-2 / green-3 | #224a3e / #2a5849 |
| Dégradé héros foncé | green-grad | `linear-gradient(152deg,#21463a,#1B3B31,#16302a)` |
| Vert pâle (aplats doux) | green-pale | #CDEAD6 |
| **Émeraude (accent, highlights, hover CTA)** | emerald | **#38a06e** |
| **Émeraude foncé (CTA, contraste AA sur blanc, eyebrow)** | emerald-d | **#2c8459** |
| Vert sauge (accent secondaire, eyebrow sur fond foncé) | sage | #79b399 |
| Bleu marine (titres alternatifs) | navy | #0f3144 |
| Encre (titres) | ink | #0a2018 |
| Texte courant | text | #3b4a48 |
| Texte secondaire | muted | #6c7a76 |
| Filets / bordures | line | #E7ECEA |
| Fonds clairs alternés | bg / bg-2 | #F4F8F6 / #EDF3F0 |
| Menthe / blanc | mint / white | #E8F5EF / #ffffff |

Règles couleur : **max 3 couleurs par visuel**. Vert signature #1B3B31 en fond structurant ; émeraude #38a06e pour accents et CTA ; sauge en secondaire. Sur fond foncé, l'eyebrow et les accents passent en sauge ; le CTA principal reste en émeraude foncé pour le contraste.

### Typographie
- **Police unique : Montserrat** (Google Fonts), poids 400 / 500 / 600 / 700 / 800. Repli `system-ui, sans-serif`.
- **Titres** : graisse 700-800, interlettrage serré (`-.03em`), grands. H1 ≈ 34 à 56 px (large mobile-first), H2 ≈ 28 à 46 px, H3 ≈ 18 à 32 px selon le contexte.
- **Eyebrow** (sur-titre) : 12 px, graisse 700, MAJUSCULES, interlettrage `.14em`, couleur émeraude foncé (ou sauge sur fond foncé).
- **Chapô / lead** : ≈ 18 px, interligne 1,6.
- **Corps** : interligne 1,6, couleur #3b4a48.

### Logo
Wordmark texte **« Lex » en vert signature + « a » en émeraude** (#38a06e), ou tout blanc sur fond vert foncé. Fichiers : `assets/logo-lexa.png` (512×512, logo officiel), `favicon.svg`. Image sociale par défaut : `assets/og-lexa.jpg` (1200×630, fond vert dégradé + wordmark + tagline).

### Mise en page et composants
- **Largeur de contenu** : 1200 px, marges latérales 28 px. **Espaces blancs généreux**, alternance de fonds (blanc / #F4F8F6 / vert foncé).
- **Coins arrondis** : cartes et blocs **8 px**, boutons et pilules **6 px**, cercles 50 %. Style SaaS épuré.
- **Ombres** : douces, longues, teintées vert, ex. `0 30px 60px -28px rgba(6,59,28,.20)`. Jamais d'ombre dure et grise.
- **Boutons** :
  - *CTA principal* : fond émeraude foncé #2c8459, texte blanc, radius 6 px, graisse 600.
  - *CTA secondaire (fond clair)* : contour fin, texte encre.
  - *CTA secondaire (fond foncé)* : contour blanc translucide, texte blanc.
- **Icônes** : style **duotone à trait fin** (badge doux gris-vert sans bordure, tracé foncé + un accent émeraude), façon jeu d'icônes linéaire.
- **Imagerie** : interface produit, documents juridiques / contrats, langues et globe, sécurité numérique, IA, productivité.

### Les 5 mockups produit (comment les représenter dans un visuel)
Chaque produit a une métaphore visuelle propre, à réutiliser telle quelle dans les slides, fiches produit et posts (fenêtre d'app épurée, coins arrondis 8 px, ombre verte douce, accents émeraude).

- **Lexa Texte** : interface à **deux panneaux bilingues côte à côte** (source FR à gauche, cible EN à droite) dans une fenêtre d'app ; la traduction se construit **segment par segment en temps réel**, avec un petit indicateur de **score qualité** par segment et un sélecteur de domaine du droit. Accent émeraude sur le segment actif.
- **Lexa Documents** : fenêtre d'app montrant un **document importé avec sa mise en page préservée** (titres, tableaux), une **rangée de badges de formats** (Word, PDF, Excel, PowerPoint…), une **file de traitement par lots** avec barre de progression, et une comparaison **avant / après**. Idée maîtresse : la fidélité de mise en page.
- **Lexa Word** : **vraie fenêtre Microsoft Word** stylisée (barre de titre + ruban) avec un **onglet « Lexa »** dédié et un **volet complément** ancré à droite ; un paragraphe juridique **traduit en place** (FR vers EN, surligné vert), le reste du texte laissé en FR. Idée maîtresse : « sans quitter Word ».
- **Lexa API** : **fenêtre de code** sur fond sombre (pastilles rouge / jaune / vert en haut) affichant une **requête REST** (POST) et la **réponse JSON**, avec mention webhooks et SLA. Idée maîtresse : intégration dans les outils existants.
- **Lexa Writing** (« Personnaliser ») : présentation **horizontale « avant / après »** (texte source à gauche, version transformée à droite) illustrant l'**anonymisation** (noms et chiffres surlignés), la reformulation, le changement de style ou le résumé. Idée maîtresse : adapter le texte selon l'audience.

### Réutilisation pour documents commerciaux et marketing
- **Slides / PDF** : couverture et slides structurantes sur fond vert signature #1B3B31 (ou dégradé héros) ; slides de contenu sur fond clair ; émeraude réservé aux accents et CTA. Aligne-toi sur les règles carrousel déjà définies (pattern interrupt émeraude, jamais le doré de Legal 230).
- **One-pagers / fiches produit** : héros foncé + chiffres clés en bandeau + sections claires ; Montserrat partout ; arrondis 8 px ; ombres vertes douces.
- **Cohérence** : reprendre les hex exacts ci-dessus, la typo Montserrat, le logo « Lex » + « a » émeraude. Max 3 couleurs. Pas de tiret cadratin. Marque au masculin. Chiffres clés uniquement parmi les valeurs autorisées de la section CHIFFRES CLÉS.
