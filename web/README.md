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
      polices auto-hébergées, images optimisées via `astro:assets` (Lighthouse ~94-100 sur
      toutes les pages testées, cf. "SEO & performance" ci-dessous)
- [x] Photos définitives choisies avec Gilles pour le hero, le portrait et l'image OG
- [x] Hébergeur choisi (Netlify) et site déployé — https://gilles-gambini.netlify.app
- [x] Galeries photo par thématique (accueil, mentoring, stages, hyperbare, banque d'images,
      plongée scientifique) et section interviews sur l'accueil, pour retrouver la richesse
      visuelle de la version Streamlit
- [x] Lien du CTA "Banque d'images" corrigé (pointait vers /contact au lieu de Pond5)
- [x] Motion design GSAP piloté par attributs `data-*` (`src/scripts/motion.ts`) : entrée et
      parallaxe du hero (ScrollTrigger), apparition des blocs au défilement, inclinaison 3D des
      cartes et boutons "magnétiques" à la souris, soulignement animé de la navigation ;
      `prefers-reduced-motion` respecté, contenu lisible sans JavaScript. Menu mobile
      accessible et liens Facebook/Instagram/LinkedIn dans le hero, sur Contact et en pied de page

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
- Audits Lighthouse (build de prod, en local, mobile), avec le motion design : Accueil
  99/100/100/100, Services 100/100/100/100, Mentoring 95-97/100/100/100, détail de stage
  94/100/100/100, Contact 100/100/100/100 (Performance/Accessibilité/Bonnes pratiques/SEO).

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

## Fonctionnalités en réserve

Fonctionnalités entièrement codées mais **désactivées par défaut**, pour pouvoir les montrer
rapidement à Gilles sans qu'elles apparaissent sur le site de production.

### Globe interactif des expéditions

Globe 3D en points (WebGL, librairie [cobe](https://github.com/shuding/cobe), ~6 Ko gzip chargés
seulement quand la section arrive à l'écran) avec les lieux d'expédition et de stage ; une liste
accessible à côté du globe fait tourner celui-ci vers le lieu choisi et affiche sa fiche.
Fichiers : `src/components/ExpeditionsGlobe.astro` (+ `.css`), `src/scripts/globe.ts`,
`src/data/expeditions.ts`, page de démo `src/pages/labo/[demo].astro`.

- **Flag** : `PUBLIC_ENABLE_GLOBE` (voir `.env.example`). Sans `PUBLIC_ENABLE_GLOBE=true`, le
  build ne contient ni la page `/labo/globe/`, ni le JavaScript/CSS du globe, ni d'entrée dans le
  sitemap (`/labo/` en est de toute façon exclu, et la page de démo est en `noindex`).
- **Démo en local** : `PUBLIC_ENABLE_GLOBE=true npm run dev` puis ouvrir
  http://localhost:4321/labo/globe
- **Démo en ligne pour le client** : sur Netlify, Site configuration → Environment variables,
  ajouter `PUBLIC_ENABLE_GLOBE` = `true` **uniquement pour les contextes « Deploy Previews » et/ou
  « Branch deploys »** (jamais « Production »), puis partager l'URL de la preview + `/labo/globe/`.
- **Intégration future dans « Qui suis-je »** : afficher le composant dans
  `src/pages/qui-suis-je.astro` derrière le flag, en une ligne :
  `{import.meta.env.PUBLIC_ENABLE_GLOBE === 'true' && <ExpeditionsGlobe />}`.
  Attention : un `import` statique du composant suffit à embarquer son script et son CSS dans le
  build même flag désactivé ; tant que le flag existe, l'importer comme dans la page de démo
  (`const ExpeditionsGlobe = import.meta.env.PUBLIC_ENABLE_GLOBE === 'true' ? (await
  import('../components/ExpeditionsGlobe.astro')).default : null;`). Une fois validé, retirer la
  condition, le flag et la page `/labo`.
- **Données à compléter avec Gilles** : `src/data/expeditions.ts` ne contient pour l'instant que
  les lieux déjà cités sur le site (Groenland, Nice/Méditerranée, Caraïbes, stages sous glace),
  avec des coordonnées approximatives, des périodes `[À compléter]` et un badge « à confirmer ».
  À remplacer par les vrais lieux, dates et missions (dont les missions ESA).

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
