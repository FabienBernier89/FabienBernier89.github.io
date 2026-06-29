# Lexa : nouvelle version du site (preview + package d'intégration)

Ce dépôt héberge la **nouvelle version du site lexamt.com** (refonte 2026) pour revue par les équipes **avant intégration dans WordPress**, ainsi que tout le package d'intégration.

## Rendu en ligne

Une fois le déploiement GitHub Pages terminé, le site complet est visible ici :

**https://fabienbernier89.github.io/**

> Aperçu de pré-production. L'indexation par les moteurs de recherche est volontairement bloquée (`robots.txt` en `Disallow`) pour ne pas créer de doublon SEO avec lexamt.com. Ne pas diffuser publiquement cette URL au-delà des équipes concernées.

Pour parcourir toutes les pages, ouvrir la page **/plan-du-site/** une fois en ligne.

## Contenu du dépôt

- `site-statique/` : la source de vérité (toutes les pages HTML, CSS/JS, images, PDF, favicons).
- `00-PROMPT-INTEGRATION-WORDPRESS.md` : le cahier des charges d'intégration WordPress.
- `CHARTE-ET-REGLES-LEXA.md` : charte graphique et règles de marque / contenu / SEO / accessibilité.
- `CLAUDE.md` : règles du projet (lues automatiquement par Claude Code).
- `LISEZ-MOI.md` : manifeste détaillé du package.
- `docs-conception/` : specs et plans de conception.

## Prévisualiser en local (sans attendre Pages)

```
cd site-statique
python3 -m http.server 8000
```
Puis ouvrir http://localhost:8000/
