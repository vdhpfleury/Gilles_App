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
- [ ] Câblage du formulaire de contact (Phase 4 — service de formulaire géré / fonction serverless)
- [ ] CMS Decap pour édition autonome du contenu (Phase 1 suite)
- [ ] Optimisation images finales (remplacer les photos placeholder dans `public/images/`)
- [ ] SEO/perf (sitemap, meta, Lighthouse)
- [ ] Déploiement (Vercel ou Netlify, tier gratuit)

## Structure du contenu

Chaque service (`src/content/services/*.md`) et chaque stage (`src/content/stages/*.md`) est un
fichier Markdown avec des `formules` (offres/tarifs) en frontmatter et une description en corps de
texte — c'est cette structure que le CMS éditera plus tard sans toucher au code.
