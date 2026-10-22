import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import sitemap from '@astrojs/sitemap';

// TODO: remplacer par le vrai nom de domaine une fois le nom de domaine et
// l'hébergeur choisis — utilisé pour le sitemap, les URLs canoniques et les
// balises Open Graph. `.example` est un TLD réservé aux placeholders (RFC 2606).
export default defineConfig({
  site: 'https://gilles-gambini.example',
  integrations: [sitemap()],
  vite: {
    plugins: [tailwindcss()],
  },
});
