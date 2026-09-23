import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const formule = z.object({
  titre: z.string(),
  description: z.string(),
  prix: z.string(),
  cta: z.string().optional(),
});

const services = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/services' }),
  schema: z.object({
    title: z.string(),
    order: z.number(),
    icon: z.enum(['apnee', 'biologie', 'hyperbare', 'conference', 'stage', 'contact']),
    tagline: z.string(),
    formules: z.array(formule).default([]),
  }),
});

const stages = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/stages' }),
  schema: z.object({
    title: z.string(),
    order: z.number(),
    niveau: z.enum(['Débutant', 'Avancé', 'Sur mesure', 'Scientifique']),
    prerequis: z.string().optional(),
    formules: z.array(formule).default([]),
  }),
});

export const collections = { services, stages };
