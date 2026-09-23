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
- [ ] Optimisation images finales (remplacer les photos placeholder dans `public/images/` et
      `src/assets/images/`)
- [ ] Déploiement (Vercel ou Netlify, tier gratuit)

## SEO & performance

- Sitemap généré automatiquement (`@astrojs/sitemap`) + `public/robots.txt`.
- Chaque page a un titre, une description, une URL canonique et des balises Open
  Graph/Twitter Card (voir `src/layouts/BaseLayout.astro`). Image OG par défaut :
  `public/og-default.jpg` (à remplacer par une vraie photo dès que possible).
- Polices Fraunces/Archivo auto-hébergées via `@fontsource*` plutôt que chargées depuis
  fonts.googleapis.com — supprime une requête bloquante et une dépendance externe.
- Les images utilisées dans les pages (`src/assets/images/`) passent par `astro:assets`
  (`<Image />`) : conversion WebP, tailles responsives, `width`/`height` explicites contre le
  layout shift. Les photos encore en `public/images/` sont des placeholders non utilisés par
  une page — à trier une fois les photos définitives choisies.
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

## Structure du contenu

Chaque service (`src/content/services/*.md`) et chaque stage (`src/content/stages/*.md`) est un
fichier Markdown avec des `formules` (offres/tarifs) en frontmatter et une description en corps de
texte — c'est cette structure que le CMS éditera plus tard sans toucher au code.
