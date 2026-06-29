# CLAUDE.md · Projet intégration WordPress du site Lexa

Ce fichier est lu automatiquement par Claude Code. Il fixe le cadre du projet. **Respecte-le en priorité.**

## Mission
Intégrer dans WordPress la nouvelle version du site **Lexa** (lexamt.com), livrée comme site statique dans `site-statique/`, **en remplacement de la version actuellement en ligne**, sans perdre le référencement (URLs conservées), avec formulaires branchés sur l'outil CRM existant du client, et un gabarit d'article garantissant le format des futures publications.

## Ordre de lecture obligatoire
1. **`LISEZ-MOI.md`** : contenu et structure du package.
2. **`00-PROMPT-INTEGRATION-WORDPRESS.md`** : le cahier des charges complet (la tâche maître). C'est la référence pas à pas.
3. **`CHARTE-ET-REGLES-LEXA.md`** : règles de marque, de contenu, SEO et accessibilité à respecter.
4. **`site-statique/`** : la source de vérité (balisage, design, contenus, JSON-LD).
5. **`docs-conception/`** : specs et plans (contexte de conception, facultatif).

## Règles non négociables
- **Source de vérité = `site-statique/`.** Tu intègres ce qui existe, tu n'éditorialises pas les contenus, titres, slugs ou métadonnées validés.
- **URLs conservées.** Toute URL aujourd'hui indexée doit répondre au même slug, ou être redirigée en 301. Voir la liste des 83 URLs dans le prompt.
- **Aucun tiret cadratin** (le signe « tiret long ») nulle part, ni dans le contenu, ni dans le code. Utiliser « : », « , », « - » ou « · ».
- **Formulaires : ne rien présumer.** L'outil de réception des leads/deals n'est pas connu d'avance (pas forcément HubSpot). **Demander au client avant de coder.**
- **Accessibilité préservée** : skip-link, `<main id="main">`, attributs ARIA, contrastes, navigation clavier déjà en place.
- **Bloc « En bref »** réservé aux articles de blog uniquement.
- **Marque au masculin** (« Le traducteur ... »), logo texte « Lex » + « a » émeraude conservé, palette et typo via les variables de `site-statique/assets/lexa.css` (ne pas réécrire les couleurs en dur).
- **Ne casse jamais** le JSON-LD, les canoniques, les hreflang, ni le bloc favicons/manifest présents dans chaque page.

En cas de doute sur une URL ou une mécanique : se référer au site actuel + Google Search Console, jamais présumer.
