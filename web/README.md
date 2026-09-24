# Site Gilles Gambini — Astro + Tailwind

Nouveau site (en cours de migration depuis l'app Streamlit `Gille_App.py` à la racine du repo).

## Stack

- [Astro](https://astro.build) (rendu statique)
- Tailwind CSS v4 (via `@tailwindcss/vite`)
- Content Collections (`src/content/services`, `src/content/stages`) pour les données éditoriales

## Démarrage

```bash
npm install
npm run dev       # http://localhost:4321
npm run build     # build de production dans dist/
npm run preview   # sert le build de production
```

## État d'avancement

- [x] Charte graphique "Abysse" (couleurs, typographies) appliquée dans `src/styles/global.css`
- [x] Layout de base, navigation, footer
- [x] Contenu des services et stages migré depuis le site Streamlit
- [x] Formulaire de contact câblé sur Formspree (voir "Formulaire de contact" ci-dessous)
- [x] CMS Decap configuré (voir "Édition de contenu" ci-dessous)
- [x] SEO/perf : sitemap, robots.txt, meta canonical/OG/Twitter, image OG par défaut,
      polices auto-hébergées, images optimisées via `astro:assets` (Lighthouse ~97-100 sur
      toutes les pages testées, cf. "SEO & performance" ci-dessous)
- [x] Photos définitives choisies avec Gilles pour le hero, le portrait et l'image OG
- [x] Hébergeur choisi (Netlify) et site déployé — https://gilles-gambini.netlify.app
- [x] Galeries photo par thématique (accueil, mentoring, stages, hyperbare, banque d'images,
      plongée scientifique) et section interviews sur l'accueil, pour retrouver la richesse
      visuelle de la version Streamlit
- [x] Lien du CTA "Banque d'images" corrigé (pointait vers /contact au lieu de Pond5)

## SEO & performance

- Sitemap généré automatiquement (`@astrojs/sitemap`) + `public/robots.txt`.
- Chaque page a un titre, une description, une URL canonique et des balises Open
  Graph/Twitter Card (voir `src/layouts/BaseLayout.astro`). Image OG par défaut :
  `public/og-default.jpg`, générée à partir de la photo hero définitive (`APNEE/gilles 4.jpg`
  dans le repo d'origine).
- Polices Fraunces/Archivo auto-hébergées via `@fontsource*` plutôt que chargées depuis
  fonts.googleapis.com — supprime une requête bloquante et une dépendance externe.
- Toutes les images de pages passent par `astro:assets` (`<Image />`/`<Carousel />`) : conversion
  WebP, tailles responsives, `width`/`height` explicites contre le layout shift. Les galeries
  thématiques vivent dans `src/assets/gallery/<thème>/` (accueil, mentoring, stage-apnee,
  stage-ice, scientifique) ; le composant `Carousel.astro` s'appuie sur `import.meta.glob` pour
  les charger. La correspondance page → dossier de galerie est codée en dur dans
  `src/pages/services/[id].astro` et `src/pages/stages/[id].astro` (à adapter si de nouvelles
  photos ou pages sont ajoutées).
- **`site` dans `astro.config.mjs` est un placeholder (`gilles-gambini.example`)** — à
  remplacer par le vrai nom de domaine dès qu'il est choisi (utilisé par le sitemap, les URLs
  canoniques et les balises Open Graph).
- Audits Lighthouse (build de prod, en local) : Accueil 97/100/100/100, Services 100/100/100/100,
  détail de stage 99/100/100/100, Contact 99/100/100/100 (Performance/Accessibilité/Bonnes
  pratiques/SEO).

## Formulaire de contact

Le formulaire (`/contact`) envoie vers [Formspree](https://formspree.io) (plan gratuit, 50
soumissions/mois). Pour l'activer :

1. Créer un compte Formspree et un formulaire avec `gilles.gambini@hotmail.fr` comme destinataire.
2. Copier son ID dans `PUBLIC_FORMSPREE_ID` (voir `.env.example`).

Sans cette variable, le formulaire affiche un message d'attente et un lien mailto de secours au
lieu de soumettre silencieusement dans le vide. Un champ honeypot (`_gotcha`) filtre une partie du
spam automatiquement (convention native Formspree).

## Édition de contenu (CMS)

Un CMS [Decap](https://decapcms.org) est configuré sur `/admin` (`public/admin/config.yml`), pour
que Gilles puisse éditer services, stages, tarifs et textes sans toucher au code.

- Backend actuellement configuré : `git-gateway`, ce qui suppose un **hébergement final sur
  Netlify** avec Netlify Identity + Git Gateway activés (gratuit). Si l'hébergement retenu est
  Vercel, il faudra remplacer ce backend par `github` + un fournisseur OAuth dédié.
- Test en local : `npm run cms` (lance `decap-server`) puis ouvrir `/admin` en même temps que
  `npm run dev`.

## Déploiement

Le repo contient à la fois l'ancienne app Streamlit (racine) et ce site (`web/`) : dans les deux
hébergeurs, il faut préciser que le projet vit dans le sous-dossier `web/`.

### Netlify (recommandé pour le CMS — voir ci-dessus)

1. "Add new site" → importer le repo GitHub.
2. **Base directory** : `web`. Build command et publish directory sont déjà dans `netlify.toml`
   (`npm run build` / `dist`), Netlify les reprend automatiquement.
3. Dans les variables d'environnement du site : ajouter `PUBLIC_FORMSPREE_ID`.
4. Activer **Netlify Identity** puis **Git Gateway** (Site settings → Identity) pour que le CMS
   Decap (`/admin`) puisse authentifier Gilles et committer ses modifications.
5. Une fois un nom de domaine choisi : le brancher dans Site settings → Domain management, puis
   mettre à jour `site` dans `astro.config.mjs` et `Sitemap:` dans `public/robots.txt`.

### Vercel

1. "Add New Project" → importer le repo GitHub.
2. **Root Directory** : `web` (Vercel détecte Astro automatiquement, aucune autre config requise
   — `vercel.json` ne fait qu'ajouter les en-têtes de sécurité).
3. Ajouter `PUBLIC_FORMSPREE_ID` dans les variables d'environnement du projet.
4. Le CMS Decap est actuellement configuré pour Netlify (`git-gateway`) : avec Vercel il faudra
   remplacer ce backend par `github` + un fournisseur OAuth (à faire si Vercel est retenu).
5. Une fois un nom de domaine choisi : le brancher dans Project settings → Domains, puis mettre à
   jour `site` dans `astro.config.mjs` et `Sitemap:` dans `public/robots.txt`.

## Structure du contenu

Chaque service (`src/content/services/*.md`) et chaque stage (`src/content/stages/*.md`) est un
fichier Markdown avec des `formules` (offres/tarifs) en frontmatter et une description en corps de
texte — c'est cette structure que le CMS éditera plus tard sans toucher au code.
