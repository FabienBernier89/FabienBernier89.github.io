# Lexa : nouvelle version du site (preview + package d'intégration)

Ce dépôt héberge la **nouvelle version du site lexamt.com** (refonte 2026) pour revue par les équipes **avant intégration dans WordPress**, ainsi que les documents d'intégration.

## Rendu en ligne

Le site complet est visible ici :

**https://fabienbernier89.github.io/**

> Aperçu de pré-production. L'indexation par les moteurs de recherche est volontairement bloquée (`robots.txt` en `Disallow`) pour ne pas créer de doublon SEO avec lexamt.com. Ne pas diffuser publiquement cette URL au-delà des équipes concernées.

Pour parcourir toutes les pages, ouvrir la page **/plan-du-site/** une fois en ligne.

## Contenu du dépôt

- `site-statique/` : la source de vérité (toutes les pages HTML, CSS/JS, images, PDF, favicons).
- `00-PROMPT-INTEGRATION-WORDPRESS.md` : le cahier des charges d'intégration WordPress.
- `CHARTE-ET-REGLES-LEXA.md` : charte graphique et règles de marque / contenu / SEO / accessibilité.
- `CLAUDE.md` : règles du projet (lues automatiquement par Claude Code).
- `LISEZ-MOI.md` : manuel du dépôt.

> Les coulisses (specs et plans de conception, scripts générateurs, sources de build, doc de mise à jour du skill marketing) ne figurent pas dans ce dépôt public ; elles sont fournies dans le package complet remis séparément.

## Prévisualiser en local

```
cd site-statique
python3 -m http.server 8000
```
Puis ouvrir http://localhost:8000/
